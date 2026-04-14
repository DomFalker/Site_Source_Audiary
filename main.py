from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from db.conex import engine, Base
from rotas.produto import product_router
from rotas.user import user_router
import os

app = FastAPI(title="Site Audiário API")

# Criar tabelas
Base.metadata.create_all(bind=engine)

# Configuração de Arquivos Estáticos e Templates
# Verificando se as pastas existem para evitar erros na inicialização
if os.path.exists("public"):
    app.mount("/public", StaticFiles(directory="public"), name="public")
if os.path.exists("views"):
    templates = Jinja2Templates(directory="views")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rotas de API
app.include_router(user_router)
app.include_router(product_router)

# Rotas de Visualização (Frontend)
@app.get("/", response_class=HTMLResponse)
async def read_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
async def read_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/cadastro", response_class=HTMLResponse)
async def read_cadastro(request: Request):
    return templates.TemplateResponse("cadastro.html", {"request": request})

@app.get("/produtos", response_class=HTMLResponse)
async def read_produtos(request: Request):
    return templates.TemplateResponse("produtos.html", {"request": request})

@app.get("/senha-esquecida", response_class=HTMLResponse)
async def read_senha(request: Request):
    return templates.TemplateResponse("senha-esquecida.html", {"request": request})

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "Backend do Site Audiário está online"}

