from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.conex import get_db
from modseesquemas.model import User
from modseesquemas.schemas import UserCreate, UserLogin
from modseesquemas.auth import hash_password, verify_password, create_token

user_router = APIRouter(prefix="/users", tags=["users"])

@user_router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    
    new_user = User(
        name=user.name,
        email=user.email,
        password=hash_password(user.password),
        type=user.type,
        store_name=user.store_name
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"msg": "Usuário criado", "id": new_user.id}
@user_router.get("/")
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()

@user_router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Credenciais inválidas")

    token = create_token({"user_id": db_user.id, "type": db_user.type})

    return {"access_token": token}

