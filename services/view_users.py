from models.user import User
from database import SessionLocal

def get_all_users():
    db = SessionLocal()
    users = db.query(User).all()  # Récupère tous les utilisateurs
    db.close()  # Toujours fermer la session après usage
    return users

if __name__ == "__main__":
    users = get_all_users()
    print("Liste des utilisateurs :")
    for user in users:
        print(f"ID: {user.id} | Email: {user.email}")
