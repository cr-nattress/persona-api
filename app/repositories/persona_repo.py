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
    PersonaWithHistory,
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
            # Detailed input validation logging
            logger.debug(f"PersonaRepository.create() called")
            logger.debug(f"  - raw_text type: {type(raw_text)}, length: {len(raw_text) if isinstance(raw_text, str) else 'N/A'}")
            logger.debug(f"  - raw_text preview: {raw_text[:100] if isinstance(raw_text, str) else repr(raw_text)}")
            logger.debug(f"  - persona_json type: {type(persona_json)}")
            logger.debug(f"  - persona_json is dict: {isinstance(persona_json, dict)}")

            if isinstance(persona_json, dict):
                logger.debug(f"  - persona_json keys: {list(persona_json.keys())}")
                logger.debug(f"  - persona_json size: {len(str(persona_json))} chars")
                logger.debug(f"  - persona_json preview: {str(persona_json)[:300]}")
            else:
                logger.debug(f"  - persona_json is NOT a dict! It is: {repr(persona_json)[:300]}")

            logger.debug(f"Creating persona from text: {raw_text[:50] if isinstance(raw_text, str) else repr(raw_text)[:50]}...")

            data = {
                "raw_text": raw_text,
                "persona": persona_json,
            }

            logger.debug(f"About to insert data into '{self.table_name}' table")
            logger.debug(f"Data structure being inserted:")
            logger.debug(f"  - 'raw_text' key present: {'raw_text' in data}")
            logger.debug(f"  - 'persona' key present: {'persona' in data}")
            logger.debug(f"  - data['raw_text'] type: {type(data['raw_text'])}")
            logger.debug(f"  - data['persona'] type: {type(data['persona'])}")

            response = (
                self.supabase.client.table(self.table_name)
                .insert(data)
                .execute()
            )

            logger.debug(f"Supabase insert response received")
            logger.debug(f"  - response type: {type(response)}")
            logger.debug(f"  - response.data available: {response.data is not None}")

            if not response.data:
                logger.error(f"No data returned from insert operation. Response: {response}")
                raise ValueError("No data returned from insert operation")

            result = response.data[0]
            logger.debug(f"Database returned record:")
            logger.debug(f"  - record type: {type(result)}")
            logger.debug(f"  - record keys: {list(result.keys()) if isinstance(result, dict) else 'NOT A DICT'}")
            logger.debug(f"  - record['id']: {result.get('id', 'KEY NOT FOUND')}")
            logger.debug(f"  - record['raw_text'] type: {type(result.get('raw_text', 'NOT FOUND'))}")
            logger.debug(f"  - record['persona'] type: {type(result.get('persona', 'NOT FOUND'))}")

            logger.info(f"Persona created successfully: {result['id']}")

            logger.debug(f"About to instantiate PersonaInDB(**result)")
            logger.debug(f"  - result keys being passed: {list(result.keys())}")

            return PersonaInDB(**result)
        except APIError as e:
            logger.error(f"API error creating persona: {e}")
            logger.error(f"  - APIError type: {type(e).__name__}")
            logger.error(f"  - APIError details: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error creating persona: {e}")
            logger.error(f"  - Exception type: {type(e).__name__}")
            logger.error(f"  - Exception args: {e.args}")
            logger.error(f"  - Full traceback:", exc_info=True)
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

    # ========================================================================
    # New Methods for Person Aggregate Root Support (Version & Lineage)
    # ========================================================================

    async def get_by_person_id(self, person_id: UUID) -> Optional[PersonaInDB]:
        """
        Retrieve the current persona for a person.

        Each person has exactly one persona record (UNIQUE constraint on person_id).
        This retrieves the latest/current computed persona for the person.

        Args:
            person_id: UUID of the person (not the persona)

        Returns:
            PersonaInDB: Current persona if exists, None otherwise

        Raises:
            APIError: If database operation fails
        """
        try:
            logger.debug(f"PersonaRepository.get_by_person_id() for person_id: {person_id}")

            response = (
                self.supabase.client.table(self.table_name)
                .select("*")
                .eq("person_id", str(person_id))
                .execute()
            )

            if not response.data or len(response.data) == 0:
                logger.debug(f"No persona found for person: {person_id}")
                return None

            persona_data = response.data[0]
            logger.debug(f"Persona retrieved for person {person_id}")

            return PersonaInDB(**persona_data)

        except APIError as e:
            logger.error(f"Database error reading persona for person {person_id}: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error reading persona for person {person_id}: {str(e)}")
            raise APIError(f"Failed to read persona for person: {str(e)}")

    async def create_for_person(
        self,
        person_id: UUID,
        persona_json: Dict[str, Any],
        data_ids: List[UUID],
        version: int = 1
    ) -> PersonaInDB:
        """
        Create a new persona for a person with versioning and lineage.

        Args:
            person_id: UUID of the person (aggregate root)
            persona_json: Generated persona JSON
            data_ids: List of person_data IDs used to generate this persona
            version: Version number (default 1 for first persona)

        Returns:
            PersonaInDB: Created persona with versioning info

        Raises:
            APIError: If database operation fails
        """
        try:
            logger.debug(f"PersonaRepository.create_for_person() for person_id: {person_id}")
            logger.debug(f"  - version: {version}")
            logger.debug(f"  - data_ids: {data_ids}")

            data = {
                "person_id": str(person_id),
                "persona": persona_json,
                "computed_from_data_ids": [str(uid) for uid in data_ids],
                "version": version,
            }

            response = (
                self.supabase.client.table(self.table_name)
                .insert(data)
                .execute()
            )

            if not response.data or len(response.data) == 0:
                logger.error(f"No data returned from persona creation")
                raise APIError("Failed to create persona: no data returned")

            persona_data = response.data[0]
            logger.info(f"Persona created for person {person_id} with version {version}")

            return PersonaInDB(**persona_data)

        except APIError as e:
            logger.error(f"Database error creating persona for person {person_id}: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error creating persona for person {person_id}: {str(e)}")
            raise APIError(f"Failed to create persona: {str(e)}")

    async def update_by_person_id(
        self,
        person_id: UUID,
        persona_json: Dict[str, Any],
        data_ids: List[UUID],
        version: int
    ) -> PersonaInDB:
        """
        Update persona for a person with new version and lineage.

        Increments version, updates persona JSON, and tracks which
        person_data IDs were used in this computation.

        Args:
            person_id: UUID of the person
            persona_json: New persona JSON
            data_ids: Updated list of person_data IDs used
            version: New version number

        Returns:
            PersonaInDB: Updated persona

        Raises:
            APIError: If database operation fails
        """
        try:
            logger.debug(f"PersonaRepository.update_by_person_id() for person_id: {person_id}")
            logger.debug(f"  - new version: {version}")
            logger.debug(f"  - new data_ids count: {len(data_ids)}")

            update_data = {
                "persona": persona_json,
                "computed_from_data_ids": [str(uid) for uid in data_ids],
                "version": version,
            }

            response = (
                self.supabase.client.table(self.table_name)
                .update(update_data)
                .eq("person_id", str(person_id))
                .execute()
            )

            if not response.data or len(response.data) == 0:
                logger.warning(f"Persona not found for update: {person_id}")
                raise ValueError(f"Persona not found for person: {person_id}")

            persona_data = response.data[0]
            logger.info(f"Persona updated for person {person_id} to version {version}")

            return PersonaInDB(**persona_data)

        except APIError as e:
            logger.error(f"Database error updating persona for person {person_id}: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error updating persona for person {person_id}: {str(e)}")
            raise APIError(f"Failed to update persona: {str(e)}")

    async def upsert(
        self,
        person_id: UUID,
        persona_json: Dict[str, Any],
        data_ids: List[UUID],
        version: int = 1
    ) -> PersonaInDB:
        """
        Create or update persona for a person (upsert).

        Atomically creates a new persona if one doesn't exist,
        or updates the existing one. Handles version tracking.

        Args:
            person_id: UUID of the person
            persona_json: Persona JSON
            data_ids: List of person_data IDs
            version: Version number (1 for new, incremented for updates)

        Returns:
            PersonaInDB: Created or updated persona

        Raises:
            APIError: If database operation fails
        """
        try:
            logger.debug(f"PersonaRepository.upsert() for person_id: {person_id}")

            # Check if persona exists
            existing = await self.get_by_person_id(person_id)

            if existing:
                # Update existing
                return await self.update_by_person_id(person_id, persona_json, data_ids, version)
            else:
                # Create new
                return await self.create_for_person(person_id, persona_json, data_ids, version)

        except Exception as e:
            logger.error(f"Error in upsert for person {person_id}: {str(e)}")
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
