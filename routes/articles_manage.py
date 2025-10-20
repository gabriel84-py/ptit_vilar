# routes/articles_manage.py
from fastapi import APIRouter, Request, Depends, Form, HTTPException, status, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from itsdangerous import URLSafeSerializer
import os, shutil

from services.article_admin import get_all_articles, get_article, create_article, update_article, delete_article

# ------------------- CONFIGURATION -------------------
SECRET_KEY = "ma_cle_super_secrete"
serializer = URLSafeSerializer(SECRET_KEY)
templates = Jinja2Templates(directory="templates")

router = APIRouter(prefix="/admin/articles", tags=["Admin Articles"])
UPLOAD_DIR = "static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


# ------------------- Vérification admin -------------------
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


# ------------------- LISTE DES ARTICLES -------------------
@router.get("/", response_class=HTMLResponse, dependencies=[Depends(require_login)])
def list_articles(request: Request):
    articles = get_all_articles()
    return templates.TemplateResponse("admin_articles.html", {"request": request, "articles": articles})


# ------------------- CRÉER UN ARTICLE -------------------
@router.get("/create", response_class=HTMLResponse, dependencies=[Depends(require_login)])
def create_article_page(request: Request):
    return templates.TemplateResponse("create_article.html", {"request": request})


@router.post("/create", dependencies=[Depends(require_login)])
async def process_create_article(
    request: Request,
    title: str = Form(...),
    subtitle: str = Form(""),
    content: str = Form(...),
    category: str = Form(""),  # ✅ Nouveau champ
    image: UploadFile = File(...)
):
    # Sauvegarde de l'image
    image_path = f"{UPLOAD_DIR}/{image.filename}"
    with open(image_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)
    image_url = f"/{image_path}"

    # Création en base
    create_article(
        title=title,
        subtitle=subtitle,
        content=content,
        category=category,  # ✅ On envoie la catégorie à la BDD
        image_url=image_url
    )
    return RedirectResponse("/admin/articles", status_code=303)



# ------------------- MODIFIER UN ARTICLE -------------------
@router.get("/edit/{article_id}", response_class=HTMLResponse, dependencies=[Depends(require_login)])
def edit_article_page(request: Request, article_id: int):
    article = get_article(article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article non trouvé")
    return templates.TemplateResponse("edit_article.html", {"request": request, "article": article})


@router.post("/edit/{article_id}", dependencies=[Depends(require_login)])
async def process_edit_article(
    request: Request,
    article_id: int,
    title: str = Form(...),
    subtitle: str = Form(""),
    content: str = Form(...),
    category: str = Form(""),  # ✅ Nouveau champ
    image: UploadFile = File(None)
):
    # Gestion d'une nouvelle image (si upload)
    image_url = None
    if image and image.filename != "":
        image_path = f"{UPLOAD_DIR}/{image.filename}"
        with open(image_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        image_url = f"/{image_path}"

    # Mise à jour de l'article
    update_article(
        article_id,
        title,
        subtitle,
        content,
        category,  # ✅ Mettre à jour la catégorie
        image_url or get_article(article_id).image_url
    )
    return RedirectResponse("/admin/articles", status_code=303)



# ------------------- SUPPRIMER UN ARTICLE -------------------
@router.post("/delete/{article_id}", dependencies=[Depends(require_login)])
def process_delete_article(article_id: int):
    delete_article(article_id)
    return RedirectResponse("/admin/articles", status_code=303)


# ------------------- PAGE PUBLIQUE DE L’ARTICLE -------------------
@router.get("/view/{article_id}", response_class=HTMLResponse)
def article_detail(request: Request, article_id: int):
    article = get_article(article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article non trouvé")
    return templates.TemplateResponse("article_detail.html", {"request": request, "article": article})
