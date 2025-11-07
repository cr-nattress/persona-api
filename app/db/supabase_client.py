"""
Supabase database client wrapper.

Provides a singleton client for database operations with connection pooling
and error handling.
"""

from supabase import create_client, Client
from app.core.config import settings
from app.core.logging import get_logger
from typing import Optional

logger = get_logger(__name__)


class SupabaseClient:
    """Supabase database client wrapper with connection management."""

    _instance: Optional["SupabaseClient"] = None
    _client: Optional[Client] = None

    def __new__(cls) -> "SupabaseClient":
        """Implement singleton pattern."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """Initialize Supabase client."""
        if self._client is None:
            self._initialize_client()

    def _initialize_client(self) -> None:
        """
        Initialize the Supabase client.

        Raises:
            Exception: If client initialization fails
        """
        try:
            logger.debug(
                f"Initializing Supabase client for {settings.supabase_url}"
            )
            self._client = create_client(
                settings.supabase_url,
                settings.supabase_anon_key,
            )
            logger.info("Supabase client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Supabase client: {e}")
            raise

    @property
    def client(self) -> Client:
        """Get the Supabase client instance."""
        if self._client is None:
            self._initialize_client()
        return self._client

    def get_table(self, table_name: str):
        """
        Get a reference to a table.

        Args:
            table_name: Name of the table

        Returns:
            Table reference for queries
        """
        try:
            return self.client.table(table_name)
        except Exception as e:
            logger.error(f"Failed to get table reference for {table_name}: {e}")
            raise

    def is_connected(self) -> bool:
        """
        Check if client is connected.

        Returns:
            True if connected, False otherwise
        """
        try:
            # Test connection by querying system tables
            self.client.table("personas").select("id", count="exact").limit(1).execute()
            return True
        except Exception as e:
            logger.warning(f"Connection check failed: {e}")
            return False

    def close(self) -> None:
        """Close the client connection."""
        if self._client is not None:
            try:
                # Supabase client doesn't have explicit close, but we can reset
                self._client = None
                logger.info("Supabase client connection closed")
            except Exception as e:
                logger.error(f"Error closing Supabase client: {e}")


# Global client instance
_supabase: Optional[SupabaseClient] = None


def get_supabase_client() -> SupabaseClient:
    """
    Get the Supabase client instance.

    Returns:
        SupabaseClient instance

    Usage:
        from app.db.supabase_client import get_supabase_client
        supabase = get_supabase_client()
        result = supabase.client.table('personas').select('*').execute()
    """
    global _supabase
    if _supabase is None:
        _supabase = SupabaseClient()
    return _supabase


def reset_supabase_client() -> None:
    """Reset the global Supabase client instance (for testing)."""
    global _supabase
    if _supabase is not None:
        _supabase.close()
    _supabase = None
