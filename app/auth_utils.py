# auth_ms/app/auth_utils.py
from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta
from typing import Optional

# SECRET - em produção use variável ambiente
SECRET_KEY = "CHANGE_THIS_SECRET_KEY"  # troque por valor forte / usar env var
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_token(token: str) -> dict:
    # jwt.decode levantará exceção se inválido ou expirado
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return payload
