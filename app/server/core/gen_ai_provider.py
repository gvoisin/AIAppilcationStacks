# region Imports
import logging
import os
from typing import Any

import httpx
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_oci.embeddings import OCIGenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from oci_openai import OciUserPrincipalAuth

from core.external_logging import (
    get_external_logger,
    is_debug_enabled,
    log_external_error,
    log_external_request,
    log_external_response
)
from database.connections import RAGDBConnection

load_dotenv()
# endregion Imports

# region Constants
EMBED_MODEL = "cohere.embed-v4.0"
DEFAULT_CHAT_MODEL = "xai.grok-4-fast-non-reasoning"
# endregion Constants

logger = logging.getLogger(__name__)
external_logger = get_external_logger()


class TracedHttpxClient(httpx.Client):
    """httpx client that traces outbound requests/responses when DEBUG logging is enabled."""

    def send(self, request: httpx.Request, *args: Any, **kwargs: Any) -> httpx.Response:
        request_body: str | None = None
        if request.content:
            try:
                request_body = request.content.decode("utf-8")
            except UnicodeDecodeError:
                request_body = f"<binary {len(request.content)} bytes>"

        log_external_request(
            external_logger,
            target="oci-http",
            url=str(request.url),
            request_payload={
                "method": request.method,
                "headers": dict(request.headers),
                "body": request_body,
            },
        )

        try:
            response = super().send(request, *args, **kwargs)
        except Exception as exc:
            log_external_error(
                external_logger,
                target="oci-http",
                url=str(request.url),
                request_payload={
                    "method": request.method,
                    "headers": dict(request.headers),
                    "body": request_body,
                },
                error=exc,
            )
            raise

        response_payload: str | None = None
        content_type = response.headers.get("content-type", "")
        if "application/json" in content_type or content_type.startswith("text/"):
            response_payload = response.text
        elif response.content:
            response_payload = f"<binary {len(response.content)} bytes>"

        log_external_response(
            external_logger,
            target="oci-http",
            url=str(request.url),
            response_payload={
                "status_code": response.status_code,
                "headers": dict(response.headers),
                "body": response_payload,
            },
        )
        return response


class TracedAsyncHttpxClient(httpx.AsyncClient):
    """Async httpx client that traces outbound requests/responses when DEBUG logging is enabled."""

    async def send(self, request: httpx.Request, *args: Any, **kwargs: Any) -> httpx.Response:
        request_body: str | None = None
        if request.content:
            try:
                request_body = request.content.decode("utf-8")
            except UnicodeDecodeError:
                request_body = f"<binary {len(request.content)} bytes>"

        log_external_request(
            external_logger,
            target="httpx-async",
            url=str(request.url),
            request_payload={
                "method": request.method,
                "headers": dict(request.headers),
                "body": request_body,
            },
        )

        try:
            response = await super().send(request, *args, **kwargs)
        except Exception as exc:
            log_external_error(
                external_logger,
                target="httpx-async",
                url=str(request.url),
                request_payload={
                    "method": request.method,
                    "headers": dict(request.headers),
                    "body": request_body,
                },
                error=exc,
            )
            raise

        response_payload: str | None = None
        content_type = response.headers.get("content-type", "")
        if "application/json" in content_type or content_type.startswith("text/"):
            response_payload = response.text
        elif response.content:
            response_payload = f"<binary {len(response.content)} bytes>"

        log_external_response(
            external_logger,
            target="httpx-async",
            url=str(request.url),
            response_payload={
                "status_code": response.status_code,
                "headers": dict(response.headers),
                "body": response_payload,
            },
        )
        return response


class TracedOCIGenAIEmbeddings(OCIGenAIEmbeddings):
    """Embedding client with DEBUG logging for external requests/responses."""

    def embed_query(self, text: str) -> list[float]:
        payload = {"model_id": self.model_id, "text": text}
        log_external_request(
            external_logger,
            target="oci-embeddings.query",
            url=getattr(self, "service_endpoint", None),
            request_payload=payload,
        )
        try:
            result = super().embed_query(text)
        except Exception as exc:
            log_external_error(
                external_logger,
                target="oci-embeddings.query",
                url=getattr(self, "service_endpoint", None),
                request_payload=payload,
                error=exc,
            )
            raise
        log_external_response(
            external_logger,
            target="oci-embeddings.query",
            url=getattr(self, "service_endpoint", None),
            response_payload={"embedding_length": len(result)},
        )
        return result

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        payload = {"model_id": self.model_id, "texts": texts}
        log_external_request(
            external_logger,
            target="oci-embeddings.documents",
            url=getattr(self, "service_endpoint", None),
            request_payload=payload,
        )
        try:
            result = super().embed_documents(texts)
        except Exception as exc:
            log_external_error(
                external_logger,
                target="oci-embeddings.documents",
                url=getattr(self, "service_endpoint", None),
                request_payload=payload,
                error=exc,
            )
            raise
        log_external_response(
            external_logger,
            target="oci-embeddings.documents",
            url=getattr(self, "service_endpoint", None),
            response_payload={
                "documents": len(result),
                "embedding_length": len(result[0]) if result else 0,
            },
        )
        return result


