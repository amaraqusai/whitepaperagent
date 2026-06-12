"""Logging & Retry Utilities."""

import functools
import logging
import os
import random
import time
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Callable, TypeVar

F = TypeVar("F", bound=Callable)

# ─── Constants ────────────────────────────────────────────────────────
LOG_DIR = Path(__file__).resolve().parent / "logs"
LOG_FILE = LOG_DIR / "pipeline.log"
MAX_BYTES = 5 * 1024 * 1024  # 5 MB per log file
BACKUP_COUNT = 3

# ANSI color codes for console output
_COLORS = {
    logging.DEBUG: "\033[90m",     # Gray
    logging.INFO: "\033[32m",      # Green
    logging.WARNING: "\033[33m",   # Yellow
    logging.ERROR: "\033[31m",     # Red
    logging.CRITICAL: "\033[1;31m",  # Bold red
}
_RESET = "\033[0m"


# ─── Custom Formatter ────────────────────────────────────────────────
class ColoredFormatter(logging.Formatter):
    """Formatter that adds ANSI colors based on log level."""

    FMT = "%(asctime)s │ %(levelname)-8s │ %(name)-20s │ %(message)s"
    DATE_FMT = "%Y-%m-%d %H:%M:%S"

    def format(self, record: logging.LogRecord) -> str:
        """Format *record* with ANSI color wrapping."""
        color = _COLORS.get(record.levelno, "")
        formatter = logging.Formatter(
            f"{color}{self.FMT}{_RESET}", datefmt=self.DATE_FMT
        )
        return formatter.format(record)


class PlainFormatter(logging.Formatter):
    """Formatter for file output — no ANSI codes."""

    FMT = "%(asctime)s │ %(levelname)-8s │ %(name)-20s │ %(message)s"
    DATE_FMT = "%Y-%m-%d %H:%M:%S"

    def format(self, record: logging.LogRecord) -> str:
        """Format *record* without color codes."""
        formatter = logging.Formatter(self.FMT, datefmt=self.DATE_FMT)
        return formatter.format(record)


# ─── Logger Factory ──────────────────────────────────────────────────
def get_logger(name: str, level: int = logging.DEBUG) -> logging.Logger:
    """Return a logger configured with console and file handlers."""
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger  # Already configured — avoid duplicate handlers
    logger.setLevel(level)

    # Console handler
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    console.setFormatter(ColoredFormatter())
    logger.addHandler(console)

    # File handler (rotating)
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    file_h = RotatingFileHandler(
        LOG_FILE, maxBytes=MAX_BYTES, backupCount=BACKUP_COUNT,
        encoding="utf-8",
    )
    file_h.setLevel(logging.DEBUG)
    file_h.setFormatter(PlainFormatter())
    logger.addHandler(file_h)

    return logger


# ─── Retry Decorator ─────────────────────────────────────────────────
_API_ERRORS: tuple[type[Exception], ...] = (
    ConnectionError, TimeoutError, OSError,
)

_logger = get_logger("retry")


def retry_on_api_error(
    max_retries: int = 3, base_delay: float = 2.0
) -> Callable[[F], F]:
    """Decorator: retry on transient API / network errors."""
    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):  # noqa: ANN
            last_exc: Exception | None = None
            for attempt in range(1, max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except _API_ERRORS as exc:
                    last_exc = exc
                except Exception as exc:
                    # Catch HTTP 429 from requests / httpx
                    status = getattr(
                        getattr(exc, "response", None), "status_code", None
                    )
                    if status != 429:
                        raise
                    last_exc = exc
                delay = base_delay * (2 ** (attempt - 1))
                jitter = random.uniform(0, delay * 0.25)
                _logger.warning(
                    "%s failed (attempt %d/%d): %s — retrying in %.1fs",
                    func.__name__, attempt, max_retries,
                    last_exc, delay + jitter,
                )
                time.sleep(delay + jitter)
            _logger.error(
                "%s: all %d retries exhausted.", func.__name__, max_retries
            )
            raise last_exc  # type: ignore[misc]
        return wrapper  # type: ignore[return-value]
    return decorator


# ─── Execution-Time Decorator ────────────────────────────────────────
def log_execution_time(func: F) -> F:
    """Decorator that logs the wall-clock execution time of *func*."""
    _timer_logger = get_logger(f"timer.{func.__name__}")

    @functools.wraps(func)
    def wrapper(*args, **kwargs):  # noqa: ANN
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        _timer_logger.info(
            "%s completed in %.3f s", func.__name__, elapsed
        )
        return result
    return wrapper  # type: ignore[return-value]
