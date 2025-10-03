from .models import SnippetParams, Levels, Languages

user_prompt = """
Génère {snippet_count} snippets de code au format JSON, chacun avec 4 réponses possibles, une bonne réponse et une explication.
- Langage : {language}
- Niveau : {level}
> {level_description}
- Thème : {theme}
Respecte strictement les règles définies dans le prompt système, notamment :
- Le format du snippet défini dans le prompt système.
- Les 4 réponses possibles, avec une seule correcte.
- L'explication en Markdown avec les 2 paragraphes
Respecte scrupuleusement le nombre de snippets demandé: {snippet_count}.
"""

level_description = {
    Levels.BEGINNER: """Niveau débutant : snippets très courts et lisibles (0–10 lignes), centrés sur une seule idée. 
    Ils doivent illustrer clairement un concept de base sans piégeage inutile. Le snippet doit manipuler des données simulant un contexte métier minimal (listes de prix, utilisateurs, votes, logs, etc.), où les noms de variables peuvent aider à deviner la réponse.""",
    Levels.INTERMEDIATE: """Niveau confirmé : snippets de taille moyenne (5–15 lignes), pouvant contenir des fonctions ou des classes, illustrant le thème donné tout en utilisant des notions de bases pour étoffer l'exemple ({base_features}).
    Ils doivent mettre en évidence des subtilités du langage et pousser à lire attentivement l’exécution. Les noms de variables/fonctions/classes sont neutres et ne doivent pas aider à deviner la réponse.""",
    Levels.EXPERT: """Niveau expert : snippets longs et complexes (10–20 lignes), comprenant soit plusieurs fonctions, soit une ou des classes. Ils illustrent le thème proposé, et doivent inclure au moins un mécanisme de niveau intermédiaire ({intermediate_features}).
    Ils doivent forcer une réflexion approfondie sur l'ordre d'exécution, contenir des mécanismes complexes. Les noms de variables/fonctions/classes sont neutres et ne doivent pas aider à deviner la réponse.""",
}

features_config = {
    Languages.PYTHON: {
        "base_features": "variables, types primitifs, listes, dictionnaires, boucles, conditions, fonctions simples, exceptions de base",
        "intermediate_features": "fonctions avancées (args, kwargs, lambda), compréhensions, POO simple, itérateurs, générateurs",
    },
    Languages.JAVASCRIPT: {
        "base_features": "variables, types primitifs, tableaux, objets, boucles, conditions, fonctions simples, erreurs de base",
        "intermediate_features": "fonctions fléchées, closures, classes simples, callbacks, promesses, gestion d'exceptions",
    },
    Languages.TYPESCRIPT: {
        "base_features": "variables, types primitifs, tableaux, objets typés, boucles, conditions, fonctions simples, erreurs de base",
        "intermediate_features": "interfaces, génériques simples, unions/intersections, classes, async/await, gestion d'exceptions",
    },
    Languages.JAVA: {
        "base_features": "variables, types primitifs, tableaux, boucles, conditions, méthodes simples, exceptions de base",
        "intermediate_features": "POO (héritage, polymorphisme), collections (List, Map), lambdas, try/catch/finally",
    },
    Languages.CPP: {
        "base_features": "variables, types primitifs, tableaux, boucles, conditions, fonctions simples, exceptions de base",
        "intermediate_features": "classes, héritage, références, pointeurs, exceptions, templates simples",
    },
    Languages.CSHARP: {
        "base_features": "variables, types primitifs, tableaux, List, boucles, conditions, méthodes simples, exceptions de base",
        "intermediate_features": "POO (héritage, polymorphisme), LINQ basique, async/await, interfaces",
    },
    Languages.C: {
        "base_features": "variables, types primitifs, tableaux, boucles, conditions, fonctions simples",
        "intermediate_features": "pointeurs, arithmétique avancée, structures, gestion mémoire manuelle",
    },
}


def get_filled_level_description(level: Levels, language: Languages) -> str:
    """Retourne la description du niveau avec les fonctionnalités insérées."""
    return level_description[level].format(
        base_features=features_config[language]["base_features"],
        intermediate_features=features_config[language]["intermediate_features"],
    )


def get_user_prompt(prompt_params: SnippetParams, snippet_count: int) -> str:
    """Construit le prompt utilisateur pour la génération de snippets."""

    level_description_filled = get_filled_level_description(
        prompt_params.level, prompt_params.language
    )
    return user_prompt.format(
        snippet_count=snippet_count,
        language=prompt_params.language.value,
        level=prompt_params.level.value,
        level_description=level_description_filled,
        theme=prompt_params.theme,
    )


if __name__ == "__main__":
    # Fais la liste des langages présent dans la config
    print("Langages supportés pour les snippets de quiz :")
    for lang in Languages:
        if not lang in features_config:
            print(f"- {lang.name} (non supporté, pas de configuration)")

    # Vérifie que chaque élément de configuration est présent pour chaque langage
    supported_langs = [lang for lang in Languages if lang in features_config]
    print(
        f"\nVérification des configurations pour {len(supported_langs)} langages supportés..."
    )
    for lang in supported_langs:
        try:
            prompt = get_user_prompt(
                SnippetParams(
                    language=lang,
                    level=Levels.BEGINNER,
                    theme="Variables",
                    snippet_count=2,
                )
            )
            assert prompt.count("{") == 0, "Il reste des placeholders non remplis"
            assert "{snippet_count}" not in prompt
            assert "{language}" not in prompt
            assert "{level}" not in prompt
            assert "{level_description}" not in prompt
            assert "{theme}" not in prompt
            assert "{base_features}" not in prompt
            assert "{intermediate_features}" not in prompt
            print(f"Configuration OK pour {lang.name}")
        except AssertionError as ae:
            print(f"Erreur dans la configuration pour {lang.name}: {ae}")
        except Exception as e:
            print(f"Erreur inconnue dans {lang.name}: {e}")

    # Print un exemple de prompt
    example_prompt = get_user_prompt(
        SnippetParams(
            language=Languages.PYTHON,
            level=Levels.BEGINNER,
            theme="Listes",
            snippet_count=2,
        )
    )
    print("\nExemple de prompt généré :\n")
    print(example_prompt)
