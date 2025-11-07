"""
Integration tests for API endpoints.

Tests full request/response flow including error handling.
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
from uuid import uuid4

from app.main import app


@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)


@pytest.mark.integration
class TestAPIEndpoints:
    """Integration tests for API endpoints."""

    def test_health_check(self, client):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "persona-api"

    def test_root_endpoint(self, client):
        """Test root endpoint."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert data["version"] == "1.0.0"

    def test_list_personas_empty(self, client):
        """Test listing personas when none exist."""
        with patch("app.api.routes.get_persona_service") as mock_service:
            service = AsyncMock()
            service.list_personas.return_value = ([], 0)
            mock_service.return_value = service

            response = client.get("/v1/persona?limit=10")
            assert response.status_code == 200
            data = response.json()
            assert data["items"] == []
            assert data["total"] == 0
            assert data["limit"] == 10
            assert data["offset"] == 0

    def test_list_personas_pagination(self, client):
        """Test pagination parameters."""
        with patch("app.api.routes.get_persona_service") as mock_service:
            service = AsyncMock()
            service.list_personas.return_value = ([], 100)
            mock_service.return_value = service

            response = client.get("/v1/persona?limit=20&offset=10")
            assert response.status_code == 200
            data = response.json()
            assert data["limit"] == 20
            assert data["offset"] == 10
            service.list_personas.assert_called_once_with(20, 10)

    def test_list_personas_invalid_limit(self, client):
        """Test invalid limit parameter."""
        response = client.get("/v1/persona?limit=200")
        assert response.status_code == 422  # Validation error

    def test_search_personas_success(self, client):
        """Test successful search."""
        with patch("app.api.routes.get_persona_service") as mock_service:
            service = AsyncMock()
            service.search_personas.return_value = []
            mock_service.return_value = service

            response = client.get("/v1/persona/search?q=engineer&limit=10")
            assert response.status_code == 200
            data = response.json()
            assert isinstance(data, list)
            service.search_personas.assert_called_once_with("engineer", 10)

    def test_search_personas_missing_query(self, client):
        """Test search without query parameter."""
        response = client.get("/v1/persona/search")
        assert response.status_code == 422  # Missing required parameter

    def test_search_personas_empty_query(self, client):
        """Test search with empty query."""
        response = client.get("/v1/persona/search?q=")
        assert response.status_code == 422  # Validation error (min_length=1)

    def test_stats_endpoint_success(self, client):
        """Test statistics endpoint."""
        with patch("app.api.routes.get_persona_service") as mock_service:
            service = AsyncMock()
            service.get_persona_stats.return_value = {
                "total_personas": 0,
                "oldest_created": None,
                "newest_created": None,
                "days_active": 0,
            }
            mock_service.return_value = service

            response = client.get("/v1/persona/stats")
            assert response.status_code == 200
            data = response.json()
            assert "total_personas" in data
            assert data["total_personas"] == 0

    def test_export_endpoint_success(self, client):
        """Test export endpoint."""
        with patch("app.api.routes.get_persona_service") as mock_service:
            service = AsyncMock()
            service.export_personas.return_value = {
                "export_format": "json",
                "exported_at": "2025-11-07T00:00:00",
                "total_exported": 0,
                "total_in_system": 0,
                "personas": [],
            }
            mock_service.return_value = service

            response = client.get("/v1/persona/export?format=json")
            assert response.status_code == 200
            data = response.json()
            assert data["export_format"] == "json"
            assert "personas" in data

    def test_export_invalid_format(self, client):
        """Test export with invalid format."""
        with patch("app.api.routes.get_persona_service") as mock_service:
            service = AsyncMock()
            service.export_personas.side_effect = ValueError("Unsupported export format")
            mock_service.return_value = service

            response = client.get("/v1/persona/export?format=csv")
            assert response.status_code == 400

    def test_openapi_schema(self, client):
        """Test OpenAPI schema generation."""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        data = response.json()
        assert "openapi" in data
        assert "paths" in data
        assert "/v1/persona" in data["paths"]

    def test_swagger_ui_endpoint(self, client):
        """Test Swagger UI endpoint exists."""
        response = client.get("/docs")
        # docs redirect may return 200 or different content
        assert response.status_code in [200, 307]

    def test_redoc_endpoint(self, client):
        """Test ReDoc endpoint exists."""
        response = client.get("/redoc")
        assert response.status_code in [200, 307]


