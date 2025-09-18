from pathlib import Path
from pydantic import BaseModel
from fastapi import HTTPException

from .conf import HISTORY_DIR

from .multi_request_informations import (
    get_multi_request_informations,
    MultiRequestInformation,
)

# Sub models for the responses


class FileInfo(BaseModel):
    file_name: str
    request_name: str
    created_at: str


class FolderInfo(BaseModel):
    folder_name: str
    files_count: int
    total_size_kb: float


# Models for the responses


class RHFolderListResponse(BaseModel):
    folders: list[FolderInfo]


class RHFolderContentResponse(BaseModel):
    files_infos: list[FileInfo]
    folder_info: MultiRequestInformation


# Main functions, called by the routes /get_request_history_file_list and /get_request_history_folder_list


def get_request_history_folder_list() -> RHFolderListResponse:
    """Liste les dossiers dans le dossier platform/request_history
    Envoie la liste des informations de fichiers dans une seule réponse"""
    folder_list = HISTORY_DIR.glob("*/")
    return RHFolderListResponse(
        folders=[get_folder_info(f) for f in folder_list if f.is_dir()]
    )


def get_request_history_folder_content(
    folder_name: str,
) -> RHFolderContentResponse:
    """Retourne le contenu d'un dossier spécifique dans le dossier platform/request_history
    Envoie la liste des informations de fichiers dans une seule réponse"""
    folder_path = HISTORY_DIR / folder_name
    if not folder_path.exists() or not folder_path.is_dir():
        raise HTTPException(status_code=404, detail="Folder not found")
    file_list = list(folder_path.glob("*.json"))
    file_names = [f.name for f in file_list if f.is_file()]

    return RHFolderContentResponse(
        files_infos=[
            get_file_info_from_file_name(file_name) for file_name in file_names
        ],
        folder_info=get_multi_request_informations(folder_name, file_names),
    )


# Sub functions


def get_folder_info(folder_path: Path) -> FolderInfo:
    """Récupère les informations d'un dossier."""
    file_list = list(folder_path.glob("*.json"))
    total_size_kb = sum(f.stat().st_size for f in file_list) / 1024  # en KB
    return FolderInfo(
        folder_name=folder_path.name,
        files_count=len(file_list),
        total_size_kb=round(total_size_kb, 2),
    )


def get_file_info_from_file_name(file_name: str) -> FileInfo:
    """Récupère les informations d'un fichier à partir de son nom."""
    # filename example: 20250909_085027_test.json
    parts = file_name.split("_")
    created_at = "_".join(parts[0:2])  # 20250909_085027
    request_name = "_".join(parts[2:]).replace(".json", "")  # test
    return FileInfo(
        file_name=file_name, request_name=request_name, created_at=created_at
    )
