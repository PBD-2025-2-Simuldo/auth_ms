from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.database import Base, engine, SessionLocal
from app import models, crud, auth_utils
from app.schemas import LoginRequest, TokenResponse, AuthRequest, AuthResponse
from datetime import timedelta

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Auth Microservice")

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/api/v1/login/", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db, payload.username)
    if not user:
        raise HTTPException(status_code=401, detail="Usuário ou senha inválidos")
    if not auth_utils.verify_password(payload.password, user.password):
        raise HTTPException(status_code=401, detail="Usuário ou senha inválidos")

    token_data = {"sub": user.username, "nome": user.nome}
    access_token = auth_utils.create_access_token(data=token_data, expires_delta=timedelta(minutes=60))
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/api/v1/authentication/", response_model=AuthResponse)
def authenticate_token(payload: AuthRequest, db: Session = Depends(get_db)):
    token = payload.token
    try:
        decoded = auth_utils.decode_token(token)
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Token inválido: {str(e)}")

    username = decoded.get("sub")
    if not username:
        raise HTTPException(status_code=401, detail="Token inválido (sub ausente).")

    user = crud.get_user_by_username(db, username)
    if not user:
        raise HTTPException(status_code=401, detail="Usuário do token não encontrado.")

    return {"valid": True, "username": user.username, "nome": user.nome}
