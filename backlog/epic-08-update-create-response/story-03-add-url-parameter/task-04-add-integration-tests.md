# TASK-08-03-04: Add Integration Tests for URL Input Flow

**Story:** US-08-03

**Estimated Time:** 25 minutes

**Description:** Create integration tests to verify the POST /v1/persona endpoint correctly handles URL inputs, error cases, and content combination.

## Agent Prompt

You are implementing **EPIC-08: Enhance POST /persona Endpoint with URL Support and Optimized Response**.

**Goal:** Write comprehensive integration tests for URL input functionality.

**Context:** We need to test that the endpoint:
- Accepts URLs and fetches content correctly
- Validates inputs (requires at least raw_text or urls)
- Handles URL fetch errors gracefully
- Combines content from multiple URLs and raw_text
- Returns correct response format

**Instructions:**

1. Update test file: `tests/test_api/test_personas.py` (or create if needed)

2. Add tests covering:
   - URL input only (single URL)
   - URL input only (multiple URLs)
   - raw_text only (existing behavior)
   - Combined raw_text and URLs
   - Neither raw_text nor URLs (validation error)
   - Invalid URL format
   - URL fetch timeout error
   - URL returns 404
   - URL content oversized

3. Test cases should mock URLFetcher for reliability:
   ```python
   @pytest.fixture
   def mock_url_fetcher(monkeypatch):
       async def mock_fetch(urls):
           return "Content from URL"
       # Patch URLFetcher
   ```

4. Mock external HTTP calls (don't make real requests in tests)

5. Verify response format (id, created_at, updated_at only)

## Verification Steps

1. Run tests: `pytest tests/test_api/test_personas.py -v -k url`
2. All tests should pass
3. Code coverage for URL handling should be > 85%
4. Test both success and error scenarios

## Expected Output

Test file with:
- 8+ test cases covering URL scenarios
- Mock URL fetching for reliability
- Error case testing
- All tests passing
- Clear test names

## Code Example

```python
import pytest
from datetime import datetime
from unittest.mock import AsyncMock, patch
from httpx import AsyncClient
from app.main import app
from app.services.url_fetcher import URLFetchError, URLTimeoutError


@pytest.fixture
def mock_url_fetcher():
    """Mock URLFetcher for testing."""
    with patch('app.api.routes.URLFetcher') as mock:
        instance = AsyncMock()
        mock.return_value = instance
        yield instance


@pytest.mark.asyncio
async def test_create_persona_with_urls_only(mock_url_fetcher):
    """Test creating persona with URLs only."""
    mock_url_fetcher.fetch_multiple.return_value = "Persona info from URL"

    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/v1/persona",
            json={
                "urls": ["https://example.com/bio"]
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert "id" in data
        assert "created_at" in data
        assert "updated_at" in data
        assert len(data) == 3  # Only 3 fields


@pytest.mark.asyncio
async def test_create_persona_with_multiple_urls(mock_url_fetcher):
    """Test creating persona with multiple URLs."""
    mock_url_fetcher.fetch_multiple.return_value = "Combined content from URLs"

    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/v1/persona",
            json={
                "urls": [
                    "https://example.com/bio",
                    "https://example.com/resume"
                ]
            }
        )
        assert response.status_code == 201
        # Verify fetch_multiple was called with both URLs
        mock_url_fetcher.fetch_multiple.assert_called_once()


@pytest.mark.asyncio
async def test_create_persona_with_raw_text_and_urls(mock_url_fetcher):
    """Test creating persona with both raw_text and URLs."""
    mock_url_fetcher.fetch_multiple.return_value = "Content from URL"

    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/v1/persona",
            json={
                "raw_text": "Direct persona text",
                "urls": ["https://example.com/bio"]
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert len(data) == 3


@pytest.mark.asyncio
async def test_create_persona_without_raw_text_or_urls():
    """Test validation error when neither raw_text nor URLs provided."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/v1/persona",
            json={}
        )
        assert response.status_code == 422  # Validation error


@pytest.mark.asyncio
async def test_create_persona_with_invalid_url_format():
    """Test validation error with invalid URL format."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/v1/persona",
            json={
                "urls": ["not a valid url"]
            }
        )
        assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_persona_url_fetch_timeout(mock_url_fetcher):
    """Test error handling when URL fetch times out."""
    mock_url_fetcher.fetch_multiple.side_effect = URLTimeoutError(
        "Request timed out"
    )

    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/v1/persona",
            json={
                "urls": ["https://example.com/bio"]
            }
        )
        assert response.status_code == 400
        data = response.json()
        assert "Failed to fetch" in data["detail"]


@pytest.mark.asyncio
async def test_create_persona_url_too_many():
    """Test validation error when more than 10 URLs provided."""
    urls = [f"https://example.com/page{i}" for i in range(11)]
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/v1/persona",
            json={"urls": urls}
        )
        assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_persona_empty_urls_list():
    """Test validation error when empty URLs list provided."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/v1/persona",
            json={"urls": []}
        )
        assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_persona_raw_text_only_still_works():
    """Test that original raw_text only behavior still works."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/v1/persona",
            json={
                "raw_text": "Sample persona information"
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert len(data) == 3
```

## Commit Message

```
test(api): add integration tests for URL input flow

Add comprehensive integration tests for POST /v1/persona endpoint URL support:
- Test single and multiple URL inputs
- Test combined raw_text and URLs
- Test validation for invalid inputs
- Test URL fetch error handling
- Mock external HTTP calls for reliability
```

---

**Completion Time:** ~25 minutes
**Dependencies:** Endpoint must be implemented (TASK-08-03-03)

