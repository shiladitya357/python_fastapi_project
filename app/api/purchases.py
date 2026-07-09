"""
Edit History:
| Person | Date | Comment |
| --- | --- | --- |
| Shiladitya | 07/10/2026 | Created |
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.purchase import PurchaseCreate, PurchaseRead
from app.services import purchases as purchase_service

router = APIRouter(prefix="/purchases", tags=["purchases"])


@router.post("", response_model=PurchaseRead, status_code=201)
def create_purchase(payload: PurchaseCreate, db: Session = Depends(get_db)) -> PurchaseRead:
    return purchase_service.create_purchase(db, payload)


@router.get("", response_model=list[PurchaseRead])
def list_purchases(
    user_id: int | None = None,
    db: Session = Depends(get_db),
) -> list[PurchaseRead]:
    return purchase_service.list_purchases(db, user_id=user_id)
