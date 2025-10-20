from models.article import Article
from database import SessionLocal

def get_all_articles():
    db = SessionLocal()
    articles = db.query(Article).order_by(Article.created_at.desc()).all()
    db.close()
    return articles

def get_article(article_id: int):
    db = SessionLocal()
    article = db.query(Article).filter(Article.id == article_id).first()
    db.close()
    return article

def create_article(title: str, subtitle: str, content: str, image_url: str):
    db = SessionLocal()
    article = Article(title=title, subtitle=subtitle, content=content, image_url=image_url)
    db.add(article)
    db.commit()
    db.refresh(article)
    db.close()
    return article

def update_article(article_id: int, title: str, subtitle: str, content: str, image_url: str):
    db = SessionLocal()
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        db.close()
        return None
    article.title = title
    article.subtitle = subtitle
    article.content = content
    article.image_url = image_url
    db.commit()
    db.refresh(article)
    db.close()
    return article

def delete_article(article_id: int):
    db = SessionLocal()
    article = db.query(Article).filter(Article.id == article_id).first()
    if article:
        db.delete(article)
        db.commit()
    db.close()
    return article
