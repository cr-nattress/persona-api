"""Tests for persona data models."""

import pytest
from datetime import datetime
from uuid import UUID
from pydantic import ValidationError
from app.models.persona import (
    PersonaCreateResponse,
    PersonaCreate,
    PersonaUpdate,
    PersonaInDB,
)


class TestPersonaCreateResponse:
    """Test PersonaCreateResponse model."""

    def test_persona_create_response_valid(self):
        """Test PersonaCreateResponse with valid data."""
        response = PersonaCreateResponse(
            id="550e8400-e29b-41d4-a716-446655440000",
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        assert response.id == "550e8400-e29b-41d4-a716-446655440000"
        assert isinstance(response.created_at, datetime)
        assert isinstance(response.updated_at, datetime)

    def test_persona_create_response_serialization(self):
        """Test JSON serialization with proper datetime formatting."""
        now = datetime.fromisoformat("2024-01-15T10:30:00")
        response = PersonaCreateResponse(
            id="test-id",
            created_at=now,
            updated_at=now,
        )
        json_data = response.model_dump_json()
        assert "2024-01-15T10:30:00" in json_data

    def test_persona_create_response_model_dump(self):
        """Test model_dump returns correct fields."""
        response = PersonaCreateResponse(
            id="test-id",
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        data = response.model_dump()
        assert len(data) == 3
        assert "id" in data
        assert "created_at" in data
        assert "updated_at" in data
        assert "raw_text" not in data
        assert "persona" not in data

    def test_persona_create_response_missing_id(self):
        """Test validation error when id is missing."""
        with pytest.raises(ValidationError):
            PersonaCreateResponse(
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )

    def test_persona_create_response_invalid_created_at(self):
        """Test validation error when created_at has wrong type."""
        with pytest.raises(ValidationError):
            PersonaCreateResponse(
                id="test-id",
                created_at="not-a-datetime",
                updated_at=datetime.now(),
            )

    def test_persona_create_response_invalid_updated_at(self):
        """Test validation error when updated_at has wrong type."""
        with pytest.raises(ValidationError):
            PersonaCreateResponse(
                id="test-id",
                created_at=datetime.now(),
                updated_at="not-a-datetime",
            )

    def test_persona_create_response_none_values(self):
        """Test validation error when required fields are None."""
        with pytest.raises(ValidationError):
            PersonaCreateResponse(
                id=None,
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )

    def test_persona_create_response_from_attributes(self):
        """Test from_attributes config allows ORM model conversion."""
        # Simulate an ORM object with attributes
        class FakeORM:
            id = "fake-id"
            created_at = datetime.now()
            updated_at = datetime.now()

        fake_orm = FakeORM()
        response = PersonaCreateResponse.model_validate(fake_orm)
        assert response.id == "fake-id"


class TestPersonaCreate:
    """Test PersonaCreate request model."""

    def test_persona_create_with_raw_text_only(self):
        """Test creating persona with raw_text only."""
        request = PersonaCreate(
            raw_text="Sample persona text",
        )
        assert request.raw_text == "Sample persona text"
        assert request.urls is None

    def test_persona_create_with_urls_only(self):
        """Test creating persona with URLs only."""
        request = PersonaCreate(
            urls=["https://example.com/bio"]
        )
        assert request.raw_text is None
        assert len(request.urls) == 1

    def test_persona_create_with_multiple_urls(self):
        """Test creating persona with multiple URLs."""
        urls = [
            "https://example.com/bio",
            "https://example.com/resume",
            "https://example.com/profile",
        ]
        request = PersonaCreate(urls=urls)
        assert len(request.urls) == 3
        assert str(request.urls[0]) == "https://example.com/bio"

    def test_persona_create_with_raw_text_and_urls(self):
        """Test creating persona with both raw_text and URLs."""
        request = PersonaCreate(
            raw_text="Direct persona text",
            urls=["https://example.com/bio"]
        )
        assert request.raw_text == "Direct persona text"
        assert len(request.urls) == 1

    def test_persona_create_without_raw_text_or_urls(self):
        """Test validation error when neither raw_text nor URLs provided."""
        with pytest.raises(ValidationError) as exc_info:
            PersonaCreate()
        error = exc_info.value
        assert "Either raw_text or urls must be provided" in str(error)

    def test_persona_create_with_empty_urls_list(self):
        """Test validation error when empty URLs list provided."""
        with pytest.raises(ValidationError):
            PersonaCreate(urls=[])

    def test_persona_create_with_invalid_url_format(self):
        """Test validation error with invalid URL format."""
        with pytest.raises(ValidationError):
            PersonaCreate(urls=["not a valid url"])

    def test_persona_create_with_too_many_urls(self):
        """Test validation error when more than 10 URLs provided."""
        urls = [f"https://example.com/page{i}" for i in range(11)]
        with pytest.raises(ValidationError):
            PersonaCreate(urls=urls)

    def test_persona_create_with_max_raw_text_length(self):
        """Test max length validation for raw_text."""
        # Create text with 50,000 characters (at limit)
        long_text = "a" * 50000
        request = PersonaCreate(raw_text=long_text)
        assert len(request.raw_text) == 50000

    def test_persona_create_with_oversized_raw_text(self):
        """Test validation error when raw_text exceeds max length."""
        oversized_text = "a" * 50001
        with pytest.raises(ValidationError):
            PersonaCreate(raw_text=oversized_text)

    def test_persona_create_with_empty_raw_text(self):
        """Test validation error when raw_text is empty string."""
        with pytest.raises(ValidationError):
            PersonaCreate(raw_text="")

    def test_persona_create_with_max_urls(self):
        """Test creating persona with maximum 10 URLs."""
        urls = [f"https://example.com/page{i}" for i in range(10)]
        request = PersonaCreate(urls=urls)
        assert len(request.urls) == 10

    def test_persona_create_serialization(self):
        """Test JSON serialization."""
        request = PersonaCreate(raw_text="Sample text")
        json_data = request.model_dump_json()
        assert "Sample text" in json_data


class TestPersonaUpdate:
    """Test PersonaUpdate model."""

    def test_persona_update_with_raw_text(self):
        """Test updating with raw_text."""
        update = PersonaUpdate(raw_text="Updated text")
        assert update.raw_text == "Updated text"
        assert update.persona is None

    def test_persona_update_with_persona(self):
        """Test updating with persona JSON."""
        persona_data = {"name": "John", "age": 30}
        update = PersonaUpdate(persona=persona_data)
        assert update.persona == persona_data
        assert update.raw_text is None

    def test_persona_update_partial(self):
        """Test that both fields are optional."""
        update = PersonaUpdate()
        assert update.raw_text is None
        assert update.persona is None


class TestPersonaInDB:
    """Test PersonaInDB model (database model)."""

    def test_persona_in_db_complete(self):
        """Test PersonaInDB with all fields."""
        now = datetime.now()
        persona = PersonaInDB(
            id=UUID("550e8400-e29b-41d4-a716-446655440000"),
            raw_text="Sample text",
            persona={"name": "John"},
            created_at=now,
            updated_at=now,
        )
        assert persona.raw_text == "Sample text"
        assert persona.persona == {"name": "John"}
        assert persona.created_at == now

    def test_persona_in_db_without_persona(self):
        """Test PersonaInDB without persona JSON."""
        now = datetime.now()
        persona = PersonaInDB(
            id=UUID("550e8400-e29b-41d4-a716-446655440000"),
            raw_text="Sample text",
            created_at=now,
            updated_at=now,
        )
        assert persona.persona is None

    def test_persona_in_db_uuid_conversion(self):
        """Test PersonaInDB handles UUID fields."""
        now = datetime.now()
        persona = PersonaInDB(
            id=UUID("550e8400-e29b-41d4-a716-446655440000"),
            raw_text="Sample text",
            created_at=now,
            updated_at=now,
        )
        assert isinstance(persona.id, UUID)
        assert str(persona.id) == "550e8400-e29b-41d4-a716-446655440000"
