import os

from langchain.agents import create_agent
from langchain.messages import AIMessage
from pydantic import BaseModel, Field

from dynamic_app.ui_agents_graph.widget_tools import get_widget_catalog, get_native_component_catalog
from core.gen_ai_provider import GenAIProvider
from core.dynamic_app.dynamic_struct import UIOrchestratorOutput
from core.dynamic_app.dynamic_struct import DynamicGraphState
from core.dynamic_app.prompts import UI_ORCHESTRATOR_INSTRUCTIONS

class SuggestedQuestions(BaseModel):
    """Structured output for follow-up question suggestions."""
    suggested_questions: list[str] = Field(description="List of suggested questions based on context")

#region Suggestions
class SuggestionsReponseLLM:
    """LLM wrapper that generates follow-up questions in structured format."""

    def __init__(self):
        self._suggestion_out = self._build_suggestion_model()
        self._out_query = "A partir du contexte fourni, genere 1 a 3 questions de suivi courtes, claires et en francais. Elles doivent etre affichables dans des boutons UI et porter sur les marques, filieres, sites, qualite, logistique, tracabilite, export ou risques LIMAGRAIN Vegetable Seeds."

    def _build_suggestion_model(self):
        genai_provider = GenAIProvider()
        suggestions_llm = genai_provider.build_oci_client()

        return suggestions_llm.with_structured_output(SuggestedQuestions)
    
    async def __call__(self, state: DynamicGraphState) -> DynamicGraphState:
        suggestions = await self._suggestion_out.ainvoke(self._out_query+f"\n\nContext for question generation:\n{state['messages'][-1].content}")

        if not suggestions: suggestions = SuggestedQuestions(suggested_questions=["Quels risques concernent HM.CLAUSE ?", "Resume les priorites pour Hazera"])

        return {
            'messages': state['messages'] + [
                AIMessage(content=(
                    str(suggestions.model_dump_json())
                ), name="suggestions_agent")
            ],
            'suggestions': str(suggestions.model_dump_json())
        }
#endregion


#region Orchestrator
class UIOrchestrator:
    """Selects UI components based on backend results and available widget tools."""

    def __init__(self):
        self.gen_ai_provider = GenAIProvider()
        self._ui_model_id = os.getenv("UI_ORCHESTRATOR_MODEL", "openai.gpt-4.1")
        self._client = self.gen_ai_provider.build_oci_client(model_id=self._ui_model_id, model_kwargs={"temperature": 0.7})
        self._output_client = self.gen_ai_provider.build_oci_client(model_id=self._ui_model_id, model_kwargs={"temperature": 0.7})
        self.agent_name = "ui_orchestrator"
        self.agent = self._build_agent()
        self.output_response = self._build_output_llm()

    async def __call__(self, state: DynamicGraphState):
        response = await self.agent.ainvoke(state)

        # Structured output is produced in this second pass due to OCI adapter limitations.
        structured_response = await self.output_response.ainvoke(
            f"Build the component list with the information on: {response['messages'][-1].content}"
        )

        return {
            'messages': state['messages'] + [
                AIMessage(content=(
                    str(structured_response.model_dump_json())
                ), name=self.agent_name)
            ]
        }
    
    def _build_agent(self):
        return create_agent(
            model=self._client,
            system_prompt=UI_ORCHESTRATOR_INSTRUCTIONS,
            tools=[get_widget_catalog, get_native_component_catalog],
            name=self.agent_name
        )
    
    def _build_output_llm(self):
        return self._output_client.with_structured_output(UIOrchestratorOutput)
#endregion


#region Local Test Harness
async def main():
    from langchain.messages import HumanMessage
    orchestrator = UIOrchestrator()
    messages:DynamicGraphState = {'messages':[HumanMessage("What is my bill?")]}
    response = await orchestrator(messages)
    print(response)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
#endregion
