"""
URL fetching utility for retrieving persona information from web sources.

Provides safe, timeout-protected HTTP requests with HTML text extraction.
Handles error cases gracefully and respects size limits to prevent abuse.
"""

import httpx
from typing import List
from bs4 import BeautifulSoup
from pydantic import HttpUrl
from app.core.logging import get_logger

logger = get_logger(__name__)


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
    - HTML to text extraction using BeautifulSoup
    - Error handling for network issues and invalid URLs
    - Support for multiple URLs with combined output
    """

    MAX_CONTENT_SIZE = 1024 * 1024  # 1MB
    TIMEOUT = 10.0  # seconds
    USER_AGENT = "PersonaAPI/1.0 (+https://github.com/persona-api)"

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

                # Check content size before processing
                content_length = len(response.content)
                if content_length > self.MAX_CONTENT_SIZE:
                    logger.warning(
                        f"Content from {url} exceeds size limit: "
                        f"{content_length} > {self.MAX_CONTENT_SIZE}"
                    )
                    raise ContentSizeExceededError(
                        f"Content size {content_length} exceeds limit {self.MAX_CONTENT_SIZE}"
                    )

                # Extract text from HTML
                text = self._extract_text(response.text)
                logger.info(f"Successfully fetched {len(text)} chars from {url}")
                return text

        except httpx.TimeoutException as e:
            logger.warning(f"Timeout fetching {url} after {self.TIMEOUT}s")
            raise URLTimeoutError(
                f"Request to {url} timed out after {self.TIMEOUT}s"
            ) from e
        except httpx.InvalidURL as e:
            logger.warning(f"Invalid URL format: {url}")
            raise InvalidURLError(f"Invalid URL format: {url}") from e
        except httpx.HTTPStatusError as e:
            logger.warning(f"HTTP {e.response.status_code} error for {url}")
            raise HTTPError(f"HTTP {e.response.status_code} from {url}") from e
        except httpx.RequestError as e:
            logger.warning(f"Request error for {url}: {str(e)}")
            raise URLFetchError(f"Failed to fetch {url}: {str(e)}") from e

    async def fetch_multiple(self, urls: List[str]) -> str:
        """
        Fetch from multiple URLs and combine content.

        Args:
            urls: List of URLs to fetch

        Returns:
            Combined text from all successful fetches

        Raises:
            URLFetchError: If all URLs fail to fetch
        """
        contents = []
        errors = []

        for url in urls:
            try:
                content = await self.fetch_url(url)
                if content.strip():  # Only add non-empty content
                    contents.append(content)
            except URLFetchError as e:
                logger.warning(f"Failed to fetch {url}: {str(e)}")
                errors.append((url, str(e)))

        if not contents:
            error_details = "; ".join([f"{url}: {error}" for url, error in errors])
            raise URLFetchError(
                f"Failed to fetch content from all {len(urls)} URLs: {error_details}"
            )

        # Combine with separator for clarity
        logger.info(f"Successfully fetched from {len(contents)}/{len(urls)} URLs")
        return "\n\n---\n\n".join(contents)

    @staticmethod
    def _extract_text(html: str) -> str:
        """
        Extract readable text from HTML content.

        Removes script and style elements, then extracts text with
        proper line breaks and stripping of excess whitespace.

        Args:
            html: HTML content

        Returns:
            Extracted text with formatting preserved
        """
        try:
            soup = BeautifulSoup(html, 'html.parser')

            # Remove script and style elements (they will not be displayed)
            for script in soup(["script", "style"]):
                script.decompose()

            # Get text with newline separator for paragraphs
            text = soup.get_text(separator='\n', strip=True)

            # Clean up excessive whitespace while preserving paragraphs
            lines = [line.strip() for line in text.split('\n')]
            text = '\n'.join(line for line in lines if line)

            return text
        except Exception as e:
            logger.warning(f"Error parsing HTML: {str(e)}")
            # Return empty string if parsing fails
            return ""
