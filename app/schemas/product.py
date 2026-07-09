"""
Edit History:
| Person | Date | Comment |
| --- | --- | --- |
| Shiladitya | 07/10/2026 | Created |
"""

from pydantic import BaseModel, Field


class ProductCreate(BaseModel):
    name: str = Field(min_length=1, max_length=150)
    description: str | None = None
    price: float = Field(gt=0)
    stock_quantity: int = Field(ge=0)


class ProductUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=150)
    description: str | None = None
    price: float | None = Field(default=None, gt=0)
    stock_quantity: int | None = Field(default=None, ge=0)


class ProductRead(BaseModel):
    id: int
    name: str
    description: str | None
    price: float
    stock_quantity: int

    model_config = {"from_attributes": True}
