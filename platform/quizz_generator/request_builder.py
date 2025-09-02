from random import random
from pydantic import BaseModel
from enum import Enum

from quizz_generator.data.prompts import user_prompt, system_prompt
from quizz_generator.llm_api import RequestParams


class RequestInput(BaseModel):
    model: str = None
    language: str = None
    level: str = None
    theme: str = None
    snippet_count: int = None
    test: bool = False
    fast: bool = False


def build_user_prompt(data: RequestInput) -> str:
    return user_prompt.format(
        LANGUAGE=data.language,
        LEVEL=data.level,
        THEME=data.theme,
        SNIPPETS_COUNT=data.snippet_count,
    )


def build_request_params(data: RequestInput) -> RequestParams:
    """Construit les paramètres de requête pour l'API LLM à partir des données d'entrée."""

    # Construction du prompt (say hello si "test")
    prompt = system_prompt + build_user_prompt(data)
    prompt = "Say Hello." if data.test else prompt

    # Détermination du niveau de service (fast ou flex)
    service_tier = "default" if data.fast else "flex"

    return RequestParams(model=data.model, prompt=prompt, service_tier=service_tier)
