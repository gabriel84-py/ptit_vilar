from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from models.article import Article
from database import SessionLocal
import markdown

from services.article_admin import get_article, get_all_articles

router = APIRouter(prefix="/articles", tags=["Articles Public"])
templates = Jinja2Templates(directory="templates")


@router.get("/{article_id}", response_class=HTMLResponse)
def view_article(request: Request, article_id: int):
    db = SessionLocal()
    article = db.query(Article).get(article_id)
    db.close()

    if not article:
        return HTMLResponse("<h1>Article introuvable</h1>", status_code=404)

    # Convertir le contenu Markdown en HTML
    html_content = markdown.markdown(article.content, extensions=["fenced_code", "tables", "toc"])

    return templates.TemplateResponse(
        "article_detail.html",
        {"request": request, "article": article, "html_content": html_content}
    )

