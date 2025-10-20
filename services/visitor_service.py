import requests
from models.visitors import Visitor
from database import SessionLocal
from datetime import datetime

def get_city_from_ip(ip: str) -> str:
    try:
        response = requests.get(f"https://ipapi.co/{ip}/json/", timeout=1.5)
        if response.status_code == 200:
            data = response.json()
            return data.get("city", "Inconnue")
    except requests.Timeout:
        # Trop long, on passe
        return "Inconnue"
    except Exception:
        return "Inconnue"
    return "Inconnue"


# --- Enregistrement du visiteur ---
def register_visitor(ip: str, user_agent: str):
    # Anonymisation légère de l’adresse IP (RGPD-friendly)
    if ip.count('.') >= 3:
        ip = ip.rsplit('.', 1)[0] + ".xxx"

    db = SessionLocal()
    visitor = db.query(Visitor).filter_by(ip_address=ip).first()

    # Si c’est une nouvelle IP → nouveau visiteur
    if not visitor:
        city = get_city_from_ip(ip)
        visitor = Visitor(
            ip_address=ip,
            user_agent=user_agent,
            city=city,
            first_visit=datetime.utcnow()
        )
        db.add(visitor)
        db.commit()
        db.refresh(visitor)

    db.close()


# --- Nombre total de visiteurs uniques ---
def get_total_visitors():
    db = SessionLocal()
    total = db.query(Visitor).count()
    db.close()
    return total
