from typing import Optional
from pydantic import BaseModel


class StoreBase(BaseModel):
    name: str
    location: str


class StoreCreate(StoreBase):
    pass


class StoreUpdate(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None


class StoreOut(StoreBase):
    id: int

    class Config:
        orm_mode = True


class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    category: Optional[str] = None
    price: float
    stock_quantity: int = 0


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = None
    stock_quantity: Optional[int] = None


class ProductOut(ProductBase):
    id: int
    store_id: int

    class Config:
        orm_mode = True


class StockUpdate(BaseModel):
    # negative to decrement (e.g. an order consuming stock), positive to increment (restock)
    quantity_change: int
