# execute: python add_user.py
from app.database import SessionLocal, Base, engine
from app.models import models
from app.crud import create_user
from app.auth_utils import get_password_hash

Base.metadata.create_all(bind=engine)
db = SessionLocal()

nome = input("Nome: ")
username = input("Username: ")
password = input("Password: ")

hashed = get_password_hash(password)
user = create_user(db, nome=nome, username=username, hashed_password=hashed)
print("Usuário criado:", user.username)
db.close()
