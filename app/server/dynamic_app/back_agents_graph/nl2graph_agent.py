import logging
import re
import uuid

import oracledb

from langchain_core.messages import HumanMessage
from langchain.tools import tool

from database.connections import RAGDBConnection
from core.base_agent import BaseAgent
from core.langfuse_tracing import LangfuseTracingProvider
from core.dynamic_app.prompts.graph_agent import GRAPH_SCHEMA_DESCRIPTION, GRAPH_FEW_SHOT_EXAMPLES
from chat_app.nl2sql_agent import create_nl2sql_agent

logger = logging.getLogger(__name__)

UNSUPPORTED_GRAPH_PATTERNS = (
    re.compile(r"\bOPTIONAL\s+MATCH\b", re.IGNORECASE),
    re.compile(r"\bGRAPH_TABLE\b[\s\S]*\bMATCH\b[\s\S]*\bOPTIONAL\s+MATCH\b", re.IGNORECASE),
)
TRANSVERSE_SQL_HINT_PATTERNS = (
    re.compile(r"\bvue\s+transverse\b", re.IGNORECASE),
    re.compile(r"\bvue\s+globale\b", re.IGNORECASE),
    re.compile(r"\bsynth[eè]se\s+globale\b", re.IGNORECASE),
    re.compile(r"\bpilotage\s+transverse\b", re.IGNORECASE),
)


