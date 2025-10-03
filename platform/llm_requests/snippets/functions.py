import random

from .models import Levels, Languages, SnippetParams

from .system_prompt import get_system_prompt
from .user_prompt import get_user_prompt
from .themes import themes_data


def get_prompt(snippet_params: SnippetParams, snippet_count: int) -> str:
    """Crée les paramètres de requête pour un test de génération de snippets.
    Prends un objet SnippetParams en entrée.
    """
    prompt = (
        get_system_prompt(snippet_params.language)
        + "\n"
        + get_user_prompt(snippet_params, snippet_count)
    )
    return prompt


def get_theme_list(language: Languages, level: Levels) -> list[dict]:
    """Retourne la liste des thèmes disponibles pour un langage et un niveau donné."""
    if language not in themes_data.keys():
        raise ValueError(f"Pas de thèmes disponibles pour: {language}")
    language_themes = themes_data[language]

    if level not in language_themes.keys():
        raise ValueError(f"Pas de thèmes disponibles pour: {language} {level}")
    return language_themes[level]


# ---------------------------------------------------------------
# Pour les tests


def get_prompt_with_random_theme(
    language: Languages, level: Levels, snippet_count: int
) -> str:
    """Crée les paramètres de requête pour un test de génération de snippets.
    Le thème est choisi aléatoirement parmi ceux disponibles pour le langage et le niveau donnés.
    """

    themes = get_theme_list(language, level)
    if not themes:
        raise ValueError(f"Aucun thème trouvé pour {language} {level}")
    theme = random.choice(themes)

    prompt_params = SnippetParams(
        language=language, level=level, theme=theme, snippet_count=snippet_count
    )

    return get_prompt(prompt_params)


# ---------------------------------------------------------------
# Pour la génération de tout un niveau de snippets


# def get_prompt_list_for_a_level(
#     level: Levels, snippet_count: int, model: str
# ) -> list[RequestParams]:
#     """Pour la génération de tout un niveau de snippets
#     level: str, un des Level enum (BEGINNER, INTERMEDIATE, EXPERT)
#     """
#     themes = theme_list_for_one_level(level)

#     all_snippets = []
#     for theme_data in themes:
#         prompt_params = SnippetParams(
#             language="Python",
#             level=theme_data.level_string,
#             level_description=theme_data.level_description,
#             theme=theme_data.theme,
#             snippet_count=snippet_count,
#         )
#         prompt = get_snippet_prompt(prompt_params)

#         all_snippets.append(
#             RequestParams(
#                 model=model,
#                 prompt=prompt,
#                 service_tier="default",
#                 response_model=SnippetBatch,
#             )
#         )

#     return all_snippets


# ---------------------------------------------------------------
# Tests unitaires pour vérifier que les prompts sont bien générés
if __name__ == "__main__":
    # Test de génération de prompt
    test_language = Languages.PYTHON
    test_level = Levels.BEGINNER
    test_snippet_count = 3

    try:
        prompt = get_prompt_with_random_theme(
            language=test_language,
            level=test_level,
            snippet_count=test_snippet_count,
        )
        print("Prompt généré avec succès:\n")
        print(prompt)
    except Exception as e:
        print(f"Erreur lors de la génération du prompt: {e}")
