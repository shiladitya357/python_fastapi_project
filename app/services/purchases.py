"""
Edit History:
| Person | Date | Comment |
| --- | --- | --- |
| Shiladitya | 07/10/2026 | Created |
"""

import logging
from decimal import Decimal

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.product import Product
from app.models.purchase import Purchase
from app.models.user import User
from app.schemas.purchase import PurchaseCreate

logger = logging.getLogger(__name__)


def create_purchase(db: Session, payload: PurchaseCreate) -> Purchase:
    user = db.get(User, payload.user_id)
    if not user:
        logger.warning("Purchase rejected because user is missing id=%s", payload.user_id)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")

    product = db.get(Product, payload.product_id)
    if not product:
        logger.warning("Purchase rejected because product is missing id=%s", payload.product_id)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found.")

    if product.stock_quantity < payload.quantity:
        logger.warning(
            "Purchase rejected due to insufficient stock product_id=%s requested=%s available=%s",
            product.id,
            payload.quantity,
            product.stock_quantity,
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Not enough stock available.",
        )

    total_price = Decimal(str(product.price)) * Decimal(payload.quantity)
    if Decimal(str(user.balance)) < total_price:
        logger.warning(
            "Purchase rejected due to insufficient balance user_id=%s total=%s balance=%s",
            user.id,
            total_price,
            user.balance,
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User does not have enough balance.",
        )

    product.stock_quantity -= payload.quantity
    user.balance = Decimal(str(user.balance)) - total_price
    purchase = Purchase(
        user_id=user.id,
        product_id=product.id,
        quantity=payload.quantity,
        total_price=total_price,
    )

    db.add(purchase)
    db.commit()
    db.refresh(purchase)

    logger.info(
        "Purchase created id=%s user_id=%s product_id=%s quantity=%s total=%s",
        purchase.id,
        user.id,
        product.id,
        payload.quantity,
        total_price,
    )
    return purchase


def list_purchases(db: Session, user_id: int | None = None) -> list[Purchase]:
    stmt = select(Purchase).order_by(Purchase.purchased_at.desc())
    if user_id:
        logger.debug("Listing purchases for user_id=%s", user_id)
        stmt = stmt.where(Purchase.user_id == user_id)
    else:
        logger.debug("Listing all purchases")
    return list(db.scalars(stmt))
