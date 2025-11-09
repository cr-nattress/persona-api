"""
API route definitions for person aggregate root endpoints.

Provides REST endpoints for person management, data submission history,
and persona retrieval with versioning and lineage tracking.
"""

from fastapi import APIRouter, HTTPException, Query, status
from typing import Optional, List
from uuid import UUID
from app.models.person import PersonResponse, PersonInDB
from app.models.person_data import PersonDataResponse, PersonDataListResponse
from app.models.persona import PersonaResponse, PersonaWithHistory
from app.services.person_service import get_person_service
from app.core.logging import get_logger

logger = get_logger(__name__)

# Create single router for all person endpoints
router = APIRouter(prefix="/v1/person", tags=["Person"])

# ============================================================================
# PERSON MANAGEMENT ENDPOINTS
# ============================================================================


@router.post(
    "",
    response_model=PersonResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new person",
    responses={
        201: {"description": "Person created successfully"},
        500: {"description": "Internal server error"},
    },
)
async def create_person() -> PersonResponse:
    """
    Create a new person aggregate root.

    Creates a new person with no initial data. Data submissions and personas
    are added separately via dedicated endpoints.

    Returns:
        PersonResponse: Created person with ID, timestamps, and metadata

    Raises:
        HTTPException: If creation fails
    """
    try:
        logger.info("POST /v1/person - Creating new person")
        service = get_person_service()

        # Create person
        person = await service.create_person()

        # Build response with metadata
        response = PersonResponse(
            **person.model_dump(),
            person_data_count=0,
            latest_persona_version=None,
        )

        logger.info(f"Person created successfully: {person.id}")
        return response

    except Exception as e:
        logger.error(f"Failed to create person: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create person: {str(e)}",
        )


@router.get(
    "/{person_id}",
    response_model=PersonResponse,
    summary="Get person by ID",
    responses={
        200: {"description": "Person found"},
        404: {"description": "Person not found"},
        500: {"description": "Internal server error"},
    },
)
async def get_person(person_id: UUID) -> PersonResponse:
    """
    Retrieve a person by ID with metadata.

    Returns the person aggregate root with:
    - ID and timestamps
    - Count of data submissions
    - Latest persona version

    Args:
        person_id: UUID of the person to retrieve

    Returns:
        PersonResponse: Person with metadata

    Raises:
        HTTPException: If person not found or operation fails
    """
    try:
        logger.debug(f"GET /v1/person/{person_id}")
        service = get_person_service()

        person = await service.get_person(person_id)
        if not person:
            logger.warning(f"Person not found: {person_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Person not found: {person_id}",
            )

        logger.debug(f"Person retrieved: {person_id}")
        return person

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get person {person_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get person: {str(e)}",
        )


@router.get(
    "",
    response_model=List[PersonInDB],
    summary="List all persons",
    responses={
        200: {"description": "Persons retrieved"},
        500: {"description": "Internal server error"},
    },
)
async def list_persons(
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
) -> List[PersonInDB]:
    """
    List all persons with pagination.

    Args:
        limit: Maximum persons per page (1-100, default 50)
        offset: Number of persons to skip (default 0)

    Returns:
        List[PersonInDB]: Paginated list of persons

    Raises:
        HTTPException: If operation fails
    """
    try:
        logger.debug(f"GET /v1/person (limit={limit}, offset={offset})")
        service = get_person_service()

        persons, total = await service.list_persons(limit, offset)
        logger.debug(f"Listed {len(persons)} persons (total: {total})")

        return persons

    except Exception as e:
        logger.error(f"Failed to list persons: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list persons: {str(e)}",
        )


@router.delete(
    "/{person_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a person",
    responses={
        204: {"description": "Person deleted successfully"},
        404: {"description": "Person not found"},
        500: {"description": "Internal server error"},
    },
)
async def delete_person(person_id: UUID) -> None:
    """
    Delete a person and all related data.

    Cascade delete removes all person_data submissions and personas
    associated with the person. This is permanent and cannot be undone.

    Args:
        person_id: UUID of the person to delete

    Raises:
        HTTPException: If person not found or operation fails
    """
    try:
        logger.info(f"DELETE /v1/person/{person_id}")
        service = get_person_service()

        success = await service.delete_person(person_id)
        if not success:
            logger.warning(f"Person not found for deletion: {person_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Person not found: {person_id}",
            )

        logger.info(f"Person deleted: {person_id}")

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to delete person {person_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete person: {str(e)}",
        )


# ============================================================================
# PERSON DATA HISTORY ENDPOINTS
# ============================================================================


