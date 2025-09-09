#!/usr/bin/env python3

import json
import datetime
from pathlib import Path
import typer

from quizz_generator.snippet_request.prompt_builder import get_snippet_prompt

from quizz_generator.llm_api import get_response_from_llm_client, RequestParams
from quizz_generator.snippet_to_json_data import (
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
    """Génère des requêtes vers le LLM et sauvegarde les réponses dans des fichiers JSON.

    - Si --test est activé, utilise un prompt simple.
    - Si --fast est activé, utilise le service_tier 'default', sinon, 'flex'.
    - Le nom de la requête est obligatoire et sert à nommer le fichier de sortie.
    """

    if test:
        prompt = "Say hello in French."
    else:
        prompt = get_snippet_prompt()

    request_params = RequestParams(
        model="gpt-5-nano",
        prompt=prompt,
        service_tier="default" if fast else "flex",
    )

    # Envoi de la requête à l'API LLM
    response = get_response_from_llm_client(request_params)

    # ----------------------------------------------------------------------------------
    # Stockage de l'historique des requêtes

    request_report = {
        "model": request_params.model,
        "prompt": request_params.prompt,
        "response": response,
    }

    # Créer filename avec prompt_type et timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = Path(REQUESTS_OUTPUT_DIR)
    output_dir.mkdir(parents=True, exist_ok=True)

    file_name = output_dir / f"{timestamp}_{request_name}.json"
    # Sauvegarder les données dans un fichier JSON
    with open(file_name, "w", encoding="utf-8") as f:
        json.dump(request_report, f, indent=2, ensure_ascii=False)

    # ----------------------------------------------------------------------------------
    # Traitement de la réponse, stockage des snippets en ndjson
    # à activer plus tard :)

    if True:
        return

    output_dir = Path(NDJSON_OUTPUT_DIR)
    output_dir.mkdir(parents=True, exist_ok=True)
    save_snippet_batch_to_ndjson(
        snippet_batch,
        output_dir / f"output_{request_name}_{timestamp}.ndjson",
    )


if __name__ == "__main__":
    app()
