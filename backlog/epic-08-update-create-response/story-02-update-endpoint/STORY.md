# US-08-02: Update POST /v1/persona Endpoint to Use PersonaCreateResponse

**Epic:** EPIC-08: Update POST /persona Response Format

**User Story:** As a developer, I want the POST /v1/persona endpoint to return only id, created_at, and updated_at in the 201 response, so that the API response is minimal and optimized.

**Story Points:** 5

**Priority:** 🟡 Medium (Enhancement)

## Acceptance Criteria
- [ ] POST /v1/persona endpoint response_model updated to PersonaCreateResponse
- [ ] Endpoint returns 201 status with only id, created_at, updated_at
- [ ] raw_text and persona JSON fields are NOT included in response
- [ ] Swagger/OpenAPI documentation reflects new response structure
- [ ] Integration tests updated and passing
- [ ] Manual testing confirms response format is correct

## Definition of Done
- [ ] Code complete (endpoint update)
- [ ] Integration tests updated and passing
- [ ] Swagger documentation verified
- [ ] Code reviewed and approved by team

## Technical Notes

**Endpoint Location:** `app/api/routes.py` or `app/api/v1/personas.py`

**Current Implementation (Example):**
```python
@router.post("/v1/persona", response_model=PersonaResponse, status_code=201)
async def create_persona(request: CreatePersonaRequest):
    # Current returns PersonaResponse with all fields
```

**Updated Implementation:**
```python
@router.post("/v1/persona", response_model=PersonaCreateResponse, status_code=201)
async def create_persona(request: CreatePersonaRequest):
    # Return only id, created_at, updated_at
```

**Response Example:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "created_at": "2024-01-15T10:30:00.000Z",
  "updated_at": "2024-01-15T10:30:00.000Z"
}
```

## Tasks
- TASK-08-02-01: Update POST /v1/persona endpoint to use PersonaCreateResponse
- TASK-08-02-02: Update integration tests for new response format
- TASK-08-02-03: Verify Swagger documentation and test endpoint

---

**Estimated Story Points:** 5
**Priority:** Medium
**Target Sprint:** Sprint N+1

