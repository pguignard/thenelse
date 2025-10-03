#!/usr/bin/env python3

import json
import typer
import pathlib


from admin_backend.services.request_information import (
    get_request_infos,
)

"""
Generate a ndjson database with "request_history" files from a folder.
Get the request information from each file with api services.
"""


app = typer.Typer()

ROOT_DIR = pathlib.Path(__file__).parent
HISTORY_DIR = ROOT_DIR / "request_history"
DATA_DIR = ROOT_DIR / "databases"


@app.command()
def main(
    folder_name: str = typer.Option(
        ..., help="Nom du dossier dans platform/request_history"
    )
):
    """Génère une base de données ndjson à partir des fichiers request_history d'un dossier.

    - folder_name: nom du dossier dans platform/request_history
    """

    # Create path and check it exists
    folder_path = HISTORY_DIR / folder_name
    if not folder_path.exists() or not folder_path.is_dir():
        raise ValueError(f"Dossier inconnu: {folder_path}")

    # Crée la liste des noms de fichiers .json dans le dossier
    file_list = [
        f.name for f in folder_path.iterdir() if f.is_file() and f.suffix == ".json"
    ]
    if not file_list:
        raise ValueError(f"Aucun fichier .json trouvé dans le dossier: {folder_path}")
    print(f"{len(file_list)} fichiers trouvés dans le dossier {folder_path}")

    # Create output file
    output_path = DATA_DIR / f"{folder_name}.ndjson"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as output_file:
        for file_name in file_list:
            request_info = get_request_infos(folder_name, file_name)
            content = request_info.response_content
            # convert content string to dict
            content_dict = json.loads(content)
            snippet_batch = content_dict.get("snippets", [])
            # Write each snippet as a json line
            for snippet in snippet_batch:
                output_file.write(json.dumps(snippet))
                output_file.write("\n")
            print(f" - {file_name} > {len(snippet_batch)} snippets extraits.")


if __name__ == "__main__":
    app()
# To run: python platform/generate_database.py --folder-name=snippets_beginner
