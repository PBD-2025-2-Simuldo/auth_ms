from sqlalchemy.orm import Session
from app.models import models

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, nome: str, username: str, hashed_password: str):
    user = models.User(nome=nome, username=username, password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
