# routes/articles_public.py
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from services.article_admin import get_article, get_all_articles

router = APIRouter(prefix="/articles", tags=["Articles Public"])
templates = Jinja2Templates(directory="templates")


# ------------------- Liste des articles (publique) -------------------
@router.get("/", response_class=HTMLResponse)
def list_articles(request: Request):
    articles = get_all_articles()

    # Si la table est vide
    if not articles or len(articles) == 0:
        return templates.TemplateResponse(
            "article_list.html",
            {"request": request, "articles": []}
        )

    return templates.TemplateResponse(
        "article_list.html",
        {"request": request, "articles": articles}
    )


# ------------------- Page d’un article -------------------
@router.get("/{article_id}", response_class=HTMLResponse)
def article_detail(request: Request, article_id: int):
    article = get_article(article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article non trouvé")

    return templates.TemplateResponse(
        "article_detail.html",
        {"request": request, "article": article}
    )
