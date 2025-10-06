from models.user import User
from database import Base, engine, SessionLocal
import hashlib

def create_user(email: str, passwd: str):
    Base.metadata.create_all(bind=engine)
    passwd = bytes(passwd, "utf-8")
    hash_one = hashlib.sha512(passwd).hexdigest()

    db = SessionLocal()

    new_user = User(email=email, hashed_password=hash_one)

    existing_user = db.query(User).filter_by(email=email).first()

    if existing_user:
        print("Utilisateur déjà existant :", existing_user)
        return existing_user
    else:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)  # <= seulement ici, après ajout réussi
        print("Utilisateur ajouté :", new_user)

        return new_user


if __name__ == "__main__":
    user = create_user("test@hello.com", "hello")
    print(user.id)
    print(user.email)
