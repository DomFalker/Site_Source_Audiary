from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from db.conex import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    username = Column(String, unique=True, index=True, nullable=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    type = Column(String)  # buyer ou seller
    cep = Column(String, nullable=True)
    rua = Column(String, nullable=True)
    store_name = Column(String, nullable=True)

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    brand = Column(String)
    price = Column(Float)
    condition = Column(String)
    id_seller = Column(Integer, ForeignKey("users.id"))

    seller = relationship("User")