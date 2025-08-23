import pytest
from unittest.mock import patch, MagicMock
from fastapi import HTTPException
from pydantic import ValidationError

from quiz_api.models.quiz import Snippet
from quiz_api.services.quiz_service import QuizService


class TestSnippetModel:
    """Tests du modèle Snippet."""

    def test_snippet_creation_valid(self, sample_snippet_data):
        """Test de création d'un snippet valide."""
        snippet = Snippet(**sample_snippet_data)
        assert snippet.snippet == "print(5 // 2)"
        assert snippet.reponses == ["2", "2.5", "3", "TypeError"]
        assert snippet.bonne_reponse_id == 0
        assert snippet.explication.startswith("// est la division")

    def test_snippet_validation_bonne_reponse_id_valid(self):
        """Test de validation avec bonne_reponse_id valide."""
        data = {
            "snippet": "test",
            "reponses": ["a", "b", "c"],
            "bonne_reponse_id": 2,  # Index valide (0, 1, 2)
            "explication": "Test",
        }
        snippet = Snippet(**data)
        assert snippet.bonne_reponse_id == 2

    def test_snippet_validation_bonne_reponse_id_invalid(self):
        """Test de validation avec bonne_reponse_id invalide."""
        data = {
            "snippet": "test",
            "reponses": ["a", "b", "c"],
            "bonne_reponse_id": 5,  # Index invalide (hors limite)
            "explication": "Test",
        }
        with pytest.raises(ValidationError) as exc_info:
            Snippet(**data)
        assert "bonne_reponse_id" in str(exc_info.value)

    def test_snippet_validation_bonne_reponse_id_negative(self):
        """Test de validation avec bonne_reponse_id négatif."""
        data = {
            "snippet": "test",
            "reponses": ["a", "b", "c"],
            "bonne_reponse_id": -1,  # Index négatif
            "explication": "Test",
        }
        with pytest.raises(ValidationError):
            Snippet(**data)

    def test_snippet_validation_missing_fields(self):
        """Test de validation avec champs manquants."""
        data = {
            "snippet": "test",
            # reponses manquant
            "bonne_reponse_id": 0,
            "explication": "Test",
        }
        with pytest.raises(ValidationError):
            Snippet(**data)

    @pytest.mark.parametrize(
        "field", ["snippet", "reponses", "bonne_reponse_id", "explication"]
    )
    def test_snippet_required_fields(self, sample_snippet_data, field):
        """Test que tous les champs sont obligatoires."""
        data = sample_snippet_data.copy()
        del data[field]
        with pytest.raises(ValidationError):
            Snippet(**data)


class TestQuizService:
    """Tests du service QuizService."""

    @patch('quiz_api.services.quiz_service.snippet_db_json')
    def test_get_random_snippet_success(self, mock_db, mock_snippet_db):
        """Test de récupération d'un snippet aléatoire avec succès."""
        mock_db.__bool__ = MagicMock(return_value=True)
        mock_db.__iter__ = MagicMock(return_value=iter(mock_snippet_db))

        with patch('quiz_api.services.quiz_service.random.choice') as mock_choice:
            mock_choice.return_value = mock_snippet_db[0]

            result = QuizService.get_random_snippet()

            assert isinstance(result, Snippet)
            assert result.snippet == "print(5 // 2)"
            mock_choice.assert_called_once()

    @patch('quiz_api.services.quiz_service.snippet_db_json')
    def test_get_random_snippet_empty_db(self, mock_db, mock_empty_db):
        """Test de récupération avec base de données vide."""
        mock_db.__bool__ = MagicMock(return_value=False)

        with pytest.raises(HTTPException) as exc_info:
            QuizService.get_random_snippet()

        assert exc_info.value.status_code == 404
        assert "Aucun snippet disponible" in exc_info.value.detail

    @patch('quiz_api.services.quiz_service.snippet_db_json')
    def test_get_snippet_by_id_success(self, mock_db, mock_snippet_db):
        """Test de récupération d'un snippet par ID avec succès."""
        mock_db.__len__ = MagicMock(return_value=len(mock_snippet_db))
        mock_db.__getitem__ = MagicMock(side_effect=lambda x: mock_snippet_db[x])

        result = QuizService.get_snippet_by_id(1)

        assert isinstance(result, Snippet)
        assert result.snippet == "print(3 ** 2)"
        assert result.bonne_reponse_id == 1

    @patch('quiz_api.services.quiz_service.snippet_db_json')
    def test_get_snippet_by_id_invalid_negative(self, mock_db, mock_snippet_db):
        """Test avec ID négatif."""
        mock_db.__len__ = MagicMock(return_value=len(mock_snippet_db))

        with pytest.raises(HTTPException) as exc_info:
            QuizService.get_snippet_by_id(-1)

        assert exc_info.value.status_code == 404
        assert "Snippet non trouvé" in exc_info.value.detail

    @patch('quiz_api.services.quiz_service.snippet_db_json')
    def test_get_snippet_by_id_invalid_too_high(self, mock_db, mock_snippet_db):
        """Test avec ID trop élevé."""
        mock_db.__len__ = MagicMock(return_value=len(mock_snippet_db))

        with pytest.raises(HTTPException) as exc_info:
            QuizService.get_snippet_by_id(999)

        assert exc_info.value.status_code == 404
        assert "Snippet non trouvé" in exc_info.value.detail

    @patch('quiz_api.services.quiz_service.snippet_db_json')
    def test_get_snippets_count(self, mock_db, mock_snippet_db):
        """Test de comptage des snippets."""
        mock_db.__len__ = MagicMock(return_value=len(mock_snippet_db))

        result = QuizService.get_snippets_count()

        assert result == {"total_snippets": 3}
        mock_db.__len__.assert_called_once()


