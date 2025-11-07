"""
Repository pattern implementation for persona data access.

Provides CRUD operations (Create, Read, Update, Delete) for personas
with proper error handling and logging.
"""

from typing import List, Optional, Dict, Any
from uuid import UUID
from app.models.persona import (
    PersonaCreate,
    PersonaUpdate,
    PersonaInDB,
)
from app.db.supabase_client import get_supabase_client
from app.core.logging import get_logger
from postgrest.exceptions import APIError

logger = get_logger(__name__)


class PersonaRepository:
    """Repository for persona data access."""

    def __init__(self):
        """Initialize repository with Supabase client."""
        self.supabase = get_supabase_client()
        self.table_name = "personas"

    async def create(self, raw_text: str, persona_json: Dict[str, Any]) -> PersonaInDB:
        """
        Create a new persona.

        Args:
            raw_text: Original unstructured text about the person
            persona_json: Generated persona JSON data

        Returns:
            PersonaInDB: Created persona with ID and timestamps

        Raises:
            APIError: If database operation fails
        """
        try:
            logger.debug(f"Creating persona from text: {raw_text[:50]}...")

            data = {
                "raw_text": raw_text,
                "persona": persona_json,
            }

            response = (
                self.supabase.client.table(self.table_name)
                .insert(data)
                .execute()
            )

            if not response.data:
                raise ValueError("No data returned from insert operation")

            result = response.data[0]
            logger.info(f"Persona created successfully: {result['id']}")

            return PersonaInDB(**result)
        except APIError as e:
            logger.error(f"API error creating persona: {e}")
            raise
        except Exception as e:
            logger.error(f"Error creating persona: {e}")
            raise

    async def read(self, persona_id: UUID) -> Optional[PersonaInDB]:
        """
        Read a persona by ID.

        Args:
            persona_id: UUID of the persona

        Returns:
            PersonaInDB if found, None otherwise

        Raises:
            APIError: If database operation fails
        """
        try:
            logger.debug(f"Reading persona: {persona_id}")

            response = (
                self.supabase.client.table(self.table_name)
                .select("*")
                .eq("id", str(persona_id))
                .execute()
            )

            if not response.data:
                logger.debug(f"Persona not found: {persona_id}")
                return None

            result = response.data[0]
            logger.debug(f"Persona retrieved: {persona_id}")

            return PersonaInDB(**result)
        except APIError as e:
            logger.error(f"API error reading persona: {e}")
            raise
        except Exception as e:
            logger.error(f"Error reading persona: {e}")
            raise

    async def read_all(
        self, limit: int = 10, offset: int = 0
    ) -> tuple[List[PersonaInDB], int]:
        """
        Read all personas with pagination.

        Args:
            limit: Number of items per page
            offset: Number of items to skip

        Returns:
            Tuple of (list of personas, total count)

        Raises:
            APIError: If database operation fails
        """
        try:
            logger.debug(f"Reading personas: limit={limit}, offset={offset}")

            # Get total count
            count_response = (
                self.supabase.client.table(self.table_name)
                .select("id", count="exact")
                .execute()
            )
            total = count_response.count or 0

            # Get paginated results
            response = (
                self.supabase.client.table(self.table_name)
                .select("*")
                .order("created_at", desc=True)
                .range(offset, offset + limit - 1)
                .execute()
            )

            personas = [PersonaInDB(**item) for item in response.data]
            logger.debug(f"Retrieved {len(personas)} personas (total: {total})")

            return personas, total
        except APIError as e:
            logger.error(f"API error reading personas: {e}")
            raise
        except Exception as e:
            logger.error(f"Error reading personas: {e}")
            raise

    async def update(
        self, persona_id: UUID, update_data: PersonaUpdate
    ) -> PersonaInDB:
        """
        Update a persona.

        Args:
            persona_id: UUID of the persona to update
            update_data: PersonaUpdate model with fields to update

        Returns:
            PersonaInDB: Updated persona

        Raises:
            APIError: If database operation fails
            ValueError: If persona not found
        """
        try:
            logger.debug(f"Updating persona: {persona_id}")

            # Build update data (only non-None fields)
            data = update_data.model_dump(exclude_unset=True)
            if not data:
                logger.debug("No fields to update")
                return await self.read(persona_id)

            response = (
                self.supabase.client.table(self.table_name)
                .update(data)
                .eq("id", str(persona_id))
                .execute()
            )

            if not response.data:
                logger.warning(f"Persona not found for update: {persona_id}")
                raise ValueError(f"Persona not found: {persona_id}")

            result = response.data[0]
            logger.info(f"Persona updated: {persona_id}")

            return PersonaInDB(**result)
        except APIError as e:
            logger.error(f"API error updating persona: {e}")
            raise
        except Exception as e:
            logger.error(f"Error updating persona: {e}")
            raise

    async def delete(self, persona_id: UUID) -> bool:
        """
        Delete a persona.

        Args:
            persona_id: UUID of the persona to delete

        Returns:
            True if deleted, False if not found

        Raises:
            APIError: If database operation fails
        """
        try:
            logger.debug(f"Deleting persona: {persona_id}")

            response = (
                self.supabase.client.table(self.table_name)
                .delete()
                .eq("id", str(persona_id))
                .execute()
            )

            if not response.data:
                logger.debug(f"Persona not found for deletion: {persona_id}")
                return False

            logger.info(f"Persona deleted: {persona_id}")
            return True
        except APIError as e:
            logger.error(f"API error deleting persona: {e}")
            raise
        except Exception as e:
            logger.error(f"Error deleting persona: {e}")
            raise

    async def count(self) -> int:
        """
        Get total count of personas.

        Returns:
            Total number of personas

        Raises:
            APIError: If database operation fails
        """
        try:
            response = (
                self.supabase.client.table(self.table_name)
                .select("id", count="exact")
                .execute()
            )
            count = response.count or 0
            logger.debug(f"Total personas: {count}")
            return count
        except APIError as e:
            logger.error(f"API error counting personas: {e}")
            raise
        except Exception as e:
            logger.error(f"Error counting personas: {e}")
            raise


def get_persona_repository() -> PersonaRepository:
    """
    Get a persona repository instance.

    Returns:
        PersonaRepository instance

    Usage:
        from app.repositories.persona_repo import get_persona_repository
        repo = get_persona_repository()
        persona = await repo.create(persona_data)
    """
    return PersonaRepository()
