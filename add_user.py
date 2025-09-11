from app.database import SessionLocal, Base, engine
from app.models import User
from app.crud import create_user
from app.auth_utils import get_password_hash

Base.metadata.create_all(bind=engine)

def main():
    db = SessionLocal()
    try:
        nome = input("Nome: ").strip()
        username = input("Username: ").strip()
        password = input("Password: ").strip()

        if not nome or not username or not password:
            print("Nome, username e password são obrigatórios.")
            return

        hashed = get_password_hash(password)
        user = create_user(db, nome=nome, username=username, hashed_password=hashed)
        print("Usuário criado:", user.username)
    finally:
        db.close()

if __name__ == "__main__":
    main()
