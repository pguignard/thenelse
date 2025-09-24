from fastapi import HTTPException
import random
import pathlib
from enum import Enum

from quiz_api.models.quiz import Snippet, SnippetsCount

"""Service pour gérer les opérations liées aux quiz.
Les snippets sont stockés dans des fichiers ndjson dans le dossier "data".
Le noms des fichiers sont au format <language>_<level>.ndjson,
    > ex: python_beginner.ndjson
"""


data_folder_path = pathlib.Path(__file__).resolve().parent.parent / 'data'


class QuizService:
    @staticmethod
    def get_random_snippet_by_level(language: str, level: str) -> Snippet:
        """Récupère un snippet de code au hasard dans le fichier correspondant au langage et au niveau demandé."""
        file_path = data_folder_path / f"{language.lower()}_{level.lower()}.ndjson"
        if not file_path.exists():
            raise HTTPException(
                status_code=404,
                detail="Fichier de snippets non trouvé pour ce langage et niveau.",
            )

        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            if not lines:
                raise HTTPException(
                    status_code=404,
                    detail="Aucun snippet disponible pour ce langage et niveau.",
                )
            random_line = random.choice(lines)
            snippet_data = Snippet.model_validate_json(random_line)
            return snippet_data

    @staticmethod
    def get_snippets_count() -> SnippetsCount:
        """Retourne le nombre de snippets disponibles pour chaque langage et chaque level, en se basant sur les noms de fichiers."""
        snippets_count = SnippetsCount(total_snippets=0, snippets_per_language_level={})
        for file_path in data_folder_path.glob("*.ndjson"):
            language, level = file_path.stem.split("_")
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
                snippets_count.total_snippets += len(lines)
                snippets_count.snippets_per_language_level.setdefault(language, {})[
                    level
                ] = len(lines)
        return snippets_count
