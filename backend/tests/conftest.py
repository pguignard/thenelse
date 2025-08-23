import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

from quiz_api.main import app


@pytest.fixture
def client():
    """Client de test FastAPI."""
    return TestClient(app)


@pytest.fixture
def sample_snippet_data():
    """Données d'exemple pour les tests."""
    return {
        "snippet": "print(5 // 2)",
        "reponses": ["2", "2.5", "3", "TypeError"],
        "bonne_reponse_id": 0,
        "explication": "// est la division entière (floor) sur des int: 5 // 2 = 2.",
    }


@pytest.fixture
def mock_snippet_db():
    """Mock de la base de données de snippets."""
    return [
        {
            "snippet": "print(5 // 2)",
            "reponses": ["2", "2.5", "3", "TypeError"],
            "bonne_reponse_id": 0,
            "explication": "// est la division entière (floor) sur des int: 5 // 2 = 2.",
        },
        {
            "snippet": "print(3 ** 2)",
            "reponses": ["6", "9", "12", "SyntaxError"],
            "bonne_reponse_id": 1,
            "explication": "** est l'opérateur d'exponentiation: 3 ** 2 = 9.",
        },
        {
            "snippet": "print([1, 2, 3][1])",
            "reponses": ["1", "2", "3", "IndexError"],
            "bonne_reponse_id": 1,
            "explication": "L'indexation commence à 0: [1, 2, 3][1] = 2.",
        },
    ]


@pytest.fixture
def mock_empty_db():
    """Mock d'une base de données vide."""
    return []
