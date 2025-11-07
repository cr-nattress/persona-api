# TASK-01-03-01: Create Logging Configuration with Loguru

**Story:** US-01-03

**Estimated Time:** 15 minutes

**Description:** Create core/logging.py that configures Loguru for structured logging throughout the application.

## Agent Prompt

You are implementing **EPIC-01: Project Setup & Infrastructure**.

**Goal:** Create app/core/logging.py that configures Loguru for development and production environments.

**Context:** Loguru provides structured logging with automatic context injection. This module centralizes logging configuration so all parts of the app use consistent logging.

**Instructions:**

1. Create `app/core/logging.py`:

```python
\"\"\"
Logging configuration using Loguru.

Provides structured logging with console and file output depending on environment.
\"\"\"

import sys
from pathlib import Path
from loguru import logger

# Configure logging based on environment
def setup_logging(log_level: str = "INFO", environment: str = "development") -> None:
    \"\"\"
    Configure Loguru for the application.

    Args:
        log_level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        environment: Environment name (development, staging, production)
    \"\"\"
    # Remove default handler
    logger.remove()

    # Console handler - always present
    logger.add(
        sys.stderr,
        format="<level>{time:YYYY-MM-DD HH:mm:ss}</level> | "
               "<level>{level: <8}</level> | "
               "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
               "<level>{message}</level>",
        level=log_level,
        colorize=True if environment == "development" else False,
    )

    # File handler for errors and above
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    logger.add(
        log_dir / "app.log",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level="INFO",
        rotation="00:00",  # Rotate daily
        retention="7 days",  # Keep 7 days of logs
    )

    logger.info(f"Logging initialized - Environment: {environment}, Level: {log_level}")


def get_logger():
    \"\"\"Get the logger instance.\"\"\"
    return logger
```

2. Create logs directory and ensure it's writable.

## Verification Steps

1. Check file exists:
   ```bash
   ls -la app/core/logging.py
   ```

2. Test import:
   ```bash
   python -c "from app.core.logging import setup_logging, get_logger; setup_logging(); get_logger().info('Test log')"
   ```

3. Check logs directory created:
   ```bash
   ls -la logs/
   ```

## Expected Output

- app/core/logging.py with Loguru configuration
- logs/ directory created
- Sample log message printed to console

## Commit Message

```
feat(logging): add Loguru configuration module

Create app/core/logging.py with structured logging setup supporting development and production environments with file rotation.
```

---

**Completion Time:** ~15 minutes
**Dependencies:** TASK-01-02-02 (config.py must exist)
