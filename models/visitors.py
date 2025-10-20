from sqlalchemy import Column, Integer, String, DateTime
from database import Base
from datetime import datetime

class Visitor(Base):
    __tablename__ = "visitors"

    id = Column(Integer, primary_key=True, index=True)
    ip_address = Column(String(100), unique=True)  # adresse IP anonymisée
    user_agent = Column(String(255))               # info sur le navigateur
    city = Column(String(100))                     # ville du visiteur
    first_visit = Column(DateTime, default=datetime.utcnow)
