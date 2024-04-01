from pydantic import BaseModel, Field
from pydantic.v1 import validator


class OrderCreate(BaseModel):
    product_name: str = Field(default='Test Product')
    quantity: int = Field(default=10)

    @validator("quantity")
    def quantity_must_be_positive(cls, value):
        if value <= 0:
            raise ValueError("Quantity must be positive")
        return value


class OrderResponse(BaseModel):
    id: int
    product_name: str
    quantity: int


class OrderUpdate(BaseModel):
    product_name: str
    quantity: int
