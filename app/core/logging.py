"""
Logging configuration using Loguru.

Provides structured logging with console and file output depending on environment.
"""

import sys
from pathlib import Path
from loguru import logger
from datetime import datetime, timedelta
import glob


def setup_logging(log_level: str = "INFO", environment: str = "development") -> None:
    """
    Configure Loguru for the application.

    Args:
        log_level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        environment: Environment name (development, staging, production)
    """
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


def get_logger(name: str = None):
    """
    Get a logger instance.

    Usage:
        from app.core.logging import get_logger
        logger = get_logger(__name__)
        logger.info("Message")

    Args:
        name: Optional logger name (usually __name__)

    Returns:
        Logger instance
    """
    if name:
        return logger.bind(name=name)
    return logger


def cleanup_old_logs(days_to_keep: int = 7) -> None:
    """Remove log files older than specified days."""
    log_dir = Path("logs")
    if not log_dir.exists():
        return

    cutoff_time = datetime.now() - timedelta(days=days_to_keep)

    for log_file in glob.glob(str(log_dir / "*.log")):
        file_mtime = datetime.fromtimestamp(Path(log_file).stat().st_mtime)
        if file_mtime < cutoff_time:
            try:
                Path(log_file).unlink()
                logger.info(f"Deleted old log file: {log_file}")
            except Exception as e:
                logger.error(f"Failed to delete log file {log_file}: {e}")
