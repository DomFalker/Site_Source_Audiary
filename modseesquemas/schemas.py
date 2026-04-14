from pydantic import BaseModel

class UserCreate(BaseModel):
    nome: str
    email: str
    senha: str
    cep: str | None = None
    rua: str | None = None
    tipo: str = "comprador"
    nome_loja: str | None = None

class UserLogin(BaseModel):
    email: str
    password: str

class ProductCreate(BaseModel):
    name: str
    brand: str
    price: float
    condition: str
    id_seller: int