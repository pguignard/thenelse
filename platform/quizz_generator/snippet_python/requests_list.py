import random

from .prompt import PromptParams, get_snippet_prompt
from .level_themes import (
    theme_list_for_all_levels,
    theme_list_for_one_level,
    level_description,
    LevelThemeParams,
    Level,
)
from .response_model import SnippetBatch

from quizz_generator.openai_api import RequestParams

"""
Ces fonctions sont appellées pour générer des prompts de test et des paramètres de requête.
Elles renvoient un RequestParams complet prêt à être utilisé par launch_request.py.
"""


def test_theme_request() -> RequestParams:
    """Requête de test, thème donné, 5 snippets."""
    level = Level.INTERMEDIATE
    theme_level_data = LevelThemeParams(
        level_string=level.name,
        level_description=level_description[level],
        theme="Flux composite : combiner fonctions à paramètres par défaut, *args/**kwargs, compréhensions conditionnelles et exceptions (ValueError/TypeError) pour aboutir à un seul print.",
    )

    prompt_params = PromptParams(
        language="Python",
        level=theme_level_data.level_string,
        level_description=theme_level_data.level_description,
        theme=theme_level_data.theme,
        snippet_count=5,
    )
    prompt = get_snippet_prompt(prompt_params)
    return RequestParams(
        model="gpt-4.1-mini",
        prompt=prompt,
        service_tier="default",
        response_model=SnippetBatch,
    )


def test_request(level: Level = None) -> RequestParams:
    """Requête de test,
    theme/level au hasard dans tous les niveaux,
    5 snippets."""
    if level is None:
        themes = theme_list_for_all_levels()
    else:
        themes = theme_list_for_one_level(level)

    theme_level_data: LevelThemeParams = random.choice(themes)
    prompt_params = PromptParams(
        language="Python",
        level=theme_level_data.level_string,
        level_description=theme_level_data.level_description,
        theme=theme_level_data.theme,
        snippet_count=5,
    )
    prompt = get_snippet_prompt(prompt_params)

    return RequestParams(
        model="gpt-4.1-mini",
        prompt=prompt,
        service_tier="default",
        response_model=SnippetBatch,
    )


def test_beginner_request() -> RequestParams:
    return test_request(level=Level.BEGINNER)


def test_intermediate_request() -> RequestParams:
    return test_request(level=Level.INTERMEDIATE)


def test_expert_request() -> RequestParams:
    return test_request(level=Level.EXPERT)


# ---------------------------------------------------------------
# Pour la génération de tout un niveau de snippets


def for_snippet_multi_request(
    level: Level, snippet_count: int, model: str
) -> list[RequestParams]:
    """Pour la génération de tout un niveau de snippets
    level: str, un des Level enum (BEGINNER, INTERMEDIATE, EXPERT)
    """
    themes = theme_list_for_one_level(level)

    all_snippets = []
    for theme_data in themes:
        prompt_params = PromptParams(
            language="Python",
            level=theme_data.level_string,
            level_description=theme_data.level_description,
            theme=theme_data.theme,
            snippet_count=snippet_count,
        )
        prompt = get_snippet_prompt(prompt_params)

        all_snippets.append(
            RequestParams(
                model=model,
                prompt=prompt,
                service_tier="default",
                response_model=SnippetBatch,
            )
        )

    return all_snippets
