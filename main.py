from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db.conex import engine, Base
from rotas.produto import product_router
from rotas.user import user_router

app = FastAPI(title="Site Audiário API")

# Criar tabelas (Alembic é preferível, mas mantendo create_all para compatibilidade)
Base.metadata.create_all(bind=engine)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rotas
app.include_router(user_router)
app.include_router(product_router)

@app.get("/")
def health_check():
    return {"status": "ok", "message": "Backend do Site Audiário está online"}

