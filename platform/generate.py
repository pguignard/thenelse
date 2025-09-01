import json
import datetime
from pathlib import Path
import typer

from quizz_generator import *
from quizz_generator.llm_api import LLMParams, get_response_from_llm_client

app = typer.Typer()
OUTPUT_DIR = "request_history"


@app.command()
def main(test: bool = typer.Option(False, help="Active le mode test (prompt simple)")):
    if not test:
        prompt = generate_prompt()
    else:
        prompt = "Say Hello"

    request_params = LLMParams(prompt=prompt)
    response = get_response_from_llm_client(request_params)

    # Créer filename avec prompt_type et timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = Path(OUTPUT_DIR)
    output_dir.mkdir(parents=True, exist_ok=True)
    file_name = output_dir / f"output__{request_params.prompt_type}__{timestamp}.json"

    # écrire dans un fichier JSON
    with open(file_name, "w", encoding="utf-8") as f:
        json.dump(response.to_dict(), f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    app()
