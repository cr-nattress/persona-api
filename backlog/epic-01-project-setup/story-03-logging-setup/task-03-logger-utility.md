# TASK-01-03-03: Create Logger Utility Function

**Story:** US-01-03

**Estimated Time:** 5 minutes

**Description:** Create a utility function to easily access logger from any module in the application.

## Agent Prompt

You are implementing **EPIC-01: Project Setup & Infrastructure**.

**Goal:** Create a simple logger utility that can be imported throughout the application.

**Context:** Developers should be able to import logger easily without manually calling setup functions.

**Instructions:**

1. Add to `app/core/logging.py`:

```python
def get_logger(name: str = __name__):
    \"\"\"
    Get a logger instance for the given module name.

    Usage:
        from app.core.logging import get_logger
        logger = get_logger(__name__)
        logger.info("Message")
    \"\"\"
    return logger.bind(name=name)
```

2. Add usage example comments throughout the module.

3. Create an optional `app/core/__init__.py` export:

```python
from .logging import setup_logging, get_logger

__all__ = ["setup_logging", "get_logger"]
```

## Verification Steps

1. Test import from different modules:
   ```bash
   python -c "from app.core.logging import get_logger; logger = get_logger(); logger.info('Test')"
   ```

2. Test usage:
   ```python
   from app.core.logging import get_logger
   logger = get_logger(__name__)
   logger.info("This should work from any module")
   ```

## Expected Output

- get_logger() function available for import
- Can be used in any module with `from app.core.logging import get_logger`
- Automatic context binding with module name

## Commit Message

```
feat(logging): add get_logger utility function

Create get_logger() utility for easy logger access throughout the application with automatic context binding.
```

---

**Completion Time:** ~5 minutes
**Dependencies:** TASK-01-03-01
