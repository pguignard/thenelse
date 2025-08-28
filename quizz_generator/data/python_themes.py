python_themes = {
    "Python Standard": {
        "Débutant": [
            "Syntaxe et variables de base",
            "Types primitifs (int, float, str, bool)",
            "Opérateurs arithmétiques et logiques",
            "Contrôle de flux (if, for, while)",
            "Listes et tuples",
            "Dictionnaires et ensembles",
            "Fonctions simples (def, return)",
            "Entrées/sorties de base (input, print)",
        ],
        "Confirmé": [
            "Compréhensions de listes/dicts/sets",
            "Fonctions avancées (args, kwargs, lambda)",
            "Gestion des exceptions (try/except/raise)",
            "Modules et imports",
            "Lecture/écriture de fichiers",
            "Context managers (with)",
        ],
        "Expert": [
            "Programmation orientée objet avancée",
            "Méthodes spéciales (__init__, __str__, __repr__...)",
            "Itérateurs et générateurs (yield, __iter__)",
            "Décorateurs simples et paramétrés",
            "Gestion fine de la mémoire (mutabilité, deepcopy)",
            "Programmation fonctionnelle (map, filter, reduce, closures)",
            "Context managers personnalisés",
        ],
    },
    "Librairies Utiles": {
        "Confirmé": [
            "datetime (dates, heures, formats, fuseaux)",
            "os et pathlib (fichiers, répertoires)",
            "json et csv (sérialisation, parsing)",
            "re (expressions régulières)",
            "collections (Counter, defaultdict, deque)",
            "random et statistics",
            "unittest / pytest (tests simples)",
        ],
        "Expert": [
            "asyncio (coroutines, tasks, futures)",
            "threading et multiprocessing",
            "subprocess (exécution et communication)",
            "logging avancé (handlers, formatters)",
            "argparse (scripts CLI complexes)",
            "typing (Union, Protocol, generics, mypy)",
            "dataclasses avancées",
            "functools (lru_cache, partial, wraps)",
            "concurrent.futures (threads/process pools)",
            "inspect et importlib (introspection)",
        ],
    },
    "Data Science": {
        "Débutant": [
            "Numpy (tableaux, opérations de base)",
            "Pandas (DataFrames, séries, import CSV/Excel)",
            "Matplotlib (graphiques simples)",
        ],
        "Confirmé": [
            "Numpy (indexation avancée, broadcasting)",
            "Pandas (groupby, merge, nettoyage de données)",
            "Matplotlib/Seaborn (visualisation avancée)",
            "Statistiques de base",
        ],
        "Expert": [
            "Optimisation avec Numpy (vectorisation)",
            "Pandas (multi-index, performance)",
            "Matplotlib (customisation poussée, subplots)",
            "SciPy (optimisation, stats avancées)",
        ],
    },
    "Web": {
        "Débutant": ["HTTP et API basics", "Flask (routes simples, réponses JSON)"],
        "Confirmé": [
            "Flask (blueprints, middlewares)",
            "FastAPI (schemas, validation, réponses spécifiques)",
            "Django (models, views, templates)",
        ],
        "Expert": [
            "FastAPI avancé (async, dépendances, websockets)",
            "Django avancé (ORM, migrations complexes, admin)",
            "Sécurité (authentification, tokens, sessions)",
        ],
    },
    "Automatisation & Scripting": {
        "Confirmé": [
            "Scripts CLI avec argparse",
            "Manipulation fichiers et répertoires",
            "Automatisation système (os, shutil, pathlib)",
        ],
        "Expert": [
            "Scripting avancé avec subprocess",
            "Tâches parallèles (multiprocessing)",
            "Création de CLI robustes (click, argparse avancé)",
        ],
    },
    "Tests & Qualité": {
        "Confirmé": [
            "unittest (tests unitaires, assertions)",
            "pytest (tests paramétrés, fixtures simples)",
            "doctest",
        ],
        "Expert": [
            "pytest avancé (fixtures, mocks, plugins)",
            "CI/CD (intégration des tests)",
            "Couverture de code et bonnes pratiques",
        ],
    },
}
