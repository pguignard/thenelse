from fastapi import APIRouter

from quiz_api.services.quiz_service import QuizService
from quiz_api.models.quiz import SnippetsCount

router = APIRouter(prefix="/stats", tags=["Stats"])


@router.get("/snippets/count", response_model=SnippetsCount)
def get_snippets_count():
    """Retourne le nombre total de snippets disponibles."""
    return QuizService.get_snippets_count()
