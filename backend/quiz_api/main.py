from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from quiz_api.models.quiz import Snippet
from quiz_api.services.quiz_service import QuizService

app = FastAPI(title="ThenElse - Quiz API", version="1.0.0")

# Configuration CORS pour le frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # À restreindre en production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Health"])
def read_root():
    return {"message": "ThenElse Quiz API", "status": "running"}


@app.get("/get_random_snippet", response_model=Snippet, tags=["Quiz"])
def get_random_snippet() -> Snippet:
    """Récupère un snippet de code aléatoire avec ses réponses possibles."""
    return QuizService.get_random_snippet()


@app.get("/snippets/count", tags=["Stats"])
def get_snippets_count():
    """Retourne le nombre total de snippets disponibles."""
    return QuizService.get_snippets_count()


@app.get("/snippets/{snippet_id}", response_model=Snippet, tags=["Quiz"])
def get_snippet_by_id(snippet_id: int):
    """Récupère un snippet spécifique par son ID."""
    return QuizService.get_snippet_by_id(snippet_id)
