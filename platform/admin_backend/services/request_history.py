from pathlib import Path
from pydantic import BaseModel
import json

BASE_DIR = Path(__file__).parent.parent.parent
history_dir = BASE_DIR / "request_history"

# --------------------------------------------------------------------------------------
# Request History File list


class FileInfo(BaseModel):
    file_name: str
    request_name: str
    created_at: str


class RequestHistoryFileListResponse(BaseModel):
    files: list[FileInfo]


def get_request_history_file_list() -> RequestHistoryFileListResponse:
    """Liste les fichiers dans le dossier platform/request_history
    Envoie la liste des informations de fichiers dans une seule réponse"""
    file_list = history_dir.glob("*.json")
    return RequestHistoryFileListResponse(
        files=[get_file_info_from_file_name(f.name) for f in file_list]
    )


def get_file_info_from_file_name(file_name: str) -> FileInfo:
    """Récupère les informations d'un fichier à partir de son nom."""
    # filename example: output_test_1_snippets_20250902_093020.json
    # parts : request_name : test_1_snippets, created_at: 20250902_093020
    parts = file_name.split("_")
    request_name = " ".join(parts[1:-2])
    created_at = f"{parts[-2]}_{parts[-1].split('.')[0]}"
    return FileInfo(
        file_name=file_name, request_name=request_name, created_at=created_at
    )


# --------------------------------------------------------------------------------------
# Request informations


class RequestInput(BaseModel):
    model: str
    language: str
    level: str
    theme: str
    snippet_count: int
    prompt: str = None


class LLMResponse(BaseModel):
    model: str
    temperature: float
    service_tier: str
    input_tokens: int
    output_tokens: int
    reasoning_tokens: int = 0


class CostInfo(BaseModel):
    input_cost: float = 0.0
    output_cost: float = 0.0
    reasoning_cost: float = 0.0
    reasoning_percent: float = 0.0
    total_cost: float = 0.0
    total_cost_per_cent: float = 0.0


class RequestInformations(BaseModel):
    snippet_batch: list[dict]
    request_input: RequestInput
    llm_response: LLMResponse
    cost_info: CostInfo


def get_request_informations(file_name: str) -> RequestInformations:
    content = get_file_content_as_dict(file_name)
    request_input = get_request_input(content)
    llm_response = get_llm_response(content)
    cost_info = calculate_cost(llm_response, request_input.model)
    return RequestInformations(
        snippet_batch=get_snippet_batch(content),
        request_input=request_input,
        llm_response=llm_response,
        cost_info=cost_info,
    )


# Sub functions


def get_file_content_as_dict(file_name: str) -> dict:
    """Récupère le contenu d'un fichier spécifique dans le dossier platform/request_history"""
    file_path = history_dir / f"{file_name}.json"
    print(f"Reading: {file_path.resolve()}")
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    return json.loads(file_path.read_text())


def get_snippet_batch(file_content_dict: dict) -> list[dict]:
    if not file_content_dict.get("snippet_batch", False):
        return []
    snippet_json = json.loads(file_content_dict.get("snippet_batch", {}))
    return snippet_json.get("snippets", [])


def get_request_input(file_content_dict: dict) -> RequestInput:
    request_input = file_content_dict.get("request_input", {})
    return RequestInput(**request_input)


def get_llm_response(file_content_dict: dict) -> LLMResponse:
    llm_response_dict = file_content_dict.get("response", {})
    llm_usage_dict = llm_response_dict.get("usage", {})
    reasoning_tokens = llm_usage_dict.get("output_tokens_details", {})
    joined_dict = {**llm_response_dict, **llm_usage_dict, **reasoning_tokens}
    return LLMResponse(**joined_dict)


def calculate_cost(llm_response: LLMResponse, model: str) -> CostInfo:
    """Calcule le coût approximatif en dollars en fonction des tokens et du modèle."""
    # Prices are in dollars per 1 Million tokens
    pricing = {
        "gpt-5-nano": {"input": 0.05, "output": 0.40},
        "gpt-5-mini": {"input": 0.25, "output": 2.00},
        "gpt-4.1-nano": {"input": 0.10, "output": 0.40},
    }
    if model not in pricing:
        return CostInfo()
    input_cost = (llm_response.input_tokens / 1_000_000) * pricing[model]["input"]
    output_cost = (llm_response.output_tokens / 1_000_000) * pricing[model]["output"]
    total_cost = input_cost + output_cost

    # If reasoning tokens are present, calculate their cost as well
    reasoning_cost = (llm_response.reasoning_tokens / 1_000_000) * pricing[model][
        "output"
    ]
    reasoning_percent = (
        (llm_response.reasoning_tokens / llm_response.output_tokens) * 100
        if llm_response.output_tokens > 0
        else 0
    )

    return CostInfo(
        input_cost=round(input_cost, 10),
        output_cost=round(output_cost, 10),
        reasoning_cost=round(reasoning_cost, 10),
        reasoning_percent=round(reasoning_percent, 2),
        total_cost=round(total_cost, 10),
        total_cost_per_cent=round(total_cost * 100, 10),
    )
