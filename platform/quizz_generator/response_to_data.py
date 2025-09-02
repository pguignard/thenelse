from pydantic import BaseModel, ValidationError
import json
from pathlib import Path

from quizz_generator.models import SnippetModel


def get_json_content_from_response(response: dict) -> dict:
    content = response.get("output", [])[1].get("content", [])[0].get("text", "")
    return content


def save_snippet_batch_to_ndjson(snippet_batch_json: str, path: Path) -> int:
    """
    Prend en entrée une string JSON représentant un batch de snippets,
    valide chaque élément avec Pydantic, et les écrit en NDJSON.

    Args:
        snippet_batch_json: string JSON (ex: réponse OpenAI, champ output.content.text)
        path: chemin du fichier NDJSON (créé si inexistant, append sinon)

    Returns:
        int: nombre de snippets ajoutés
    """
    # 1) Charger la string JSON
    data = json.loads(snippet_batch_json)  # dict avec "snippets": [...]

    # 2) Validation avec Pydantic
    snippets = [SnippetModel.model_validate(snippet) for snippet in data["snippets"]]

    # 3) Écriture NDJSON
    with path.open("a", encoding="utf-8") as f:
        for snippet in snippets:
            f.write(snippet.model_dump_json() + "\n")

    return len(snippets)
