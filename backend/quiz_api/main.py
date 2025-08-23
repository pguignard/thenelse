from quiz_api.core.config import create_app
from quiz_api.routers import health, quiz, stats

# Création de l'application
app = create_app()

# Enregistrement des routers
app.include_router(health.router)
app.include_router(quiz.router)
app.include_router(stats.router)
