# TASK-08-01-02: Add Tests for PersonaCreateResponse Model

**Story:** US-08-01

**Estimated Time:** 15 minutes

**Description:** Create unit tests to verify the PersonaCreateResponse model works correctly with valid and invalid data.

## Agent Prompt

You are implementing **EPIC-08: Update POST /persona Response Format**.

**Goal:** Write unit tests to validate the PersonaCreateResponse model behavior.

**Context:** We need to ensure the PersonaCreateResponse model properly validates data, serializes to JSON, and rejects invalid inputs before it's used in the endpoint.

**Instructions:**

1. Create a test file: `tests/test_models/test_persona_models.py` (create test_models directory if needed)

2. Add tests for PersonaCreateResponse covering:
   - Valid instantiation with all required fields
   - JSON serialization (to verify datetime formatting)
   - Validation error when missing required fields
   - Validation error when fields have wrong types
   - Validation error when None is passed for required fields

3. Test Cases to Implement:
   ```python
   def test_persona_create_response_valid():
       # Test valid data
       pass

   def test_persona_create_response_serialization():
       # Test JSON serialization with datetime
       pass

   def test_persona_create_response_missing_id():
       # Test validation when id is missing
       pass

   def test_persona_create_response_invalid_type():
       # Test validation when field has wrong type
       pass
   ```

4. Use pytest as the testing framework
5. Ensure tests are descriptive with clear assertions

## Verification Steps

1. Run tests: `pytest tests/test_models/test_persona_models.py -v`
2. All tests should pass
3. Verify datetime fields serialize to ISO 8601 format
4. Verify validation errors are raised for invalid data

## Expected Output

Test file with:
- 5+ test cases covering happy path and error cases
- All tests passing
- Clear test names indicating what is being tested
- Assertions that verify expected behavior

## Code Example

```python
import pytest
from datetime import datetime
from uuid import UUID
from pydantic import ValidationError
from app.models.persona import PersonaCreateResponse


def test_persona_create_response_valid():
    """Test PersonaCreateResponse with valid data."""
    response = PersonaCreateResponse(
        id="123e4567-e89b-12d3-a456-426614174000",
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    assert response.id == "123e4567-e89b-12d3-a456-426614174000"
    assert isinstance(response.created_at, datetime)
    assert isinstance(response.updated_at, datetime)


def test_persona_create_response_serialization():
    """Test JSON serialization with proper datetime formatting."""
    now = datetime.fromisoformat("2024-01-15T10:30:00")
    response = PersonaCreateResponse(
        id="test-id",
        created_at=now,
        updated_at=now
    )
    json_data = response.model_dump_json()
    assert "2024-01-15T10:30:00" in json_data


def test_persona_create_response_missing_id():
    """Test validation error when id is missing."""
    with pytest.raises(ValidationError):
        PersonaCreateResponse(
            created_at=datetime.now(),
            updated_at=datetime.now()
        )


def test_persona_create_response_invalid_created_at():
    """Test validation error when created_at has wrong type."""
    with pytest.raises(ValidationError):
        PersonaCreateResponse(
            id="test-id",
            created_at="not-a-datetime",
            updated_at=datetime.now()
        )


def test_persona_create_response_none_values():
    """Test validation error when required fields are None."""
    with pytest.raises(ValidationError):
        PersonaCreateResponse(
            id=None,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
```

## Commit Message

```
test(models): add tests for PersonaCreateResponse model

Add comprehensive unit tests for PersonaCreateResponse model covering valid instantiation, JSON serialization, and validation of invalid inputs. Tests verify proper datetime formatting and type checking.
```

---

**Completion Time:** ~15 minutes
**Dependencies:** PersonaCreateResponse model must be created first (TASK-08-01-01)

