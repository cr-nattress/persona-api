# EPIC-08: Enhance POST /persona Endpoint with URL Support and Optimized Response

**Business Value:** Enhance the POST /v1/persona endpoint to accept URLs containing persona information, and optimize API response by reducing payload size and returning only essential metadata (id, created_at, updated_at) in the 201 response.

**Current State:** POST /v1/persona endpoint only accepts raw_text input and returns full persona object including raw_text and generated persona JSON in 201 response.

**Target State:** POST /v1/persona endpoint accepts either raw_text OR 1+ URLs as input sources, and returns a minimal response with only id, created_at, and updated_at fields in 201 response.

**Technical Approach:**
- Create a new Pydantic response model for POST /v1/persona (PersonaCreateResponse)
- Enhance CreatePersonaRequest to accept optional URLs (1 to many)
- Update endpoint to handle both raw_text and URL inputs
- Implement URL content fetching logic
- Update endpoint to use the new response model
- Verify response structure in API documentation
- Update integration tests to reflect new response format

## Acceptance Criteria
- [ ] New PersonaCreateResponse model created with only id, created_at, updated_at fields
- [ ] CreatePersonaRequest enhanced with optional urls parameter (accepts 1 to many URLs)
- [ ] URL content fetching utility implemented
- [ ] POST /v1/persona endpoint accepts both raw_text and URLs
- [ ] Endpoint validates that at least one of raw_text or urls is provided
- [ ] Response returns 201 status with minimal payload
- [ ] Swagger/OpenAPI documentation reflects new request and response format
- [ ] Integration tests updated and passing for both input methods
- [ ] raw_text and persona fields are NOT included in 201 response
- [ ] URL fetching handles errors gracefully (timeouts, 404s, malformed URLs)

## User Stories
- US-08-01: Create PersonaCreateResponse model
- US-08-02: Update endpoint and tests
- US-08-03: Add URL parameter support to CreatePersonaRequest and endpoint

## Risks & Mitigations
- **Risk:** Breaking change for existing API consumers
  **Mitigation:** Clearly document the change in release notes and API documentation
- **Risk:** URL fetching could be slow or timeout
  **Mitigation:** Implement reasonable timeout (5-10s), return meaningful error messages
- **Risk:** Malicious URLs or URL content could cause issues
  **Mitigation:** Validate URLs, set content size limits, sanitize before processing

## Success Metrics
- 201 response payload reduced by excluding raw_text and persona JSON
- API response time potentially improved due to smaller payload
- Endpoint supports both raw_text and URL inputs
- URL fetching completes within acceptable time (< 10s)
- All integration tests passing for both input methods
- Swagger documentation correctly reflects the request and response structure

## Estimated Story Points
- US-08-01: 3 points
- US-08-02: 5 points
- US-08-03: 8 points
- **Total: 16 points**

## Dependencies
- Depends on EPIC-04: API Endpoints & Request Handling (must be completed)

## Next Epic
No specific dependencies for other epics

