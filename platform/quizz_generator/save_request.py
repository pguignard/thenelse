import json
import datetime
from pathlib import Path

from quizz_generator.openai_api import get_response_from_llm_client, RequestParams


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
    output_dir: str,
    request_name: str,
    request_params: RequestParams,
    response: dict,
) -> str:
    """Génère des requêtes vers le LLM et sauvegarde les réponses dans des fichiers JSON."""

    # Envoi de la requête à l'API LLM
    response = get_response_from_llm_client(request_params)

    # Stockage dans l'historique des requêtes
    request_report = {
        "model": request_params.model,
        "prompt": request_params.prompt,
        "response": response,
    }

    # Créer filename avec prompt_type et timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = Path(REQUESTS_ROOT_DIR) / output_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    # "gpt-4o-mini" -> "4o-mini"
    model_short = request_params.model[4:]

    file_path = output_dir / f"{timestamp}_{request_name}({model_short}).json"
    # Sauvegarder les données dans un fichier JSON
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(request_report, f, indent=2, ensure_ascii=False)

    return str(file_path)
