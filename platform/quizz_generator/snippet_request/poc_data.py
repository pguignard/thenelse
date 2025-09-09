from enum import Enum


class Level(Enum):
    BEGINNER = "beginner"
    ADVANCED = "advanced"
    EXPERT = "expert"
    UNDERTERMINED = "undetermined"


level_description = {
    Level.BEGINNER: "Niveau débutant : snippets très courts et lisibles, centrés sur une seule idée. Ils doivent illustrer clairement un concept de base sans piégeage inutile.",
    Level.ADVANCED: "Niveau confirmé : snippets de taille moyenne combinant plusieurs notions. Ils doivent mettre en évidence des subtilités du langage et pousser à lire attentivement l’exécution.",
    Level.EXPERT: "Niveau expert : snippets plus longs et complexes, intégrant des mécanismes avancés. Ils doivent forcer une réflexion approfondie sur l’ordre d’exécution et les comportements moins évidents.",
}

poc_data = {
    "Levels": {
        Level.BEGINNER: [
            "Syntaxe et variables de base",
            "Types primitifs (int, float, str, bool)",
            "Opérateurs arithmétiques et logiques",
            "Contrôle de flux (if, for, while)",
            "Listes et tuples",
            "Dictionnaires et ensembles",
            "Fonctions simples (def, return)",
            "Entrées/sorties de base (input, print)",
        ],
        Level.ADVANCED: [
            "Compréhensions de listes/dicts/sets",
            "Fonctions avancées (args, kwargs, lambda)",
            "Gestion des exceptions (try/except/raise)",
            "Modules et imports",
            "Lecture/écriture de fichiers",
            "Context managers (with)",
        ],
        Level.EXPERT: [
            "Programmation orientée objet avancée",
            "Méthodes spéciales (__init__ and other dunder methods)",
            "Itérateurs et générateurs (yield, __iter__)",
            "Décorateurs simples et paramétrés",
            "Gestion fine de la mémoire (mutabilité, deepcopy)",
            "Programmation fonctionnelle (map, filter, reduce, closures)",
            "Context managers personnalisés",
        ],
    },
}

# Fonction pour obtenir le thème suivant, ainsi que sa difficulté (return tuple (level, theme))


def get_next_theme():
    """Générateur: l'ensemble des thèmes sous forme de tuples (niveau, thème)"""
    for level, themes in poc_data["Levels"].items():
        for theme in themes:
            yield (level, theme)


def get_random_theme(level: Level = Level.UNDERTERMINED):
    """Un seul thème.
    Préciser le niveau avec `level`."""
    import random

    if level == Level.UNDERTERMINED:
        level, theme = random.choice(list(get_next_theme()))
        return level, theme

    themes = poc_data["Levels"].get(level, [])
    if not themes:
        raise ValueError(f"Niveau inconnu ou sans thèmes : {level}")
    theme = random.choice(themes)
    return level, theme
