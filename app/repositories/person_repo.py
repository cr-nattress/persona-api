"""
Repository pattern implementation for person data access.

Provides CRUD operations (Create, Read, Update, Delete) for persons
with proper error handling and logging.
"""

from typing import List, Optional
from uuid import UUID
from app.models.person import PersonInDB
from app.db.supabase_client import get_supabase_client
from app.core.logging import get_logger
from postgrest.exceptions import APIError

logger = get_logger(__name__)


class PersonRepository:
    """Repository for person aggregate root data access."""

    def __init__(self):
        """Initialize repository with Supabase client."""
        self.supabase = get_supabase_client()
        self.table_name = "persons"

    async def create(
        self,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        gender: Optional[str] = None
    ) -> PersonInDB:
        """
        Create a new person aggregate root.

        The person is created with optional demographic information.
        Related submissions (person_data) and computed personas are added separately.

        Args:
            first_name: Optional first name of the person
            last_name: Optional last name of the person
            gender: Optional gender of the person

        Returns:
            PersonInDB: Created person with ID and timestamps

        Raises:
            APIError: If database operation fails
        """
        try:
            logger.debug(f"PersonRepository.create() called - creating new person aggregate root")
            logger.debug(f"  - first_name: {first_name}")
            logger.debug(f"  - last_name: {last_name}")
            logger.debug(f"  - gender: {gender}")

            # Build data dict with only non-None values
            data = {}
            if first_name is not None:
                data["first_name"] = first_name
            if last_name is not None:
                data["last_name"] = last_name
            if gender is not None:
                data["gender"] = gender

            response = (
                self.supabase.client.table(self.table_name)
                .insert(data)
                .execute()
            )

            if not response.data or len(response.data) == 0:
                logger.error(f"No data returned from Supabase insert")
                raise APIError("Failed to create person: no data returned")

            person_data = response.data[0]
            logger.debug(f"Person created successfully with ID: {person_data.get('id')}")
            logger.debug(f"  - first_name: {person_data.get('first_name')}")
            logger.debug(f"  - last_name: {person_data.get('last_name')}")
            logger.debug(f"  - gender: {person_data.get('gender')}")

            return PersonInDB(**person_data)

        except APIError as e:
            logger.error(f"Database error while creating person: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error while creating person: {str(e)}")
            raise APIError(f"Failed to create person: {str(e)}")

    async def read(self, person_id: UUID) -> Optional[PersonInDB]:
        """
        Retrieve a person by ID.

        Args:
            person_id: UUID of the person to retrieve

        Returns:
            PersonInDB: Person if found, None otherwise

        Raises:
            APIError: If database operation fails
        """
        try:
            logger.debug(f"PersonRepository.read() called for person_id: {person_id}")

            response = (
                self.supabase.client.table(self.table_name)
                .select("*")
                .eq("id", str(person_id))
                .execute()
            )

            if not response.data or len(response.data) == 0:
                logger.debug(f"Person not found: {person_id}")
                return None

            person_data = response.data[0]
            logger.debug(f"Person retrieved successfully: {person_id}")

            return PersonInDB(**person_data)

        except APIError as e:
            logger.error(f"Database error while reading person {person_id}: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error while reading person {person_id}: {str(e)}")
            raise APIError(f"Failed to read person: {str(e)}")

    async def read_all(self, limit: int = 50, offset: int = 0) -> List[PersonInDB]:
        """
        Retrieve all persons with pagination.

        Args:
            limit: Maximum number of records to return (default 50)
            offset: Number of records to skip (default 0)

        Returns:
            List[PersonInDB]: List of persons

        Raises:
            APIError: If database operation fails
        """
        try:
            logger.debug(f"PersonRepository.read_all() called with limit={limit}, offset={offset}")

            response = (
                self.supabase.client.table(self.table_name)
                .select("*")
                .order("created_at", desc=True)
                .range(offset, offset + limit - 1)
                .execute()
            )

            persons = [PersonInDB(**person) for person in response.data]
            logger.debug(f"Retrieved {len(persons)} persons")

            return persons

        except APIError as e:
            logger.error(f"Database error while reading all persons: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error while reading all persons: {str(e)}")
            raise APIError(f"Failed to read persons: {str(e)}")

    async def delete(self, person_id: UUID) -> bool:
        """
        Delete a person and all related data (cascade delete).

        Deletes the person aggregate root. Foreign key constraints
        ensure that related person_data and personas records are deleted.

        Args:
            person_id: UUID of the person to delete

        Returns:
            bool: True if deletion succeeded, False if person not found

        Raises:
            APIError: If database operation fails
        """
        try:
            logger.debug(f"PersonRepository.delete() called for person_id: {person_id}")

            # Check if person exists
            existing = await self.read(person_id)
            if not existing:
                logger.warning(f"Person not found for deletion: {person_id}")
                return False

            # Delete person (cascade delete handles related records)
            response = (
                self.supabase.client.table(self.table_name)
                .delete()
                .eq("id", str(person_id))
                .execute()
            )

            logger.debug(f"Person deleted successfully: {person_id}")
            return True

        except APIError as e:
            logger.error(f"Database error while deleting person {person_id}: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error while deleting person {person_id}: {str(e)}")
            raise APIError(f"Failed to delete person: {str(e)}")

    async def count(self) -> int:
        """
        Count total number of persons.

        Returns:
            int: Total count of persons

        Raises:
            APIError: If database operation fails
        """
        try:
            logger.debug(f"PersonRepository.count() called")

            response = (
                self.supabase.client.table(self.table_name)
                .select("id", count="exact")
                .execute()
            )

            count = response.count or 0
            logger.debug(f"Total persons: {count}")

            return count

        except APIError as e:
            logger.error(f"Database error while counting persons: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error while counting persons: {str(e)}")
            raise APIError(f"Failed to count persons: {str(e)}")
