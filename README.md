
# ThenElse – Fullstack Quiz App (POC)

Application de quiz interactive.

- **Backend**: FastAPI + Uvicorn (port 8000)
- **Frontend**: React + Vite (port 5173)


## Installation et lancement du projet en local

### 💾 - Installation

#### Backend env
Créer l'environnement virtuel à la racine du projet (pas dans le dossier backend)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

#### Frontend (React + Vite)

Installer [Node.js + npm](https://nodejs.org/en/download) 

```bash
cd website
npm install
```
L'install utilise le fichier "package.json" du dossier website

---

### 🚀 - Lancement

#### 🔄 Avec le script de lancement

À la racine du projet, dans deux terminaux différents:

```bash
./run-dev.sh -b # backend
./run-dev.sh -w # website
```

#### 🕹️ En manuel

Pour le backend python (uvicorn)

```bash
cd backend
uvicorn quiz_api.main:app --reload --host 0.0.0.0 --port 8000
```

Pour le React (website)

```bash
cd website
npm run dev
```


#### ✅ Résultat 

- **API** disponible sur [http://127.0.0.1:8000](http://127.0.0.1:8000)
- **Website** disponible sur [http://127.0.0.1:5173](http://127.0.0.1:5173)

Arrêt avec `CTRL+C`.

---

### 🛠️ - Troubleshooting

#### Port déjà utilisé (8000 ou 5173)

Erreur classique si un vieux process tourne encore.  
Vérifier :

```bash
lsof -i :8000
lsof -i :5173
```

et tuer le process :

```bash
kill -9 <PID>
```

👉 Astuce : ajoute un alias dans `~/.zshrc` :

```bash
alias killport='f() { lsof -ti :$1 | xargs kill -9; }; f'
```

Ensuite :

```bash
killport 8000
killport 5173
```
