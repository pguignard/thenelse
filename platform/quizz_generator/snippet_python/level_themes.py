from enum import Enum
from pydantic import BaseModel


class Level(Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    EXPERT = "expert"


level_description = {
    Level.BEGINNER: "Niveau débutant : snippets très courts et lisibles (0–10 lignes), centrés sur une seule idée. Ils doivent illustrer clairement un concept de base sans piégeage inutile. Le snippet doit manipuler des données simulant un contexte métier minimal (listes de prix, utilisateurs, votes, logs, etc.), où les noms de variables peuvent aider à deviner la réponse.",
    Level.INTERMEDIATE: "Niveau confirmé : snippets de taille moyenne, comprenant éventuellement des fonctions ou des classes, et combinant plusieurs notions: le thème proposé, ainsi que des notions de bases et avancées (5–20 lignes). Ils doivent mettre en évidence des subtilités du langage et pousser à lire attentivement l’exécution. Les noms de variables/fonctions/classes sont neutres et ne doivent pas aider à deviner la réponse.",
    Level.EXPERT: "Niveau expert : snippets longs et complexes, comprenant soit plusieurs fonctions, soit une ou des classes, intégrant en plus du thème proposé, des mécanismes avancés de divers types (10–25 lignes). Ils doivent forcer une réflexion approfondie sur l’ordre d’exécution et les comportements moins évidents. Les noms de variables/fonctions/classes sont neutres et ne doivent pas aider à deviner la réponse.",
}

themes = {
    Level.BEGINNER: [
        "Syntaxe et variables de base (affectation, conventions de nommage)",
        "Types primitifs (int, float, str, bool)",
        "Chaînes de caractères (f-strings, format, slicing simple)",
        "Conversion de types (int(), str(), float(), bool())",
        "Opérateurs arithmétiques et logiques (+, -, *, /, %, //, **, and, or, not)",
        "Contrôle de flux (if, for, while)",
        "Vérité implicite et booléens (if [], if 0, if 'abc')",
        "Opérateurs d’identité et de comparaison (== vs is, in, not in)",
        "Listes (indexation, slicing, méthodes append/pop)",
        "Indexation négative et slicing avec pas ([::-1])",
        "Tuples (immutabilité, unpacking)",
        "Différence mutable vs immutable (list vs tuple vs str)",
        "Dictionnaires (ajout, accès, get, keys, values)",
        "Ensembles (ajout, intersection, union, différences)",
        "Fonctions simples (def, return, paramètres)",
    ],
    Level.INTERMEDIATE: [
        "Programmation orientée objet simple (classe, attributs, héritage simple)",
        "Compréhensions de listes, sets et dictionnaires",
        "Fonctions avancées (args, kwargs, lambda)",
        "Portée des variables et closures simples",
        "Fonctions intégrées utiles (enumerate, zip, any, all, min, max...)",
        "Tri et clés de tri (sorted, key=, min/max avec key), tri stable",
        "Gestion des exceptions (try/except/finally/raise)",
        "Itérateurs (iter, next), générateurs (yield)",
        "Mutabilité et paramètres par défaut (piège de la liste mutable)",
        "Fonctions imbriquées, décorateurs simples",
        "Modules standards courants (math, random, datetime)",
        "Expressions régulières de base (re.match, re.search, re.findall)",
        "Manipulation avancée de listes (insertion, suppression, tri in-place)",
        "Manipulation avancée de chaînes (join, split, replace, slicing complexe)",
        "Manipulation avancée de dictionnaires (comprehensions, fusion, tri)",
        "Utilisation d’all() et any() avec générateurs",
    ],
    Level.EXPERT: [
        "Classes avancées (propriétés, méthodes de classe/instance, attributs statiques)",
        "Méthodes spéciales (__init__, __str__, __len__, __getitem__)",
        "Itérateurs personnalisés (__iter__, __next__), générateurs avancés",
        "Décorateurs avancés (avec paramètres, empilement)",
        "Programmation fonctionnelle (map, filter, reduce, sorted avec key)",
        "Métaclasses et introspection (type(), isinstance(), getattr(), setattr())",
        "Mutabilité avancée et copies (shallow vs deepcopy sur structures imbriquées)",
        "Modules standards puissants (itertools, functools, collections)",
        "Typage et annotations avancées (Union, Optional, Callable, generics simples)",
        "Context managers personnalisés (__enter__, __exit__)",
        "Slots (__slots__) et optimisation mémoire",
        "Async/await basique (exemples avec asyncio.sleep, exécution concurrente)",
    ],
}


class LevelThemeParams(BaseModel):
    level_string: str
    level_description: str
    theme: str


def theme_list_for_one_level(level: Level) -> list[LevelThemeParams]:
    """Retourne la liste des thèmes disponibles pour un niveau donné."""
    return [
        LevelThemeParams(
            level_string=level.name,
            level_description=level_description[level],
            theme=theme,
        )
        for theme in themes.get(level, [])
    ]


def theme_list_for_all_levels() -> list[LevelThemeParams]:
    """Retourne la liste de tous les thèmes pour tous les niveaux."""
    return [theme for level in Level for theme in theme_list_for_one_level(level)]


if __name__ == "__main__":
    # Test de la fonction
    all_themes = theme_list_for_all_levels()
    print(f"Total themes: {len(all_themes)}")
    print(all_themes[0])
    print(all_themes[1])
    print(all_themes[-1])
