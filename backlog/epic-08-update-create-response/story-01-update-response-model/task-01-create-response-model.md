# TASK-08-01-01: Create PersonaCreateResponse Model

**Story:** US-08-01

**Estimated Time:** 15 minutes

**Description:** Create a new Pydantic response model for the POST /v1/persona endpoint that includes only essential metadata fields.

## Agent Prompt

You are implementing **EPIC-08: Update POST /persona Response Format**.

**Goal:** Create a Pydantic response model for the POST /v1/persona endpoint that only includes id, created_at, and updated_at fields.

**Context:** The current POST /v1/persona endpoint returns the full persona object including raw_text and persona JSON, which is unnecessary for the 201 response. We need a minimal response model to reduce payload size.

**Instructions:**

1. Open `app/models/persona.py` (or create it if it doesn't exist)

2. Add a new class `PersonaCreateResponse` with the following fields:
   - `id`: str or UUID (match your database schema)
   - `created_at`: datetime
   - `updated_at`: datetime

3. Add proper Pydantic configuration:
   ```python
   class Config:
       from_attributes = True  # For ORM model conversion
   ```

4. Add comprehensive docstring to the model explaining its purpose

5. Ensure proper imports:
   - `from pydantic import BaseModel`
   - `from datetime import datetime`
   - `from uuid import UUID` (if using UUID type)

## Verification Steps

1. Verify the model is properly defined in `app/models/persona.py`
2. Check that all three fields are present and correctly typed
3. Verify the model can be instantiated with valid data:
   ```python
   response = PersonaCreateResponse(
       id="123e4567-e89b-12d3-a456-426614174000",
       created_at=datetime.now(),
       updated_at=datetime.now()
   )
   ```
4. Verify the model rejects invalid data (wrong types)

## Expected Output

A new Pydantic model class that:
- Has exactly 3 fields: id, created_at, updated_at
- Properly validates input data
- Can serialize to JSON with ISO 8601 datetime formatting
- Has clear documentation

## Code Example

```python
from datetime import datetime
from typing import Union
from pydantic import BaseModel
from uuid import UUID

class PersonaCreateResponse(BaseModel):
    """
    Response model for POST /v1/persona endpoint (201 Created).

    Only includes essential metadata about the created persona.
    raw_text and persona JSON are excluded to minimize payload size.

    Fields:
        id: Unique identifier of the created persona
        created_at: ISO 8601 timestamp when the persona was created
        updated_at: ISO 8601 timestamp when the persona was last updated
    """
    id: Union[str, UUID]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
```

## Commit Message

```
feat(models): add PersonaCreateResponse model

Create a minimal response model for POST /v1/persona endpoint that includes only id, created_at, and updated_at fields. This reduces payload size by excluding raw_text and persona JSON data from 201 responses.
```

---

**Completion Time:** ~15 minutes
**Dependencies:** app/models/persona.py must exist or be created

