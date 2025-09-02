    echo "🚀 Lancement du backend ADMIN"
    source .venv/bin/activate
    cd platform
    uvicorn admin_backend.main:app --reload --host 0.0.0.0 --port 8000
