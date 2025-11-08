"""
API route definitions for persona endpoints.

Provides REST endpoints for persona creation, retrieval, and updates
with full Swagger documentation and error handling.
"""

from fastapi import APIRouter, HTTPException, Query, status
from typing import Optional, Dict, Any, List
from uuid import UUID
from app.models.persona import (
    PersonaCreate,
    PersonaResponse,
    PersonaCreateResponse,
    PersonaListResponse,
    PersonaInDB,
)
from app.services.persona_service import get_persona_service
from app.services.url_fetcher import URLFetcher, URLFetchError
from app.core.logging import get_logger

logger = get_logger(__name__)

router = APIRouter(
    prefix="/v1/persona",
    tags=["Personas"],
)


@router.post(
    "",
    response_model=PersonaCreateResponse,
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
) -> PersonaCreateResponse:
    """
    Create a new persona from raw text and/or URLs.

    Supports flexible input sources:
    - raw_text: Direct text input for persona generation
    - urls: 1-10 URLs containing persona information
    - Both: Combines URL content with raw_text

    Generates a comprehensive persona profile using a two-step LLM pipeline:
    1. Clean and normalize the input text
    2. Generate structured persona JSON

    Args:
        request: PersonaCreate containing either raw_text or urls (or both)

    Returns:
        PersonaCreateResponse: Created persona with ID, created_at, and updated_at
        (minimal response excluding raw_text and persona JSON for optimized payload)

    Raises:
        HTTPException: If persona generation fails or URL fetching fails

    Example:
        ```json
        POST /v1/persona
        {
            "raw_text": "John is an engineer who loves building systems..."
        }
        ```
        or
        ```json
        {
            "urls": ["https://example.com/bio", "https://example.com/resume"]
        }
        ```
    """
    try:
        # Detailed request validation logging
        logger.debug(f"create_persona() endpoint called")
        logger.debug(f"  - request type: {type(request)}")
        logger.debug(f"  - request class: {request.__class__.__name__}")

        # Determine input source
        logger.debug(f"Processing request input:")
        logger.debug(f"  - request.raw_text type: {type(request.raw_text)}")
        logger.debug(f"  - request.raw_text value: {request.raw_text if request.raw_text else 'None or empty'}")
        logger.debug(f"  - request.urls type: {type(request.urls)}")
        logger.debug(f"  - request.urls value: {request.urls if request.urls else 'None or empty'}")

        input_text = request.raw_text or ""

        logger.debug(f"Initial input_text: type={type(input_text)}, length={len(input_text)}")

        # Fetch content from URLs if provided
        if request.urls:
            logger.info(f"Creating persona from {len(request.urls)} URL(s)")
            try:
                url_fetcher = URLFetcher()
                logger.debug(f"Fetching content from {len(request.urls)} URL(s)...")
                url_content = await url_fetcher.fetch_multiple(
                    [str(url) for url in request.urls]
                )
                logger.debug(f"URL fetch complete: {len(url_content)} chars retrieved")

                # Combine URL content with raw_text if provided
                if input_text:
                    input_text = f"{input_text}\n\n---\n\n{url_content}"
                    logger.debug(f"Combined input: raw_text + url_content = {len(input_text)} chars")
                else:
                    input_text = url_content
                    logger.debug(f"Using url_content only: {len(input_text)} chars")

                logger.debug(f"Final combined input_text: type={type(input_text)}, length={len(input_text)}")

            except URLFetchError as e:
                logger.error(f"URL fetch failed: {str(e)}")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Failed to fetch content from provided URLs: {str(e)}",
                )
        else:
            logger.info("Creating persona from raw text")
            logger.debug(f"Input text length: {len(input_text)} chars")
            logger.debug(f"Input text type: {type(input_text)}")
            logger.debug(f"Input text preview: {input_text[:200] if input_text else 'empty'}")

        # Create persona with combined input
        logger.debug(f"About to call service.generate_persona() with:")
        logger.debug(f"  - input_text type: {type(input_text)}")
        logger.debug(f"  - input_text length: {len(input_text)}")
        logger.debug(f"  - input_text preview: {input_text[:300]}")

        service = get_persona_service()
        persona = await service.generate_persona(input_text)

        logger.debug(f"service.generate_persona() returned:")
        logger.debug(f"  - persona type: {type(persona)}")
        logger.debug(f"  - persona class: {persona.__class__.__name__}")
        logger.debug(f"  - persona.id: {persona.id}")
        logger.debug(f"  - persona.created_at: {persona.created_at}")
        logger.debug(f"  - persona.updated_at: {persona.updated_at}")

        logger.info(f"Persona created successfully: {persona.id}")

        # Return minimal response with only id, created_at, updated_at
        logger.debug(f"Building PersonaCreateResponse...")
        response = PersonaCreateResponse(
            id=str(persona.id),
            created_at=persona.created_at,
            updated_at=persona.updated_at,
        )
        logger.debug(f"PersonaCreateResponse created successfully")
        return response

    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except ValueError as e:
        logger.error(f"Validation error creating persona: {e}")
        logger.error(f"  - ValueError type: {type(e).__name__}")
        logger.error(f"  - ValueError details: {str(e)}")
        logger.error(f"  - Full traceback: ", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except Exception as e:
        logger.error(f"Error creating persona: {e}")
        logger.error(f"  - Exception type: {type(e).__name__}")
        logger.error(f"  - Exception details: {str(e)}")
        logger.error(f"  - Full traceback: ", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate persona. Please try again.",
        )


@router.get(
    "",
    response_model=PersonaListResponse,
    summary="List all personas",
    responses={
        200: {"description": "Personas retrieved successfully"},
        500: {"description": "Internal server error"},
    },
    include_in_schema=False,
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

        service = get_persona_service()
        personas, total = await service.list_personas(limit, offset)

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


@router.post(
    "/merge",
    response_model=PersonaResponse,
    summary="Merge two personas",
    responses={
        200: {"description": "Personas merged successfully"},
        404: {"description": "One or both personas not found"},
        400: {"description": "Invalid request data"},
        500: {"description": "Internal server error"},
    },
    include_in_schema=False,
)
async def merge_personas(
    persona_id_1: str = Query(..., description="UUID of first persona"),
    persona_id_2: str = Query(..., description="UUID of second persona"),
    merged_raw_text: Optional[str] = Query(None, description="Optional merged text"),
) -> PersonaResponse:
    """
    Merge two personas into one.

    Combines information from both personas. The first persona ID becomes
    the merged result, and the second persona is deleted.

    Args:
        persona_id_1: UUID of first persona (result will use this ID)
        persona_id_2: UUID of second persona (will be deleted)
        merged_raw_text: Optional new raw text. If not provided, both texts are combined.

    Returns:
        PersonaResponse: Merged persona

    Example:
        ```
        POST /v1/persona/merge?persona_id_1=uuid1&persona_id_2=uuid2
        ```
    """
    try:
        logger.info(f"Merging personas: {persona_id_1} + {persona_id_2}")
        service = get_persona_service()
        merged = await service.merge_personas(persona_id_1, persona_id_2, merged_raw_text)
        logger.info(f"Merge successful: {persona_id_1}")
        return PersonaResponse(**merged.model_dump())

    except ValueError as e:
        logger.warning(f"Merge error: {e}")
        if "not found" in str(e).lower():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e),
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except Exception as e:
        logger.error(f"Error merging personas: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to merge personas.",
        )


@router.post(
    "/batch",
    response_model=List[PersonaResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Batch generate personas",
    responses={
        201: {"description": "Personas generated successfully"},
        400: {"description": "Invalid request data"},
        500: {"description": "Internal server error"},
    },
    include_in_schema=False,
)
async def batch_generate_personas(
    raw_texts: List[str],
) -> List[PersonaResponse]:
    """
    Batch generate multiple personas.

    Creates multiple personas in sequence from a list of raw texts.

    Args:
        raw_texts: List of unstructured text entries

    Returns:
        List of created personas

    Example:
        ```json
        POST /v1/persona/batch
        ["Text about person 1", "Text about person 2"]
        ```
    """
    try:
        if not raw_texts:
            raise ValueError("raw_texts list cannot be empty")

        logger.info(f"Batch generating {len(raw_texts)} personas")
        service = get_persona_service()
        personas = await service.batch_generate_personas(raw_texts)
        logger.info(f"Batch generation complete: {len(personas)} personas")
        return [PersonaResponse(**p.model_dump()) for p in personas]

    except ValueError as e:
        logger.warning(f"Batch error: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except Exception as e:
        logger.error(f"Error in batch generation: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to batch generate personas.",
        )


@router.get(
    "/search",
    response_model=List[PersonaResponse],
    summary="Search personas",
    responses={
        200: {"description": "Search completed successfully"},
        400: {"description": "Invalid query"},
        500: {"description": "Internal server error"},
    },
    include_in_schema=False,
)
async def search_personas(
    q: str = Query(..., min_length=1, description="Search query (name, role, keywords)"),
    limit: int = Query(10, ge=1, le=100, description="Maximum results"),
) -> List[PersonaResponse]:
    """
    Search for personas by name, role, or keywords.

    Searches across persona metadata and raw text.

    Args:
        q: Search query
        limit: Maximum results to return (1-100)

    Returns:
        List of matching personas

    Example:
        ```
        GET /v1/persona/search?q=engineer&limit=20
        ```
    """
    try:
        logger.debug(f"Searching personas for '{q}'")
        service = get_persona_service()
        results = await service.search_personas(q, limit)
        logger.info(f"Search found {len(results)} results for '{q}'")
        return [PersonaResponse(**p.model_dump()) for p in results]

    except Exception as e:
        logger.error(f"Error searching personas: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to search personas.",
        )


@router.get(
    "/stats",
    summary="Get persona statistics",
    responses={
        200: {"description": "Stats retrieved successfully"},
        500: {"description": "Internal server error"},
    },
    include_in_schema=False,
)
async def get_persona_stats() -> Dict[str, Any]:
    """
    Get statistics about personas in the system.

    Returns metrics like total count, creation date ranges, and activity.

    Returns:
        Dictionary with statistics

    Example:
        ```
        GET /v1/persona/stats
        ```
    """
    try:
        logger.debug("Getting persona statistics")
        service = get_persona_service()
        stats = await service.get_persona_stats()
        logger.info("Statistics retrieved")
        return stats

    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get persona statistics.",
        )


@router.get(
    "/export",
    summary="Export all personas",
    responses={
        200: {"description": "Export successful"},
        400: {"description": "Invalid format"},
        500: {"description": "Internal server error"},
    },
    include_in_schema=False,
)
async def export_personas(
    format: str = Query("json", description="Export format (json)"),
    limit: int = Query(1000, ge=1, le=10000, description="Max personas to export"),
) -> Dict[str, Any]:
    """
    Export personas in specified format.

    Args:
        format: Export format (currently 'json' only)
        limit: Maximum personas to include (1-10000)

    Returns:
        Exported data with metadata

    Example:
        ```
        GET /v1/persona/export?format=json&limit=500
        ```
    """
    try:
        logger.info(f"Exporting personas as {format}")
        service = get_persona_service()
        export_data = await service.export_personas(format, limit)
        logger.info(f"Export complete: {export_data['total_exported']} personas")
        return export_data

    except ValueError as e:
        logger.warning(f"Export format error: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except Exception as e:
        logger.error(f"Error exporting personas: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to export personas.",
        )


# GENERIC PERSONA ENDPOINTS - MUST BE LAST!
# These generic routes must come after all specific routes (/search, /stats, /export, etc.)
# to avoid catching those paths as persona IDs


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

        service = get_persona_service()
        persona = await service.get_persona(persona_id)

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
async def update_persona_endpoint(
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

        service = get_persona_service()
        persona = await service.update_persona(persona_id, request.raw_text)

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
async def delete_persona_endpoint(
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

        service = get_persona_service()
        deleted = await service.delete_persona(persona_id)

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
