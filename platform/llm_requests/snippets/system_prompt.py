from .models import Languages


system_prompt = """
Tu es un créateur de quiz techniques, destinés à s'entraîner et à s'évaluer sur la lecture de code.
L'objectif est de créer des portions de code qui mettent en évidence un concept ou une fonctionnalité spécifique de {language_name}, et dont il faut deviner la sortie en lisant le code.
Le principe est de définir une variable dans le code, puis de demander quelle est sa valeur après exécution du code. 
La valeur peut être un type de données standard {types} ou une exception {exceptions}.
Le code se termine systématiquement par un {print_function} pour afficher la valeur à deviner.

Règles du snippet :
- Peut être exécuté dans un environnement standard {language_name} {version}.
- Déterministe, pas d’I/O, pas de hasard, pas de dépendances externes.
- Définit et modifie une variable, et se termine par un {print_function_name}.
- Il ne doit y avoir qu'un seul {print_function_name}, si on veut afficher plusieurs valeurs à différents moments, utiliser une structure de données ({collections}) pour les stocker, puis les afficher en une seule fois.
- Doit illustrer un concept ou une fonctionnalité spécifique de {language_name}, en lien avec le thème donné.
- Pas de calcul mental compliqué nécessaire pour deviner la sortie (valeurs simples, pas de calculs complexes avec flottants).
- Le code doit être lisible, structuré, et pédagogique, respectant les conventions de style de {language_name}.
{poo_boilerplate}
- Pas de commentaires.

Règles des réponses :
- 4 propositions différentes, une seule correcte.
- Les réponses incorrectes doivent être variées : certaines proches du bon résultat, d’autres reflétant des erreurs fréquentes de compréhension des concepts.
- L'ID de la bonne réponse est entre 0 et 3 (index dans la liste).

Explication :
- Explication en Markdown (≈500 caractères ±50%), claire et concise, structurée en 2 paragraphes distincts.
- Utiliser **gras** pour les points essentiels, `inline code` pour les noms techniques, et *italique* pour les définitions théoriques.
- Le premier paragraphe doit expliquer en détail l'exécution du code, étape par étape, et comment on arrive à la bonne réponse.
- Le deuxième paragraphe doit donner une explication encyclopédique et pédagogique des concepts clés du snippet (définitions, origine, usage courant en {language_name}), indépendamment du code.
- Ne mentionne pas les numéros des réponses dans l'explication (évite "réponse 1", "réponse 2", etc.).

Rappels machine :
- Échapper correctement les caractères spéciaux dans "snippet" et "text".
- Un seul {print_function_name}, si on veut afficher plusieurs choses, utiliser une structure de données ({collections}).
"""

