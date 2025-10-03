import datetime
from pathlib import Path
from pydantic import BaseModel

from llm_requests.openai_api import RequestParams
from llm_requests.request_information import (
    get_response_content,
    get_response_info,
    get_cost_info,
)
from llm_requests.models import (
    RequestInfo,
    ResponseInfo,
    CostInfo,
)

"""
Lance des requêtes vers le LLM et sauvegarde les réponses dans des fichiers JSON.
Utilise open_ai.py pour la communication avec le LLM
    (ce module est séparé au cas où on voudrait changer de fournisseur LLM).

Arguments :
- flex (bool) : si True, utilise le service_tier 'flex' (plus lent, moins cher)
- file_name (str) : nom de la requête, utilisé pour nommer le fichier de sortie

"""

REQUESTS_ROOT_DIR = "request_history"


def save_request(
    folder_name: str,
    request_name: str,
    prompt: str,
    response: dict,
) -> str:
    """Génère des requêtes vers le LLM et sauvegarde les réponses dans des fichiers JSON."""

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    response_content = get_response_content(response)
    response_info: ResponseInfo = get_response_info(response)
    cost_info: CostInfo = get_cost_info(response_info)

    request_info = RequestInfo(
        request_name=request_name,
        timestamp=timestamp,
        prompt=prompt,
        response_content=response_content,
        response_info=response_info,
        cost_info=cost_info,
    )

    # Créer filename avec prompt_type et timestamp
    output_dir = Path(REQUESTS_ROOT_DIR) / folder_name
    output_dir.mkdir(parents=True, exist_ok=True)
    # "gpt-4o-mini" -> "4o-mini"
    model_short = response_info.model[4:]

    file_path = output_dir / f"{timestamp}_{request_name}({model_short}).json"
    # Sauvegarder les données dans un fichier JSON
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(request_info.model_dump_json(indent=2))

    return str(file_path)
