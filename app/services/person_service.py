"""
Person service - high-level business logic for person aggregate root operations.

Coordinates person lifecycle, data accumulation, and persona recomputation.
Implements the core domain logic for the person aggregate root pattern.
"""

from typing import Dict, Any, List, Optional
from uuid import UUID
from app.models.person import PersonInDB, PersonCreate, PersonResponse
from app.models.person_data import PersonDataInDB, PersonDataCreate
from app.models.persona import PersonaInDB
from app.repositories.person_repo import PersonRepository
from app.repositories.person_data_repo import PersonDataRepository
from app.repositories.persona_repo import PersonaRepository
from app.services.llm_chain import get_persona_llm_chain
from app.core.logging import get_logger

logger = get_logger(__name__)


class PersonService:
    """High-level business service for person aggregate root operations."""

    def __init__(
        self,
        person_repo: Optional[PersonRepository] = None,
        person_data_repo: Optional[PersonDataRepository] = None,
        persona_repo: Optional[PersonaRepository] = None,
    ):
        """
        Initialize PersonService.

        Args:
            person_repo: PersonRepository instance
            person_data_repo: PersonDataRepository instance
            persona_repo: PersonaRepository instance
        """
        self.person_repo = person_repo or PersonRepository()
        self.person_data_repo = person_data_repo or PersonDataRepository()
        self.persona_repo = persona_repo or PersonaRepository()
        self.llm_chain = get_persona_llm_chain()

    # ========================================================================
    # Person Aggregate Root Operations
    # ========================================================================

    async def create_person(self) -> PersonInDB:
        """
        Create a new person aggregate root.

        The person is created with minimal data. Related submissions and
        personas are added separately via dedicated endpoints.

        Returns:
            PersonInDB: Created person with ID and timestamps

        Raises:
            ValueError: If creation fails
        """
        logger.info("PersonService: Creating new person aggregate root")

        try:
            person = await self.person_repo.create()
            logger.info(f"Person created: {person.id}")
            return person

        except Exception as e:
            logger.error(f"Failed to create person: {str(e)}")
            raise ValueError(f"Failed to create person: {str(e)}")

    async def get_person(self, person_id: UUID) -> Optional[PersonResponse]:
        """
        Retrieve a person with metadata.

        Includes count of data submissions and latest persona version.

        Args:
            person_id: UUID of the person

        Returns:
            PersonResponse with metadata, or None if not found

        Raises:
            ValueError: If retrieval fails
        """
        logger.debug(f"PersonService: Getting person {person_id}")

        try:
            person = await self.person_repo.read(person_id)
            if not person:
                logger.debug(f"Person not found: {person_id}")
                return None

            # Get metadata
            data_count = await self.person_data_repo.count_for_person(person_id)
            persona = await self.persona_repo.get_by_person_id(person_id)

            return PersonResponse(
                **person.model_dump(),
                person_data_count=data_count,
                latest_persona_version=persona.version if persona else None,
            )

        except Exception as e:
            logger.error(f"Failed to get person {person_id}: {str(e)}")
            raise ValueError(f"Failed to get person: {str(e)}")

    async def list_persons(
        self, limit: int = 50, offset: int = 0
    ) -> tuple[List[PersonInDB], int]:
        """
        List all persons with pagination.

        Args:
            limit: Maximum number of persons
            offset: Number to skip

        Returns:
            Tuple of (persons list, total count)

        Raises:
            ValueError: If listing fails
        """
        logger.debug(f"PersonService: Listing persons (limit={limit}, offset={offset})")

        try:
            persons = await self.person_repo.read_all(limit, offset)
            count = await self.person_repo.count()
            logger.debug(f"Retrieved {len(persons)} persons (total: {count})")
            return persons, count

        except Exception as e:
            logger.error(f"Failed to list persons: {str(e)}")
            raise ValueError(f"Failed to list persons: {str(e)}")

    async def delete_person(self, person_id: UUID) -> bool:
        """
        Delete a person and all related data.

        Cascade delete removes person_data and personas associated with
        the person. This is permanent and cannot be undone.

        Args:
            person_id: UUID of person to delete

        Returns:
            True if deleted, False if not found

        Raises:
            ValueError: If deletion fails
        """
        logger.info(f"PersonService: Deleting person {person_id}")

        try:
            success = await self.person_repo.delete(person_id)
            if success:
                logger.info(f"Person deleted: {person_id}")
            else:
                logger.warning(f"Person not found for deletion: {person_id}")
            return success

        except Exception as e:
            logger.error(f"Failed to delete person {person_id}: {str(e)}")
            raise ValueError(f"Failed to delete person: {str(e)}")

    # ========================================================================
    # Data Accumulation Operations
    # ========================================================================

    async def add_person_data(
        self,
        person_id: UUID,
        raw_text: str,
        source: str = "api",
    ) -> PersonDataInDB:
        """
        Add unstructured data to a person.

        Creates a new immutable record of the data submission.
        Does not trigger persona recomputation (use add_and_recompute for that).

        Args:
            person_id: UUID of the person
            raw_text: Unstructured data to add
            source: Source of data (api, urls, import, etc)

        Returns:
            PersonDataInDB: Created submission record

        Raises:
            ValueError: If person not found or operation fails
        """
        logger.debug(f"PersonService: Adding data to person {person_id}")

        try:
            # Verify person exists
            person = await self.person_repo.read(person_id)
            if not person:
                raise ValueError(f"Person not found: {person_id}")

            # Add data submission
            submission = await self.person_data_repo.create(person_id, raw_text, source)
            logger.debug(f"Data added to person {person_id}: {submission.id}")

            return submission

        except Exception as e:
            logger.error(f"Failed to add data to person {person_id}: {str(e)}")
            raise

    async def add_person_data_and_regenerate(
        self,
        person_id: UUID,
        raw_text: str,
        source: str = "api",
    ) -> tuple[PersonDataInDB, PersonaInDB]:
        """
        Add data to a person and regenerate their persona.

        Atomically adds a new data submission and recomputes the persona
        using all accumulated data. Returns both the new submission and
        the updated persona.

        Args:
            person_id: UUID of the person
            raw_text: Unstructured data to add
            source: Source of data (api, urls, import, etc)

        Returns:
            Tuple of (created submission, regenerated persona)

        Raises:
            ValueError: If person not found or operation fails
        """
        logger.info(f"PersonService: Adding data and regenerating persona for {person_id}")

        try:
            # Verify person exists
            person = await self.person_repo.read(person_id)
            if not person:
                raise ValueError(f"Person not found: {person_id}")

            # Add data submission
            submission = await self.person_data_repo.create(person_id, raw_text, source)
            logger.debug(f"Data submitted: {submission.id}")

            # Regenerate persona from all accumulated data
            persona = await self.recompute_persona(person_id)

            if not persona:
                raise ValueError(f"Failed to regenerate persona for person {person_id}")

            logger.info(f"Persona regenerated for person {person_id} (version {persona.version})")

            return submission, persona

        except Exception as e:
            logger.error(f"Failed to add data and regenerate for {person_id}: {str(e)}")
            raise

    async def get_person_data_history(
        self,
        person_id: UUID,
        limit: int = 50,
        offset: int = 0,
    ) -> tuple[List[PersonDataInDB], int]:
        """
        Get paginated history of data submissions for a person.

        Results ordered by created_at (oldest first) to show
        accumulation order.

        Args:
            person_id: UUID of the person
            limit: Maximum submissions per page
            offset: Number to skip

        Returns:
            Tuple of (submissions list, total count)

        Raises:
            ValueError: If operation fails
        """
        logger.debug(f"PersonService: Getting data history for person {person_id}")

        try:
            submissions = await self.person_data_repo.get_all_for_person(
                person_id, limit, offset
            )
            count = await self.person_data_repo.count_for_person(person_id)

            logger.debug(f"Retrieved {len(submissions)} submissions (total: {count})")
            return submissions, count

        except Exception as e:
            logger.error(f"Failed to get data history for {person_id}: {str(e)}")
            raise ValueError(f"Failed to get data history: {str(e)}")

    # ========================================================================
    # Persona Recomputation (Core Business Logic)
    # ========================================================================

    async def recompute_persona(self, person_id: UUID) -> Optional[PersonaInDB]:
        """
        Recompute persona from all accumulated data.

        This is the core business logic that makes persona improvement possible:
        1. Fetch ALL person_data submissions (ordered by creation time)
        2. Concatenate all raw_text values with separators
        3. Generate new persona JSON from accumulated text via LLM
        4. Increment version number
        5. Store new persona with lineage tracking (data IDs used)

        This method is called automatically when new data is added via
        add_person_data_and_regenerate().

        Args:
            person_id: UUID of the person

        Returns:
            PersonaInDB: Regenerated persona, or None if no data exists

        Raises:
            ValueError: If persona generation fails
        """
        logger.info(f"PersonService: Recomputing persona for person {person_id}")

        try:
            # Get all accumulated data for this person
            all_data = await self.person_data_repo.get_all_for_person_unordered(person_id)

            if not all_data:
                logger.debug(f"No data for person {person_id}, cannot generate persona")
                return None

            logger.debug(f"Found {len(all_data)} data submissions for persona generation")

            # Concatenate all raw_text in chronological order with separators
            accumulated_text = self._concatenate_person_data(all_data)
            logger.debug(f"Accumulated text length: {len(accumulated_text)}")

            # Generate new persona from accumulated text via LLM
            persona_json = await self.llm_chain.generate_persona(accumulated_text)
            logger.debug(f"LLM generated persona JSON")

            # Get current persona to determine version
            current_persona = await self.persona_repo.get_by_person_id(person_id)
            new_version = (current_persona.version + 1) if current_persona else 1

            # Collect all data IDs for lineage tracking
            data_ids = [item.id for item in all_data]

            logger.debug(f"Creating persona version {new_version} with {len(data_ids)} data IDs")

            # Create or update persona with versioning and lineage
            persona = await self.persona_repo.upsert(
                person_id=person_id,
                persona_json=persona_json,
                data_ids=data_ids,
                version=new_version,
            )

            logger.info(
                f"Persona recomputed for person {person_id}: "
                f"v{persona.version} using {len(data_ids)} data submissions"
            )

            return persona

        except Exception as e:
            logger.error(f"Failed to recompute persona for {person_id}: {str(e)}")
            raise ValueError(f"Failed to recompute persona: {str(e)}")

    def _concatenate_person_data(self, submissions: List[PersonDataInDB]) -> str:
        """
        Concatenate all person data submissions with separators.

        Preserves chronological order and makes it clear where each
        submission boundary is for the LLM.

        Args:
            submissions: List of PersonDataInDB ordered by created_at

        Returns:
            str: Concatenated text with separators
        """
        parts = []
        for i, submission in enumerate(submissions, 1):
            header = f"\n--- Data Submission #{i} (submitted {submission.created_at.isoformat()}) ---\n"
            parts.append(header)
            parts.append(submission.raw_text)

        result = "".join(parts)
        logger.debug(f"Concatenated {len(submissions)} submissions into {len(result)} chars")
        return result


def get_person_service() -> PersonService:
    """
    Get a person service instance.

    Returns:
        PersonService instance

    Usage:
        from app.services.person_service import get_person_service
        service = get_person_service()
        person = await service.create_person()
    """
    return PersonService()
