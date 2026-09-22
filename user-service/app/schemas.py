from typing import Optional
from pydantic import BaseModel


class UserBase(BaseModel):
    name: str
    email: str
    phone: str
    address: Optional[str] = None


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None


class UserOut(UserBase):
    id: int

    class Config:
        orm_mode = True
