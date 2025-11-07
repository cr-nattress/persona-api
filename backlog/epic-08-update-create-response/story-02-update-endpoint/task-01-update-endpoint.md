# TASK-08-02-01: Update POST /v1/persona Endpoint Response Model

**Story:** US-08-02

**Estimated Time:** 10 minutes

**Description:** Update the POST /v1/persona endpoint to use PersonaCreateResponse as the response model instead of the full Persona response model.

## Agent Prompt

You are implementing **EPIC-08: Update POST /persona Response Format**.

**Goal:** Update the POST /v1/persona endpoint to return PersonaCreateResponse (id, created_at, updated_at only) in the 201 response.

**Context:** The endpoint currently returns the full persona object including raw_text and persona JSON. We need to modify it to return only essential metadata.

**Instructions:**

1. Locate the POST /v1/persona endpoint (typically in `app/api/routes.py` or similar)

2. Import PersonaCreateResponse at the top of the file:
   ```python
   from app.models.persona import PersonaCreateResponse
   ```

3. Update the endpoint decorator:
   - Change `response_model=PersonaResponse` to `response_model=PersonaCreateResponse`
   - Keep `status_code=201` for successful persona creation

4. Update the endpoint implementation to return only the necessary fields:
   ```python
   @router.post("/v1/persona", response_model=PersonaCreateResponse, status_code=201)
   async def create_persona(request: CreatePersonaRequest):
       # Existing logic to create persona...
       persona = await persona_service.create_persona(request.raw_text)

       # Return only id, created_at, updated_at
       return PersonaCreateResponse(
           id=persona.id,
           created_at=persona.created_at,
           updated_at=persona.updated_at
       )
   ```

5. Ensure no other modifications to business logic

## Verification Steps

1. Check the endpoint signature:
   ```bash
   grep -n "response_model=PersonaCreateResponse" app/api/routes.py
   ```

2. Verify the endpoint returns PersonaCreateResponse object

3. Run the endpoint locally and confirm the 201 response contains only:
   - id
   - created_at
   - updated_at

4. Verify raw_text and persona fields are NOT in response

## Expected Output

Updated POST /v1/persona endpoint that:
- Uses PersonaCreateResponse as response_model
- Returns 201 status code
- Includes only id, created_at, updated_at in response body
- No raw_text or persona JSON fields present

## Code Example

```python
from fastapi import APIRouter
from app.models.persona import CreatePersonaRequest, PersonaCreateResponse
from app.services.persona_service import PersonaService

router = APIRouter()

@router.post("/v1/persona", response_model=PersonaCreateResponse, status_code=201)
async def create_persona(
    request: CreatePersonaRequest,
    service: PersonaService = Depends(get_persona_service)
):
    """
    Create a new persona from raw text.

    Returns:
        PersonaCreateResponse with id, created_at, updated_at
    """
    persona = await service.create_persona(request.raw_text)

    return PersonaCreateResponse(
        id=persona.id,
        created_at=persona.created_at,
        updated_at=persona.updated_at
    )
```

## Commit Message

```
feat(api): update POST /v1/persona response to use PersonaCreateResponse

Change the POST /v1/persona endpoint to return PersonaCreateResponse containing only id, created_at, and updated_at in the 201 response. This reduces payload size by excluding raw_text and persona JSON data.
```

---

**Completion Time:** ~10 minutes
**Dependencies:** PersonaCreateResponse model must exist (TASK-08-01-01)

