from models.user import User
from database import Base, engine, SessionLocal


def user_exist(email: str):
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    existing_user = db.query(User).filter_by(email=email).first()

    if existing_user:
        return True
    else:
        return False


if __name__ == "__main__":
    print(auth_user("test@hello.com"))