import json
import datetime
from pathlib import Path
import typer

from quizz_generator.request_builder import build_request_params, RequestInput
from quizz_generator.llm_api import get_response_from_llm_client
from quizz_generator.data.poc_data import get_random_theme
from quizz_generator.response_to_data import (
    get_json_content_from_response,
    save_snippet_batch_to_ndjson,
)

REQUESTS_OUTPUT_DIR = "request_history"
NDJSON_OUTPUT_DIR = "ndjson_snippets"

app = typer.Typer()


@app.command()
def main(
    test: bool = typer.Option(False, help="Prompt de test (hello)"),
    fast: bool = typer.Option(False, help="Désactive le mode flex"),
    request_name: str = typer.Option(..., help="Nom de la requête (file name)"),
):
    """Génère des requêtes vers le LLM et sauvegarde les réponses dans des fichiers JSON."""

    # Création des données d'entrée
    level, theme = get_random_theme()
    request_input = RequestInput(
        model="gpt-5-nano",
        language="Python",
        level=level,
        theme=theme,
        snippet_count=3,
        test=test,
        fast=fast,
    )

    # Affichage des données d'entrée pour vérification
    print(json.dumps(request_input.model_dump(), indent=2, ensure_ascii=False))
    input()

    # ----------------------------------------------------------------------------------
    # Construction et lancement de la requête

    # Construction des paramètres de requête
    request_params = build_request_params(request_input)

    # Envoi de la requête à l'API LLM
    response = get_response_from_llm_client(request_params)

    # ----------------------------------------------------------------------------------
    # Stockage de l'historique des requêtes

    # Traitement de la réponse
    snippet_batch = get_json_content_from_response(response)

    # Data à écrire dans le fichier JSON
    output_data = {
        "snippet_batch": snippet_batch,
        "request_input": request_input.model_dump(),
        "request_params": request_params.model_dump(),
        "response": response,
    }
    # Créer filename avec prompt_type et timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = Path(REQUESTS_OUTPUT_DIR)
    output_dir.mkdir(parents=True, exist_ok=True)

    file_name = output_dir / f"output_{request_name}_{timestamp}.json"
    # Sauvegarder les données dans un fichier JSON
    with open(file_name, "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)

    # ----------------------------------------------------------------------------------
    # Traitement de la réponse, stockage des snippets en ndjson
    output_dir = Path(NDJSON_OUTPUT_DIR)
    output_dir.mkdir(parents=True, exist_ok=True)

    save_snippet_batch_to_ndjson(
        snippet_batch,
        output_dir / f"output_{request_name}_{timestamp}.ndjson",
    )


if __name__ == "__main__":
    app()
