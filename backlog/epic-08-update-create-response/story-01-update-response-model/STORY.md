# US-08-01: Create PersonaCreateResponse Model

**Epic:** EPIC-08: Update POST /persona Response Format

**User Story:** As an API consumer, I want the POST /v1/persona endpoint to return only essential metadata (id, created_at, updated_at) in the 201 response, so that I receive a minimal payload without unnecessary raw_text and persona JSON data.

**Story Points:** 3

**Priority:** 🟡 Medium (Enhancement)

## Acceptance Criteria
- [ ] PersonaCreateResponse Pydantic model created in models/persona.py
- [ ] Model contains only: id (UUID/str), created_at (datetime), updated_at (datetime) fields
- [ ] Model includes proper field documentation/descriptions
- [ ] Model has correct validation and type hints
- [ ] Model is exportable and importable for use in endpoints
- [ ] Unit tests verify model structure and validation

## Definition of Done
- [ ] Code complete (PersonaCreateResponse model)
- [ ] Model tested with valid and invalid data
- [ ] Documentation added to model docstring
- [ ] Code reviewed and approved by team

## Technical Notes

**Model Location:** `app/models/persona.py`

**Model Definition:**
```python
class PersonaCreateResponse(BaseModel):
    """
    Response model for POST /v1/persona endpoint (201 Created).

    Only includes essential metadata about the created persona.
    raw_text and persona JSON are excluded to minimize payload size.
    """
    id: str  # or UUID depending on your implementation
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # for SQLAlchemy model conversion
```

**Field Descriptions:**
- `id`: Unique identifier of the created persona
- `created_at`: ISO 8601 timestamp when the persona was created
- `updated_at`: ISO 8601 timestamp when the persona was last updated

## Tasks
- TASK-08-01-01: Create PersonaCreateResponse model
- TASK-08-01-02: Add tests for PersonaCreateResponse model

---

**Estimated Story Points:** 3
**Priority:** Medium
**Target Sprint:** Sprint N+1

