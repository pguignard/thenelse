from ..models import Levels

themes = {
    Levels.BEGINNER: [
        "Annotations de type : savoir déclarer des variables avec un type explicite (string, number, boolean), comprendre l’inférence de type automatique.",
        "Types spéciaux : utiliser any, unknown, void et never et comprendre leurs différences d’usage.",
        "Fonctions typées : écrire des fonctions avec des paramètres et des valeurs de retour typés, éviter les erreurs de compatibilité.",
        "Objets typés : définir des objets avec des propriétés typées et optionnelles, et utiliser readonly pour les rendre immuables.",
    ],
    Levels.INTERMEDIATE: [
        "Tableaux et tuples typés : créer des collections avec des types précis, manipuler des tuples avec des longueurs et positions fixes.",
        "Unions et intersections : combiner plusieurs types possibles avec | et &, et restreindre les possibilités de valeur.",
        "Enums et littéraux de chaîne : définir des ensembles de valeurs fixes et améliorer la lisibilité du code.",
        "Interfaces et types : définir des contrats pour les objets, comparer interface et type alias et comprendre quand utiliser l’un ou l’autre.",
        "Génériques simples : créer des fonctions et structures réutilisables avec des types génériques basiques.",
    ],
    Levels.EXPERT: [
        "Narrowing et type guards : affiner les types à l’exécution avec typeof, instanceof et des prédicats personnalisés.",
        "Génériques avancés : utiliser les contraintes avec extends, les types par défaut et combiner plusieurs génériques.",
        "Types utilitaires intégrés : maîtriser Partial, Required, Pick, Omit, Record et d’autres pour transformer des types.",
        "Mapped types et conditionnels : générer des types dynamiques avec des clés calculées et des conditions (extends ? :).",
        "Décorateurs et métaprogrammation : introduire les décorateurs pour classes et méthodes, et comprendre leur usage avancé.",
    ],
}
