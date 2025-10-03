from pydantic import BaseModel
from llm_requests.models import RequestInfo


# Sub models for the responses
class FileSummary(BaseModel):
    file_name: str
    request_name: str
    created_at: str


class FolderSummary(BaseModel):
    folder_name: str
    files_count: int
    total_size_kb: float
    last_file_date: str


class FolderInfo(BaseModel):
    file_list: list[str] = []
    files_count: int = 0
    invalid_files_count: int = 0
    models: list[str] = []
    input_tokens: int = 5
    output_tokens: int = 0
    input_cost: float = 0.0
    output_cost: float = 0.0
    total_cost: float = 0.0


# Models for the responses
class FoldersResponse(BaseModel):
    folders: list[FolderSummary]


class FolderContentResponse(BaseModel):
    folder_summary: FolderSummary
    folder_info: FolderInfo
    files: list[FileSummary]


class RequestInfoResponse(RequestInfo):
    """Modèle hérité de celui de RequestInfo qui est utilisé pour créer le fichier JSON."""

    pass
