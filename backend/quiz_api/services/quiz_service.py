import random
from fastapi import HTTPException

from quiz_api.models.quiz import Snippet
import json
import os

json_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'snippet_db.json')


class QuizService:
    """Service gérant la logique métier des quiz."""

    @staticmethod
    def _load_snippets():
        try:
            with open(json_path, encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []

    @staticmethod
    def get_random_snippet() -> Snippet:
        """Récupère un snippet de code aléatoire avec ses réponses possibles."""
        snippets = QuizService._load_snippets()
        if not snippets:
            raise HTTPException(status_code=404, detail="Aucun snippet disponible")
        snippet_data = random.choice(snippets)
        return Snippet(**snippet_data)

    @staticmethod
    def get_snippet_by_id(snippet_id: int) -> Snippet:
        """Récupère un snippet spécifique par son ID."""
        snippets = QuizService._load_snippets()
        if snippet_id < 0 or snippet_id >= len(snippets):
            raise HTTPException(status_code=404, detail="Snippet non trouvé")
        snippet_data = snippets[snippet_id]
        return Snippet(**snippet_data)

    @staticmethod
    def get_snippets_count() -> dict:
        """Retourne le nombre total de snippets disponibles."""
        snippets = QuizService._load_snippets()
        return {"total_snippets": len(snippets)}
