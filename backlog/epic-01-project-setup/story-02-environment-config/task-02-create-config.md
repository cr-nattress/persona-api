# TASK-01-02-02: Create config.py with Pydantic Settings

**Story:** US-01-02

**Estimated Time:** 10 minutes

**Description:** Create Pydantic-based configuration module that loads environment variables with validation.

## Agent Prompt

You are implementing **EPIC-01: Project Setup & Infrastructure**.

**Goal:** Create app/core/config.py that safely loads and validates all environment variables using Pydantic.

**Context:** Pydantic Settings provides type-safe configuration management with automatic validation and .env file support.

**Instructions:**

1. Create `app/core/config.py` with the following content:

```python
\"\"\"
Application configuration using Pydantic Settings.

Loads environment variables from .env file and validates them.
\"\"\"

from pydantic_settings import BaseSettings
from typing import Literal


class Settings(BaseSettings):
    \"\"\"Application settings loaded from environment variables.\"\"\"

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
        \"\"\"Check if running in production.\"\"\"
        return self.environment == "production"

    @property
    def is_development(self) -> bool:
        \"\"\"Check if running in development.\"\"\"
        return self.environment == "development"


# Global settings instance
settings = Settings()
```

2. Import and use in main.py later (for now, just ensure it works).

3. Verify the configuration can be instantiated without errors.

## Verification Steps

1. Check file exists:
   ```bash
   ls -la app/core/config.py
   ```

2. Test imports:
   ```bash
   python -c "from app.core.config import settings; print(f'Config loaded: {settings.environment}')"
   ```
   Note: This will fail if .env is missing, which is expected. Check for import errors.

3. Check syntax:
   ```bash
   python -m py_compile app/core/config.py
   ```
   Should complete without errors.

## Expected Output

A config.py module with:
- Pydantic BaseSettings class
- All required environment variables
- Type validation
- Helper properties (is_production, is_development)
- .env file support

## Commit Message

```
feat(config): add Pydantic-based configuration module

Create app/core/config.py with type-safe environment variable loading and validation using Pydantic Settings.
```

---

**Completion Time:** ~10 minutes
**Dependencies:** TASK-01-02-01 (.env.example must exist)
