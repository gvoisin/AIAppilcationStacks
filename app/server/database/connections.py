import array
import logging
import os
from contextlib import contextmanager
from typing import Any

import oracledb
from dotenv import load_dotenv

from core.external_logging import (
    get_external_logger,
    log_external_error,
    log_external_request,
    log_external_response,
    summarize_rows,
)

load_dotenv()

logger = logging.getLogger(__name__)
external_logger = get_external_logger()


#region Database Connection Manager
class RAGDBConnection:
    """Singleton for database connection pool and operations."""

    _instance = None
    _initialized = False
    _pool = None

    #region Lifecycle
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if RAGDBConnection._initialized:
            return
        RAGDBConnection._initialized = True

        self._config_dir = os.getenv("DB_WALLET_PATH")
        self._user = os.getenv("DB_USER")
        self._password = os.getenv("DB_PASSWORD")
        self._dsn = os.getenv("DB_DSN")
        self._wallet_location = os.getenv("DB_WALLET_PATH")
        self._wallet_password = os.getenv("DB_WALLET_PASSWORD")
        self.table_prefix = "edge_demo"
    #endregion

    def _db_url(self) -> str:
        return f"oracle://{self._dsn}" if self._dsn else "oracle://unconfigured"

    def _trace_db_request(self, target: str, payload: dict[str, Any]) -> None:
        log_external_request(external_logger, target=target, url=self._db_url(), request_payload=payload)

    def _trace_db_response(self, target: str, payload: dict[str, Any]) -> None:
        log_external_response(external_logger, target=target, url=self._db_url(), response_payload=payload)

    def _trace_db_error(self, target: str, payload: dict[str, Any], error: Exception | str) -> None:
        log_external_error(external_logger, target=target, url=self._db_url(), request_payload=payload, error=error)

    #region Pool + Connection
    def _get_pool(self) -> oracledb.ConnectionPool:
        """Get or create the connection pool (lazy initialization)."""
        if RAGDBConnection._pool is None:
            request_payload = {
                "user": self._user,
                "dsn": self._dsn,
                "config_dir": self._config_dir,
                "wallet_location": self._wallet_location,
                "pool": {"min": 1, "max": 5, "increment": 1},
            }
            self._trace_db_request("oracle.pool.create", request_payload)
            try:
                RAGDBConnection._pool = oracledb.create_pool(
                    user=self._user,
                    password=self._password,
                    dsn=self._dsn,
                    config_dir=self._config_dir,
                    wallet_location=self._wallet_location,
                    wallet_password=self._wallet_password,
                    min=1,
                    max=5,
                    increment=1,
                )
            except oracledb.Error as exc:
                self._trace_db_error("oracle.pool.create", request_payload, exc)
                raise
            self._trace_db_response("oracle.pool.create", {"status": "created"})
        return RAGDBConnection._pool

    @contextmanager
    def get_connection(self):
        """Context manager for acquiring a connection from the pool.

        Usage:
            with db.get_connection() as conn:
                cols, rows = db.execute_query(conn, sql)
        """
        pool = self._get_pool()
        request_payload = {"operation": "acquire"}
        self._trace_db_request("oracle.connection.acquire", request_payload)
        try:
            conn = pool.acquire()
        except oracledb.Error as exc:
            self._trace_db_error("oracle.connection.acquire", request_payload, exc)
            raise
        self._trace_db_response("oracle.connection.acquire", {"status": "acquired"})
        try:
            yield conn
        finally:
            pool.release(conn)
            self._trace_db_response("oracle.connection.release", {"status": "released"})
    #endregion

    #region Direct Connection Helpers
    def connection_config_snapshot(self) -> dict[str, Any]:
        """Return sanitized connection settings for diagnostics."""
        return {
            "dsn": self._dsn,
            "wallet_location": self._wallet_location,
            "config_dir": self._config_dir,
            "user_configured": bool(self._user),
            "password_configured": bool(self._password),
            "wallet_password_configured": bool(self._wallet_password),
        }

    def preflight_check(self) -> tuple[bool, str | None]:
        """Try a minimal Oracle query to validate connectivity before real execution."""
        sql = "SELECT 1 FROM dual"
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cur:
                    self._trace_db_request("oracle.sql.preflight", {"sql": sql})
                    cur.execute(sql)
                    row = cur.fetchone()
                    self._trace_db_response("oracle.sql.preflight", {"row": row})
            return True, None
        except oracledb.Error as exc:
            self._trace_db_error("oracle.sql.preflight", {"sql": sql}, exc)
            return False, str(exc)

    def property_graph_exists(self, graph_name: str) -> tuple[bool, str | None]:
        """Check whether a named Oracle property graph is registered for the current user."""
        sql = "SELECT COUNT(*) FROM user_property_graphs WHERE graph_name = UPPER(:graph_name)"
        request_payload = {"sql": sql, "binds": {"graph_name": graph_name}}
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cur:
                    self._trace_db_request("oracle.sql.property_graph_exists", request_payload)
                    cur.execute(sql, graph_name=graph_name)
                    row = cur.fetchone()
                    self._trace_db_response(
                        "oracle.sql.property_graph_exists",
                        {"row": row, "graph_name": graph_name},
                    )
            exists = bool(row and row[0] and int(row[0]) > 0)
            return exists, None
        except oracledb.Error as exc:
            self._trace_db_error("oracle.sql.property_graph_exists", request_payload, exc)
            return False, str(exc)

    def connect_db(self) -> oracledb.Connection:
        request_payload = {
            "user": self._user,
            "dsn": self._dsn,
            "config_dir": self._config_dir,
            "wallet_location": self._wallet_location,
        }
        self._trace_db_request("oracle.connection.direct", request_payload)
        try:
            connection = oracledb.connect(
                user=self._user,
                password=self._password,
                dsn=self._dsn,
                config_dir=self._config_dir,
                wallet_location=self._wallet_location,
                wallet_password=self._wallet_password,
            )
        except oracledb.Error as exc:
            self._trace_db_error("oracle.connection.direct", request_payload, exc)
            logger.error("ERROR: DB connection failed: %s", exc)
            raise
        self._trace_db_response("oracle.connection.direct", {"status": "connected"})
        return connection

    def disconnect(self, connection: oracledb.Connection):
        connection.close()
        self._trace_db_response("oracle.connection.direct", {"status": "closed"})

    def get_cursor(self):
        self.db_connection = self.connect_db()
        self.cursor = self.db_connection.cursor()
    #endregion

    #region Query Operations
    def execute_query(self, conn: oracledb.Connection, sql: str):
        """Execute SQL query and return column names and rows."""
        request_payload = {"sql": sql}
        with conn.cursor() as cur:
            try:
                self._trace_db_request("oracle.sql.execute", request_payload)
                cur.execute(sql)
                columns = [d[0] for d in cur.description] if cur.description else []
                rows = cur.fetchall()
                self._trace_db_response(
                    "oracle.sql.execute",
                    summarize_rows(columns, rows),
                )
                return columns, rows
            except oracledb.Error as exc:
                self._trace_db_error("oracle.sql.execute", request_payload, exc)
                raise

    def create_table(self, conn: oracledb.Connection):
        """Drop and create embedding table."""
        logger.info("Creating table for embeddings...")

        sql_statements = [
            f"DROP TABLE {self.table_prefix}_embedding PURGE",
            f"""
            CREATE TABLE {self.table_prefix}_embedding (
                id NUMBER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
                text VARCHAR2(4000),
                vec VECTOR,
                source VARCHAR2(100)
            )
            """,
        ]

        with conn.cursor() as cur:
            for stmt in sql_statements:
                request_payload = {"sql": stmt}
                try:
                    self._trace_db_request("oracle.sql.schema", request_payload)
                    cur.execute(stmt)
                    self._trace_db_response("oracle.sql.schema", {"status": "ok"})
                except Exception as exc:
                    self._trace_db_error("oracle.sql.schema", request_payload, exc)
                    logger.info("Skipping error: %s", exc)

    def insert_embedding(self, conn: oracledb.Connection, embeddings, texts, splits):
        sql = f"INSERT INTO {self.table_prefix}_embedding (text, vec, source) VALUES (:1, :2, :3)"
        for i, emb in enumerate(embeddings):
            chunk_text = texts[i][:3900]
            metadata_source = f"{splits[i].metadata.get('source', 'pdf-doc')}_start_{splits[i].metadata.get('start_index', 0)}"
            request_payload = {
                "sql": sql,
                "binds": [chunk_text, f"<vector length {len(emb)}>", metadata_source],
            }

            with conn.cursor() as cur:
                try:
                    self._trace_db_request("oracle.sql.insert_embedding", request_payload)
                    cur.execute(
                        sql,
                        [chunk_text, array.array("f", emb), metadata_source],
                    )
                    self._trace_db_response("oracle.sql.insert_embedding", {"status": "inserted", "source": metadata_source})
                except oracledb.Error as exc:
                    self._trace_db_error("oracle.sql.insert_embedding", request_payload, exc)
                    raise

        conn.commit()
        self._trace_db_response("oracle.sql.insert_embedding", {"status": "committed", "rows": len(embeddings)})
    #endregion
#endregion
