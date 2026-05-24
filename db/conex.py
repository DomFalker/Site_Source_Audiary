from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import psycopg2
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://postgres:7869@localhost:5432/audiary")

# Se a URL começar com postgres:// (comum no Render/Heroku),
# alteramos para postgresql+psycopg2:// para compatibilidade com o SQLAlchemy.
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+psycopg2://", 1)

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
        # psycopg2 não aceita +psycopg2 no protocolo da URL, então limpamos se existir
        psycopg_url = DATABASE_URL
        if psycopg_url.startswith("postgresql+psycopg2://"):
            psycopg_url = psycopg_url.replace("postgresql+psycopg2://", "postgresql://", 1)
        return psycopg2.connect(psycopg_url)
    except psycopg2.Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None