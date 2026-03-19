import logging
import os
import uuid

from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.runnables import RunnableConfig
from langfuse import Langfuse, propagate_attributes

from dynamic_app.back_agents_graph.rag_agent import semantic_search
from dynamic_app.back_agents_graph.nl2graph_agent import call_graphDB
from core.gen_ai_provider import GenAIProvider
from core.langfuse_tracing import LangfuseTracingProvider
from core.dynamic_app.dynamic_struct import DynamicGraphState
from core.dynamic_app.prompts import BACKEND_ORCHESTRATOR_INSTRUCTIONS

logger = logging.getLogger(__name__)


#region Agent Definition
class BackendOrchestratorAgent:
    """Supervisor agent that coordinates data collection from worker agents and provides consolidated data to UI agents."""

    def __init__(self, langfuse_client: Langfuse | None = None):
        self.gen_ai_provider = GenAIProvider()
        self._client = self.gen_ai_provider.build_oci_client(model_id="xai.grok-4-fast-reasoning",model_kwargs={"temperature": 0.1})
        self.agent_name = "backend_orchestrator"
        self.system_prompt = BACKEND_ORCHESTRATOR_INSTRUCTIONS
        self.agent = self._build_agent()
        self.langfuse_client = langfuse_client
        self.langfuse_tracing_provider = LangfuseTracingProvider(langfuse_client=langfuse_client)

    async def __call__(self, state: DynamicGraphState):
        """Orchestrate data collection and return consolidated results."""
        session_id = self.langfuse_tracing_provider.get_current_session_id() or uuid.uuid4().hex
        run_id = uuid.uuid4().hex
        langfuse_client = self.langfuse_client or self.langfuse_tracing_provider.get_current_client()
        trace_context = self.langfuse_tracing_provider.get_current_trace_context()

        with langfuse_client.start_as_current_observation(
            as_type="span",
            name="DynamicGraph -> Backend Orchestrator",
            trace_context=trace_context,
            input={"messages_count": len(state.get("messages", []))},
            metadata=self.langfuse_tracing_provider.build_observation_metadata(
                session_id=session_id,
                user_id=os.getenv("LANGFUSE_USER_ID", "default_user"),
                tags=["backend_orchestrator"],
                extra={"request_id": run_id},
            ),
        ) as observation:
            config:RunnableConfig = self.langfuse_tracing_provider.build_runnable_config(
                run_id=run_id,
                session_id=session_id,
                thread_id=session_id,
                user_id=os.getenv("LANGFUSE_USER_ID", "default_user"),
                tags=["backend_orchestrator"],
                extra_metadata={"request_id": run_id},
                trace_context=trace_context,
            )
            with propagate_attributes(
                session_id=session_id,
                user_id=os.getenv("LANGFUSE_USER_ID", "default_user"),
                tags=["backend_orchestrator"],
            ):
                response = await self.agent.ainvoke(state, config)
            observation.update(output={"messages_count": len(response.get("messages", []))})
            return response

    def _build_agent(self):
        """Build the agent with worker tools."""
        tools = [call_graphDB, semantic_search]

        return create_agent(
            model=self._client,
            tools=tools,
            system_prompt=self.system_prompt,
            name=self.agent_name,
            checkpointer=InMemorySaver()
        )
#endregion
