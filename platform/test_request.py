#!/usr/bin/env python3

from datetime import date
import typer

from quizz_generator.save_request import save_request
from quizz_generator.openai_api import get_response_from_llm_client, RequestParams

from quizz_generator.snippet_python import (
    request_list as python_request_list,
)

# Output directory style : test_MM-DD
OUTPUT_DIR = f"test_{date.today().strftime('%m-%d')}"
REQUEST_LIST = python_request_list  # On peut ajouter d'autres listes de requêtes ici

app = typer.Typer()


def print_request_options():
    """Affiche les options de requêtes disponibles."""
    typer.echo("Options de requêtes disponibles:")
    for name, info in REQUEST_LIST.items():
        typer.echo(f"- {name}: {info['desc']}")


@app.command()
def main(
    fake: bool = typer.Option(False, help="Active le mode fake"),
    model: str = typer.Option(None, help="Modèle LLM à utiliser (override)"),
    flex: bool = typer.Option(False, help="Active le mode flex"),
    request_name: str = typer.Option(..., help="Nom de la requête (> file name)"),
):
    """Génère des requêtes vers le LLM et sauvegarde les réponses dans des fichiers JSON.

    - Si --test est activé, utilise un prompt simple.
    - Si --flex est activé, utilise le service_tier 'flex' (plus lent, moins cher).
    - Le nom de la requête est obligatoire et sert à nommer le fichier de sortie.
    """

    # ----------------------------------------------------------------------------------
    # Création de la requête

    # Trouver la requête dans la liste
    if request_name not in REQUEST_LIST:
        print_request_options()
        raise typer.Exit(code=1)

    # Obtenir les paramètres de la requête
    try:
        request_params: RequestParams = REQUEST_LIST[request_name]["func"]()
    except Exception as e:
        typer.echo(f"Erreur lors de la création des paramètres de requête: {e}")
        raise

    # Override des paramètres si besoin
    if model:
        request_params.model = model
    if flex:
        request_params.service_tier = "flex"

    # Mode fake : affiche les paramètres de la requête et quitte
    if fake:
        print(request_params.model_dump())
        raise typer.Exit()

    # ----------------------------------------------------------------------------------
    # Envoi de la requête à l'API LLM
    try:
        response = get_response_from_llm_client(
            request_params=request_params,
        )
        typer.echo(f"Requête '{request_name}' envoyée avec succès.")
    except Exception as e:
        typer.echo(f"Erreur lors de l'envoi de la requête: {e}")
        raise

    # ----------------------------------------------------------------------------------
    # Stockage dans l'historique des requêtes
    try:
        save_request(
            output_dir=OUTPUT_DIR,
            request_name=request_name,
            request_params=request_params,
            response=response,
        )
        typer.echo(f"Réponse sauvegardée avec succès.")
    except Exception as e:
        typer.echo(f"Erreur lors de la sauvegarde de la réponse: {e}")
        raise


if __name__ == "__main__":
    app()
