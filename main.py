from fastapi import FastAPI, Request, Cookie, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from db.conex import engine, Base, get_db
from sqlalchemy.orm import Session
from rotas.produto import product_router
from rotas.user import user_router
from modseesquemas.auth import decode_token
from modseesquemas.model import User, Product
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

# Helper para obter o usuário autenticado a partir do cookie
def obter_usuario_logado(access_token: str | None, db: Session) -> User | None:
    if not access_token:
        return None
    payload = decode_token(access_token)
    if not payload:
        return None
    user_id = payload.get("user_id")
    if not user_id:
        return None
    return db.query(User).filter(User.id == user_id).first()

# Rotas de Visualização (Frontend)
@app.get("/", response_class=HTMLResponse)
async def read_index(request: Request, access_token: str | None = Cookie(None), db: Session = Depends(get_db)):
    user = obter_usuario_logado(access_token, db)
    return templates.TemplateResponse(request, "index.html", {"user": user})

@app.get("/login", response_class=HTMLResponse)
async def read_login(request: Request, access_token: str | None = Cookie(None), db: Session = Depends(get_db)):
    user = obter_usuario_logado(access_token, db)
    if user:
        return RedirectResponse(url="/produtos", status_code=303)
    return templates.TemplateResponse(request, "login.html")

@app.get("/cadastro", response_class=HTMLResponse)
async def read_cadastro(request: Request, access_token: str | None = Cookie(None), db: Session = Depends(get_db)):
    user = obter_usuario_logado(access_token, db)
    if user:
        return RedirectResponse(url="/produtos", status_code=303)
    return templates.TemplateResponse(request, "cadastro.html")

@app.get("/produtos", response_class=HTMLResponse)
async def read_produtos(request: Request, search: str | None = None, access_token: str | None = Cookie(None), db: Session = Depends(get_db)):
    user = obter_usuario_logado(access_token, db)
    if not user:
        response = RedirectResponse(url="/login", status_code=303)
        response.delete_cookie("access_token")
        return response
    
    query = db.query(Product)
    if search:
        query = query.filter(
            (Product.name.ilike(f"%{search}%")) |
            (Product.brand.ilike(f"%{search}%")) |
            (Product.condition.ilike(f"%{search}%"))
        )
    produtos = query.all()
    return templates.TemplateResponse(request, "produtos.html", {"user": user, "produtos": produtos, "search": search})

@app.get("/produtos/novo", response_class=HTMLResponse)
async def read_novo_produto(request: Request, access_token: str | None = Cookie(None), db: Session = Depends(get_db)):
    user = obter_usuario_logado(access_token, db)
    if not user:
        return RedirectResponse(url="/login", status_code=303)
    return templates.TemplateResponse(request, "novo-produto.html", {"user": user})

@app.get("/senha-esquecida/sucesso", response_class=HTMLResponse)
async def read_senha_sucesso(request: Request, email: str = ""):
    return templates.TemplateResponse(request, "senha-esquecida-sucesso.html", {"email": email})

@app.get("/checkout/{product_id}", response_class=HTMLResponse)
async def read_checkout(product_id: int, request: Request, access_token: str | None = Cookie(None), db: Session = Depends(get_db)):
    user = obter_usuario_logado(access_token, db)
    if not user:
        return RedirectResponse(url="/login", status_code=303)
    produto = db.query(Product).filter(Product.id == product_id).first()
    if not produto:
        return RedirectResponse(url="/produtos", status_code=303)
    return templates.TemplateResponse(request, "checkout.html", {"user": user, "produto": produto})

@app.post("/checkout/{product_id}/pagar")
async def processar_pagamento(product_id: int, access_token: str | None = Cookie(None), db: Session = Depends(get_db)):
    user = obter_usuario_logado(access_token, db)
    if not user:
        raise HTTPException(status_code=401, detail="Não autenticado")
    produto = db.query(Product).filter(Product.id == product_id).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    db.delete(produto)
    db.commit()
    return {"success": True, "msg": "Pagamento processado com sucesso!"}

@app.get("/senha-esquecida", response_class=HTMLResponse)
async def read_senha(request: Request):
    return templates.TemplateResponse(request, "senha-esquecida.html")

@app.get("/logout")
async def logout():
    response = RedirectResponse(url="/login", status_code=303)
    response.delete_cookie("access_token")
    return response

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "Backend do Site Audiário está online"}

