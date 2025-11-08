"""
Persona synthesis service - coordinates LLM generation with persistence.

Combines the LLM chain (generation) with the repository (persistence)
to create a complete persona generation workflow.
"""

from typing import Dict, Any
from app.models.persona import PersonaCreate, PersonaInDB
from app.services.llm_chain import get_persona_llm_chain
from app.repositories.persona_repo import get_persona_repository
from app.core.logging import get_logger

logger = get_logger(__name__)


class PersonaSynthesizer:
    """Coordinates LLM persona generation and persistence."""

    def __init__(self):
        """Initialize synthesizer with dependencies."""
        self.llm_chain = get_persona_llm_chain()
        self.repository = get_persona_repository()

    async def generate_and_save_persona(self, raw_text: str) -> PersonaInDB:
        """
        Generate a persona from raw text and save to database.

        This is the main workflow:
        1. Use LLM chain to generate persona JSON from raw text
        2. Create PersonaCreate model
        3. Save to database via repository
        4. Return the complete PersonaInDB with ID and timestamps

        Args:
            raw_text: Unstructured text about a person

        Returns:
            PersonaInDB: Complete persona with database metadata

        Raises:
            ValueError: If generation or persistence fails
        """
        try:
            logger.info("Starting persona generation and save workflow")
            logger.debug(f"Input text length: {len(raw_text)} chars")
            logger.debug(f"Input raw_text type: {type(raw_text)}")
            logger.debug(f"Input raw_text preview: {raw_text[:200] if isinstance(raw_text, str) else repr(raw_text)}")

            # Step 1: Generate persona using LLM
            logger.debug("Generating persona with LLM chain...")
            persona_json = await self.llm_chain.generate_persona(raw_text)
            logger.info("Persona generated successfully")

            # Detailed logging about the generated persona
            logger.debug(f"Generated persona JSON type: {type(persona_json)}")
            logger.debug(f"Generated persona JSON keys: {list(persona_json.keys()) if isinstance(persona_json, dict) else 'NOT A DICT'}")
            logger.debug(f"Generated persona JSON size: {len(str(persona_json))} chars")
            logger.debug(f"Generated persona JSON preview: {str(persona_json)[:500]}")

            # Step 2: Save to database
            logger.debug("Persisting persona to database...")
            logger.debug(f"About to call repository.create() with:")
            logger.debug(f"  - raw_text type: {type(raw_text)}, length: {len(raw_text) if isinstance(raw_text, str) else 'N/A'}")
            logger.debug(f"  - persona_json type: {type(persona_json)}, keys: {list(persona_json.keys()) if isinstance(persona_json, dict) else 'NOT A DICT'}")

            persona_in_db = await self.repository.create(raw_text, persona_json)

            logger.debug(f"Repository.create() returned PersonaInDB object")
            logger.debug(f"  - ID: {persona_in_db.id}")
            logger.debug(f"  - created_at: {persona_in_db.created_at}")
            logger.debug(f"  - updated_at: {persona_in_db.updated_at}")
            logger.info(f"Persona saved with ID: {persona_in_db.id}")

            return persona_in_db

        except Exception as e:
            logger.error(f"Persona generation and save failed: {e}")
            logger.error(f"Exception type: {type(e).__name__}")
            logger.error(f"Exception traceback: ", exc_info=True)
            raise ValueError(
                f"Failed to generate and save persona: {e}"
            ) from e

    async def regenerate_persona(
        self, persona_id: str, new_raw_text: str
    ) -> PersonaInDB:
        """
        Regenerate a persona with new text and update in database.

        Useful for refining existing personas with new information.

        Args:
            persona_id: UUID of existing persona
            new_raw_text: New or updated text about the person

        Returns:
            PersonaInDB: Updated persona

        Raises:
            ValueError: If generation, update, or persistence fails
        """
        try:
            from uuid import UUID

            logger.info(f"Regenerating persona: {persona_id}")

            # Generate new persona
            new_persona_json = await self.llm_chain.generate_persona(
                new_raw_text
            )

            # Update in database
            from app.models.persona import PersonaUpdate

            persona_update = PersonaUpdate(
                raw_text=new_raw_text,
                persona=new_persona_json,
            )

            updated_persona = await self.repository.update(
                UUID(persona_id), persona_update
            )
            logger.info(f"Persona regenerated and updated: {persona_id}")

            return updated_persona

        except Exception as e:
            logger.error(f"Persona regeneration failed: {e}")
            raise ValueError(f"Failed to regenerate persona: {e}") from e

    async def get_persona(self, persona_id: str) -> PersonaInDB:
        """
        Retrieve a persona by ID.

        Args:
            persona_id: UUID of the persona

        Returns:
            PersonaInDB: The persona if found

        Raises:
            ValueError: If persona not found
        """
        try:
            from uuid import UUID

            logger.debug(f"Retrieving persona: {persona_id}")
            persona = await self.repository.read(UUID(persona_id))

            if persona is None:
                raise ValueError(f"Persona not found: {persona_id}")

            logger.debug(f"Persona retrieved: {persona_id}")
            return persona

        except Exception as e:
            logger.error(f"Persona retrieval failed: {e}")
            raise ValueError(f"Failed to retrieve persona: {e}") from e

    async def list_personas(
        self, limit: int = 10, offset: int = 0
    ) -> tuple[list[PersonaInDB], int]:
        """
        List all personas with pagination.

        Args:
            limit: Number of items per page
            offset: Number of items to skip

        Returns:
            Tuple of (list of personas, total count)

        Raises:
            ValueError: If listing fails
        """
        try:
            logger.debug(f"Listing personas: limit={limit}, offset={offset}")
            personas, total = await self.repository.read_all(limit, offset)
            logger.debug(f"Retrieved {len(personas)} personas (total: {total})")
            return personas, total

        except Exception as e:
            logger.error(f"Persona listing failed: {e}")
            raise ValueError(f"Failed to list personas: {e}") from e

    async def delete_persona(self, persona_id: str) -> bool:
        """
        Delete a persona.

        Args:
            persona_id: UUID of the persona to delete

        Returns:
            True if deleted, False if not found

        Raises:
            ValueError: If deletion fails
        """
        try:
            from uuid import UUID

            logger.info(f"Deleting persona: {persona_id}")
            deleted = await self.repository.delete(UUID(persona_id))

            if deleted:
                logger.info(f"Persona deleted: {persona_id}")
            else:
                logger.debug(f"Persona not found for deletion: {persona_id}")

            return deleted

        except Exception as e:
            logger.error(f"Persona deletion failed: {e}")
            raise ValueError(f"Failed to delete persona: {e}") from e


def get_persona_synthesizer() -> PersonaSynthesizer:
    """
    Get a PersonaSynthesizer instance.

    Returns:
        PersonaSynthesizer instance

    Usage:
        from app.services.persona_synthesizer import get_persona_synthesizer
        synthesizer = get_persona_synthesizer()
        persona = await synthesizer.generate_and_save_persona(raw_text)
    """
    return PersonaSynthesizer()
