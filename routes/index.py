# routes/index.py
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from services.article_admin import get_all_articles
from services.templating import templates 

router = APIRouter(prefix="", tags=["racine"])

@router.get("/", response_class=HTMLResponse)
def dashboard(request: Request):
    articles = get_all_articles()
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "articles": articles}
    )
