from pydantic import BaseModel


class OrderCreate(BaseModel):
    user_id: int
    store_id: int
    product_id: int
    quantity: int


class OrderUpdate(BaseModel):
    status: str


class OrderOut(BaseModel):
    id: int
    user_id: int
    store_id: int
    product_id: int
    quantity: int
    total_price: float
    status: str

    class Config:
        orm_mode = True
