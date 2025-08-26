from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


def create_app() -> FastAPI:
    """Crée et configure l'application FastAPI."""
    app = FastAPI(title="ThenElse - Quiz API", version="1.0.0")

    # Configuration CORS pour le frontend
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173"],  # ou ["*"] en dev
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app
