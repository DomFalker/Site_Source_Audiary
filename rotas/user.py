from fastapi import APIRouter, Depends, HTTPException, Form
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from db.conex import get_db
from modseesquemas.model import User
from modseesquemas.auth import hash_password, verify_password, create_token

user_router = APIRouter(prefix="/users", tags=["users"])

@user_router.post("/register")
async def register(
    nome: str = Form(...),
    email: str = Form(...),
    senha: str = Form(...),
    cep: str = Form(None),
    rua: str = Form(None),
    tipo: str = Form("buyer"),
    db: Session = Depends(get_db)
):
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        # Em uma app real, poderíamos redirecionar com um erro
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    
    new_user = User(
        name=nome,
        email=email,
        password=hash_password(senha),
        type=tipo,
        cep=cep,
        rua=rua
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Redireciona para o login após o cadastro
    return RedirectResponse(url="/login", status_code=303)

@user_router.get("/")
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()

@user_router.post("/login")
async def login(
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    db_user = db.query(User).filter(User.email == email).first()

    if not db_user or not verify_password(password, db_user.password):
        raise HTTPException(status_code=400, detail="Credenciais inválidas")

    token = create_token({"user_id": db_user.id, "type": db_user.type})

    # Em uma app real, salvaríamos o token em um cookie ou localStorage
    # Por enquanto, redireciona para a home
    response = RedirectResponse(url="/", status_code=303)
    response.set_cookie(key="access_token", value=token, httponly=True)
    return response

@user_router.post("/recover-password")
async def recover_password(email: str = Form(...)):
    return {"msg": f"Um link de recuperação já foi enviado para {email} esquecidinho!"}

