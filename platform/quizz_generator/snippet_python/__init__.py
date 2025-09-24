from quizz_generator.snippet_python.requests_list import *

request_list = {
    "python_test": {
        "func": test_request,
        "desc": "Requête de test simple, theme/level au hasard, 5 snippets.",
    },
    "python_beginner": {
        "func": test_beginner_request,
        "desc": "Snippets Python niveau débutant, thème au hasard, 5 snippets.",
    },
    "python_intermediate": {
        "func": test_intermediate_request,
        "desc": "Snippets Python niveau intermédiaire, thème au hasard, 5 snippets.",
    },
    "python_expert": {
        "func": test_expert_request,
        "desc": "Snippets Python niveau expert, thème au hasard, 5 snippets.",
    },
    "python_test_theme": {
        "func": test_theme_request,
        "desc": "Requête de test, thème donné (niveau débutant), 5 snippets.",
    },
}
