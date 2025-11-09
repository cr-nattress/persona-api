"""
Repository pattern implementation for person data submissions.

Provides CRUD operations for unstructured data submissions with
proper error handling and logging.
"""

from typing import List, Optional
from uuid import UUID
from app.models.person_data import PersonDataInDB
from app.db.supabase_client import get_supabase_client
from app.core.logging import get_logger
from postgrest.exceptions import APIError

logger = get_logger(__name__)


class PersonDataRepository:
    """Repository for person data (unstructured submissions) access."""

    def __init__(self):
        """Initialize repository with Supabase client."""
        self.supabase = get_supabase_client()
        self.table_name = "person_data"

    async def create(
        self,
        person_id: UUID,
        raw_text: str,
        source: str = "api"
    ) -> PersonDataInDB:
        """
        Create a new person data submission.

        Each submission represents one API call with all unstructured
        data sent in that call. This becomes a historical record that
        is never overwritten.

        Args:
            person_id: UUID of the person this data belongs to
            raw_text: Complete unstructured text submitted
            source: Source of data (api, urls, import, etc)

        Returns:
            PersonDataInDB: Created submission record

        Raises:
            APIError: If database operation fails
        """
        try:
            logger.debug(f"PersonDataRepository.create() called for person_id: {person_id}")
            logger.debug(f"  - raw_text length: {len(raw_text)}")
            logger.debug(f"  - source: {source}")

            data = {
                "person_id": str(person_id),
                "raw_text": raw_text,
                "source": source,
            }

            response = (
                self.supabase.client.table(self.table_name)
                .insert(data)
                .execute()
            )

            if not response.data or len(response.data) == 0:
                logger.error(f"No data returned from Supabase insert")
                raise APIError("Failed to create person data: no data returned")

            submission_data = response.data[0]
            logger.debug(f"Person data created: {submission_data.get('id')} for person {person_id}")

            return PersonDataInDB(**submission_data)

        except APIError as e:
            logger.error(f"Database error while creating person data: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error while creating person data: {str(e)}")
            raise APIError(f"Failed to create person data: {str(e)}")

    async def get_by_id(self, data_id: UUID) -> Optional[PersonDataInDB]:
        """
        Retrieve a person data submission by ID.

        Args:
            data_id: UUID of the submission to retrieve

        Returns:
            PersonDataInDB: Submission if found, None otherwise

        Raises:
            APIError: If database operation fails
        """
        try:
            logger.debug(f"PersonDataRepository.get_by_id() called for data_id: {data_id}")

            response = (
                self.supabase.client.table(self.table_name)
                .select("*")
                .eq("id", str(data_id))
                .execute()
            )

            if not response.data or len(response.data) == 0:
                logger.debug(f"Person data not found: {data_id}")
                return None

            submission_data = response.data[0]
            logger.debug(f"Person data retrieved: {data_id}")

            return PersonDataInDB(**submission_data)

        except APIError as e:
            logger.error(f"Database error while reading person data {data_id}: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error while reading person data {data_id}: {str(e)}")
            raise APIError(f"Failed to read person data: {str(e)}")

    async def get_all_for_person(
        self,
        person_id: UUID,
        limit: int = 50,
        offset: int = 0
    ) -> List[PersonDataInDB]:
        """
        Retrieve all data submissions for a person with pagination.

        Results are ordered by created_at (oldest first) to enable
        sequential persona recomputation.

        Args:
            person_id: UUID of the person
            limit: Maximum records to return
            offset: Number of records to skip

        Returns:
            List[PersonDataInDB]: List of submissions ordered by creation time

        Raises:
            APIError: If database operation fails
        """
        try:
            logger.debug(f"PersonDataRepository.get_all_for_person() for person_id: {person_id}")
            logger.debug(f"  - limit: {limit}, offset: {offset}")

            response = (
                self.supabase.client.table(self.table_name)
                .select("*")
                .eq("person_id", str(person_id))
                .order("created_at", desc=False)  # Oldest first for recomputation
                .range(offset, offset + limit - 1)
                .execute()
            )

            submissions = [PersonDataInDB(**item) for item in response.data]
            logger.debug(f"Retrieved {len(submissions)} person data submissions for {person_id}")

            return submissions

        except APIError as e:
            logger.error(f"Database error while reading person data for {person_id}: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error while reading person data for {person_id}: {str(e)}")
            raise APIError(f"Failed to read person data: {str(e)}")

    async def get_all_for_person_unordered(self, person_id: UUID) -> List[PersonDataInDB]:
        """
        Retrieve all data submissions for a person without pagination.

        This is used for persona recomputation where we need all data
        ordered by created_at in a single query.

        Args:
            person_id: UUID of the person

        Returns:
            List[PersonDataInDB]: All submissions ordered by creation time

        Raises:
            APIError: If database operation fails
        """
        try:
            logger.debug(f"PersonDataRepository.get_all_for_person_unordered() for person_id: {person_id}")

            response = (
                self.supabase.client.table(self.table_name)
                .select("*")
                .eq("person_id", str(person_id))
                .order("created_at", desc=False)  # Oldest first for recomputation
                .execute()
            )

            submissions = [PersonDataInDB(**item) for item in response.data]
            logger.debug(f"Retrieved {len(submissions)} total person data submissions for {person_id}")

            return submissions

        except APIError as e:
            logger.error(f"Database error while reading all person data for {person_id}: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error while reading all person data for {person_id}: {str(e)}")
            raise APIError(f"Failed to read person data: {str(e)}")

    async def count_for_person(self, person_id: UUID) -> int:
        """
        Count total data submissions for a person.

        Args:
            person_id: UUID of the person

        Returns:
            int: Total count of submissions

        Raises:
            APIError: If database operation fails
        """
        try:
            logger.debug(f"PersonDataRepository.count_for_person() for person_id: {person_id}")

            response = (
                self.supabase.client.table(self.table_name)
                .select("id", count="exact")
                .eq("person_id", str(person_id))
                .execute()
            )

            count = response.count or 0
            logger.debug(f"Person {person_id} has {count} data submissions")

            return count

        except APIError as e:
            logger.error(f"Database error while counting person data for {person_id}: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error while counting person data for {person_id}: {str(e)}")
            raise APIError(f"Failed to count person data: {str(e)}")
