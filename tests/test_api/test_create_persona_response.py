"""Integration tests for POST /v1/persona endpoint with PersonaCreateResponse."""

import pytest
from unittest.mock import AsyncMock, patch
from uuid import uuid4
from datetime import datetime


@pytest.mark.asyncio
class TestCreatePersonaResponse:
    """Test POST /v1/persona endpoint response format."""

    async def test_create_persona_with_raw_text_returns_minimal_response(self, client):
        """Test that POST /v1/persona returns PersonaCreateResponse with only id, created_at, updated_at."""
        persona_id = str(uuid4())
        created_at = datetime.now()
        updated_at = datetime.now()

        with patch("app.api.routes.get_persona_service") as mock_service_factory:
            # Mock the service
            service = AsyncMock()
            from app.models.persona import PersonaInDB

            mock_persona = PersonaInDB(
                id=persona_id,
                raw_text="Sample text",
                persona={"name": "John", "age": 30},
                created_at=created_at,
                updated_at=updated_at,
            )
            service.generate_persona.return_value = mock_persona
            mock_service_factory.return_value = service

            # Make request
            response = client.post(
                "/v1/persona",
                json={"raw_text": "Sample persona text"},
            )

            # Verify response
            assert response.status_code == 201
            data = response.json()

            # Verify only 3 fields are present
            assert len(data) == 3
            assert set(data.keys()) == {"id", "created_at", "updated_at"}

            # Verify field values
            assert data["id"] == persona_id
            assert "created_at" in data
            assert "updated_at" in data

            # Verify raw_text and persona are NOT in response
            assert "raw_text" not in data
            assert "persona" not in data

    async def test_create_persona_response_datetime_format(self, client):
        """Test that datetime fields are in ISO 8601 format."""
        persona_id = str(uuid4())
        created_at = datetime.fromisoformat("2024-01-15T10:30:00")
        updated_at = datetime.fromisoformat("2024-01-15T10:30:00")

        with patch("app.api.routes.get_persona_service") as mock_service_factory:
            service = AsyncMock()
            from app.models.persona import PersonaInDB

            mock_persona = PersonaInDB(
                id=persona_id,
                raw_text="Sample text",
                created_at=created_at,
                updated_at=updated_at,
            )
            service.generate_persona.return_value = mock_persona
            mock_service_factory.return_value = service

            response = client.post(
                "/v1/persona",
                json={"raw_text": "Sample text"},
            )

            data = response.json()
            # Datetime should be in ISO format
            assert "2024-01-15" in data["created_at"]
            assert "10:30:00" in data["created_at"]

    async def test_create_persona_with_urls_parameter(self, client):
        """Test POST /v1/persona accepts urls parameter."""
        persona_id = str(uuid4())

        with patch("app.api.routes.get_persona_service") as mock_service_factory:
            service = AsyncMock()
            from app.models.persona import PersonaInDB

            mock_persona = PersonaInDB(
                id=persona_id,
                raw_text="Content from URLs",
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )
            service.generate_persona.return_value = mock_persona
            mock_service_factory.return_value = service

            # Note: URL fetching will be implemented in Story 3
            # For now, just verify the endpoint accepts the urls parameter
            response = client.post(
                "/v1/persona",
                json={"urls": ["https://example.com/bio"]},
            )

            # Should succeed with 201
            assert response.status_code == 201
            data = response.json()
            assert "id" in data
            assert "created_at" in data
            assert "updated_at" in data

    async def test_create_persona_with_raw_text_and_urls(self, client):
        """Test POST /v1/persona accepts both raw_text and urls."""
        persona_id = str(uuid4())

        with patch("app.api.routes.get_persona_service") as mock_service_factory:
            service = AsyncMock()
            from app.models.persona import PersonaInDB

            mock_persona = PersonaInDB(
                id=persona_id,
                raw_text="Combined content",
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )
            service.generate_persona.return_value = mock_persona
            mock_service_factory.return_value = service

            response = client.post(
                "/v1/persona",
                json={
                    "raw_text": "Direct text",
                    "urls": ["https://example.com/bio"],
                },
            )

            assert response.status_code == 201
            data = response.json()
            assert len(data) == 3

    async def test_create_persona_without_inputs_returns_validation_error(self, client):
        """Test POST /v1/persona returns 422 when neither raw_text nor urls provided."""
        response = client.post("/v1/persona", json={})
        assert response.status_code == 422

    async def test_create_persona_with_empty_urls_returns_validation_error(self, client):
        """Test POST /v1/persona returns 422 with empty urls list."""
        response = client.post("/v1/persona", json={"urls": []})
        assert response.status_code == 422

    async def test_create_persona_with_invalid_url_returns_validation_error(self, client):
        """Test POST /v1/persona returns 422 with invalid URL format."""
        response = client.post(
            "/v1/persona",
            json={"urls": ["not a valid url"]},
        )
        assert response.status_code == 422

    async def test_create_persona_returns_201_status(self, client):
        """Test POST /v1/persona returns 201 Created status code."""
        persona_id = str(uuid4())

        with patch("app.api.routes.get_persona_service") as mock_service_factory:
            service = AsyncMock()
            from app.models.persona import PersonaInDB

            mock_persona = PersonaInDB(
                id=persona_id,
                raw_text="Text",
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )
            service.generate_persona.return_value = mock_persona
            mock_service_factory.return_value = service

            response = client.post(
                "/v1/persona",
                json={"raw_text": "Sample text"},
            )

            assert response.status_code == 201
            assert response.headers["content-type"] == "application/json"

    async def test_create_persona_excludes_persona_json_from_response(self, client):
        """Test that PersonaCreateResponse excludes persona JSON from response."""
        persona_id = str(uuid4())

        with patch("app.api.routes.get_persona_service") as mock_service_factory:
            service = AsyncMock()
            from app.models.persona import PersonaInDB

            # Create a mock persona with complex persona JSON
            mock_persona = PersonaInDB(
                id=persona_id,
                raw_text="Complex persona text",
                persona={
                    "name": "John Doe",
                    "age": 30,
                    "skills": ["Python", "FastAPI", "PostgreSQL"],
                    "background": "Software Engineer",
                    "interests": ["AI", "Open Source"],
                },
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )
            service.generate_persona.return_value = mock_persona
            mock_service_factory.return_value = service

            response = client.post(
                "/v1/persona",
                json={"raw_text": "Complex text"},
            )

            data = response.json()
            # Verify complex persona JSON is NOT in response
            assert "persona" not in data
            assert "skills" not in data
            assert "background" not in data
            assert "interests" not in data

    async def test_create_persona_excludes_raw_text_from_response(self, client):
        """Test that PersonaCreateResponse excludes raw_text from response."""
        persona_id = str(uuid4())
        raw_text = "This is a very long raw text input that should not appear in the response..."

        with patch("app.api.routes.get_persona_service") as mock_service_factory:
            service = AsyncMock()
            from app.models.persona import PersonaInDB

            mock_persona = PersonaInDB(
                id=persona_id,
                raw_text=raw_text,
                persona={"name": "John"},
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )
            service.generate_persona.return_value = mock_persona
            mock_service_factory.return_value = service

            response = client.post(
                "/v1/persona",
                json={"raw_text": raw_text},
            )

            data = response.json()
            # Verify raw_text is NOT in response
            assert "raw_text" not in data
            assert raw_text not in str(data)
