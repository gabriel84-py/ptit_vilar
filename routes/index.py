from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from services.article_admin import get_article, get_all_articles

router = APIRouter(prefix="", tags=["racine"])

#On configure les templates
templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
def dashboard(request: Request):
    articles = get_all_articles()
    return templates.TemplateResponse("index.html", {"request": request, "article": articles})