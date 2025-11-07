"""
Logging configuration using Loguru.

Provides structured logging with console and file output depending on environment.
"""

import sys
from pathlib import Path
from loguru import logger
from datetime import datetime, timedelta
import glob
import contextvars
from uuid import uuid4

# Context variable for storing correlation ID
correlation_id_var = contextvars.ContextVar('correlation_id', default=None)


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

    # Create logs directory
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    # File handler for general application logs
    logger.add(
        log_dir / "app.log",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level="INFO",
        rotation="00:00",  # Rotate daily
        retention="7 days",  # Keep 7 days of logs
    )

    # File handler for LLM requests and responses
    logger.add(
        log_dir / "llm_interactions.log",
        format="{time:YYYY-MM-DD HH:mm:ss} | {extra[correlation_id]} | {level: <8} | {message}",
        level="INFO",
        rotation="00:00",  # Rotate daily
        retention="7 days",  # Keep 7 days of logs
        filter=lambda record: record.get("extra", {}).get("llm_log", False),
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


def get_correlation_id() -> str:
    """Get the current correlation ID or create a new one."""
    corr_id = correlation_id_var.get()
    if not corr_id:
        corr_id = str(uuid4())[:8]  # Short 8-character ID
        correlation_id_var.set(corr_id)
    return corr_id


def set_correlation_id(corr_id: str) -> None:
    """Set the correlation ID for the current context."""
    correlation_id_var.set(corr_id)


def log_llm_request(
    model: str,
    messages: list,
    temperature: float = None,
    max_tokens: int = None,
) -> None:
    """
    Log an LLM API request.

    Args:
        model: Model name (e.g., 'gpt-4o-mini')
        messages: List of messages sent to the model
        temperature: Temperature parameter
        max_tokens: Max tokens parameter
    """
    corr_id = get_correlation_id()
    msg_count = len(messages)
    total_chars = sum(len(m.get("content", "")) for m in messages)

    logger.bind(llm_log=True, correlation_id=corr_id).info(
        f"LLM Request | Model: {model} | Messages: {msg_count} | "
        f"Chars: {total_chars} | Temp: {temperature} | MaxTokens: {max_tokens}"
    )


def log_llm_response(
    model: str,
    response_text: str,
    usage: dict = None,
    latency_ms: float = None,
) -> None:
    """
    Log an LLM API response.

    Args:
        model: Model name
        response_text: Response content
        usage: Token usage dict with 'prompt_tokens', 'completion_tokens', 'total_tokens'
        latency_ms: Request latency in milliseconds
    """
    corr_id = get_correlation_id()
    response_chars = len(response_text)

    usage_str = ""
    if usage:
        usage_str = (
            f" | Tokens - Prompt: {usage.get('prompt_tokens', 0)}, "
            f"Completion: {usage.get('completion_tokens', 0)}, "
            f"Total: {usage.get('total_tokens', 0)}"
        )

    latency_str = f" | Latency: {latency_ms:.0f}ms" if latency_ms else ""

    logger.bind(llm_log=True, correlation_id=corr_id).info(
        f"LLM Response | Model: {model} | ResponseChars: {response_chars}{usage_str}{latency_str}"
    )


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
