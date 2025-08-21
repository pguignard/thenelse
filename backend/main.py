import random

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator

from snippet_db import snippet_db_json

app = FastAPI(title="ThenElse - Quiz API", version="1.0.0")

# Configuration CORS pour le frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # À restreindre en production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Snippet(BaseModel):
    snippet: str = Field(..., example="print(5 // 2)")
    reponses: list[str] = Field(..., example=["2", "2.5", "3", "TypeError"])
    bonne_reponse_id: int = Field(..., ge=0, example=0)
    explication: str = Field(..., example="// est la division entière (floor) sur des int: 5 // 2 = 2.")
    
    @field_validator('bonne_reponse_id')
    @classmethod
    def validate_bonne_reponse_id(cls, v, info):
        # On récupère les réponses depuis le contexte de validation
        if 'reponses' in info.data:
            reponses = info.data['reponses']
            if v >= len(reponses):
                raise ValueError(f"bonne_reponse_id ({v}) doit être inférieur au nombre de réponses ({len(reponses)})")
        return v

@app.get("/", tags=["Health"])
def read_root():
    return {"message": "ThenElse Quiz API", "status": "running"}

@app.get("/get_random_snippet", response_model=Snippet, tags=["Quiz"])
def get_random_snippet() -> Snippet:
    """Récupère un snippet de code aléatoire avec ses réponses possibles."""
    if not snippet_db_json:
        raise HTTPException(status_code=404, detail="Aucun snippet disponible")
    
    snippet_data = random.choice(snippet_db_json)
    
    # La validation est maintenant automatique grâce au @field_validator
    return Snippet(**snippet_data)

@app.get("/snippets/count", tags=["Stats"])
def get_snippets_count():
    """Retourne le nombre total de snippets disponibles."""
    return {"total_snippets": len(snippet_db_json)}

@app.get("/snippets/{snippet_id}", response_model=Snippet, tags=["Quiz"])
def get_snippet_by_id(snippet_id: int):
    """Récupère un snippet spécifique par son ID."""
    if snippet_id < 0 or snippet_id >= len(snippet_db_json):
        raise HTTPException(status_code=404, detail="Snippet non trouvé")
    
    snippet_data = snippet_db_json[snippet_id]
    return Snippet(**snippet_data)
