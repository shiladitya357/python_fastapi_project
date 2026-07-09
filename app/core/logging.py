"""
Edit History:
| Person | Date | Comment |
| --- | --- | --- |
| Shiladitya | 07/10/2026 | Created |
"""

import logging
from logging.config import dictConfig
from pathlib import Path

from app.core.config import get_settings


def configure_logging() -> None:
    settings = get_settings()
    log_level = settings.log_level.upper()
    log_dir = Path(settings.log_dir)
    log_dir.mkdir(parents=True, exist_ok=True)

    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "default": {
                    "format": "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
                }
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "default",
                },
                "file": {
                    "class": "logging.handlers.RotatingFileHandler",
                    "formatter": "default",
                    "filename": settings.log_file_path,
                    "maxBytes": 10485760,
                    "backupCount": 5,
                },
            },
            "root": {
                "handlers": ["console", "file"],
                "level": log_level,
            },
            "loggers": {
                "uvicorn": {"level": log_level},
                "uvicorn.access": {"level": log_level},
                "sqlalchemy.engine": {"level": "WARNING"},
            },
        }
    )

    logging.getLogger(__name__).info(
        "Logging configured at %s level; file=%s",
        log_level,
        settings.log_file_path,
    )
