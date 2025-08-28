from pydantic import BaseModel, Field, field_validator


class Snippet(BaseModel):
    language: str = Field(...)
    level: str = Field(...)
    theme: str = Field(...)
    length: int = Field(...)
    snippet: str = Field(...)
    choices: list[str] = Field(...)
    answer_id: int = Field(..., ge=0)
    explanation: str = Field(...)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "snippet": "print(5 // 2)",
                    "choices": ["2", "2.5", "3", "TypeError"],
                    "answer_id": 0,
                    "explanation": "// est la division entière (floor) sur des int: 5 // 2 = 2.",
                }
            ]
        }
    }

    @field_validator("answer_id")
    @classmethod
    def validate_answer_id(cls, v, info):
        # On récupère les réponses depuis le contexte de validation
        if "choices" in info.data:
            choices = info.data["choices"]
            if v >= len(choices):
                raise ValueError(
                    f"answer_id ({v}) doit être inférieur au nombre de réponses ({len(choices)})"
                )
        return v
