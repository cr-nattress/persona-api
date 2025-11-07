# US-08-03: Add URL Parameter Support to POST /v1/persona Endpoint

**Epic:** EPIC-08: Enhance POST /persona Endpoint with URL Support and Optimized Response

**User Story:** As an API consumer, I want to create a persona by providing URLs that contain persona information, so that I can leverage existing web content and documentation to generate personas without manually extracting text.

**Story Points:** 8

**Priority:** 🟡 Medium (Feature Enhancement)

## Acceptance Criteria
- [ ] CreatePersonaRequest model enhanced with optional `urls` parameter (array of strings)
- [ ] `urls` parameter accepts 1 to N URLs
- [ ] Validation ensures either `raw_text` OR `urls` is provided (at least one required)
- [ ] URL content fetching utility implemented with error handling
- [ ] URL fetching respects timeout limits (5-10 seconds)
- [ ] URL fetching validates content size (set reasonable limits)
- [ ] POST /v1/persona endpoint accepts both input methods
- [ ] Endpoint merges content from multiple URLs when provided
- [ ] Integration tests verify URL input flow
- [ ] Swagger documentation shows both request patterns

## Definition of Done
- [ ] Code complete (request model, URL fetcher, endpoint update)
- [ ] URL error handling tested (timeouts, 404s, malformed URLs, oversized content)
- [ ] Integration tests passing for URL inputs
- [ ] Swagger documentation verified
- [ ] Code reviewed and approved by team

## Technical Notes

**Request Model Enhancement:**
```python
class CreatePersonaRequest(BaseModel):
    """Request model for creating a persona with flexible input sources."""
    raw_text: Optional[str] = None  # Existing field
    urls: Optional[List[HttpUrl]] = Field(None, max_items=10)  # New field: 1-10 URLs

    @validator('raw_text', 'urls', pre=True, always=True)
    def at_least_one_input(cls, v, values):
        """Ensure at least raw_text or urls is provided."""
        if not values.get('raw_text') and not v:
            raise ValueError('Either raw_text or urls must be provided')
        return v
```

**URL Fetcher Utility Location:** `app/services/url_fetcher.py`

**Key Requirements:**
- Fetch HTML content from URLs
- Extract text content (handle HTML parsing)
- Handle common errors gracefully
- Implement timeout protection (5-10 seconds per URL)
- Limit response size (e.g., max 1MB per URL)
- Combine content from multiple URLs into consolidated text

**Integration with Endpoint:**
```python
if request.urls:
    combined_text = await url_fetcher.fetch_and_extract(request.urls)
    input_text = combined_text + (request.raw_text or "")
else:
    input_text = request.raw_text
```

## Tasks
- TASK-08-03-01: Update CreatePersonaRequest model with URLs parameter
- TASK-08-03-02: Implement URL fetching utility with error handling
- TASK-08-03-03: Update POST endpoint to handle URL inputs
- TASK-08-03-04: Add integration tests for URL input flow
- TASK-08-03-05: Verify Swagger documentation for updated request model

---

**Estimated Story Points:** 8
**Priority:** Medium
**Target Sprint:** Sprint N+2

