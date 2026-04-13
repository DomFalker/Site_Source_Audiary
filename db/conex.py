from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import psycopg2
import os

DATABASE_URL = "postgresql+psycopg2://postgres:7869@localhost:5432/audiary"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def conexao_db_raw():
    """Retorna uma conexão bruta do psycopg2 se necessário."""
    try:
        conn = psycopg2.connect(
           dbname='audiary',
           user='postgres',
           password= '7869',
           host= 'localhost',
           port= '5432',
        )
        return conn
    except psycopg2.Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None