"""
Edit History:
| Person | Date | Comment |
| --- | --- | --- |
| Shiladitya | 07/10/2026 | Created |
"""

from datetime import datetime

from pydantic import BaseModel, Field


class PurchaseCreate(BaseModel):
    user_id: int = Field(gt=0)
    product_id: int = Field(gt=0)
    quantity: int = Field(gt=0)


class PurchaseRead(BaseModel):
    id: int
    user_id: int
    product_id: int
    quantity: int
    total_price: float
    purchased_at: datetime

    model_config = {"from_attributes": True}
