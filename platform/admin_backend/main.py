from fastapi import FastAPI
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware

from admin_backend.services.request_history import (
    get_request_history_file_list,
    RequestHistoryFileListResponse,
    get_request_informations,
    RequestInformations,
)

BASE_DIR = Path(__file__).parent.parent
ndjson_dir = BASE_DIR / "ndjson_snippets"

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # ou ["*"] en dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check():
    return {"status": "healthy"}


# Request History files and content


@app.get("/get_request_history_file_list")
def get_request_history_file_list_route() -> RequestHistoryFileListResponse:
    """Liste les fichiers dans le dossier platform/request_history
    Envoie la liste des noms de fichiers dans une seule réponse"""
    return get_request_history_file_list()


@app.get("/get_request_information")
def get_request_information_route(file_name: str) -> RequestInformations:
    """Récupère le contenu d'un fichier spécifique dans le dossier platform/request_history"""
    return get_request_informations(file_name)


# NDJSON Snippets


@app.get("/get_ndjson_snippets_file_list")
def get_ndjson_snippets_file_list():
    """Liste les fichiers dans le dossier platform/ndjson_snippets
    Envoie la liste des noms de fichiers dans une seule réponse"""
    files = ndjson_dir.glob("*.ndjson")
    return {"files": [f.name for f in files]}
