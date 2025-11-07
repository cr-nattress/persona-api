# TASK-08-03-05: Verify Swagger Documentation for Updated Request Model

**Story:** US-08-03

**Estimated Time:** 15 minutes

**Description:** Verify that Swagger/OpenAPI documentation correctly displays the updated POST /v1/persona request model with both raw_text and URLs parameters.

## Agent Prompt

You are implementing **EPIC-08: Enhance POST /persona Endpoint with URL Support and Optimized Response**.

**Goal:** Verify Swagger documentation accurately reflects the new URL parameter support.

**Context:** FastAPI automatically generates Swagger docs from Pydantic models. We need to ensure:
- Request schema shows both raw_text and urls parameters
- urls parameter shows it accepts 1-10 URLs
- Documentation includes field descriptions
- Examples show different input methods (raw_text, urls, both)
- Response schema shows PersonaCreateResponse (3 fields only)

**Instructions:**

1. Start the application locally:
   ```bash
   python -m uvicorn app.main:app --reload
   ```

2. Navigate to Swagger UI:
   - URL: `http://localhost:8000/docs` (or your configured path)

3. Find the POST /v1/persona endpoint

4. Verify the request body schema includes:
   - **raw_text** field (optional, string, max 50000 chars)
   - **urls** field (optional, array of strings/URLs, 1-10 items)
   - Clear description that at least one is required

5. Verify field descriptions:
   - raw_text: "Raw text containing persona information"
   - urls: "URLs containing persona information (1-10 URLs)"

6. Check the "Examples" section shows:
   - Example 1: raw_text only
   - Example 2: urls only (single or multiple)
   - Example 3: both raw_text and urls

7. Verify response schema shows:
   - 201 response status
   - Three fields: id, created_at, updated_at
   - No raw_text or persona fields

8. Test the endpoint manually:
   ```json
   {
     "urls": ["https://example.com"]
   }
   ```
   - Should return 201 with id, created_at, updated_at

9. Test with multiple URLs:
   ```json
   {
     "urls": [
       "https://example.com/page1",
       "https://example.com/page2"
     ]
   }
   ```

10. Test error case (invalid input):
    ```json
    {}
    ```
    - Should return 422 validation error

## Verification Steps

1. Open Swagger UI at `http://localhost:8000/docs`
2. POST /v1/persona endpoint visible
3. Request schema shows both raw_text and urls
4. Field descriptions are clear and helpful
5. Examples section demonstrates all input methods
6. Response schema shows PersonaCreateResponse (3 fields)
7. Manual test with urls returns 201
8. Manual test without inputs returns 422

## Expected Output

Swagger documentation correctly showing:
- Updated CreatePersonaRequest with raw_text and urls
- Clear descriptions for both parameters
- Min/max constraints (1-10 URLs)
- Examples for all input methods
- PersonaCreateResponse schema (3 fields)
- 201 and 400/422 response status codes

## Documentation Checklist

- [ ] raw_text field visible and documented
- [ ] urls field visible with 1-10 constraint
- [ ] Description states "at least one required"
- [ ] Example 1: raw_text only
- [ ] Example 2: urls only
- [ ] Example 3: both parameters
- [ ] 201 response shows id, created_at, updated_at
- [ ] 400 response shown for URL fetch errors
- [ ] 422 response shown for validation errors
- [ ] Field types are correct (string, array, datetime)

## Code Quality Checks

If documentation is incomplete, verify:

1. CreatePersonaRequest has proper field descriptions:
   ```python
   raw_text: Optional[str] = Field(
       None,
       description="Raw text containing persona information"
   )
   urls: Optional[List[HttpUrl]] = Field(
       None,
       description="URLs containing persona information (1-10 URLs)"
   )
   ```

2. Config includes examples:
   ```python
   class Config:
       json_schema_extra = {
           "examples": [
               {"raw_text": "..."},
               {"urls": ["https://..."]},
               {"raw_text": "...", "urls": ["https://..."]}
           ]
       }
   ```

3. Endpoint has proper docstring:
   ```python
   @router.post("/v1/persona", ...)
   async def create_persona(...):
       """
       Create a new persona from raw text and/or URLs.

       This endpoint supports flexible input sources:
       - raw_text: Direct text input
       - urls: 1-10 URLs containing persona information
       """
   ```

## Commit Message

```
docs(api): verify Swagger documentation for URL parameter support

Confirm Swagger/OpenAPI documentation correctly displays POST /v1/persona with:
- Updated CreatePersonaRequest schema (raw_text + urls)
- Clear field descriptions and constraints
- Examples for raw_text, urls, and combined inputs
- PersonaCreateResponse response schema (3 fields)
```

---

**Completion Time:** ~15 minutes
**Dependencies:** Endpoint and request model must be implemented (TASK-08-03-01 and TASK-08-03-03)

