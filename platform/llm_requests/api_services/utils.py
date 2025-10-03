from pathlib import Path
import json

from llm_requests.models import RequestInfo
from llm_requests.api_services.models import FolderInfo, FileSummary, FolderSummary
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.parent
HISTORY_DIR = BASE_DIR / "request_history"


# File and Folder operations
def get_file_path(folder_name: str, file_name: str) -> Path:
    folder_path = HISTORY_DIR / folder_name
    file_path = folder_path / file_name
    if not file_path.exists() or not file_path.is_file():
        raise FileNotFoundError(f"File not found: {file_name}")
    return file_path


def get_folder_path(folder_name: str) -> Path:
    folder_path = HISTORY_DIR / folder_name
    if not folder_path.exists() or not folder_path.is_dir():
        raise FileNotFoundError(f"Folder not found: {folder_name}")
    return folder_path


def get_list_of_json_files(folder_name: str) -> list[str]:
    folder_path = get_folder_path(folder_name)
    return [f.name for f in folder_path.glob("*.json") if f.is_file()]


def get_folder_summary(folder_path: Path) -> FolderSummary:
    """Récupère les infos d'un dossier."""
    file_list = list(folder_path.glob("*.json"))
    total_size_kb = sum(f.stat().st_size for f in file_list) / 1024  # en KB
    # Get last file date from get_file_info
    if file_list:
        last_file = max(file_list, key=lambda f: f.stat().st_mtime)
        last_file_date = get_info_from_file_name(last_file.name).created_at
    else:
        last_file_date = ""
    return FolderSummary(
        folder_name=folder_path.name,
        files_count=len(file_list),
        total_size_kb=round(total_size_kb, 2),
        last_file_date=last_file_date,
    )


def get_info_from_file_name(file_name: str) -> FileSummary:
    """Récupère les infos d'un fichier à partir de son nom."""
    # filename example: 20250909_085027_test.json
    parts = file_name.split("_")
    created_at = "_".join(parts[0:2])  # 20250909_085027
    request_name = "_".join(parts[2:]).replace(".json", "")  # test
    return FileSummary(
        file_name=file_name, request_name=request_name, created_at=created_at
    )


def get_file_content_as_dict(folder_name: str, file_name: str) -> dict:
    """Récupère le contenu d'un fichier spécifique dans le dossier platform/request_history"""
    file_path = get_file_path(folder_name, file_name)
    return json.loads(file_path.read_text())


def load_request_info(folder_name: str, file_name: str) -> RequestInfo:
    file_content = get_file_content_as_dict(folder_name, file_name)
    return RequestInfo.model_validate(file_content)


def get_folder_aggregated_info(folder_name: str, file_list: list[str]) -> FolderInfo:
    aggregated_info = FolderInfo()
    aggregated_info.file_list = file_list
    invalid_files = []
    for file_name in file_list:
        try:
            request_info = load_request_info(folder_name, file_name)
        except Exception as e:
            aggregated_info.invalid_files_count += 1
            invalid_files.append(file_name)
            continue
        aggregated_info.files_count += 1
        if request_info.response_info.model not in aggregated_info.models:
            aggregated_info.models.append(request_info.response_info.model)
        aggregated_info.input_tokens += request_info.response_info.input_tokens
        aggregated_info.output_tokens += request_info.response_info.output_tokens
        aggregated_info.input_cost += request_info.cost_info.input_cost
        aggregated_info.output_cost += request_info.cost_info.output_cost
        aggregated_info.total_cost += request_info.cost_info.total_cost
    # Optionnel : log ou retourne la liste des fichiers invalides
    return aggregated_info
