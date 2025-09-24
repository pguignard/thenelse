from fastapi import APIRouter

from quiz_api.models.quiz import Snippet
from quiz_api.services.quiz_service import QuizService

router = APIRouter(prefix="/quiz", tags=["Quiz"])


@router.get("/get_random_snippet/", response_model=Snippet)
def get_random_snippet_by_level_route(language: str, level: str) -> Snippet:
    """Récupère un snippet de code aléatoire avec ses réponses possibles."""
    return QuizService.get_random_snippet_by_level(language, level)
