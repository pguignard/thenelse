from fastapi import APIRouter

router = APIRouter(tags=["Health"])


@router.get("/health")
def read_root():
    """Endpoint de santé de l'API."""
    return {"message": "ThenElse Quiz API", "status": "running"}
