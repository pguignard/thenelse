
# ThenElse – Fullstack Quiz App (POC)

Application de quiz interactive avec architecture fullstack moderne.
Pour l'instant ça tourne que en local :)

- **Backend**: FastAPI + Uvicorn (port 8000)
- **Frontend**: React + Vite (port 5173)

## 🚀 Lancer le projet en local

### Prérequis
- [Node.js + npm](https://nodejs.org/en/download) (via `brew install node` sur macOS)
- Un environnement virtuel Python (`python -m venv .venv`)

---

### 1. Installation

#### Backend env
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
````

#### Frontend (React + Vite)

```bash
cd website
npm install
```

---

### 2. Lancer en mode **développement**
#### 🔹 Option A : manuel 

Pour le backend python (uvicorn)

```bash
cd backend
uvicorn main:app --reload --port 8000
```

Pour le React (website)

```bash
cd website
npm run dev
```


#### 🔹 Option B : script 

À la racine du projet, dans deux terminaux différents:

```bash
./run-dev.sh -b # backend
./run-dev.sh -w # website
```

#### 🔹Résultat 

- **API** disponible sur [http://127.0.0.1:8000](http://127.0.0.1:8000)
- **Website** disponible sur [http://127.0.0.1:5173](http://127.0.0.1:5173)

Arrêt avec `CTRL+C`.


---

## 🛠️ Troubleshooting

### Port déjà utilisé (8000 ou 5173)

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
