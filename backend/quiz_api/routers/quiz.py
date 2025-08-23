from fastapi import APIRouter

from quiz_api.models.quiz import Snippet
from quiz_api.services.quiz_service import QuizService

router = APIRouter(prefix="/quiz", tags=["Quiz"])


@router.get("/random", response_model=Snippet)
def get_random_snippet() -> Snippet:
    """Récupère un snippet de code aléatoire avec ses réponses possibles."""
    return QuizService.get_random_snippet()


@router.get("/{snippet_id}", response_model=Snippet)
def get_snippet_by_id(snippet_id: int):
    """Récupère un snippet spécifique par son ID."""
    return QuizService.get_snippet_by_id(snippet_id)
