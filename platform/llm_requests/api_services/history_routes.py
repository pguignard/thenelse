from fastapi import APIRouter

from llm_requests.api_services.models import (
    FoldersResponse,
    FolderContentResponse,
    RequestInfoResponse,
)

from llm_requests.api_services.utils import (
    HISTORY_DIR,
    get_folder_summary,
    get_folder_aggregated_info,
    get_info_from_file_name,
    get_list_of_json_files,
    load_request_info,
)


router = APIRouter()


# Request History files and content
@router.get("/folders")
def get_folders_list_route() -> FoldersResponse:
    """Retourne la liste des dossiers dans le dossier platform/request_history
    Renvoie un résumé de chaque dossier (FolderSummary) avec le nombre de fichiers, la taille totale et la date du dernier fichier.
    """
    folder_list = HISTORY_DIR.glob("*/")
    return FoldersResponse(
        folders=[get_folder_summary(f) for f in folder_list if f.is_dir()]
    )


@router.get("/folders/{folder_name}/content")
def get_folder_content_route(folder_name: str) -> FolderContentResponse:
    """Retourne le contenu d'un dossier spécifique:  avec la liste des fichiers et leurs infos (list[FileInfo]) et des infos agrégées les fichiers (FolderInfo)."""
    files_names = get_list_of_json_files(folder_name)
    return FolderContentResponse(
        folder_summary=get_folder_summary(HISTORY_DIR / folder_name),
        folder_info=get_folder_aggregated_info(folder_name, files_names),
        files=[get_info_from_file_name(file_name) for file_name in files_names],
    )


@router.get("/folders/{folder_name}/content/{file_name}")
def get_request_info_route(folder_name: str, file_name: str) -> RequestInfoResponse:
    """Récupère le contenu d'un fichier spécifique dans le dossier platform/request_history"""
    info = load_request_info(folder_name, file_name)
    return RequestInfoResponse.model_validate(info.model_dump())
