#!/bin/bash
set -e  # stoppe en cas d'erreur

# 1. Dossier du frontend
FRONTEND_DIR="./website/src/api"

# 2. Génération des types à partir de l'OpenAPI de FastAPI
echo "📥 Génération des types TypeScript depuis FastAPI..."
echo "⚠️ Assure-toi que le backend FastAPI est en cours d'exécution sur http://localhost:8000"
read -p "Appuie sur Entrée pour continuer..."
npx openapi-typescript http://localhost:8000/openapi.json --output schema.ts

# 3. Création du dossier si nécessaire
mkdir -p "$FRONTEND_DIR"

# 4. Copie dans ton projet React
echo "📦 Copie des types dans $FRONTEND_DIR/schema.ts"
cp schema.ts "$FRONTEND_DIR/schema.ts"

# 5. Nettoyage optionnel du fichier temporaire
rm schema.ts

echo "✅ Types générés et copiés avec succès !"
