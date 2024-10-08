from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime
from enum import Enum


class ProductCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    quantity: int


class ProductUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    price: Optional[float]
    quantity: Optional[int]


class ProductOut(BaseModel):
    id: int
    name: str
    description: Optional[str]
    price: float
    quantity: int

    model_config = ConfigDict(from_attributes=True)


class OrderStatusEnum(str, Enum):
    in_process = "в процессе"
    shipped = "отправлен"
    delivered = "доставлен"


class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int


class OrderItemOut(BaseModel):
    id: int
    product_id: int
    quantity: int

    model_config = ConfigDict(from_attributes=True)


class OrderCreate(BaseModel):
    items: List[OrderItemCreate]


class OrderUpdate(BaseModel):
    status: OrderStatusEnum


class OrderOut(BaseModel):
    id: int
    created_at: datetime
    status: OrderStatusEnum
    items: List[OrderItemOut]

    model_config = ConfigDict(from_attributes=True)