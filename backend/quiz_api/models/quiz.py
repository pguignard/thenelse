from pydantic import BaseModel, Field, field_validator


class Snippet(BaseModel):
    language: str = Field(...)
    level: str = Field(...)
    theme: str = Field(...)
    snippet: str = Field(...)
    choices: list[str] = Field(...)
    answer_id: int = Field(..., ge=0)
    explanation: str = Field(...)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "language": "Python",
                    "level": "BEGINNER",
                    "theme": "Listes",
                    "snippet": "notes = [12, 15, 9, 14]\nprint(notes[2])",
                    "choices": ["9", "12", "14", "15"],
                    "answer_id": 0,
                    "explanation": "Le code crée une liste `notes` contenant quatre éléments. En Python, l'indexation des listes commence à 0, donc `notes[0]` vaut 12, `notes[1]` vaut 15, et `notes[2]` vaut 9. Le print affiche donc la valeur à l'index 2, qui est 9.\n\nL'indexation des listes en Python est basée sur un système zéro-indexé, ce qui signifie que le premier élément a l'index 0. Cette propriété est fondamentale dans la manipulation des listes, car elle permet un accès direct et rapide à un élément en utilisant un entier représentant sa position.",
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


class SnippetsCount(BaseModel):
    total_snippets: int = Field(..., ge=0)
    snippets_per_language_level: dict[str, dict[str, int]] = Field(...)
    # Ex: {"Python": {"BEGINNER": 10, "INTERMEDIATE": 5}, "JavaScript": {"BEGINNER": 8}}
