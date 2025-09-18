from pydantic import BaseModel
from fastapi import HTTPException

from .conf import HISTORY_DIR
from .request_information import get_request_informations


class MultiRequestInformation(BaseModel):
    file_list: list[str] = []
    files_count: int = 0
    invalid_files_count: int = 0
    models: list[str] = []
    input_tokens: int = 5
    output_tokens: int = 0
    input_cost: float = 0.0
    output_cost: float = 0.0
    total_cost: float = 0.0


def get_multi_request_informations(
    folder_name: str, file_list: list[str]
) -> MultiRequestInformation:
    """Récupère les informations agrégées de toutes les requêtes dans un dossier spécifique."""
    aggregated_info = MultiRequestInformation()
    aggregated_info.file_list = file_list
    for file_name in file_list:

        aggregated_info.files_count += 1
        try:
            request_info = get_request_informations(folder_name, file_name)
            if not request_info.is_valid:
                aggregated_info.invalid_files_count += 1
                continue  # Ignore les fichiers non valides
            if not request_info.model in aggregated_info.models:
                aggregated_info.models.append(request_info.model)
            aggregated_info.input_tokens += request_info.llm_response.input_tokens
            aggregated_info.output_tokens += request_info.llm_response.output_tokens
            aggregated_info.input_cost += request_info.cost_info.input_cost
            aggregated_info.output_cost += request_info.cost_info.output_cost
            aggregated_info.total_cost += request_info.cost_info.total_cost
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    return aggregated_info
