from fastapi import FastAPI
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
history_dir = BASE_DIR / "request_history"
ndjson_dir = BASE_DIR / "ndjson_snippets"

app = FastAPI()


@app.get("/health")
def health_check():
    return {"status": "healthy"}


# Request History


@app.get("/get_request_history")
def get_request_history():
    """Liste les fichiers dans le dossier platform/request_history
    Envoie le contenu (json) de chaque fichier dans une seule réponse"""
    files = history_dir.glob("*.json")
    return {"request_history": [f.read_text() for f in files]}


@app.get("/get_request_history_file_list")
def get_request_history_file_list():
    """Liste les fichiers dans le dossier platform/request_history
    Envoie la liste des noms de fichiers dans une seule réponse"""
    files = history_dir.glob("*.json")
    return {"request_history_files": [f.name for f in files]}


@app.get("/get_request_history_file_content")
def get_request_history_file_content(file_name: str):
    """Récupère le contenu d'un fichier spécifique dans le dossier platform/request_history"""
    file_path = history_dir / f"{file_name}.json"
    print(file_path.resolve())
    if file_path.exists():
        return {"file_content": file_path.read_text()}
    return {"error": "File not found"}


# NDJSON Snippets


@app.get("/get_ndjson_snippets")
def get_ndjson_snippets():
    """Liste les fichiers dans le dossier platform/ndjson_snippets
    Envoie le contenu (ndjson) de chaque fichier dans une seule réponse"""
    files = ndjson_dir.glob("*.ndjson")
    return {"ndjson_snippets": [f.read_text() for f in files]}


@app.get("/get_ndjson_snippets_file_list")
def get_ndjson_snippets_file_list():
    """Liste les fichiers dans le dossier platform/ndjson_snippets
    Envoie la liste des noms de fichiers dans une seule réponse"""
    files = ndjson_dir.glob("*.ndjson")
    return {"ndjson_snippets_files": [f.name for f in files]}


@app.get("/get_ndjson_snippets_file_content")
def get_ndjson_snippets_file_content(file_name: str):
    """Récupère le contenu d'un fichier spécifique dans le dossier platform/ndjson_snippets"""
    file_path = ndjson_dir / f"{file_name}.ndjson"
    if file_path.exists():
        return {"file_content": file_path.read_text()}
    return {"error": "File not found"}
