# region Imports
from pydantic import BaseModel, Field
from core.gen_ai_provider import GenAIProvider
# endregion Imports

# region Models
class SuggestedQuestions(BaseModel):
    """Structured output with suggested follow-up questions."""
    suggested_questions: list[str] = Field(description="Liste de questions de suivi basees sur le contexte")

class SuggestionModel:
    def build_suggestion_model(self):
        suggestions_llm = GenAIProvider().build_oci_client()
        return suggestions_llm.with_structured_output(SuggestedQuestions)
# endregion Models

# region Prompt
SUGGESTION_QUERY = """
A partir du contexte fourni, genere entre 1 et 3 questions de suivi pertinentes.
Les questions doivent etre courtes, claires, affichables dans des boutons d interface et toujours en francais.
Elles doivent porter uniquement sur les donnees metier presentes: filieres, logistique, qualite, tracabilite, campagnes, production agricole, adherence cooperative, risques operationnels.
N ecris pas de question sur l interface elle-meme.
"""
# endregion Prompt