#region Agent Definition
class NL2GraphAgent(BaseAgent):
    """Agent for natural language to PGQL translation and execution."""

    def __init__(self):
        super().__init__()
        self.agent_name = "nl2graph_agent"
        self.system_prompt = f"{GRAPH_SCHEMA_DESCRIPTION}\n\n" + "\n\n".join(
            f"Q: {ex['q']}\nPGQL:\n{ex['pgql']}" for ex in GRAPH_FEW_SHOT_EXAMPLES
        )
        self.agent = self.build_agent()
        self.langfuse_tracing_provider = LangfuseTracingProvider()
        self._sql_fallback_agent = create_nl2sql_agent()

    def _normalize_generated_sql(self, generated_pgql: str) -> str:
        normalized = generated_pgql.strip()
        if normalized.startswith("```"):
            lines = normalized.split("\n")
            normalized = "\n".join(lines[1:-1] if lines[-1] == "```" else lines[1:])
        return normalized.strip()

    def _validate_graph_query_shape(self, generated_pgql: str) -> str | None:
        for pattern in UNSUPPORTED_GRAPH_PATTERNS:
            if pattern.search(generated_pgql):
                return (
                    "Unsupported GRAPH_TABLE pattern detected: do not use OPTIONAL MATCH inside GRAPH_TABLE(...). "
                    "Use a single MATCH clause with required patterns only, plus optional WHERE and COLUMNS clauses."
                )
        return None

    def _should_route_to_sql(self, question: str) -> bool:
        return any(pattern.search(question) for pattern in TRANSVERSE_SQL_HINT_PATTERNS)

    async def _run_sql_fallback(self, question: str, session_id: str) -> dict:
        logger.info("Routing broad transverse question to SQL fallback for session_id=%s", session_id)
        result = await self._sql_fallback_agent.call_nl2sql_agent({"input": question, "session_id": session_id})
        output = result.get("output", "")
        if output:
            return {"output": f"SQL fallback results:\n{output}"}
        return {"output": "SQL fallback returned no output."}

    async def call_nl2graphDB_agent(self, input: dict) -> dict:
        """Process the input question by generating PGQL and executing it."""
        question = input.get("input", "")
        original_question = question
        if not question:
            return {"output": "No question provided."}
        inherited_session_id = self.langfuse_tracing_provider.get_current_session_id()
        session_id = str(input.get("session_id") or inherited_session_id or uuid.uuid4().hex)

        if self._should_route_to_sql(question):
            return await self._run_sql_fallback(question, session_id)

        max_attempts = 2
        generated_pgql = ''
        last_error = None

        for attempt in range(max_attempts):
            try:
                messages = [HumanMessage(content=question)]
                agent_input = {'messages': messages}
                response = await self.agent.ainvoke(agent_input)
                generated_pgql = self._normalize_generated_sql(response['messages'][-1].content)

                logger.info("GENERATED PGQL (attempt %s): %s", attempt + 1, generated_pgql)

                shape_error = self._validate_graph_query_shape(generated_pgql)
                if shape_error:
                    raise ValueError(shape_error)

                db_conn = RAGDBConnection()
                connection_ok, connection_error = db_conn.preflight_check()
                if not connection_ok:
                    return {
                        "output": (
                            "Erreur de connexion Oracle avant execution de la requete graphe. "
                            f"Details techniques: {connection_error}"
                        )
                    }

                graph_exists, graph_check_error = db_conn.property_graph_exists("limagrain_operations")
                if graph_check_error is not None:
                    return {
                        "output": (
                            "Impossible de verifier l existence du property graph limagrain_operations. "
                            f"Details techniques: {graph_check_error}"
                        )
                    }
                if not graph_exists:
                    return {
                        "output": (
                            "Le graphe Oracle limagrain_operations est introuvable. "
                            "Chargez d abord les tables relationnelles puis executez @schemas/demo-graph-limagrain.sql "
                            "ou @schemas/demo-graph-load-limagrain.sql pour creer le property graph."
                        )
                    }

                try:
                    with db_conn.get_connection() as conn:
                        cols, rows = db_conn.execute_query(conn, generated_pgql)
                except oracledb.Error as db_error:
                    error_text = str(db_error)
                    logger.exception(
                        "NL2Graph Oracle execution failed for session_id=%s with config=%s",
                        session_id,
                        db_conn.connection_config_snapshot(),
                    )
                    if "ORA-42421" in error_text:
                        return {
                            "output": (
                                "Le graphe Oracle limagrain_operations est introuvable. "
                                "Chargez d abord les tables relationnelles puis executez @schemas/demo-graph-limagrain.sql "
                                "ou @schemas/demo-graph-load-limagrain.sql pour creer le property graph. "
                                f"Details techniques: {error_text}"
                            )
                        }
                    return {
                        "output": (
                            "Erreur Oracle lors de l execution de la requete graphe. "
                            f"Details techniques: {error_text}"
                        )
                    }

                if not rows:
                    return {"output": "Query executed successfully but returned no results."}

                result_lines = []
                for row in rows:
                    row_data = ", ".join(f"{col}: {val}" for col, val in zip(cols, row))
                    result_lines.append(row_data)

                return {"output": f"Graph Query Results:\n" + "\n".join(result_lines)}
            except Exception as e:
                last_error = e
                logger.exception(
                    "NL2Graph attempt %s failed for session_id=%s",
                    attempt + 1,
                    session_id,
                )
                if attempt < max_attempts - 1:
                    retry_guidance = "Fix the mistakes and consider the examples provided to solve the user question."
                    error_text = str(e)
                    if "ORA-40997" in error_text or "Unsupported GRAPH_TABLE pattern" in error_text:
                        retry_guidance = (
                            "Fix the GRAPH_TABLE syntax. Keep ORDER BY and FETCH FIRST outside GRAPH_TABLE(...). "
                            "Inside GRAPH_TABLE(...), use only one MATCH clause, an optional WHERE clause, and COLUMNS (...). "
                            "Never use OPTIONAL MATCH inside GRAPH_TABLE. "
                            "Never chain from a variable introduced only by an optional branch. "
                            "Use IS only for vertex labels, not for edge labels. "
                            "Prefer one MATCH clause with comma-separated required patterns, or simplify the graph query."
                        )
                    question = f"Original question: {original_question}\n\nYour previous query:\n{generated_pgql}\n\nhad a mistake that resulted in an error: {e}. {retry_guidance}"
                    logger.warning("Retrying due to error: %s", e)

        return {"output": f"Error executing NL2Graph after {max_attempts} attempts: {str(last_error)}"}
#endregion


#region Tool Wrapper
def create_nl2graph_agent():
    """Build an NL2Graph agent instance."""
    return NL2GraphAgent()

@tool()
async def call_graphDB(query: str) -> str:
    """Interroge le graphe LIMAGRAIN Vegetable Seeds pour les alertes, marques, filieres, sites, lots, qualite, tracabilite et flux logistiques."""
    NL2Graph_agent_tool = create_nl2graph_agent()

    try:
        result = await NL2Graph_agent_tool.call_nl2graphDB_agent({"input": query})
        return result['output']
    except Exception as e:
        return f"There was an error with the Graph DB tool: {e}"
#endregion
