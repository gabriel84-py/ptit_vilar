from fastapi import APIRouter, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from services.article_admin import get_article, get_all_articles

router = APIRouter(prefix="/articles", tags=["Public"])

templates = Jinja2Templates(directory="templates")

# ------------------- PAGE ARTICLE DÉTAILLÉ -------------------
@router.get("/{article_id}", response_class=HTMLResponse)
def article_detail_page(request: Request, article_id: int):
    article = get_article(article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article non trouvé")
    return templates.TemplateResponse("article_detail.html", {"request": request, "article": article})

# ------------------- LISTE DE TOUS LES ARTICLES -------------------
@router.get("/", response_class=HTMLResponse)
def article_list_page(request: Request):
    articles = get_all_articles()
    if not articles:
        raise HTTPException(status_code=404, detail="Aucun article trouvé")
    return templates.TemplateResponse("article_list.html", {"request": request, "articles": articles})
