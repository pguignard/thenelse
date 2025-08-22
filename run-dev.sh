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
    echo "Exemples:"
    echo "  $0 -b            Lance uniquement le backend"
    echo "  $0 -w            Lance uniquement le website"
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

# Vérification des arguments
if [ $# -eq 0 ]; then
    echo "❌ Erreur: Aucune option spécifiée"
    echo ""
    show_help
    exit 1
fi

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
    *)
        echo "❌ Erreur: Option inconnue '$1'"
        echo ""
        show_help
        exit 1
        ;;
esac