# region LLM Provider
class GenAIProvider:
    """Singleton provider for OCI GenAI LLM clients."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        pass

    def _build_default_headers(self) -> dict[str, str]:
        headers = {
            "opc-compartment-id": os.getenv("COMPARTMENT_ID", ""),
        }

        conversation_store_id = os.getenv("OCI_CONVERSATION_STORE_ID")
        if conversation_store_id:
            headers["opc-conversation-store-id"] = conversation_store_id

        return headers

    def build_oci_client(self, model_id: str | None = None, model_kwargs: dict[str, Any] | None = None):
        resolved_model_id = model_id or os.getenv("GEN_AI_MODEL", DEFAULT_CHAT_MODEL)
        resolved_model_kwargs = model_kwargs or {}
        base_url = os.getenv(
            "SERVICE_ENDPOINT",
            "https://inference.generativeai.us-chicago-1.oci.oraclecloud.com/20231130/actions/v1",
        )
        default_headers = self._build_default_headers()

        if is_debug_enabled(external_logger):
            log_external_request(
                external_logger,
                target="oci-chat-client.build",
                url=base_url,
                request_payload={
                    "model": resolved_model_id,
                    "default_headers": default_headers,
                    "model_kwargs": resolved_model_kwargs,
                },
            )

        client = ChatOpenAI(
            base_url=base_url,
            http_client=TracedHttpxClient(
                auth=OciUserPrincipalAuth(profile_name=os.getenv("AUTH_PROFILE"))
            ),
            default_headers=default_headers,
            api_key=os.getenv("OPENAI_INNO_DEV1"),
            model=resolved_model_id,
            store=False,
            **resolved_model_kwargs,
        )

        if is_debug_enabled(external_logger):
            log_external_response(
                external_logger,
                target="oci-chat-client.build",
                url=base_url,
                response_payload={
                    "model": resolved_model_id,
                    "configured": True,
                },
            )

        return client

    def update_oci_client(
        self,
        client: ChatOpenAI,
        model_id: str | None = None,
        model_kwargs: dict[str, Any] | None = None,
    ):
        client.model_name = model_id or self.get_default_chat_model()
        client.model_kwargs = model_kwargs or {}

    def get_default_chat_model(self) -> str:
        return os.getenv("GEN_AI_MODEL", DEFAULT_CHAT_MODEL)


# endregion LLM Provider

# region Embedding Provider
class GenAIEmbedProvider:
    """Singleton provider for OCI GenAI Embeddings with optional PDF processing capabilities."""

    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if GenAIEmbedProvider._initialized:
            return
        GenAIEmbedProvider._initialized = True

        self.embed_client = TracedOCIGenAIEmbeddings(
            model_id=EMBED_MODEL,
            service_endpoint="https://inference.generativeai.us-chicago-1.oci.oraclecloud.com",
            compartment_id=os.getenv("COMPARTMENT_ID"),
            auth_profile=os.getenv("AUTH_PROFILE"),
        )
        # Populated when load_pdf() runs.
        self.docs = None
        self.splits = None
        self.texts = None
        self.embed_response = None

    def load_pdf(self, pdf_path: str, chunk_size: int = 300, chunk_overlap: int = 200):
        """Load and process a PDF file for embedding.

        Args:
            pdf_path: Path to the PDF file to load.
            chunk_size: Size of text chunks for splitting.
            chunk_overlap: Overlap between chunks.

        Returns:
            List of embeddings for the document chunks.
        """
        loader = PyPDFLoader(pdf_path)
        self.docs = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            add_start_index=True,
        )
        self.splits = text_splitter.split_documents(self.docs)
        self.texts = [chunk.page_content for chunk in self.splits]
        self.embed_response = self.embed_client.embed_documents(self.texts)

        return self.embed_response

    def load_and_insert_pdf(self, pdf_path: str, db_conn: RAGDBConnection, chunk_size: int = 300, chunk_overlap: int = 200):
        """Load PDF, generate embeddings, and insert into database."""
        embeddings = self.load_pdf(pdf_path, chunk_size, chunk_overlap)

        with db_conn.get_connection() as conn:
            db_conn.insert_embedding(conn, embeddings, self.texts, self.splits)

        return embeddings

    def load_all_rag_documents(self, db_conn: RAGDBConnection, chunk_size: int = 300, chunk_overlap: int = 200):
        """Load all PDF documents from the rag_docs directory and insert into database."""
        rag_docs_dir = "./core/rag_docs/"

        with db_conn.get_connection() as conn:
            db_conn.create_table(conn)

        pdf_files = [f for f in os.listdir(rag_docs_dir) if f.endswith('.pdf')]
        loaded_count = 0

        for pdf_file in pdf_files:
            pdf_path = os.path.join(rag_docs_dir, pdf_file)
            logger.info("Loading and indexing %s...", pdf_file)
            try:
                self.load_and_insert_pdf(pdf_path, db_conn, chunk_size, chunk_overlap)
                loaded_count += 1
            except Exception as exc:
                logger.error("Error loading %s: %s", pdf_file, exc)

        logger.info("Successfully loaded and indexed %s documents.", loaded_count)
# endregion Embedding Provider
