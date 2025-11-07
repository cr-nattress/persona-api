# TASK-08-03-02: Implement URL Fetching Utility with Error Handling

**Story:** US-08-03

**Estimated Time:** 30 minutes

**Description:** Create a URL fetching utility that downloads and extracts text content from URLs with robust error handling, timeout protection, and content size limits.

## Agent Prompt

You are implementing **EPIC-08: Enhance POST /persona Endpoint with URL Support and Optimized Response**.

**Goal:** Build a URL fetcher utility that safely retrieves and extracts text content from web URLs.

**Context:** The POST /v1/persona endpoint needs to fetch content from user-provided URLs. This requires:
- Safe HTTP requests with timeout protection
- HTML parsing to extract meaningful text
- Error handling for network issues, timeouts, invalid URLs
- Content size limits to prevent abuse
- Combining content from multiple URLs

**Instructions:**

1. Create new file: `app/services/url_fetcher.py`

2. Implement URLFetcher class with the following methods:
   - `fetch_url(url: str) -> str` - Fetch and extract text from single URL
   - `fetch_multiple(urls: List[str]) -> str` - Fetch from multiple URLs and combine
   - Error handling for: timeouts, 404s, malformed URLs, oversized content

3. Key Requirements:
   - Use httpx for async HTTP requests
   - Timeout: 10 seconds per URL
   - Max content size: 1MB per URL
   - HTML parsing: use BeautifulSoup or similar to extract text
   - Combine multiple URLs with separator
   - Log errors appropriately

4. Example Implementation Structure:
   ```python
   import httpx
   from typing import List
   from bs4 import BeautifulSoup
   from app.core.logging import logger

   class URLFetcher:
       """Utility for fetching and extracting text from URLs."""

       MAX_CONTENT_SIZE = 1024 * 1024  # 1MB
       TIMEOUT = 10.0  # seconds

       async def fetch_url(self, url: str) -> str:
           """Fetch content from URL and extract text."""
           pass

       async def fetch_multiple(self, urls: List[str]) -> str:
           """Fetch from multiple URLs and combine content."""
           pass
   ```

5. Handle these error cases:
   - Network timeouts: Raise URLTimeoutError with helpful message
   - Invalid URLs: Raise InvalidURLError
   - HTTP errors (404, 500): Raise HTTPError with status code
   - Oversized content: Raise ContentSizeExceededError
   - HTML parsing failures: Log warning, return extracted text or empty string

6. Add logging for:
   - Successful URL fetches
   - Warnings for errors
   - Content size information

## Verification Steps

1. Verify file created: `app/services/url_fetcher.py`
2. Test with valid URLs (fast response expected)
3. Test error scenarios:
   - Invalid URL format
   - Non-existent URL (404)
   - Timeout (use slow endpoint or mock)
   - Oversized content (mock)
4. Test HTML parsing extracts readable text

## Expected Output

URLFetcher utility that:
- Safely fetches content from URLs with timeout protection
- Extracts text from HTML content
- Handles errors gracefully with meaningful messages
- Respects content size limits
- Combines content from multiple URLs
- Includes comprehensive error handling

## Code Example

```python
"""
URL fetching utility for retrieving persona information from web sources.

Provides safe, timeout-protected HTTP requests with HTML text extraction.
"""

import httpx
from typing import List
from bs4 import BeautifulSoup
from pydantic import HttpUrl
from app.core.logging import logger


class URLFetchError(Exception):
    """Base exception for URL fetching errors."""
    pass


class URLTimeoutError(URLFetchError):
    """Raised when URL fetch times out."""
    pass


class InvalidURLError(URLFetchError):
    """Raised when URL format is invalid."""
    pass


class HTTPError(URLFetchError):
    """Raised when HTTP request fails."""
    pass


class ContentSizeExceededError(URLFetchError):
    """Raised when content exceeds size limit."""
    pass


class URLFetcher:
    """
    Utility for safely fetching and extracting text from URLs.

    Features:
    - Timeout protection (10s per URL)
    - Content size limits (1MB per URL)
    - HTML to text extraction
    - Error handling for network issues
    """

    MAX_CONTENT_SIZE = 1024 * 1024  # 1MB
    TIMEOUT = 10.0  # seconds
    USER_AGENT = "PersonaAPI/1.0"

    async def fetch_url(self, url: str) -> str:
        """
        Fetch content from a single URL and extract text.

        Args:
            url: URL to fetch

        Returns:
            Extracted text content from the URL

        Raises:
            URLTimeoutError: If request times out
            InvalidURLError: If URL format is invalid
            HTTPError: If HTTP request fails
            ContentSizeExceededError: If content exceeds size limit
        """
        try:
            async with httpx.AsyncClient(timeout=self.TIMEOUT) as client:
                response = await client.get(
                    url,
                    headers={"User-Agent": self.USER_AGENT},
                    follow_redirects=True
                )
                response.raise_for_status()

                # Check content size
                content_length = len(response.content)
                if content_length > self.MAX_CONTENT_SIZE:
                    raise ContentSizeExceededError(
                        f"Content size {content_length} exceeds limit {self.MAX_CONTENT_SIZE}"
                    )

                # Extract text from HTML
                text = self._extract_text(response.text)
                logger.info(f"Successfully fetched {len(text)} chars from {url}")
                return text

        except httpx.TimeoutException as e:
            logger.warning(f"Timeout fetching {url}")
            raise URLTimeoutError(f"Request to {url} timed out after {self.TIMEOUT}s") from e
        except httpx.InvalidURL as e:
            logger.warning(f"Invalid URL: {url}")
            raise InvalidURLError(f"Invalid URL format: {url}") from e
        except httpx.HTTPStatusError as e:
            logger.warning(f"HTTP {e.response.status_code} error for {url}")
            raise HTTPError(f"HTTP {e.response.status_code} from {url}") from e

    async def fetch_multiple(self, urls: List[str]) -> str:
        """
        Fetch from multiple URLs and combine content.

        Args:
            urls: List of URLs to fetch

        Returns:
            Combined text from all successful fetches

        Raises:
            URLFetchError: If all URLs fail (aggregate error)
        """
        contents = []
        errors = []

        for url in urls:
            try:
                content = await self.fetch_url(url)
                contents.append(content)
            except URLFetchError as e:
                logger.warning(f"Failed to fetch {url}: {str(e)}")
                errors.append((url, str(e)))

        if not contents:
            raise URLFetchError(
                f"Failed to fetch from all {len(urls)} URLs: {errors}"
            )

        # Combine with separator
        return "\n\n---\n\n".join(contents)

    def _extract_text(self, html: str) -> str:
        """
        Extract readable text from HTML content.

        Args:
            html: HTML content

        Returns:
            Extracted text
        """
        try:
            soup = BeautifulSoup(html, 'html.parser')

            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()

            # Extract text
            text = soup.get_text(separator='\n', strip=True)
            return text
        except Exception as e:
            logger.warning(f"Error parsing HTML: {str(e)}")
            return ""
```

## Commit Message

```
feat(services): implement URLFetcher utility for content extraction

Create URLFetcher class for safely fetching and extracting text from URLs with:
- 10-second timeout protection per URL
- 1MB content size limit
- HTML to text extraction using BeautifulSoup
- Comprehensive error handling for network issues
- Support for multiple URLs with combined output
```

---

**Completion Time:** ~30 minutes
**Dependencies:** httpx, BeautifulSoup4 libraries must be in requirements.txt

