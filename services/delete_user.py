from models.user import User
from database import Base, engine, SessionLocal

def delete_user(email: str):
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    user = db.query(User).filter_by(email=email).first()

    if user:
        db.delete(user)
        db.commit()
        print("🗑️ Utilisateur supprimé :", email)
        return True
    else:
        print("❌ Utilisateur non trouvé :", email)
        return False



if __name__ == "__main__":
    user = delete_user("test@hello.com")
