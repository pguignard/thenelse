from pydantic import BaseModel, Field, field_validator


class Snippet(BaseModel):
    snippet: str = Field(..., example="print(5 // 2)")
    reponses: list[str] = Field(..., example=["2", "2.5", "3", "TypeError"])
    bonne_reponse_id: int = Field(..., ge=0, example=0)
    explication: str = Field(
        ..., example="// est la division entière (floor) sur des int: 5 // 2 = 2."
    )

    @field_validator("bonne_reponse_id")
    @classmethod
    def validate_bonne_reponse_id(cls, v, info):
        # On récupère les réponses depuis le contexte de validation
        if "reponses" in info.data:
            reponses = info.data["reponses"]
            if v >= len(reponses):
                raise ValueError(
                    f"bonne_reponse_id ({v}) doit être inférieur au nombre de réponses ({len(reponses)})"
                )
        return v
