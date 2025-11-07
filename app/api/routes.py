"""
API route definitions for persona endpoints.

Provides REST endpoints for persona creation, retrieval, and updates
with full Swagger documentation and error handling.
"""

from fastapi import APIRouter, HTTPException, Query, status
from typing import Optional
from uuid import UUID
from app.models.persona import (
    PersonaCreate,
    PersonaResponse,
    PersonaListResponse,
    PersonaInDB,
)
from app.services.persona_synthesizer import get_persona_synthesizer
from app.core.logging import get_logger

logger = get_logger(__name__)

router = APIRouter(
    prefix="/v1/persona",
    tags=["Personas"],
)


@router.post(
    "",
    response_model=PersonaResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new persona",
    responses={
        201: {"description": "Persona created successfully"},
        400: {"description": "Invalid request data"},
        500: {"description": "Internal server error during persona generation"},
    },
)
async def create_persona(
    request: PersonaCreate,
) -> PersonaResponse:
    """
    Create a new persona from raw text.

    Takes unstructured text about a person and generates a comprehensive
    persona profile using a two-step LLM pipeline:
    1. Clean and normalize the input text
    2. Generate structured persona JSON

    Args:
        request: PersonaCreate containing raw_text and initial persona data

    Returns:
        PersonaResponse: Created persona with ID and timestamps

    Raises:
        HTTPException: If persona generation fails

    Example:
        ```json
        POST /v1/persona
        {
            "raw_text": "John is an engineer who loves building systems...",
            "persona": {...}
        }
        ```
    """
    try:
        logger.info("Creating persona from raw text")
        logger.debug(f"Input text length: {len(request.raw_text)} chars")

        synthesizer = get_persona_synthesizer()
        persona = await synthesizer.generate_and_save_persona(
            request.raw_text
        )

        logger.info(f"Persona created successfully: {persona.id}")
        return PersonaResponse(**persona.model_dump())

    except ValueError as e:
        logger.error(f"Validation error creating persona: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except Exception as e:
        logger.error(f"Error creating persona: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate persona. Please try again.",
        )


@router.get(
    "/{persona_id}",
    response_model=PersonaResponse,
    summary="Retrieve a persona",
    responses={
        200: {"description": "Persona retrieved successfully"},
        404: {"description": "Persona not found"},
        500: {"description": "Internal server error"},
    },
)
async def get_persona(
    persona_id: str,
) -> PersonaResponse:
    """
    Retrieve a persona by ID.

    Args:
        persona_id: UUID of the persona to retrieve

    Returns:
        PersonaResponse: The requested persona

    Raises:
        HTTPException: If persona not found or error occurs

    Example:
        ```
        GET /v1/persona/550e8400-e29b-41d4-a716-446655440000
        ```
    """
    try:
        logger.debug(f"Retrieving persona: {persona_id}")

        synthesizer = get_persona_synthesizer()
        persona = await synthesizer.get_persona(persona_id)

        logger.info(f"Persona retrieved: {persona_id}")
        return PersonaResponse(**persona.model_dump())

    except ValueError as e:
        logger.warning(f"Persona not found: {persona_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    except Exception as e:
        logger.error(f"Error retrieving persona: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve persona.",
        )


@router.get(
    "",
    response_model=PersonaListResponse,
    summary="List all personas",
    responses={
        200: {"description": "Personas retrieved successfully"},
        500: {"description": "Internal server error"},
    },
)
async def list_personas(
    limit: int = Query(10, ge=1, le=100, description="Items per page"),
    offset: int = Query(0, ge=0, description="Number of items to skip"),
) -> PersonaListResponse:
    """
    List all personas with pagination.

    Args:
        limit: Number of personas per page (1-100, default: 10)
        offset: Number of personas to skip (default: 0)

    Returns:
        PersonaListResponse: List of personas with pagination metadata

    Raises:
        HTTPException: If listing fails

    Example:
        ```
        GET /v1/persona?limit=20&offset=0
        ```
    """
    try:
        logger.debug(f"Listing personas: limit={limit}, offset={offset}")

        synthesizer = get_persona_synthesizer()
        personas, total = await synthesizer.list_personas(limit, offset)

        logger.info(f"Listed {len(personas)} personas (total: {total})")
        return PersonaListResponse(
            items=personas,
            total=total,
            limit=limit,
            offset=offset,
        )

    except Exception as e:
        logger.error(f"Error listing personas: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to list personas.",
        )


@router.patch(
    "/{persona_id}",
    response_model=PersonaResponse,
    summary="Update a persona",
    responses={
        200: {"description": "Persona updated successfully"},
        404: {"description": "Persona not found"},
        400: {"description": "Invalid request data"},
        500: {"description": "Internal server error"},
    },
)
async def update_persona(
    persona_id: str,
    request: PersonaCreate,
) -> PersonaResponse:
    """
    Update a persona with new information.

    Takes new or updated text about the person and regenerates the
    persona profile, then saves the updated version.

    Args:
        persona_id: UUID of the persona to update
        request: PersonaCreate containing updated raw_text

    Returns:
        PersonaResponse: Updated persona

    Raises:
        HTTPException: If persona not found or update fails

    Example:
        ```json
        PATCH /v1/persona/550e8400-e29b-41d4-a716-446655440000
        {
            "raw_text": "Updated information about John...",
            "persona": {...}
        }
        ```
    """
    try:
        logger.info(f"Updating persona: {persona_id}")
        logger.debug(f"Update text length: {len(request.raw_text)} chars")

        synthesizer = get_persona_synthesizer()
        persona = await synthesizer.regenerate_persona(
            persona_id, request.raw_text
        )

        logger.info(f"Persona updated: {persona_id}")
        return PersonaResponse(**persona.model_dump())

    except ValueError as e:
        if "not found" in str(e).lower():
            logger.warning(f"Persona not found for update: {persona_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e),
            )
        else:
            logger.error(f"Validation error updating persona: {e}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e),
            )
    except Exception as e:
        logger.error(f"Error updating persona: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update persona. Please try again.",
        )


@router.delete(
    "/{persona_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a persona",
    responses={
        204: {"description": "Persona deleted successfully"},
        404: {"description": "Persona not found"},
        500: {"description": "Internal server error"},
    },
)
async def delete_persona(
    persona_id: str,
) -> None:
    """
    Delete a persona.

    Args:
        persona_id: UUID of the persona to delete

    Raises:
        HTTPException: If persona not found or deletion fails

    Example:
        ```
        DELETE /v1/persona/550e8400-e29b-41d4-a716-446655440000
        ```
    """
    try:
        logger.info(f"Deleting persona: {persona_id}")

        synthesizer = get_persona_synthesizer()
        deleted = await synthesizer.delete_persona(persona_id)

        if not deleted:
            logger.warning(f"Persona not found for deletion: {persona_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Persona not found: {persona_id}",
            )

        logger.info(f"Persona deleted: {persona_id}")

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting persona: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete persona.",
        )
