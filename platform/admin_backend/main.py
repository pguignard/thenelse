from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging


logger = logging.getLogger("uvicorn.error")  # erreurs serveur
access_logger = logging.getLogger("uvicorn.access")  # logs HTTP

from admin_backend.services.request_history import (
    get_request_history_folder_list,
    RHFolderListResponse,
    get_request_history_folder_content,
    RHFolderContentResponse,
)
from admin_backend.services.request_information import (
    get_request_informations,
    RequestInformations,
)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # ou ["*"] en dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health check
@app.get("/health")
def health_check():
    logger.info("Logger health check")
    return {"status": "healthy"}


# Request History files and content
@app.get("/get_request_history_folder_list")
def get_request_history_folder_list_route() -> RHFolderListResponse:
    """Retourne la liste des dossiers dans le dossier platform/request_history"""
    return get_request_history_folder_list()


@app.get("/get_request_history_folder_content")
def get_request_history_folder_content_route(
    folder_name: str,
) -> RHFolderContentResponse:
    """Retourne le contenu d'un dossier spécifique dans le dossier platform/request_history"""
    return get_request_history_folder_content(folder_name)


@app.get("/get_request_information")
def get_request_information_route(
    folder_name: str, file_name: str
) -> RequestInformations:
    """Récupère le contenu d'un fichier spécifique dans le dossier platform/request_history"""
    return get_request_informations(folder_name, file_name)
