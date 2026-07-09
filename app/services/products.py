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

from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate

logger = logging.getLogger(__name__)


def create_product(db: Session, payload: ProductCreate) -> Product:
    product = Product(**payload.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)

    logger.info("Created product id=%s name=%s", product.id, product.name)
    return product


def list_products(db: Session, name: str | None = None) -> list[Product]:
    stmt = select(Product).order_by(Product.id)
    if name:
        logger.debug("Searching products by name=%s", name)
        stmt = stmt.where(Product.name.ilike(f"%{name}%"))
    else:
        logger.debug("Listing all products")
    return list(db.scalars(stmt))


def get_product(db: Session, product_id: int) -> Product:
    product = db.get(Product, product_id)
    if not product:
        logger.warning("Product not found id=%s", product_id)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found.")
    return product


def update_product(db: Session, product_id: int, payload: ProductUpdate) -> Product:
    product = get_product(db, product_id)
    update_data = payload.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(product, field, value)

    db.commit()
    db.refresh(product)
    logger.info("Updated product id=%s fields=%s", product.id, sorted(update_data.keys()))
    return product


def delete_product(db: Session, product_id: int) -> None:
    product = get_product(db, product_id)
    db.delete(product)
    db.commit()
    logger.info("Deleted product id=%s", product_id)