class TestAPIEndpoints:
    """Tests des endpoints de l'API."""

    def test_health_endpoint(self, client):
        """Test de l'endpoint de santé."""
        response = client.get("/")

        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "ThenElse Quiz API"
        assert data["status"] == "running"

    @patch('quiz_api.services.quiz_service.snippet_db_json')
    def test_get_random_snippet_endpoint(self, mock_db, client, mock_snippet_db):
        """Test de l'endpoint GET /quiz/random."""
        mock_db.__bool__ = MagicMock(return_value=True)

        with patch('quiz_api.services.quiz_service.random.choice') as mock_choice:
            mock_choice.return_value = mock_snippet_db[0]

            response = client.get("/quiz/random")

            assert response.status_code == 200
            data = response.json()
            assert data["snippet"] == "print(5 // 2)"
            assert data["reponses"] == ["2", "2.5", "3", "TypeError"]
            assert data["bonne_reponse_id"] == 0

    @patch('quiz_api.services.quiz_service.snippet_db_json')
    def test_get_random_snippet_endpoint_empty_db(self, mock_db, client):
        """Test de l'endpoint GET /quiz/random avec DB vide."""
        mock_db.__bool__ = MagicMock(return_value=False)

        response = client.get("/quiz/random")

        assert response.status_code == 404
        assert "Aucun snippet disponible" in response.json()["detail"]

    @patch('quiz_api.services.quiz_service.snippet_db_json')
    def test_get_snippet_by_id_endpoint(self, mock_db, client, mock_snippet_db):
        """Test de l'endpoint GET /quiz/{id}."""
        mock_db.__len__ = MagicMock(return_value=len(mock_snippet_db))
        mock_db.__getitem__ = MagicMock(side_effect=lambda x: mock_snippet_db[x])

        response = client.get("/quiz/1")

        assert response.status_code == 200
        data = response.json()
        assert data["snippet"] == "print(3 ** 2)"
        assert data["bonne_reponse_id"] == 1

    @patch('quiz_api.services.quiz_service.snippet_db_json')
    def test_get_snippet_by_id_endpoint_not_found(
        self, mock_db, client, mock_snippet_db
    ):
        """Test de l'endpoint GET /quiz/{id} avec ID invalide."""
        mock_db.__len__ = MagicMock(return_value=len(mock_snippet_db))

        response = client.get("/quiz/999")

        assert response.status_code == 404
        assert "Snippet non trouvé" in response.json()["detail"]

    def test_get_snippet_by_id_endpoint_invalid_type(self, client):
        """Test de l'endpoint GET /quiz/{id} avec type invalide."""
        response = client.get("/quiz/abc")

        assert response.status_code == 422  # Validation error

    @patch('quiz_api.services.quiz_service.snippet_db_json')
    def test_get_snippets_count_endpoint(self, mock_db, client, mock_snippet_db):
        """Test de l'endpoint GET /stats/snippets/count."""
        mock_db.__len__ = MagicMock(return_value=len(mock_snippet_db))

        response = client.get("/stats/snippets/count")

        assert response.status_code == 200
        data = response.json()
        assert data["total_snippets"] == 3


class TestIntegration:
    """Tests d'intégration."""

    def test_api_documentation_available(self, client):
        """Test que la documentation OpenAPI est disponible."""
        response = client.get("/docs")
        assert response.status_code == 200

    def test_openapi_schema_available(self, client):
        """Test que le schéma OpenAPI est disponible."""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        schema = response.json()
        assert "ThenElse - Quiz API" in schema["info"]["title"]

    @patch('quiz_api.services.quiz_service.snippet_db_json')
    def test_complete_workflow(self, mock_db, client, mock_snippet_db):
        """Test d'un workflow complet."""
        mock_db.__len__ = MagicMock(return_value=len(mock_snippet_db))
        mock_db.__bool__ = MagicMock(return_value=True)
        mock_db.__getitem__ = MagicMock(side_effect=lambda x: mock_snippet_db[x])

        # 1. Vérifier la santé de l'API
        health_response = client.get("/")
        assert health_response.status_code == 200

        # 2. Obtenir le nombre de snippets
        count_response = client.get("/stats/snippets/count")
        assert count_response.status_code == 200
        assert count_response.json()["total_snippets"] == 3

        # 3. Récupérer un snippet spécifique
        snippet_response = client.get("/quiz/0")
        assert snippet_response.status_code == 200
        snippet_data = snippet_response.json()
        assert "snippet" in snippet_data
        assert "reponses" in snippet_data
        assert "bonne_reponse_id" in snippet_data
        assert "explication" in snippet_data
