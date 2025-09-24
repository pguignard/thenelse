import json
from pydantic import BaseModel
from fastapi import HTTPException

from .conf import HISTORY_DIR

# --------------------------------------------------------------------------------------
# Request informations

# All models are pre filled with default values to avoid validation errors
# And return empty objects with is_valid=False if data is missing


class NotValidFileError(Exception):
    pass


class LLMResponse(BaseModel):
    model: str = ""
    temperature: float = 0.0
    service_tier: str = ""
    input_tokens: int = 0
    output_tokens: int = 0
    reasoning_tokens: int = 0


class CostInformations(BaseModel):
    input_cost: float = 0.0
    output_cost: float = 0.0
    reasoning_cost: float = 0.0
    reasoning_percent: float = 0.0
    total_cost: float = 0.0


class RequestInformations(BaseModel):
    is_valid: bool = True
    validity_error: str = ""
    model: str = ""
    prompt: str = ""
    response_content: str = ""
    llm_response: LLMResponse
    cost_info: CostInformations


# Main function, called by the route /get_request_information


def get_request_informations(folder_name: str, file_name: str) -> RequestInformations:
    """Récupère les informations d'une requête spécifique à partir de son nom de fichier et de son dossier."""
    try:
        file_content = get_file_content_as_dict(folder_name, file_name)
        return compute_request_informations(file_content)
    except NotValidFileError as e:
        return RequestInformations(
            is_valid=False,
            validity_error="Erreur inconnue: " + str(e),
            llm_response=LLMResponse(),
            cost_info=CostInformations(),
        )


def compute_request_informations(file_content: dict) -> RequestInformations:
    """Transforme le contenu d'un fichier request_report en objet RequestInformations"""
    check_file_validity(file_content)

    # On a besoin de model et llm_response pour calculer le coût
    model = file_content.get("model", "")
    llm_response = get_llm_response(file_content)
    cost_info = calculate_cost(llm_response, model)

    return RequestInformations(
        model=model,
        prompt=file_content.get("prompt", ""),
        response_content=get_response_content(file_content),
        llm_response=llm_response,
        cost_info=cost_info,
    )


# Sub functions


def get_file_content_as_dict(folder_name: str, file_name: str) -> dict:
    """Récupère le contenu d'un fichier spécifique dans le dossier platform/request_history"""
    file_path = HISTORY_DIR / folder_name / f"{file_name}"
    if not file_path.exists():
        raise HTTPException(status_code=404, detail=f"File not found: {file_name}")
    return json.loads(file_path.read_text())


def check_file_validity(file_content_dict: dict) -> bool:
    """Vérifie la validité du contenu d'un fichier de requête."""
    required_keys = ["model", "prompt", "response"]
    if not all(key in file_content_dict for key in required_keys):
        raise NotValidFileError("Structure de fichier invalide")


def get_response_content(file_content_dict: dict) -> str:
    """Extrait le contenu textuel de la réponse LLM du contenu du fichier."""
    output_list = file_content_dict["response"]["output"]
    """
    Structure de la réponse: 
    ["response"]["output"] -> liste de dicts d'output, dont un "reasoning" et un "text" pour gpt-5, ou juste un "text" pour gpt-4.1
    On exclut l'output de type "reasoning"
    Sinon on regarde le champs content (liste), qui contient un dict avec un champs "text" et un champs "type" qui est égal à "output_text"
    """
    for output in output_list:
        if output.get("type") == "reasoning":
            continue
        content = output.get("content", None)

    for item in content:
        if item.get("type") == "output_text":
            return item.get("text", "")


def get_llm_response(file_content_dict: dict) -> LLMResponse:
    """Extrait les informations LLMResponse du contenu du fichier."""
    # On extrait les sous-dictionnaires imbriqués
    llm_response_dict = file_content_dict.get("response", {})
    llm_usage_dict = llm_response_dict.get("usage", {})
    reasoning_tokens = llm_usage_dict.get("output_tokens_details", {})
    # On fusionne les dictionnaires pour créer l'objet LLMResponse
    joined_dict = {**llm_response_dict, **llm_usage_dict, **reasoning_tokens}
    return LLMResponse(**joined_dict)


def calculate_cost(llm_response: LLMResponse, model: str) -> CostInformations:
    """Calcule le coût approximatif en cents en fonction des tokens et du modèle."""
    # Prices are in dollars per 1 Million tokens
    pricing = {
        "gpt-5-nano": {"input": 0.05, "output": 0.40},
        "gpt-5-mini": {"input": 0.25, "output": 2.00},
        "gpt-4.1": {"input": 2.00, "output": 8.00},
        "gpt-4.1-nano": {"input": 0.10, "output": 0.40},
        "gpt-4.1-mini": {"input": 0.40, "output": 1.60},
        "gpt-4o-mini": {"input": 0.15, "output": 0.60},
    }
    # For cent conversion
    COST_PER_CENT = 100
    if model not in pricing:
        return CostInformations()
    input_cost = (
        (llm_response.input_tokens / 1_000_000)
        * pricing[model]["input"]
        * COST_PER_CENT
    )
    output_cost = (
        (llm_response.output_tokens / 1_000_000)
        * pricing[model]["output"]
        * COST_PER_CENT
    )
    total_cost = input_cost + output_cost

    # Calcul du coût de raisonnement si les tokens de raisonnement sont disponibles
    reasoning_cost = (
        (llm_response.reasoning_tokens / 1_000_000)
        * pricing[model]["output"]
        * COST_PER_CENT
    )
    # Pourcentage du prix de raisonnement par rapport au prix total
    reasoning_percent = (reasoning_cost / total_cost) * 100 if total_cost > 0 else 0.0

    return CostInformations(
        input_cost=round(input_cost, 10),
        output_cost=round(output_cost, 10),
        reasoning_cost=round(reasoning_cost, 10),
        reasoning_percent=round(reasoning_percent, 2),
        total_cost=round(total_cost, 10),
    )
