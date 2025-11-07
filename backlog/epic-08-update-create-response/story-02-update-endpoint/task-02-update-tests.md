# TASK-08-02-02: Update Integration Tests for New Response Format

**Story:** US-08-02

**Estimated Time:** 15 minutes

**Description:** Update integration tests to verify the POST /v1/persona endpoint returns only id, created_at, and updated_at in the 201 response.

## Agent Prompt

You are implementing **EPIC-08: Update POST /persona Response Format**.

**Goal:** Update integration tests for the POST /v1/persona endpoint to verify the new PersonaCreateResponse format.

**Context:** With the endpoint now returning PersonaCreateResponse, we need to update our tests to verify:
- The response has only id, created_at, updated_at
- raw_text and persona are NOT present
- The response status is 201

**Instructions:**

1. Locate existing integration tests for POST /v1/persona (likely in `tests/test_api/test_personas.py` or similar)

2. Update or create test cases:
   - Test successful persona creation returns 201
   - Test response contains only id, created_at, updated_at
   - Test response does NOT contain raw_text
   - Test response does NOT contain persona JSON

3. Example Test Structure:
   ```python
   async def test_create_persona_returns_201_with_minimal_response():
       response = await client.post("/v1/persona", json={...})
       assert response.status_code == 201
       data = response.json()

       # Check required fields exist
       assert "id" in data
       assert "created_at" in data
       assert "updated_at" in data

       # Check prohibited fields don't exist
       assert "raw_text" not in data
       assert "persona" not in data
   ```

4. Ensure all existing create persona tests are updated to match new response format

5. Add test for response model validation (schema)

## Verification Steps

1. Run integration tests:
   ```bash
   pytest tests/test_api/test_personas.py::test_create_persona -v
   ```

2. All tests should pass

3. Verify test assertions confirm response has only 3 fields

4. Check test coverage for the endpoint

## Expected Output

Updated test file with:
- Test for successful 201 response
- Test verifying only id, created_at, updated_at are present
- Test verifying raw_text is NOT present
- Test verifying persona is NOT present
- All tests passing

## Code Example

```python
import pytest
from datetime import datetime
from httpx import AsyncClient
from app.main import app


@pytest.mark.asyncio
async def test_create_persona_returns_201_with_minimal_response():
    """Test that POST /v1/persona returns 201 with only id, created_at, updated_at."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/v1/persona",
            json={"raw_text": "Sample persona text"}
        )
        assert response.status_code == 201

        data = response.json()

        # Verify required fields
        assert "id" in data
        assert "created_at" in data
        assert "updated_at" in data

        # Verify prohibited fields
        assert "raw_text" not in data
        assert "persona" not in data

        # Verify field types
        assert isinstance(data["id"], str)
        assert isinstance(data["created_at"], str)  # ISO format datetime
        assert isinstance(data["updated_at"], str)


@pytest.mark.asyncio
async def test_create_persona_response_has_only_three_fields():
    """Test that response contains exactly 3 fields."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/v1/persona",
            json={"raw_text": "Sample persona text"}
        )
        data = response.json()
        assert len(data) == 3
        assert set(data.keys()) == {"id", "created_at", "updated_at"}


@pytest.mark.asyncio
async def test_create_persona_datetime_format():
    """Test that datetime fields are in ISO 8601 format."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/v1/persona",
            json={"raw_text": "Sample persona text"}
        )
        data = response.json()

        # Should be parseable as ISO 8601
        created_at = datetime.fromisoformat(data["created_at"].replace("Z", "+00:00"))
        updated_at = datetime.fromisoformat(data["updated_at"].replace("Z", "+00:00"))
        assert isinstance(created_at, datetime)
        assert isinstance(updated_at, datetime)
```

## Commit Message

```
test(api): update integration tests for POST /v1/persona response format

Update tests to verify POST /v1/persona returns PersonaCreateResponse with only id, created_at, and updated_at fields. Add assertions to ensure raw_text and persona fields are not present in 201 responses.
```

---

**Completion Time:** ~15 minutes
**Dependencies:** Endpoint must be updated first (TASK-08-02-01)

