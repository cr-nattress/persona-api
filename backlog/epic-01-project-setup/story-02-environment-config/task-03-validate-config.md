# TASK-01-02-03: Create Environment Validation

**Story:** US-01-02

**Estimated Time:** 5 minutes

**Description:** Add validation functions to ensure all required environment variables are present and correct.

## Agent Prompt

You are implementing **EPIC-01: Project Setup & Infrastructure**.

**Goal:** Create validation utilities in app/core/config.py to ensure environment configuration is complete and valid.

**Context:** Early validation of configuration prevents runtime errors caused by missing environment variables.

**Instructions:**

1. Update `app/core/config.py` to include a validation function:

```python
def validate_settings() -> Settings:
    \"\"\"
    Validate that all required settings are properly configured.

    Raises:
        ValueError: If required settings are missing or invalid
    \"\"\"
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
```

2. Update the global settings instantiation:

```python
# Load and validate settings
try:
    settings = validate_settings()
except ValueError as e:
    import sys
    print(f"Configuration error: {e}", file=sys.stderr)
    sys.exit(1)
```

3. This ensures the application fails fast with clear error messages if configuration is invalid.

## Verification Steps

1. With missing .env:
   ```bash
   rm -f .env
   python -c "from app.core.config import settings" 2>&1
   ```
   Should show a clear error message (not a cryptic import error).

2. With valid .env:
   ```bash
   cp .env.example .env
   # Edit .env with actual values (or dummy values for testing)
   python -c "from app.core.config import settings; print('Config valid')"
   ```

3. Check for syntax errors:
   ```bash
   python -m py_compile app/core/config.py
   ```

## Expected Output

Updated config.py with:
- validate_settings() function
- Clear error messages
- Early failure detection
- Fast feedback on configuration issues

## Commit Message

```
feat(config): add environment validation function

Add validate_settings() to ensure all required environment variables are present and valid, with clear error messages.
```

---

**Completion Time:** ~5 minutes
**Dependencies:** TASK-01-02-02 (config.py must exist)
