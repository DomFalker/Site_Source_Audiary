from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    type: str
    store_name: str | None = None

class UserLogin(BaseModel):
    email: str
    password: str

class ProductCreate(BaseModel):
    name: str
    brand: str
    price: float
    condition: str
    id_seller: int