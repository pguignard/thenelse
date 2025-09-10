from random import random
from pydantic import BaseModel
from enum import Enum

from quizz_generator.snippet_request.prompts import user_prompt, system_prompt
from quizz_generator.snippet_request.poc_data import get_random_theme
from quizz_generator.llm_api import RequestParams


class SnippetParams(BaseModel):
    language: str = "Python"
    level: str = None
    theme: str = None
    snippet_count: int = None


def get_snippet_prompt() -> str:
    """Construit le prompt utilisateur pour la génération de snippets."""

    level, theme = get_random_theme()
    data = SnippetParams(
        level=level,
        theme=theme,
        snippet_count=5,
    )

    return system_prompt + user_prompt.format(
        LANGUAGE=data.language,
        LEVEL=data.level,
        THEME=data.theme,
        SNIPPETS_COUNT=data.snippet_count,
    )
