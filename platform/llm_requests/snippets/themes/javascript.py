from ..models import Levels

themes = {
    Levels.BEGINNER: [
        "Variables et portée : savoir déclarer et manipuler des variables avec let et const, comprendre la portée bloc vs globale et éviter les redeclarations inutiles.",
        "Types primitifs : manipuler les types string, number, boolean, null, undefined, symbol et bigint, et savoir vérifier leur type avec typeof.",
        "Opérateurs : utiliser les opérateurs arithmétiques (+, -, *, /, %), les opérateurs de comparaison (===, !==) et les opérateurs logiques (&&, ||, !) pour construire des expressions.",
        "Chaînes de caractères : créer et manipuler des chaînes avec template literals, concaténation et méthodes utiles comme slice, toUpperCase, includes.",
        "Contrôle de flux : écrire des conditions avec if/else et switch, utiliser l’opérateur ternaire pour simplifier les expressions.",
        "Boucles : répéter des instructions avec for, while et for...of, et comprendre quand utiliser chaque type de boucle.",
        "Tableaux simples : créer et manipuler des tableaux, accéder aux éléments par index, utiliser les méthodes de base comme push, pop et length.",
        "Objets simples : créer des objets avec des paires clé/valeur, accéder et modifier leurs propriétés, et supprimer des clés.",
        "Fonctions simples : définir des fonctions avec function et return, utiliser des fonctions fléchées pour simplifier la syntaxe.",
        "Valeurs truthy/falsy : comprendre les valeurs évaluées comme vraies ou fausses, tester des conditions implicites et éviter les pièges de coercition.",
    ],
    Levels.INTERMEDIATE: [
        "Destructuring : extraire facilement des valeurs de tableaux et d’objets avec la syntaxe de déstructuration, simplifier la lecture et l’écriture du code.",
        "Rest & spread : utiliser les opérateurs ... pour copier, fusionner et passer un nombre variable d’arguments à une fonction.",
        "Fonctions avancées : utiliser des paramètres par défaut, écrire et appeler des callbacks, comprendre les closures et leur rôle dans la portée.",
        "Méthodes de tableau : manipuler des collections avec map, filter, reduce, find, some et every pour transformer ou analyser les données.",
        "Objets avancés : utiliser les propriétés calculées, parcourir les clés et valeurs avec Object.keys, Object.values et Object.entries.",
        "Classes (ES6) : définir des classes avec constructor et méthodes, comprendre l’héritage simple avec extends et l’utilisation de super.",
        "Promesses de base : créer et utiliser des promesses, enchaîner then et catch, écrire du code asynchrone lisible avec async/await.",
        "Manipulation du JSON : convertir des données avec JSON.stringify et JSON.parse, et stocker temporairement en mémoire.",
        "Gestion des erreurs : comprendre le comportement des erreurs, utiliser try/catch/finally, lancer des erreurs personnalisées avec throw.",
        "Timers : exécuter du code différé ou répété avec setTimeout et setInterval, et comprendre leur annulation avec clearTimeout et clearInterval.",
    ],
    Levels.EXPERT: [
        "Closures et scope avancé : comprendre les fonctions imbriquées, la mémorisation et comment les closures capturent leur environnement lexical.",
        "POO avancée : utiliser les méthodes statiques, implémenter des mixins pour simuler l’héritage multiple, et redéfinir des méthodes dans les classes filles.",
        "Asynchrone avancé : combiner plusieurs promesses avec Promise.all et Promise.race, gérer les erreurs avec try/catch dans un contexte async/await.",
        "Event loop et micro/macro-tâches : analyser l’ordre d’exécution des instructions avec setTimeout, Promise.resolve et comprendre le fonctionnement de la boucle d’événements.",
        "Itérateurs et générateurs : créer des fonctions génératrices avec function* et yield, utiliser for...of pour parcourir des itérateurs personnalisés.",
        "Symbol et propriétés privées : utiliser Symbol pour créer des clés uniques et les champs privés (#) pour encapsuler les données dans une classe.",
        "Opérateurs avancés : utiliser l’opérateur de coalescence nulle (??), le chaînage optionnel (?.) et l’affectation logique (??=) pour simplifier le code.",
        "Regex en JavaScript : créer et utiliser des expressions régulières pour rechercher, tester et remplacer des motifs dans les chaînes.",
        "Pattern de programmation fonctionnelle : utiliser la composition de fonctions, map/filter/reduce imbriqués et l’immuabilité pour écrire du code expressif.",
    ],
}
