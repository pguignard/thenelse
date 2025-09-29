#!/usr/bin/env bash
set -e

# Fonction d'aide
show_help() {
    echo "Usage: $0 [OPTION]"
    echo ""
    echo "Options:"
    echo "  -b, --backend    Lance le backend FastAPI"
    echo "  -w, --website    Lance le frontend React (Vite dev server)"
    echo "  -h, --help       Affiche cette aide"
    echo ""
    echo "Sans option, lance les deux en parallèle avec préfixes pour le logging."
}

# Fonction pour lancer le backend
run_backend() {
    echo "🚀 Lancement du backend FastAPI en mode DEV"
    source .venv/bin/activate
    cd backend
    uvicorn quiz_api.main:app --reload --host 0.0.0.0 --port 8000
}

# Fonction pour lancer le website
run_website() {
    echo "🚀 Lancement du frontend React en mode DEV"
    cd website
    npm run dev
}

# Traitement des options
case "$1" in
    -b|--backend)
        run_backend
        ;;
    -w|--website)
        run_website
        ;;
    -h|--help)
        show_help
        exit 0
        ;;
    "")
        # Aucune option : lancer les deux en parallèle avec préfixes
        # pour le logging
        run_backend  2>&1 | sed 's/^/[FASTAPI] /' &
        run_website  2>&1 | sed 's/^/[REACT] /' &
        wait
        ;;
    *)
        echo "❌ Erreur: Option inconnue '$1'"
        echo ""
        show_help
        exit 1
        ;;
esac