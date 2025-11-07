# TASK-08-03-01: Update CreatePersonaRequest Model with URLs Parameter

**Story:** US-08-03

**Estimated Time:** 20 minutes

**Description:** Enhance the CreatePersonaRequest Pydantic model to accept an optional URLs parameter while maintaining validation that at least one input source is provided.

## Agent Prompt

You are implementing **EPIC-08: Enhance POST /persona Endpoint with URL Support and Optimized Response**.

**Goal:** Update the CreatePersonaRequest model to accept URLs as an alternative or supplement to raw_text input.

**Context:** The endpoint currently only accepts raw_text. We need to enhance the request model to accept 1 to N URLs containing persona information, while ensuring that at least one input source (raw_text or urls) is always provided.

**Instructions:**

1. Locate the CreatePersonaRequest model (typically in `app/models/persona.py`)

2. Add the `urls` parameter to the class:
   ```python
   from typing import Optional, List
   from pydantic import Field, HttpUrl, validator

   class CreatePersonaRequest(BaseModel):
       """
       Request model for creating a persona.

       Supports flexible input sources: raw text or URLs containing persona information.
       At least one source (raw_text or urls) must be provided.
       """
       raw_text: Optional[str] = Field(None, min_length=1, max_length=50000)
       urls: Optional[List[HttpUrl]] = Field(
           None,
           min_items=1,
           max_items=10,
           description="1 to 10 URLs containing persona information"
       )
   ```

3. Add validation to ensure at least one input is provided:
   ```python
   @validator('urls', pre=True, always=True)
   def at_least_one_input(cls, v, values):
       """Ensure either raw_text or urls is provided."""
       raw_text = values.get('raw_text')
       if not raw_text and (v is None or len(v) == 0):
           raise ValueError(
               'Either raw_text or urls must be provided'
           )
       return v
   ```

4. Add a docstring with field descriptions explaining the constraints

5. Test the model with:
   - Valid: raw_text only
   - Valid: urls only (single URL)
   - Valid: urls with multiple URLs
   - Valid: both raw_text and urls
   - Invalid: neither raw_text nor urls
   - Invalid: empty urls list
   - Invalid: more than 10 URLs
   - Invalid: invalid URL format

## Verification Steps

1. Verify the model is updated in `app/models/persona.py`
2. Check that both parameters are optional individually
3. Verify validation requires at least one input
4. Test instantiation with different input combinations
5. Verify invalid data raises ValidationError

## Expected Output

Updated CreatePersonaRequest model that:
- Has both `raw_text` (optional) and `urls` (optional) parameters
- Accepts 1-10 URLs in the urls parameter
- Validates at least one input is provided
- Has clear field descriptions
- Includes validation error messages

## Code Example

```python
from typing import Optional, List
from pydantic import BaseModel, Field, HttpUrl, validator

class CreatePersonaRequest(BaseModel):
    """
    Request model for POST /v1/persona endpoint.

    Flexible input source: provide either raw_text, urls, or both.
    At least one source is required.

    Fields:
        raw_text: Direct text input for persona generation (optional)
        urls: 1-10 URLs containing persona information (optional)
    """
    raw_text: Optional[str] = Field(
        None,
        min_length=1,
        max_length=50000,
        description="Raw text containing persona information"
    )
    urls: Optional[List[HttpUrl]] = Field(
        None,
        min_items=1,
        max_items=10,
        description="URLs containing persona information (1-10 URLs)"
    )

    @validator('urls', pre=True, always=True)
    def at_least_one_input(cls, v, values):
        """Ensure at least one input source is provided."""
        raw_text = values.get('raw_text')
        if not raw_text and (v is None or len(v) == 0):
            raise ValueError(
                'Either raw_text or urls must be provided. '
                'Provide raw text directly or 1-10 URLs containing persona information.'
            )
        return v

    class Config:
        json_schema_extra = {
            "examples": [
                {
                    "raw_text": "John is a software engineer with 10 years of experience..."
                },
                {
                    "urls": ["https://example.com/bio", "https://example.com/resume"]
                },
                {
                    "raw_text": "Additional context here...",
                    "urls": ["https://example.com/profile"]
                }
            ]
        }
```

## Commit Message

```
feat(models): add URLs parameter to CreatePersonaRequest

Enhance CreatePersonaRequest model to accept optional URLs parameter (1-10 URLs) alongside raw_text. Add validation to ensure at least one input source is provided. Supports flexible persona creation from text and/or web sources.
```

---

**Completion Time:** ~20 minutes
**Dependencies:** models/persona.py must exist