@router.post(
    "/{person_id}/data",
    response_model=PersonDataResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Add data to a person",
    responses={
        201: {"description": "Data added successfully"},
        404: {"description": "Person not found"},
        400: {"description": "Invalid request data"},
        500: {"description": "Internal server error"},
    },
)
async def add_person_data(
    person_id: UUID,
    raw_text: str = Query(..., min_length=1, max_length=100000),
    source: str = Query("api", max_length=50),
) -> PersonDataResponse:
    """
    Add unstructured data to a person.

    Creates a new immutable record of the data submission. Does NOT trigger
    persona recomputation (use the /data-and-regenerate endpoint for that).

    Args:
        person_id: UUID of the person
        raw_text: Unstructured text to add
        source: Source of data (api, urls, import, etc)

    Returns:
        PersonDataResponse: Created submission record

    Raises:
        HTTPException: If person not found or operation fails
    """
    try:
        logger.info(f"POST /v1/person/{person_id}/data")
        service = get_person_service()

        submission = await service.add_person_data(person_id, raw_text, source)
        logger.info(f"Data added to person {person_id}: {submission.id}")

        return PersonDataResponse(**submission.model_dump())

    except ValueError as e:
        logger.warning(f"Validation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    except Exception as e:
        logger.error(f"Failed to add data to person {person_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to add data: {str(e)}",
        )


@router.get(
    "/{person_id}/data",
    response_model=PersonDataListResponse,
    summary="Get person data history",
    responses={
        200: {"description": "Data history retrieved"},
        404: {"description": "Person not found"},
        500: {"description": "Internal server error"},
    },
)
async def get_person_data_history(
    person_id: UUID,
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
) -> PersonDataListResponse:
    """
    Get paginated history of data submissions for a person.

    Results are ordered by created_at (oldest first) to show
    the accumulation order of submissions.

    Args:
        person_id: UUID of the person
        limit: Maximum submissions per page (1-100, default 50)
        offset: Number of submissions to skip (default 0)

    Returns:
        PersonDataListResponse: Paginated list with total count

    Raises:
        HTTPException: If operation fails
    """
    try:
        logger.debug(f"GET /v1/person/{person_id}/data (limit={limit}, offset={offset})")
        service = get_person_service()

        submissions, total = await service.get_person_data_history(person_id, limit, offset)
        logger.debug(f"Retrieved {len(submissions)} submissions for {person_id}")

        return PersonDataListResponse(
            items=submissions,
            total=total,
            limit=limit,
            offset=offset,
        )

    except Exception as e:
        logger.error(f"Failed to get data history for {person_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get data history: {str(e)}",
        )


# ============================================================================
# PERSONA RETRIEVAL ENDPOINTS
# ============================================================================


@router.get(
    "/{person_id}/persona",
    response_model=PersonaResponse,
    summary="Get current persona for a person",
    responses={
        200: {"description": "Persona retrieved"},
        404: {"description": "Person or persona not found"},
        500: {"description": "Internal server error"},
    },
)
async def get_current_persona(person_id: UUID) -> PersonaResponse:
    """
    Get the current/latest persona for a person.

    Returns the latest computed persona with version and lineage information.

    Args:
        person_id: UUID of the person (not the persona)

    Returns:
        PersonaResponse: Current persona with version and computed_from_data_ids

    Raises:
        HTTPException: If person or persona not found
    """
    try:
        logger.debug(f"GET /v1/person/{person_id}/persona")
        service = get_person_service()

        # Get person to verify exists
        person = await service.get_person(person_id)
        if not person:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Person not found: {person_id}",
            )

        # Get current persona
        from app.repositories.persona_repo import PersonaRepository

        persona_repo = PersonaRepository()
        persona = await persona_repo.get_by_person_id(person_id)

        if not persona:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No persona found for person: {person_id}",
            )

        logger.debug(f"Persona retrieved for {person_id} (v{persona.version})")
        return persona

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get persona for {person_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get persona: {str(e)}",
        )


# ============================================================================
# COMBINED ENDPOINTS (Data + Regenerate)
# ============================================================================


@router.post(
    "/{person_id}/data-and-regenerate",
    response_model=dict,
    status_code=status.HTTP_201_CREATED,
    summary="Add data and regenerate persona",
    responses={
        201: {"description": "Data added and persona regenerated"},
        404: {"description": "Person not found"},
        400: {"description": "Invalid request data"},
        500: {"description": "Internal server error"},
    },
)
async def add_data_and_regenerate_persona(
    person_id: UUID,
    raw_text: str = Query(..., min_length=1, max_length=100000),
    source: str = Query("api", max_length=50),
) -> dict:
    """
    Add data to a person and regenerate their persona atomically.

    This endpoint combines two operations:
    1. Add a new data submission
    2. Regenerate persona from ALL accumulated data

    Returns both the new submission and the regenerated persona.

    Args:
        person_id: UUID of the person
        raw_text: Unstructured text to add
        source: Source of data (api, urls, import, etc)

    Returns:
        dict: Contains 'person_data' (submission) and 'persona' (regenerated)

    Raises:
        HTTPException: If person not found or operation fails
    """
    try:
        logger.info(f"POST /v1/person/{person_id}/data-and-regenerate")
        service = get_person_service()

        submission, persona = await service.add_person_data_and_regenerate(
            person_id, raw_text, source
        )

        logger.info(
            f"Data added and persona regenerated for {person_id} "
            f"(persona v{persona.version})"
        )

        return {
            "person_data": PersonDataResponse(**submission.model_dump()),
            "persona": PersonaResponse(**persona.model_dump()),
        }

    except ValueError as e:
        logger.warning(f"Validation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    except Exception as e:
        logger.error(
            f"Failed to add data and regenerate persona for {person_id}: {str(e)}"
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to add data and regenerate: {str(e)}",
        )
