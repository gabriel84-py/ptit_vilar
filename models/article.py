from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from database import Base
from datetime import datetime

class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    subtitle = Column(String(42))  # pour les sous-titres
    content = Column(Text, nullable=False)
    image_url = Column(String(255))  # nouveau champ image
    created_at = Column(DateTime, default=datetime.utcnow)
    category = Column(String(200))
    featured = Column(Boolean, default=False)
