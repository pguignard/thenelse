import os
from typing import Any, Dict

from pydantic import BaseModel
from openai import OpenAI

from quizz_generator.models import SnippetBatch

# Client configuration (get api key from .env local file in the same folder)


class RequestParams(BaseModel):
    model: str
    prompt: str
    service_tier: str = "flex"


with open(".env") as f:
    for line in f:
        if line.startswith("api_key="):
            api_key = line.strip().split("=")[1]
            break

os.environ["OPENAI_API_KEY"] = api_key
client = OpenAI()


def to_openai_schema(model: type[BaseModel]) -> Dict[str, Any]:
    """
    Convertit un modèle Pydantic en schéma JSON compatible OpenAI.
    - Ajoute "additionalProperties": False à tous les objets,
      y compris ceux définis dans $defs.
    """

    def _patch(schema: Dict[str, Any]) -> Dict[str, Any]:
        if schema.get("type") == "object":
            schema["additionalProperties"] = False
            if "properties" in schema:
                for sub in schema["properties"].values():
                    if isinstance(sub, dict):
                        _patch(sub)
        elif schema.get("type") == "array" and isinstance(schema.get("items"), dict):
            _patch(schema["items"])

        # patch récursif dans $defs
        if "$defs" in schema:
            for sub in schema["$defs"].values():
                if isinstance(sub, dict):
                    _patch(sub)

        return schema

    schema = model.model_json_schema()
    return _patch(schema)


def get_response_from_llm_client(params: RequestParams) -> dict:
    """Envoie une requête au client LLM et retourne la réponse en dict"""
    schema = to_openai_schema(SnippetBatch)

    response = client.responses.create(
        model=params.model,
        input=params.prompt,
        service_tier=params.service_tier,
        # reasoning={
        #     "effort": "minimal",
        # },
        text={
            "format": {
                "type": "json_schema",
                "name": "snippet_batch",
                "schema": schema,
                "strict": True,
            }
        },
    )

    return response.to_dict()
