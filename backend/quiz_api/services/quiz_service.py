import random
from fastapi import HTTPException

from quiz_api.models.quiz import Snippet
from quiz_api.data.snippet_db import snippet_db_json


class QuizService:
    """Service gérant la logique métier des quiz."""

    @staticmethod
    def get_random_snippet() -> Snippet:
        """Récupère un snippet de code aléatoire avec ses réponses possibles."""
        if not snippet_db_json:
            raise HTTPException(status_code=404, detail="Aucun snippet disponible")

        snippet_data = random.choice(snippet_db_json)
        return Snippet(**snippet_data)

    @staticmethod
    def get_snippet_by_id(snippet_id: int) -> Snippet:
        """Récupère un snippet spécifique par son ID."""
        if snippet_id < 0 or snippet_id >= len(snippet_db_json):
            raise HTTPException(status_code=404, detail="Snippet non trouvé")

        snippet_data = snippet_db_json[snippet_id]
        return Snippet(**snippet_data)

    @staticmethod
    def get_snippets_count() -> dict:
        """Retourne le nombre total de snippets disponibles."""
        return {"total_snippets": len(snippet_db_json)}
