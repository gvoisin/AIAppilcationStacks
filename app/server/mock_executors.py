import json
import logging
from pathlib import Path

from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.server.tasks import TaskUpdater
from a2a.types import Part, Task, TaskState, TextPart, UnsupportedOperationError
from a2a.utils import new_agent_parts_message, new_agent_text_message, new_task
from a2a.utils.errors import ServerError

logger = logging.getLogger(__name__)


class MockLLMExecutor(AgentExecutor):
    """Credential-free mock LLM executor for local UI testing."""

    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        query = context.get_user_input() or "Donne-moi les principaux risques pour HM.CLAUSE, Hazera et Limagrain Vegetable Seeds"

        task = context.current_task
        if not task:
            task = new_task(context.message)
            await event_queue.enqueue_event(task)

        updater = TaskUpdater(event_queue, task.id, task.context_id)

        await updater.update_status(
            TaskState.working,
            new_agent_text_message("Le mock LLM prepare une reponse LIMAGRAIN Vegetable Seeds et marques...", task.context_id, task.id),
        )

        sources = _discover_rag_sources()
        content = (
            f"Reponse mock LIMAGRAIN Vegetable Seeds pour : '{query}'.\\n"
            "Cette reponse est generee en mode --mock pour valider les sources et les libelles LIMAGRAIN Vegetable Seeds."
        )
        final_state = "mock_state: completed"
        token_count = "128"
        suggestions = json.dumps(
            {
                "suggested_questions": [
                    "Compare les risques pour HM.CLAUSE, Hazera et Vilmorin-Mikado",
                    "Resume le premier document source",
                ]
            }
        )

        # Keep part order aligned with the frontend parser expectations.
        final_parts = [
            Part(root=TextPart(text=content)),
            Part(root=TextPart(text=final_state)),
            Part(root=TextPart(text=token_count)),
            Part(root=TextPart(text=suggestions)),
            Part(root=TextPart(text=json.dumps(sources))),
        ]

        await updater.update_status(
            TaskState.completed,
            new_agent_parts_message(final_parts, task.context_id, task.id),
            final=True,
        )

    async def cancel(self, request: RequestContext, event_queue: EventQueue) -> Task | None:
        raise ServerError(error=UnsupportedOperationError())


class MockDynamicExecutor(AgentExecutor):
    """Credential-free mock dynamic executor for local UI testing."""

    def __init__(self):
        self._config = {
            "backend_orchestrator": {
                "enabled": True,
                "model": "mock",
            }
        }

    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        query = context.get_user_input() or "Construis un tableau de bord sur HM.CLAUSE, Vilmorin-Mikado et Limagrain Vegetable Seeds"

        task = context.current_task
        if not task:
            task = new_task(context.message)
            await event_queue.enqueue_event(task)

        updater = TaskUpdater(event_queue, task.id, task.context_id)

        await updater.update_status(
            TaskState.working,
            new_agent_text_message("Le graphe dynamique mock analyse la demande...", task.context_id, task.id),
        )

        await updater.update_status(
            TaskState.working,
            new_agent_text_message("Le graphe dynamique mock a assemble une reponse.", task.context_id, task.id),
        )

        sources = _discover_rag_sources()
        content = (
            f"Reponse dynamique mock LIMAGRAIN Vegetable Seeds pour : '{query}'.\\n"
            "Utilise les liens sources ci-dessous pour verifier le comportement de la demo LIMAGRAIN Vegetable Seeds."
        )
        detailed_updates = "mock_dynamic_state: completed"
        token_count = "256"
        suggestions = json.dumps(
            {
                "suggested_questions": [
                    "Ouvre le premier document source",
                    "Compare les informations des sources",
                ]
            }
        )

        # Keep part order aligned with the frontend parser expectations.
        final_parts = [
            Part(root=TextPart(text=content)),
            Part(root=TextPart(text=detailed_updates)),
            Part(root=TextPart(text=token_count)),
            Part(root=TextPart(text=suggestions)),
            Part(root=TextPart(text=json.dumps(sources))),
        ]

        await updater.update_status(
            TaskState.completed,
            new_agent_parts_message(final_parts, task.context_id, task.id),
            final=True,
        )

    async def cancel(self, request: RequestContext, event_queue: EventQueue) -> Task | None:
        raise ServerError(error=UnsupportedOperationError())

    def get_config(self) -> dict:
        return self._config

    def update_config(self, new_config: dict) -> tuple[bool, str]:
        self._config = new_config
        return True, ""

    def reset_config(self) -> None:
        self._config = {
            "backend_orchestrator": {
                "enabled": True,
                "model": "mock",
            }
        }


def _discover_rag_sources() -> list[str]:
    """Return up to 3 document names from core/rag_docs for source-link testing."""
    rag_dir = Path(__file__).resolve().parent / "core" / "rag_docs"
    if not rag_dir.exists():
        return ["mock-source.txt"]

    candidates = [p.name for p in rag_dir.iterdir() if p.is_file()]
    if not candidates:
        return ["mock-source.txt"]

    return sorted(candidates)[:3]
