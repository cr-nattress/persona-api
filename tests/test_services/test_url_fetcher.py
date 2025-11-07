"""Tests for URL fetching utility."""

import pytest
from unittest.mock import AsyncMock, patch, MagicMock
import httpx
from app.services.url_fetcher import (
    URLFetcher,
    URLFetchError,
    URLTimeoutError,
    InvalidURLError,
    HTTPError,
    ContentSizeExceededError,
)


@pytest.mark.asyncio
class TestURLFetcher:
    """Test URLFetcher utility."""

    async def test_fetch_url_success(self):
        """Test successful URL fetch and text extraction."""
        fetcher = URLFetcher()

        html_content = """
        <html>
            <body>
                <h1>John's Bio</h1>
                <p>John is a software engineer with 10 years of experience.</p>
                <p>He loves building scalable systems.</p>
            </body>
        </html>
        """

        with patch("app.services.url_fetcher.httpx.AsyncClient") as mock_client_class:
            mock_response = MagicMock()
            mock_response.text = html_content
            mock_response.content = html_content.encode()
            mock_response.raise_for_status = MagicMock()

            mock_client = AsyncMock()
            mock_client.get = AsyncMock(return_value=mock_response)
            mock_client.__aenter__.return_value = mock_client
            mock_client.__aexit__.return_value = None

            mock_client_class.return_value = mock_client

            result = await fetcher.fetch_url("https://example.com/bio")

            assert "John's Bio" in result
            assert "software engineer" in result
            assert len(result) > 0

    async def test_fetch_url_timeout(self):
        """Test URL fetch timeout handling."""
        fetcher = URLFetcher()

        with patch("app.services.url_fetcher.httpx.AsyncClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client.get = AsyncMock(side_effect=httpx.TimeoutException("timeout"))
            mock_client.__aenter__.return_value = mock_client
            mock_client.__aexit__.return_value = None

            mock_client_class.return_value = mock_client

            with pytest.raises(URLTimeoutError):
                await fetcher.fetch_url("https://example.com/bio")

    async def test_fetch_url_invalid_url(self):
        """Test invalid URL format handling."""
        fetcher = URLFetcher()

        with patch("app.services.url_fetcher.httpx.AsyncClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client.get = AsyncMock(side_effect=httpx.InvalidURL("invalid"))
            mock_client.__aenter__.return_value = mock_client
            mock_client.__aexit__.return_value = None

            mock_client_class.return_value = mock_client

            with pytest.raises(InvalidURLError):
                await fetcher.fetch_url("not a valid url")

    async def test_fetch_url_http_error(self):
        """Test HTTP error handling."""
        fetcher = URLFetcher()

        with patch("app.services.url_fetcher.httpx.AsyncClient") as mock_client_class:
            mock_response = MagicMock()
            mock_response.status_code = 404
            mock_error = httpx.HTTPStatusError("404", request=None, response=mock_response)

            mock_client = AsyncMock()
            mock_client.get = AsyncMock(side_effect=mock_error)
            mock_client.__aenter__.return_value = mock_client
            mock_client.__aexit__.return_value = None

            mock_client_class.return_value = mock_client

            with pytest.raises(HTTPError):
                await fetcher.fetch_url("https://example.com/notfound")

    async def test_fetch_url_content_size_exceeded(self):
        """Test content size limit handling."""
        fetcher = URLFetcher()

        # Create content larger than max size
        large_content = "x" * (fetcher.MAX_CONTENT_SIZE + 1)

        with patch("app.services.url_fetcher.httpx.AsyncClient") as mock_client_class:
            mock_response = MagicMock()
            mock_response.text = large_content
            mock_response.content = large_content.encode()
            mock_response.raise_for_status = MagicMock()

            mock_client = AsyncMock()
            mock_client.get = AsyncMock(return_value=mock_response)
            mock_client.__aenter__.return_value = mock_client
            mock_client.__aexit__.return_value = None

            mock_client_class.return_value = mock_client

            with pytest.raises(ContentSizeExceededError):
                await fetcher.fetch_url("https://example.com/large")

    async def test_fetch_multiple_urls_success(self):
        """Test fetching from multiple URLs."""
        fetcher = URLFetcher()

        urls = [
            "https://example.com/bio",
            "https://example.com/resume",
        ]

        html1 = "<html><body><p>Bio content here</p></body></html>"
        html2 = "<html><body><p>Resume content here</p></body></html>"

        with patch("app.services.url_fetcher.httpx.AsyncClient") as mock_client_class:
            # Create mock responses
            mock_responses = []
            for html in [html1, html2]:
                mock_response = MagicMock()
                mock_response.text = html
                mock_response.content = html.encode()
                mock_response.raise_for_status = MagicMock()
                mock_responses.append(mock_response)

            mock_client = AsyncMock()
            mock_client.get = AsyncMock(side_effect=mock_responses)
            mock_client.__aenter__.return_value = mock_client
            mock_client.__aexit__.return_value = None

            mock_client_class.return_value = mock_client

            result = await fetcher.fetch_multiple(urls)

            assert "Bio content" in result
            assert "Resume content" in result
            assert "---" in result  # Separator between URLs

    async def test_fetch_multiple_urls_partial_failure(self):
        """Test fetching when some URLs fail."""
        fetcher = URLFetcher()

        urls = [
            "https://example.com/bio",
            "https://example.com/notfound",
            "https://example.com/resume",
        ]

        html_success = "<html><body><p>Success content</p></body></html>"

        call_count = 0

        async def mock_get(url, **kwargs):
            nonlocal call_count
            call_count += 1
            if "notfound" in url:
                raise httpx.HTTPStatusError("404", request=None, response=MagicMock(status_code=404))
            mock_response = MagicMock()
            mock_response.text = html_success
            mock_response.content = html_success.encode()
            mock_response.raise_for_status = MagicMock()
            return mock_response

        with patch("app.services.url_fetcher.httpx.AsyncClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client.get = mock_get
            mock_client.__aenter__.return_value = mock_client
            mock_client.__aexit__.return_value = None

            mock_client_class.return_value = mock_client

            # Should succeed even though one URL failed
            result = await fetcher.fetch_multiple(urls)
            assert "Success content" in result

    async def test_fetch_multiple_urls_all_failed(self):
        """Test fetching when all URLs fail."""
        fetcher = URLFetcher()

        urls = [
            "https://example.com/notfound1",
            "https://example.com/notfound2",
        ]

        async def mock_get(url, **kwargs):
            raise httpx.HTTPStatusError("404", request=None, response=MagicMock(status_code=404))

        with patch("app.services.url_fetcher.httpx.AsyncClient") as mock_client_class:
            mock_client = AsyncMock()
            mock_client.get = mock_get
            mock_client.__aenter__.return_value = mock_client
            mock_client.__aexit__.return_value = None

            mock_client_class.return_value = mock_client

            # Should raise error when all URLs fail
            with pytest.raises(URLFetchError):
                await fetcher.fetch_multiple(urls)

    def test_extract_text_removes_scripts(self):
        """Test that HTML text extraction removes script tags."""
        fetcher = URLFetcher()

        html = """
        <html>
            <body>
                <h1>Title</h1>
                <script>var x = 'hidden';</script>
                <p>Visible text</p>
            </body>
        </html>
        """

        text = fetcher._extract_text(html)
        assert "Title" in text
        assert "Visible text" in text
        assert "var x" not in text
        assert "hidden" not in text

    def test_extract_text_removes_styles(self):
        """Test that HTML text extraction removes style tags."""
        fetcher = URLFetcher()

        html = """
        <html>
            <body>
                <style>.hidden { display: none; }</style>
                <p>Visible text</p>
            </body>
        </html>
        """

        text = fetcher._extract_text(html)
        assert "Visible text" in text
        assert ".hidden" not in text
        assert "display" not in text

    def test_extract_text_preserves_paragraphs(self):
        """Test that HTML text extraction preserves paragraph structure."""
        fetcher = URLFetcher()

        html = """
        <html>
            <body>
                <p>First paragraph</p>
                <p>Second paragraph</p>
                <p>Third paragraph</p>
            </body>
        </html>
        """

        text = fetcher._extract_text(html)
        lines = text.split('\n')
        # Should have multiple lines (paragraphs separated)
        assert len(lines) >= 3
        assert "First paragraph" in text
        assert "Second paragraph" in text
        assert "Third paragraph" in text

    def test_extract_text_handles_malformed_html(self):
        """Test that HTML text extraction handles malformed HTML gracefully."""
        fetcher = URLFetcher()

        html = "<html><body><p>Text without closing tags"

        # Should not raise exception
        text = fetcher._extract_text(html)
        assert "Text without closing tags" in text

    def test_extract_text_cleans_whitespace(self):
        """Test that HTML text extraction cleans excessive blank lines."""
        fetcher = URLFetcher()

        html = """
        <html>
            <body>
                <p>Text with content</p>


                <p>And more content after blank lines</p>
            </body>
        </html>
        """

        text = fetcher._extract_text(html)
        # Should not have multiple consecutive blank lines
        assert "\n\n\n" not in text
        # Should preserve the actual content
        assert "Text with content" in text
        assert "And more content" in text
