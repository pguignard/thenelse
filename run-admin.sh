echo "🚀 Lancement du backend ADMIN"
source .venv/bin/activate
cd platform
uvicorn llm_requests.api:app --reload --host 0.0.0.0 --port 8000 2>&1 | sed 's/^/[FASTAPI] /' &
cd admin_website
npm run dev 2>&1 | sed 's/^/[REACT] /' &

