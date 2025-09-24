#!/usr/bin/env python3

from datetime import datetime
import typer

from quizz_generator.save_request import save_request
from quizz_generator.openai_api import get_response_from_llm_client, RequestParams

from quizz_generator.snippet_python import for_snippet_multi_request
from quizz_generator.snippet_python.level_themes import Level

app = typer.Typer()


@app.command()
def main(
    model: str = typer.Option("gpt-4.1-nano", help="Modèle LLM à utiliser (override)"),
    snippet_count: int = typer.Option(10, help="Nombre de snippets par thème"),
    level: str = typer.Option(..., help="Niveau des snippets à générer"),
):
    """Génère des requêtes vers le LLM et sauvegarde les réponses dans des fichiers JSON.

    - Si --test est activé, utilise un prompt simple.
    - Si --flex est activé, utilise le service_tier 'flex' (plus lent, moins cher).
    - Le nom de la requête est obligatoire et sert à nommer le fichier de sortie.
    """

    # ----------------------------------------------------------------------------------
    # Création des requêtes

    # check level validity
    try:
        level = Level[level.upper()]
    except KeyError:
        raise ValueError(f"Niveau inconnu: {level}")

    request_params_list = for_snippet_multi_request(
        level=level,
        snippet_count=snippet_count,
        model=model,
    )

    # ----------------------------------------------------------------------------------
    # Envoi des requêtes à l'API LLM

    # example: snippets_1015-1530_beginner_4o-mini
    time_stamp = datetime.now().strftime("%m%d-%H%M")
    output_dir = f"snippets_{time_stamp}_{level.name.lower()}_{model[4:]}"
    print(f"Réponses sauvegardées dans le dossier: {output_dir}")

    for id, request_params in enumerate(request_params_list):
        request_name = f"snippets_{level.name.lower()}_{id+1}"
        try:
            response = get_response_from_llm_client(request_params=request_params)
            typer.echo(f"Requête '{request_name}' envoyée avec succès.")
            save_request(
                output_dir=output_dir,
                request_name=request_name,
                request_params=request_params,
                response=response,
            )
            typer.echo(f"Réponse sauvegardée avec succès.")
        except Exception as e:
            typer.echo(f"Erreur lors de l'envoi de la requête: {e}")
            raise


if __name__ == "__main__":
    app()
