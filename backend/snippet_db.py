snippet_db_json = [
  {
    "snippet": "print(\"\".join(sorted(\"bca\")))",
    "reponses": ["\"abc\"", "\"bca\"", "[\"a\", \"b\", \"c\"]", "TypeError"],
    "bonne_reponse_id": 0,
    "explication": "sorted() retourne une liste triée de caractères. ''.join(...) recompose une chaîne. Ici: \"abc\"."
  },
  {
    "snippet": "def f(x=[]):\n    x.append(1)\n    return len(x)\n\nf()\nf()\nprint(f())",
    "reponses": ["1", "2", "3", "TypeError"],
    "bonne_reponse_id": 2,
    "explication": "L’argument par défaut liste est partagé entre appels (mutable). Après trois appels successifs, sa longueur vaut 3."
  },
  {
    "snippet": "try:\n    {}[\"x\"]\nexcept Exception as e:\n    print(type(e).__name__)",
    "reponses": ["KeyError", "NameError", "TypeError", "No exception"],
    "bonne_reponse_id": 0,
    "explication": "Accéder à une clé inexistante sur un dict lève un KeyError. On affiche le nom de l’exception."
  },
  {
    "snippet": "s = \"python\"\nprint(s[::-2])",
    "reponses": ["\"nhy\"", "\"nhto\"", "\"nhtp\"", "\"pyt\""],
    "bonne_reponse_id": 0,
    "explication": "Slicing avec step -2 parcourt les indices 5,3,1 de \"python\" → 'n','h','y' donc \"nhy\"."
  },
  {
    "snippet": "try:\n    a = (1, 2, 3)\n    a[0] = 9\nexcept Exception as e:\n    print(type(e).__name__)",
    "reponses": ["IndexError", "TypeError", "ValueError", "No exception"],
    "bonne_reponse_id": 1,
    "explication": "Les tuples sont immuables; tenter d’assigner un élément lève TypeError."
  },
  {
    "snippet": "print(5 // 2)",
    "reponses": ["2", "2.5", "3", "TypeError"],
    "bonne_reponse_id": 0,
    "explication": "// est la division entière (floor) sur des int: 5 // 2 = 2."
  },
  {
    "snippet": "print(bool(\"False\"))",
    "reponses": ["True", "False", "\"False\"", "TypeError"],
    "bonne_reponse_id": 0,
    "explication": "Toute chaîne non vide est évaluée à True en booléen, même \"False\"."
  },
  {
    "snippet": "x = 5\nlst = [x for x in range(3)]\nprint(x)",
    "reponses": ["5", "2", "3", "NameError"],
    "bonne_reponse_id": 0,
    "explication": "Depuis Python 3, la compréhension a sa portée locale; elle n’écrase pas la variable x externe. On affiche 5."
  },
  {
    "snippet": "d = {\"a\": 1}\nprint(d.get(\"b\", d.get(\"a\") + 1))",
    "reponses": ["1", "2", "None", "KeyError"],
    "bonne_reponse_id": 1,
    "explication": "get(\"b\", défaut) retourne le défaut si la clé n’existe pas. Ici défaut = d.get(\"a\") + 1 = 2."
  },
  {
    "snippet": "def gen():\n    yield 10\n    return 7\n\ng = gen()\ntry:\n    next(g)\n    next(g)\nexcept StopIteration as e:\n    print(e.value)",
    "reponses": ["10", "7", "None", "StopIteration"],
    "bonne_reponse_id": 1,
    "explication": "À la fin d’un générateur, return X lève StopIteration avec value=X. On capture puis on affiche 7."
  }
]
