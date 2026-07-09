"""
Edit History:
| Person | Date | Comment |
| --- | --- | --- |
| Shiladitya | 07/10/2026 | Created |
"""

import logging

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.models.user import User
from app.schemas.user import UserCreate

logger = logging.getLogger(__name__)


def create_user(db: Session, payload: UserCreate) -> User:
    existing_user = db.scalar(select(User).where(User.email == payload.email))
    if existing_user:
        logger.warning("Attempted duplicate user registration for email=%s", payload.email)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with this email already exists.",
        )

    settings = get_settings()
    user = User(
        name=payload.name,
        email=str(payload.email),
        balance=settings.default_user_balance,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    logger.info("Created user id=%s email=%s", user.id, user.email)
    return user


def list_users(db: Session) -> list[User]:
    logger.debug("Listing users")
    return list(db.scalars(select(User).order_by(User.id)))


def get_user(db: Session, user_id: int) -> User:
    user = db.get(User, user_id)
    if not user:
        logger.warning("User not found id=%s", user_id)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    return user
