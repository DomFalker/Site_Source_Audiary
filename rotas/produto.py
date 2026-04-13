from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.conex import get_db
from modseesquemas.model import Product
from modseesquemas.schemas import ProductCreate

product_router = APIRouter(prefix="/products", tags=["products"])

@product_router.get("/")
def get_products(db: Session = Depends(get_db)):
    return db.query(Product).all()

@product_router.post("/")
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    new_product = Product(
        name=product.name,
        brand=product.brand,
        price=product.price,
        condition=product.condition,
        id_seller=product.id_seller,
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return {"msg": "Produto criado", "id": new_product.id}