language_configs = {
    Languages.PYTHON: {
        "language_name": "Python",
        "version": "3.13",
        "print_function": "print(<variable>)",
        "print_function_name": "print()",
        "types": "(int, float, str, list, dict, bool, etc.)",
        "exceptions": "(ZeroDivisionError, IndexError, TypeError, etc.)",
        "collections": "tuple, list, dict",
        "poo_boilerplate": "",
    },
    Languages.JAVASCRIPT: {
        "language_name": "JavaScript",
        "version": "ES2023",
        "print_function": "console.log(<variable>)",
        "print_function_name": "console.log()",
        "types": "(number, string, boolean, array, object, null, undefined)",
        "exceptions": "(TypeError, ReferenceError, RangeError, etc.)",
        "collections": "array, object, Map, Set",
        "poo_boilerplate": "",
    },
    Languages.TYPESCRIPT: {
        "language_name": "TypeScript",
        "version": "5.x",
        "print_function": "console.log(<variable>)",
        "print_function_name": "console.log()",
        "types": "(number, string, boolean, array, tuple, enum, any, unknown, etc.)",
        "exceptions": "(TypeError, ReferenceError, etc.)",
        "collections": "array, tuple, Map, Set",
        "poo_boilerplate": "",
    },
    Languages.JAVA: {
        "language_name": "Java",
        "version": "21",
        "print_function": "System.out.println(<variable>)",
        "print_function_name": "System.out.println()",
        "types": "(int, double, String, array, List, Map, etc.)",
        "exceptions": "(ArithmeticException, NullPointerException, ArrayIndexOutOfBoundsException, etc.)",
        "collections": "array, List, Map",
        "poo_boilerplate": """- Le snippet montré à l’utilisateur contient uniquement le code utile (déclarations, opérations, affichage) sans forcément afficher le code nécessaire à l'exécution. Par exemple :  `public class Quiz { public static void main(String[] args) { /* snippet */ } } `}`Seul le contenu de la méthode main "/* snippet */" est visible.`""",
    },
    Languages.CPP: {
        "language_name": "C++",
        "version": "C++20",
        "print_function": "std::cout << <variable> << std::endl",
        "print_function_name": "std::cout",
        "types": "(int, double, string, array, vector, map, etc.)",
        "exceptions": "(std::out_of_range, std::bad_alloc, etc.)",
        "collections": "array, vector, map, set",
        "poo_boilerplate": """- Le snippet montré à l’utilisateur contient uniquement le code utile (déclarations, opérations, affichage) sans forcément afficher le code nécessaire à l'exécution. Par exemple : `#include <iostream>\nint main() { /* snippet */ return 0; }` seul le contenu de la fonction main "/* snippet */" est visible.""",
    },
    Languages.CSHARP: {
        "language_name": "C#",
        "version": "12",
        "print_function": "Console.WriteLine(<variable>)",
        "print_function_name": "Console.WriteLine()",
        "types": "(int, double, string, array, List, Dictionary, etc.)",
        "exceptions": "(DivideByZeroException, NullReferenceException, IndexOutOfRangeException, etc.)",
        "collections": "array, List, Dictionary",
        "concepts": "portée des variables, classes, héritage, polymorphisme, LINQ, exceptions",
        "poo_boilerplate": """- Le snippet montré à l’utilisateur contient uniquement le code utile (déclarations, opérations, affichage) sans forcément afficher le code nécessaire à l'exécution. Par exemple :   `class Program { static void Main() { /* snippet */ } }` seul le contenu de la méthode Main "/* snippet */" est visible.""",
    },
    Languages.C: {
        "language_name": "C",
        "version": "C17",
        "print_function": "printf(<format_string>, <variable>)",
        "print_function_name": "printf()",
        "types": "(int, float, char*, arrays, structs, etc.)",
        "exceptions": "(segmentation fault, undefined behavior, etc. – simulées pour le quiz)",
        "collections": "arrays, structs",
        "poo_boilerplate": """- Le snippet montré à l’utilisateur contient uniquement le code utile (déclarations, opérations, affichage) sans forcément afficher le code nécessaire à l'exécution. Par exemple :   `#include <stdio.h>\nint main() { /* snippet */ return 0; }` seul le contenu de la fonction main "/* snippet */" est visible.""",
    },
}


def get_system_prompt(language: Languages) -> str:
    """Construit le prompt système pour la génération de snippets."""
    config = language_configs.get(language)
    if not config:
        raise ValueError(f"Unsupported language: {language}")

    return system_prompt.format(
        language_name=config["language_name"],
        version=config["version"],
        print_function=config["print_function"],
        print_function_name=config["print_function_name"],
        types=config["types"],
        exceptions=config["exceptions"],
        collections=config["collections"],
        poo_boilerplate=config["poo_boilerplate"],
    )


if __name__ == "__main__":
    # Fais la liste des langages présent dans la config
    print("Langages supportés pour les snippets de quiz :")
    for lang in Languages:
        if not lang in language_configs:
            print(f"- {lang.name} (non supporté, pas de configuration)")
    # Vérifie que chaque élément de configuration est présent pour chaque langage
    supported_langs = [lang for lang in Languages if lang in language_configs]
    print(
        f"\nVérification des configurations pour {len(supported_langs)} langages supportés..."
    )
    for lang in supported_langs:
        try:
            prompt = get_system_prompt(lang)
            assert "{language_name}" not in prompt
            assert "{print_function}" not in prompt
            assert "{print_function_name}" not in prompt
            assert "{version}" not in prompt
            assert "{types}" not in prompt
            assert "{exceptions}" not in prompt
            assert "{collections}" not in prompt
            print(f"Configuration OK pour {lang.name}")
        except Exception as e:
            print(f"Erreur dans la configuration pour {lang.name}: {e}")

    # Print un exemple de prompt
    example_prompt = get_system_prompt(Languages.PYTHON)
    print("\nExemple de prompt système pour Python :\n")
    print(example_prompt)
