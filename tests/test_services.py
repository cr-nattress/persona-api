"""
Unit tests for service layer (PersonaService, PersonaSynthesizer, PersonaLLMChain).

Tests core business logic and error handling.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4
from datetime import datetime

from app.services.persona_service import PersonaService
from app.models.persona import PersonaInDB


@pytest.mark.asyncio
@pytest.mark.unit
class TestPersonaService:
    """Tests for PersonaService."""

    async def test_generate_persona_success(
        self, persona_service: PersonaService, sample_raw_text: str,
        sample_persona_in_db: PersonaInDB
    ):
        """Test successful persona generation."""
        persona_service.synthesizer.generate_and_save_persona = AsyncMock(
            return_value=sample_persona_in_db
        )

        result = await persona_service.generate_persona(sample_raw_text)

        assert result.id == sample_persona_in_db.id
        assert result.raw_text == sample_raw_text
        persona_service.synthesizer.generate_and_save_persona.assert_called_once_with(sample_raw_text)

    async def test_generate_persona_empty_text(self, persona_service: PersonaService):
        """Test persona generation with empty text."""
        persona_service.synthesizer.generate_and_save_persona = AsyncMock(
            side_effect=ValueError("Text cannot be empty")
        )

        with pytest.raises(ValueError):
            await persona_service.generate_persona("")

    async def test_get_persona_success(
        self, persona_service: PersonaService, sample_persona_in_db: PersonaInDB
    ):
        """Test successful persona retrieval."""
        persona_id = str(sample_persona_in_db.id)
        persona_service.synthesizer.get_persona = AsyncMock(
            return_value=sample_persona_in_db
        )

        result = await persona_service.get_persona(persona_id)

        assert result.id == sample_persona_in_db.id
        persona_service.synthesizer.get_persona.assert_called_once_with(persona_id)

    async def test_get_persona_not_found(self, persona_service: PersonaService):
        """Test persona retrieval with non-existent ID."""
        persona_service.synthesizer.get_persona = AsyncMock(
            side_effect=ValueError("Persona not found")
        )

        with pytest.raises(ValueError):
            await persona_service.get_persona("invalid-id")

    async def test_list_personas_success(
        self, persona_service: PersonaService, sample_persona_in_db: PersonaInDB
    ):
        """Test successful persona listing."""
        personas = [sample_persona_in_db]
        persona_service.synthesizer.list_personas = AsyncMock(
            return_value=(personas, 1)
        )

        result_personas, total = await persona_service.list_personas(limit=10, offset=0)

        assert len(result_personas) == 1
        assert total == 1
        persona_service.synthesizer.list_personas.assert_called_once_with(10, 0)

    async def test_list_personas_empty(self, persona_service: PersonaService):
        """Test listing personas when none exist."""
        persona_service.synthesizer.list_personas = AsyncMock(
            return_value=([], 0)
        )

        result_personas, total = await persona_service.list_personas(limit=10, offset=0)

        assert len(result_personas) == 0
        assert total == 0

    async def test_list_personas_pagination(self, persona_service: PersonaService):
        """Test pagination in persona listing."""
        personas = [MagicMock() for _ in range(5)]
        persona_service.synthesizer.list_personas = AsyncMock(
            return_value=(personas, 50)
        )

        result_personas, total = await persona_service.list_personas(limit=5, offset=10)

        assert len(result_personas) == 5
        assert total == 50
        persona_service.synthesizer.list_personas.assert_called_once_with(5, 10)

    async def test_update_persona_success(
        self, persona_service: PersonaService, sample_persona_in_db: PersonaInDB,
        sample_raw_text: str
    ):
        """Test successful persona update."""
        persona_id = str(sample_persona_in_db.id)
        updated_persona = sample_persona_in_db
        persona_service.synthesizer.regenerate_persona = AsyncMock(
            return_value=updated_persona
        )

        result = await persona_service.update_persona(persona_id, sample_raw_text)

        assert result.id == sample_persona_in_db.id
        persona_service.synthesizer.regenerate_persona.assert_called_once_with(
            persona_id, sample_raw_text
        )

    async def test_update_persona_not_found(self, persona_service: PersonaService):
        """Test updating non-existent persona."""
        persona_service.synthesizer.regenerate_persona = AsyncMock(
            side_effect=ValueError("Persona not found")
        )

        with pytest.raises(ValueError):
            await persona_service.update_persona("invalid-id", "new text")

    async def test_delete_persona_success(self, persona_service: PersonaService):
        """Test successful persona deletion."""
        persona_id = str(uuid4())
        persona_service.synthesizer.delete_persona = AsyncMock(return_value=True)

        result = await persona_service.delete_persona(persona_id)

        assert result is True
        persona_service.synthesizer.delete_persona.assert_called_once_with(persona_id)

    async def test_delete_persona_not_found(self, persona_service: PersonaService):
        """Test deleting non-existent persona."""
        persona_service.synthesizer.delete_persona = AsyncMock(return_value=False)

        result = await persona_service.delete_persona("invalid-id")

        assert result is False

    async def test_merge_personas_success(
        self, persona_service: PersonaService, sample_persona_in_db: PersonaInDB
    ):
        """Test successful persona merge."""
        persona_id_1 = str(sample_persona_in_db.id)
        persona_id_2 = str(uuid4())

        # Mock get_persona to return two different personas
        persona_1 = sample_persona_in_db
        persona_2 = PersonaInDB(
            id=uuid4(),
            raw_text="Different text",
            persona=sample_persona_in_db.persona,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

        persona_service.get_persona = AsyncMock(side_effect=[persona_1, persona_2])
        persona_service.synthesizer.regenerate_persona = AsyncMock(
            return_value=persona_1
        )
        persona_service.synthesizer.delete_persona = AsyncMock(return_value=True)

        result = await persona_service.merge_personas(persona_id_1, persona_id_2)

        assert result.id == persona_1.id
        persona_service.synthesizer.regenerate_persona.assert_called_once()
        persona_service.synthesizer.delete_persona.assert_called_once_with(persona_id_2)

    async def test_merge_personas_with_custom_text(
        self, persona_service: PersonaService, sample_persona_in_db: PersonaInDB
    ):
        """Test merge with custom merged text."""
        persona_id_1 = str(sample_persona_in_db.id)
        persona_id_2 = str(uuid4())
        custom_text = "Custom merged text"

        persona_1 = sample_persona_in_db
        persona_2 = PersonaInDB(
            id=uuid4(),
            raw_text="Different text",
            persona=sample_persona_in_db.persona,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

        persona_service.get_persona = AsyncMock(side_effect=[persona_1, persona_2])
        persona_service.synthesizer.regenerate_persona = AsyncMock(
            return_value=persona_1
        )
        persona_service.synthesizer.delete_persona = AsyncMock(return_value=True)

        await persona_service.merge_personas(persona_id_1, persona_id_2, custom_text)

        # Verify the custom text was used
        args = persona_service.synthesizer.regenerate_persona.call_args
        assert args[0][1] == custom_text

    async def test_merge_personas_first_not_found(self, persona_service: PersonaService):
        """Test merge when first persona not found."""
        persona_service.get_persona = AsyncMock(
            side_effect=ValueError("Persona not found")
        )

        with pytest.raises(ValueError):
            await persona_service.merge_personas(str(uuid4()), str(uuid4()))

    async def test_batch_generate_personas_success(
        self, persona_service: PersonaService, sample_persona_in_db: PersonaInDB
    ):
        """Test successful batch generation."""
        texts = ["Text 1", "Text 2", "Text 3"]
        persona_service.synthesizer.generate_and_save_persona = AsyncMock(
            return_value=sample_persona_in_db
        )

        result = await persona_service.batch_generate_personas(texts)

        assert len(result) == 3
        assert persona_service.synthesizer.generate_and_save_persona.call_count == 3

    async def test_batch_generate_personas_empty_list(self, persona_service: PersonaService):
        """Test batch generation with empty list."""
        persona_service.synthesizer.generate_and_save_personas = AsyncMock()

        with pytest.raises(ValueError, match="raw_texts list cannot be empty"):
            await persona_service.batch_generate_personas([])

    async def test_search_personas_success(
        self, persona_service: PersonaService, sample_persona_in_db: PersonaInDB
    ):
        """Test successful persona search."""
        query = "engineer"
        persona_service.synthesizer.list_personas = AsyncMock(
            return_value=([sample_persona_in_db], 1)
        )

        result = await persona_service.search_personas(query, limit=10)

        assert isinstance(result, list)
        persona_service.synthesizer.list_personas.assert_called_once()

    async def test_search_personas_no_results(self, persona_service: PersonaService):
        """Test search with no results."""
        persona_service.synthesizer.list_personas = AsyncMock(
            return_value=([], 0)
        )

        result = await persona_service.search_personas("nonexistent", limit=10)

        assert len(result) == 0

    async def test_get_persona_stats_success(self, persona_service: PersonaService):
        """Test successful stats retrieval."""
        persona_service.synthesizer.list_personas = AsyncMock(
            return_value=([], 0)
        )

        result = await persona_service.get_persona_stats()

        assert "total_personas" in result
        assert result["total_personas"] == 0
        assert result["oldest_created"] is None

    async def test_get_persona_stats_with_data(
        self, persona_service: PersonaService, sample_persona_in_db: PersonaInDB
    ):
        """Test stats with existing personas."""
        persona_service.synthesizer.list_personas = AsyncMock(
            side_effect=[
                ([sample_persona_in_db], 1),  # First call for total
                ([sample_persona_in_db], 1),  # Second call for all personas
            ]
        )

        result = await persona_service.get_persona_stats()

        assert result["total_personas"] == 1
        assert result["oldest_created"] is not None
        assert result["newest_created"] is not None

    async def test_export_personas_success(self, persona_service: PersonaService):
        """Test successful export."""
        persona_service.synthesizer.list_personas = AsyncMock(
            return_value=([], 0)
        )

        result = await persona_service.export_personas(format="json", limit=100)

        assert result["export_format"] == "json"
        assert "exported_at" in result
        assert result["total_exported"] == 0

    async def test_export_personas_invalid_format(self, persona_service: PersonaService):
        """Test export with invalid format."""
        with pytest.raises(ValueError, match="Unsupported export format"):
            await persona_service.export_personas(format="csv", limit=100)

    async def test_export_personas_respects_limit(self, persona_service: PersonaService):
        """Test that export respects limit parameter."""
        persona_service.synthesizer.list_personas = AsyncMock(
            return_value=([], 0)
        )

        await persona_service.export_personas(format="json", limit=50)

        # Verify limit was passed to list_personas
        args = persona_service.synthesizer.list_personas.call_args
        assert args[0][0] == 50
