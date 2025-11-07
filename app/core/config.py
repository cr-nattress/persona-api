"""
Application configuration using Pydantic Settings.

Loads environment variables from .env file and validates them.
"""

from pydantic_settings import BaseSettings
from typing import Literal
import sys


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # OpenAI Configuration
    openai_api_key: str
    openai_model: str = "gpt-4o-mini"

    # Supabase Configuration
    supabase_url: str
    supabase_anon_key: str

    # Application Configuration
    environment: Literal["development", "staging", "production"] = "development"
    log_level: str = "INFO"
    debug: bool = False

    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"  # Ignore extra fields in .env

    @property
    def is_production(self) -> bool:
        """Check if running in production."""
        return self.environment == "production"

    @property
    def is_development(self) -> bool:
        """Check if running in development."""
        return self.environment == "development"


def validate_settings() -> Settings:
    """
    Validate that all required settings are properly configured.

    Raises:
        ValueError: If required settings are missing or invalid
    """
    try:
        s = Settings()
    except Exception as e:
        raise ValueError(
            f"Configuration validation failed. Ensure all required environment "
            f"variables are set in .env file. Error: {str(e)}"
        ) from e

    # Additional validation
    if not s.openai_api_key:
        raise ValueError("OPENAI_API_KEY is required but not set")
    if not s.supabase_url:
        raise ValueError("SUPABASE_URL is required but not set")
    if not s.supabase_anon_key:
        raise ValueError("SUPABASE_ANON_KEY is required but not set")

    return s


# Load and validate settings
try:
    settings = validate_settings()
except ValueError as e:
    print(f"Configuration error: {e}", file=sys.stderr)
    sys.exit(1)
