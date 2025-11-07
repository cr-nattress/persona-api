# TASK-08-03-03: Update POST /v1/persona Endpoint to Handle URL Inputs

**Story:** US-08-03

**Estimated Time:** 20 minutes

**Description:** Update the POST /v1/persona endpoint to handle both raw_text and URLs input, fetching and combining content as needed.

## Agent Prompt

You are implementing **EPIC-08: Enhance POST /persona Endpoint with URL Support and Optimized Response**.

**Goal:** Update the POST /v1/persona endpoint to accept and process URL inputs alongside raw_text.

**Context:** With the request model enhanced and URL fetcher implemented, we need to update the endpoint to:
- Accept the new URLs parameter
- Fetch and extract content from URLs if provided
- Combine URL content with raw_text if both are provided
- Pass combined content to persona service
- Return PersonaCreateResponse as before

**Instructions:**

1. Locate the POST /v1/persona endpoint (typically in `app/api/routes.py`)

2. Import necessary modules:
   ```python
   from app.services.url_fetcher import URLFetcher, URLFetchError
   from app.models.persona import CreatePersonaRequest, PersonaCreateResponse
   ```

3. Update endpoint to handle URLs:
   ```python
   @router.post("/v1/persona", response_model=PersonaCreateResponse, status_code=201)
   async def create_persona(
       request: CreatePersonaRequest,
       service: PersonaService = Depends(get_persona_service),
       url_fetcher: URLFetcher = Depends(get_url_fetcher)
   ):
       """
       Create a new persona from raw text and/or URLs.

       Request can provide:
       - raw_text: Direct text input
       - urls: 1-10 URLs containing persona information
       - Both raw_text and urls can be provided together

       Returns:
           PersonaCreateResponse with id, created_at, updated_at
       """
       input_text = request.raw_text or ""

       # Fetch content from URLs if provided
       if request.urls:
           try:
               url_content = await url_fetcher.fetch_multiple(
                   [str(url) for url in request.urls]
               )
               # Combine URL content with raw_text
               input_text = (input_text + "\n\n" + url_content).strip()
           except URLFetchError as e:
               raise HTTPException(
                   status_code=400,
                   detail=f"Failed to fetch content from URLs: {str(e)}"
               )

       # Pass combined input to service
       persona = await service.create_persona(input_text)

       return PersonaCreateResponse(
           id=persona.id,
           created_at=persona.created_at,
           updated_at=persona.updated_at
       )
   ```

4. Create dependency injection for URLFetcher:
   ```python
   def get_url_fetcher() -> URLFetcher:
       """Provide URLFetcher instance."""
       return URLFetcher()
   ```

5. Add error handling for URL fetching failures

6. Update endpoint docstring to document both input methods

## Verification Steps

1. Verify endpoint imports URLFetcher and related classes
2. Test endpoint with raw_text only (existing behavior)
3. Test endpoint with urls only (new behavior)
4. Test endpoint with both raw_text and urls
5. Test error handling when URL fetch fails
6. Verify response is PersonaCreateResponse (id, created_at, updated_at only)

## Expected Output

Updated POST /v1/persona endpoint that:
- Accepts both raw_text and urls parameters
- Fetches content from URLs when provided
- Combines content from multiple sources
- Returns 201 with PersonaCreateResponse
- Handles URL fetch errors gracefully
- Includes clear documentation

## Code Example

```python
from fastapi import APIRouter, Depends, HTTPException
from app.models.persona import CreatePersonaRequest, PersonaCreateResponse
from app.services.persona_service import PersonaService
from app.services.url_fetcher import URLFetcher, URLFetchError
from app.core.logging import logger

router = APIRouter()


def get_persona_service() -> PersonaService:
    """Provide PersonaService instance."""
    return PersonaService()


def get_url_fetcher() -> URLFetcher:
    """Provide URLFetcher instance."""
    return URLFetcher()


@router.post("/v1/persona", response_model=PersonaCreateResponse, status_code=201)
async def create_persona(
    request: CreatePersonaRequest,
    service: PersonaService = Depends(get_persona_service),
    url_fetcher: URLFetcher = Depends(get_url_fetcher)
) -> PersonaCreateResponse:
    """
    Create a new persona from raw text and/or URLs.

    This endpoint supports flexible input sources:

    **Option 1: Raw Text**
    Provide raw_text field with direct text content about the persona.

    **Option 2: URLs**
    Provide urls field with 1-10 URLs containing persona information.
    Content from all URLs will be fetched and extracted.

    **Option 3: Combined**
    Provide both raw_text and urls. Content will be combined.

    Args:
        request: CreatePersonaRequest with either raw_text or urls (or both)
        service: PersonaService instance (injected)
        url_fetcher: URLFetcher instance (injected)

    Returns:
        PersonaCreateResponse with id, created_at, updated_at

    Raises:
        HTTPException: If URL content cannot be fetched (400)
    """
    input_text = request.raw_text or ""

    # Fetch content from URLs if provided
    if request.urls:
        try:
            logger.info(f"Fetching content from {len(request.urls)} URL(s)")
            url_content = await url_fetcher.fetch_multiple(
                [str(url) for url in request.urls]
            )
            # Combine with raw_text if provided
            if input_text:
                input_text = f"{input_text}\n\n---\n\n{url_content}"
            else:
                input_text = url_content
            logger.info(f"Combined input text: {len(input_text)} characters")

        except URLFetchError as e:
            logger.error(f"URL fetch failed: {str(e)}")
            raise HTTPException(
                status_code=400,
                detail=f"Failed to fetch content from provided URLs: {str(e)}"
            )

    # Create persona with combined input
    persona = await service.create_persona(input_text)

    return PersonaCreateResponse(
        id=persona.id,
        created_at=persona.created_at,
        updated_at=persona.updated_at
    )
```

## Commit Message

```
feat(api): add URL support to POST /v1/persona endpoint

Update endpoint to accept optional urls parameter (1-10 URLs) alongside raw_text.
Fetches and extracts content from URLs, combines with raw_text if provided.
Handles URL fetch errors gracefully with meaningful error messages.
```

---

**Completion Time:** ~20 minutes
**Dependencies:** CreatePersonaRequest and URLFetcher must be created first (TASK-08-03-01 and TASK-08-03-02)

