# routes/articles_manage.py
from fastapi import APIRouter, Request, Depends, Form, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from itsdangerous import URLSafeSerializer

from services.article_admin import get_all_articles, get_article, create_article, update_article, delete_article

SECRET_KEY = "ma_cle_super_secrete"
serializer = URLSafeSerializer(SECRET_KEY)

router = APIRouter(prefix="/admin/articles", tags=["Articles"])
templates = Jinja2Templates(directory="templates")

# ------------------- Dépendance pour vérifier admin -------------------
def require_login(request: Request):
    token = request.cookies.get("auth")
    if not token:
        raise HTTPException(status_code=status.HTTP_302_FOUND, headers={"Location": "/login"})
    try:
        data = serializer.loads(token)
    except Exception:
        raise HTTPException(status_code=status.HTTP_302_FOUND, headers={"Location": "/login"})
    if not data.get("is_admin"):
        raise HTTPException(status_code=403, detail="Accès refusé")
    return data

# ------------------- LISTE ARTICLES -------------------
@router.get("/", response_class=HTMLResponse, dependencies=[Depends(require_login)])
def list_articles(request: Request):
    articles = get_all_articles()
    return templates.TemplateResponse("admin_articles.html", {"request": request, "articles": articles})

# ------------------- CREATE ARTICLE -------------------
@router.get("/create", response_class=HTMLResponse, dependencies=[Depends(require_login)])
def create_article_page(request: Request):
    return templates.TemplateResponse("create_article.html", {"request": request})

@router.post("/create", dependencies=[Depends(require_login)])
def process_create_article(title: str = Form(...), content: str = Form(...)):
    create_article(title=title, content=content)
    return RedirectResponse("/admin/articles", status_code=303)

# ------------------- EDIT ARTICLE -------------------
@router.get("/edit/{article_id}", response_class=HTMLResponse, dependencies=[Depends(require_login)])
def edit_article_page(request: Request, article_id: int):
    article = get_article(article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article non trouvé")
    return templates.TemplateResponse("edit_article.html", {"request": request, "article": article})

@router.post("/edit/{article_id}", dependencies=[Depends(require_login)])
def process_edit_article(article_id: int, title: str = Form(...), content: str = Form(...)):
    update_article(article_id, title, content)
    return RedirectResponse("/admin/articles", status_code=303)

# ------------------- DELETE ARTICLE -------------------
@router.post("/delete/{article_id}", dependencies=[Depends(require_login)])
def process_delete_article(article_id: int):
    delete_article(article_id)
    return RedirectResponse("/admin/articles", status_code=303)

# ------------------- PAGE PUBLIQUE ARTICLE -------------------
@router.get("/view/{article_id}", response_class=HTMLResponse)
def article_detail(request: Request, article_id: int):
    article = get_article(article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article non trouvé")
    return templates.TemplateResponse("article_detail.html", {"request": request, "article": article})
