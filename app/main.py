"""
Edit History:
| Person | Date | Comment |
| --- | --- | --- |
| Shiladitya | 07/10/2026 | Created |
"""

import logging

from fastapi import FastAPI

from app.api import health, products, purchases, users
from app.core.config import get_settings
from app.core.logging import configure_logging
from app.db.session import create_tables

configure_logging()
logger = logging.getLogger(__name__)
settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="A small FastAPI e-commerce inventory and purchase API backed by MySQL.",
)


@app.on_event("startup")
def on_startup() -> None:
    logger.info("Starting %s", settings.app_name)
    create_tables()
    logger.debug("Database metadata check completed")


app.include_router(health.router)
app.include_router(users.router)
app.include_router(products.router)
app.include_router(purchases.router)
