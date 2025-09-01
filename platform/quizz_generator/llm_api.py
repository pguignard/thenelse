import os
import json
from enum import Enum

from fastapi import params
from pydantic import BaseModel
from openai import OpenAI

__all__ = ["LLMParams", "get_response_from_llm_client", "PromptType"]


class PromptType(str, Enum):
    TEST = "test"
    SNIPPET = "snippet"
    QUIZZ = "quizz"


class LLMParams(BaseModel):
    model: str = "gpt-4.1-nano"
    prompt: str = "Say Hello"
    prompt_type: PromptType = PromptType.TEST


# Client configuration (get api key from .env local file in the same folder)

with open(".env") as f:
    for line in f:
        if line.startswith("api_key="):
            api_key = line.strip().split("=")[1]
            break

os.environ["OPENAI_API_KEY"] = api_key
client = OpenAI()


def get_response_from_llm_client(params: LLMParams):
    response = client.responses.create(
        model=params.model,
        input=params.prompt,
    )
    return response
