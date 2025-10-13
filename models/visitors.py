from sqlalchemy import Column, Integer, String, DateTime
from database import Base
from datetime import datetime

class Visitor(Base):
    __tablename__ = "visitors"

    id = Column(Integer, primary_key=True, index=True)
    ip_address = Column(String(100), unique=True)  # l'adresse IP du visiteur
    user_agent = Column(String(255))               # info sur le navigateur
    first_visit = Column(DateTime, default=datetime.utcnow)
