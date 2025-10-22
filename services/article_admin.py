from models.article import Article
from database import SessionLocal

def get_all_articles():
    db = SessionLocal()
    articles = db.query(Article).filter(Article.archive == False).order_by(Article.created_at.desc()).all()
    db.close()
    return articles

def get_all_archive():
    db = SessionLocal()
    articles = db.query(Article).filter(Article.archive == True).order_by(Article.created_at.desc()).all()
    db.close()
    return articles

def get_article(article_id: int):
    db = SessionLocal()
    article = db.query(Article).filter(Article.id == article_id).first()
    db.close()
    return article

def create_article(title, subtitle, content, category, image_url):
    db = SessionLocal()
    article = Article(
        title=title,
        subtitle=subtitle,
        content=content,
        category=category,
        image_url=image_url
    )
    db.add(article)
    db.commit()
    db.refresh(article)
    return article

def update_article(article_id, title, subtitle, content, category, image_url, featured=None):
    db = SessionLocal()
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        return None
    article.title = title
    article.subtitle = subtitle
    article.content = content
    article.category = category
    article.image_url = image_url
    if featured is not None:
        article.featured = featured
    db.commit()
    return article


def delete_article(article_id: int):
    db = SessionLocal()
    article = db.query(Article).filter(Article.id == article_id).first()
    if article:
        article.archive = True
        db.commit()
    db.close()
    return article

def de_archive(article_id: int):
    db = SessionLocal()
    article = db.query(Article).filter(Article.id == article_id).first()
    if article:
        article.archive = False
        db.commit()
    db.close()
    return article
