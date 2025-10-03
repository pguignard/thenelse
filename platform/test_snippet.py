#!/usr/bin/env python3

from datetime import date
import typer
import random

from llm_requests.save_request import save_request
from llm_requests.openai_api import get_response_from_llm_client, RequestParams
from llm_requests.snippets.models import SnippetBatch, Languages, Levels, SnippetParams
from llm_requests.snippets.functions import get_theme_list, get_prompt

# Output directory style : test_MM-DD
FOLDER_NAME = f"test_{date.today().strftime('%m-%d')}"

app = typer.Typer()


@app.command()
def main(
    language: str = typer.Argument(..., help="Langage de programmation (en minuscule)"),
    level: str = typer.Argument(
        ..., help="Niveau de difficulté (beginner, intermediate, advanced)"
    ),
    snippet_count: int = typer.Argument(5, help="Nombre de snippets à générer"),
    fake: bool = typer.Option(
        False,
        help="Active le mode fake (affiche les paramètres sans envoyer la requête)",
    ),
    model: str = typer.Option(None, help="Modèle LLM à utiliser (override)"),
):
    """Génère des requêtes vers le LLM et sauvegarde les réponses dans des fichiers JSON.

    - Si --test est activé, utilise un prompt simple.
    - Si --flex est activé, utilise le service_tier 'flex' (plus lent, moins cher).
    - Le nom de la requête est obligatoire et sert à nommer le fichier de sortie.
    """

    # ----------------------------------------------------------------------------------
    # Check arguments

    try:
        language: Languages = Languages[language.upper()]
    except KeyError:
        typer.echo(f"Erreur: Langage inconnu '{language}'.")
        typer.echo(f"Langages disponibles: {[l.name for l in Languages]}")
        raise

    try:
        level: Levels = Levels[level.upper()]
    except KeyError:
        typer.echo(f"Erreur: Niveau inconnu '{level}'.")
        typer.echo(f"Niveaux disponibles: {[l.value for l in Levels]}")
        raise

    if snippet_count <= 0 or snippet_count > 10:
        typer.echo("Erreur: Le nombre de snippets doit être entre 1 et 10.")
        raise

    request_name: str = (
        f"{language.name.lower()}_{level.value.lower()}_{snippet_count}_snippets"
    )

    # ----------------------------------------------------------------------------------
    # Création de la requête

    # Choix du thème aléatoire et création du prompt
    try:
        theme_list = get_theme_list(language, level)
        assert theme_list, f"Theme list vide pour {language} {level}"
    except Exception as e:
        typer.echo(f"Erreur lors de la récupération des thèmes: {e}")
        raise

    theme = random.choice(theme_list)
    snippet_params = SnippetParams(
        language=language, level=level, theme=theme, snippet_count=snippet_count
    )

    # Obtenir les paramètres de la requête
    try:
        request_params = RequestParams(
            model="gpt-4.1-mini",
            prompt=get_prompt(snippet_params, snippet_count),
            service_tier="default",
            response_model=SnippetBatch,
        )
    except Exception as e:
        typer.echo(f"Erreur lors de la création des paramètres de requête: {e}")
        raise

    # Override des paramètres si besoin
    if model:
        request_params.model = model

    # Mode fake : affiche les paramètres de la requête et quitte
    if fake:
        print(request_params.model_dump())
        raise

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
            folder_name=FOLDER_NAME,
            request_name=request_name,
            prompt=request_params.prompt,
            response=response,
        )
        typer.echo(f"Réponse sauvegardée avec succès.")
    except Exception as e:
        typer.echo(f"Erreur lors de la sauvegarde de la réponse: {e}")
        raise


if __name__ == "__main__":
    app()
