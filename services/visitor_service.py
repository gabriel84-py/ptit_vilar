from models.visitor import Visitor
from database import SessionLocal

def register_visitor(ip: str, user_agent: str):
    db = SessionLocal()
    visitor = db.query(Visitor).filter_by(ip_address=ip).first()

    # Si c’est une nouvelle IP → nouveau visiteur
    if not visitor:
        visitor = Visitor(ip_address=ip, user_agent=user_agent)
        db.add(visitor)
        db.commit()
        db.refresh(visitor)

    db.close()

def get_total_visitors():
    db = SessionLocal()
    total = db.query(Visitor).count()
    db.close()
    return total
