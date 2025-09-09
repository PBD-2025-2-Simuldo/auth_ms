from pydantic import BaseModel

class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class AuthRequest(BaseModel):
    token: str

class AuthResponse(BaseModel):
    valid: bool
    username: str | None = None
    nome: str | None = None
    detail: str | None = None
