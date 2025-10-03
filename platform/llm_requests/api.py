from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from llm_requests.api_services.history_routes import router as history


logger = logging.getLogger("uvicorn.error")  # erreurs serveur
access_logger = logging.getLogger("uvicorn.access")  # logs HTTP

app = FastAPI()
app.include_router(history, prefix="/history")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # ou ["*"] en dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health check
@app.get("/health")
def health_check():
    logger.info("Logger health check")
    return {"status": "healthy"}
