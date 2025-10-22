from sqlalchemy import update
from database import SessionLocal
from models.article import Article

db = SessionLocal()

# Mettre toutes les valeurs NULL de `archive` à False
db.execute(update(Article).where(Article.archive == None).values(archive=False))
db.commit()
db.close()