@pytest.mark.integration
class TestAPIErrorHandling:
    """Tests for API error handling."""

    def test_invalid_route(self, client):
        """Test accessing non-existent route."""
        response = client.get("/v1/nonexistent")
        assert response.status_code == 404

    def test_merge_missing_parameters(self, client):
        """Test merge endpoint without required parameters."""
        response = client.post("/v1/persona/merge")
        assert response.status_code == 422  # Missing parameters

    def test_merge_personas_not_found(self, client):
        """Test merge with non-existent persona."""
        with patch("app.api.routes.get_persona_service") as mock_service:
            service = AsyncMock()
            service.merge_personas.side_effect = ValueError("Persona not found")
            mock_service.return_value = service

            persona_id_1 = str(uuid4())
            persona_id_2 = str(uuid4())
            response = client.post(
                f"/v1/persona/merge?persona_id_1={persona_id_1}&persona_id_2={persona_id_2}"
            )
            assert response.status_code == 404

    def test_batch_empty_list(self, client):
        """Test batch endpoint with empty list."""
        with patch("app.api.routes.get_persona_service") as mock_service:
            service = AsyncMock()
            service.batch_generate_personas.side_effect = ValueError(
                "raw_texts list cannot be empty"
            )
            mock_service.return_value = service

            response = client.post("/v1/persona/batch", json=[])
            assert response.status_code == 400

    def test_batch_invalid_json(self, client):
        """Test batch endpoint with invalid JSON."""
        response = client.post(
            "/v1/persona/batch",
            json="invalid",  # Should be list
        )
        assert response.status_code == 422  # Validation error

    def test_create_persona_missing_fields(self, client):
        """Test create persona with missing required fields."""
        response = client.post("/v1/persona", json={})
        assert response.status_code == 422

    def test_create_persona_invalid_json(self, client):
        """Test create persona with invalid JSON."""
        response = client.post(
            "/v1/persona",
            json={"raw_text": "some text"},  # Missing required 'persona' field
        )
        assert response.status_code == 422

    def test_get_nonexistent_persona(self, client):
        """Test getting non-existent persona."""
        with patch("app.api.routes.get_persona_service") as mock_service:
            service = AsyncMock()
            service.get_persona.side_effect = ValueError("Persona not found")
            mock_service.return_value = service

            response = client.get(f"/v1/persona/{uuid4()}")
            assert response.status_code == 404

    def test_delete_nonexistent_persona(self, client):
        """Test deleting non-existent persona."""
        with patch("app.api.routes.get_persona_service") as mock_service:
            service = AsyncMock()
            service.delete_persona.return_value = False
            mock_service.return_value = service

            response = client.delete(f"/v1/persona/{uuid4()}")
            assert response.status_code == 404


@pytest.mark.integration
class TestAPIRouteOrdering:
    """Tests to verify correct route matching order."""

    def test_stats_route_not_matched_as_persona_id(self, client):
        """Verify /stats route matches before /{persona_id} route."""
        with patch("app.api.routes.get_persona_service") as mock_service:
            service = AsyncMock()
            service.get_persona_stats.return_value = {
                "total_personas": 0,
                "oldest_created": None,
                "newest_created": None,
                "days_active": 0,
            }
            mock_service.return_value = service

            # This should match /stats, not /{persona_id}
            response = client.get("/v1/persona/stats")
            assert response.status_code == 200
            # Verify it called stats, not get_persona
            service.get_persona_stats.assert_called_once()
            service.get_persona.assert_not_called()

    def test_search_route_not_matched_as_persona_id(self, client):
        """Verify /search route matches before /{persona_id} route."""
        with patch("app.api.routes.get_persona_service") as mock_service:
            service = AsyncMock()
            service.search_personas.return_value = []
            mock_service.return_value = service

            response = client.get("/v1/persona/search?q=test")
            assert response.status_code == 200
            service.search_personas.assert_called_once()
            service.get_persona.assert_not_called()

    def test_export_route_not_matched_as_persona_id(self, client):
        """Verify /export route matches before /{persona_id} route."""
        with patch("app.api.routes.get_persona_service") as mock_service:
            service = AsyncMock()
            service.export_personas.return_value = {
                "export_format": "json",
                "exported_at": "2025-11-07T00:00:00",
                "total_exported": 0,
                "total_in_system": 0,
                "personas": [],
            }
            mock_service.return_value = service

            response = client.get("/v1/persona/export")
            assert response.status_code == 200
            service.export_personas.assert_called_once()
            service.get_persona.assert_not_called()
