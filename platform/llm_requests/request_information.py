from llm_requests.models import CostInfo, ResponseInfo


def get_response_content(response_dict: dict) -> str:
    """Extrait le contenu textuel de la réponse LLM du contenu du fichier.

    Structure de la réponse:
    ["response"]["output"] -> liste de dicts d'output, dont un "reasoning" et un "text" pour gpt-5, ou juste un "text" pour gpt-4.1
    On exclut l'output de type "reasoning"
    Sinon on regarde le champs content (liste), qui contient un dict avec un champs "text" et un champs "type" qui est égal à "output_text"
    """
    output_list = response_dict["output"]
    for output in output_list:
        if output.get("type") == "reasoning":
            continue
        content = output.get("content", None)

    for item in content:
        if item.get("type") == "output_text":
            return item.get("text", "")


def get_response_info(response_dict: dict) -> ResponseInfo:
    """Extrait les info LLMResponse du contenu du fichier."""
    # Model come in format "gpt-4o-mini-2024-08-06" > "gpt-4o-mini"
    model_long = response_dict.get("model", "")
    model_short = "-".join(model_long.split("-")[:3])
    info_dict = {
        "model": model_short,
        "temperature": response_dict.get("temperature", 0.0),
        "service_tier": response_dict.get("service_tier", ""),
    }
    usage_dict = response_dict.get("usage", {})
    info_dict.update(
        {
            "input_tokens": usage_dict.get("input_tokens", 0),
            "output_tokens": usage_dict.get("output_tokens", 0),
        }
    )
    # Cached tokens are in usage/input_tokens_details
    input_tokens_details = usage_dict.get("input_tokens_details", {})
    info_dict["cached_tokens"] = input_tokens_details.get("cached_tokens", 0)
    # reasoning_tokens are in usage/output_tokens_details
    output_tokens_details = usage_dict.get("output_tokens_details", {})
    info_dict["reasoning_tokens"] = output_tokens_details.get("reasoning_tokens", 0)

    return ResponseInfo(**info_dict)


def get_cost_info(llm_response: ResponseInfo) -> CostInfo:
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
    # Price per million
    PRICE_PER = 1_000_000

    if llm_response.model in pricing:
        model_pricing = pricing[llm_response.model]
    else:
        raise ValueError(f"Modèle inconnu pour le calcul du coût: {llm_response.model}")

    input_cost = (
        (llm_response.input_tokens / PRICE_PER) * model_pricing["input"] * COST_PER_CENT
    )
    output_cost = (
        (llm_response.output_tokens / PRICE_PER)
        * model_pricing["output"]
        * COST_PER_CENT
    )
    total_cost = input_cost + output_cost

    # Calcul du coût de raisonnement si les tokens de raisonnement sont disponibles
    reasoning_cost = (
        (llm_response.reasoning_tokens / PRICE_PER)
        * model_pricing["output"]
        * COST_PER_CENT
    )
    # Pourcentage du prix de raisonnement par rapport au prix total
    reasoning_percent = (reasoning_cost / total_cost) * 100 if total_cost > 0 else 0.0

    return CostInfo(
        input_cost=round(input_cost, 10),
        output_cost=round(output_cost, 10),
        reasoning_cost=round(reasoning_cost, 10),
        reasoning_percent=round(reasoning_percent, 2),
        total_cost=round(total_cost, 10),
    )
