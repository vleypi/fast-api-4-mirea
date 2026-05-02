from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, conint, constr


class ProductCreate(BaseModel):
    title: str
    price: float
    count: int
    description: str


class ProductRead(ProductCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)


class User(BaseModel):
    username: str
    age: conint(gt=18)
    email: EmailStr
    password: constr(min_length=8, max_length=16)
    phone: Optional[str] = "Unknown"


class UserIn(BaseModel):
    username: str
    age: int


class UserOut(BaseModel):
    id: int
    username: str
    age: int


class ErrorResponse(BaseModel):
    error: str
    detail: str
