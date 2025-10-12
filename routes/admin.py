from fastapi import APIRouter, Request, Depends, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from itsdangerous import URLSafeSerializer

from services.delete_user import delete_user
from services.user_exist import user_exist
from services.create_user import create_user
from services.view_users import get_all_users

SECRET_KEY = "ma_cle_super_secrete"
serializer = URLSafeSerializer(SECRET_KEY)

router = APIRouter(prefix="/admin", tags=["Auth"])
templates = Jinja2Templates(directory="templates")

# Dépendance pour vérifier connexion et rôle admin
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

# ------------------- ADMIN DASHBOARD -------------------
@router.get("/", response_class=HTMLResponse, dependencies=[Depends(require_login)])
def dashboard(request: Request):
    return templates.TemplateResponse("admin_dashboard.html", {"request": request})

# ------------------- CREATE USER -------------------
@router.get("/create_user", response_class=HTMLResponse, dependencies=[Depends(require_login)])
def create_user_page(request: Request):
    return templates.TemplateResponse("create_user.html", {"request": request})

@router.get("/endpoint_create_user", response_class=HTMLResponse, dependencies=[Depends(require_login)])
def process_create_user(request: Request, email: str, password: str, is_admin: bool):
    if user_exist(email):
        return templates.TemplateResponse(
            "user_created.html",
            {"request": request, "message": "Utilisateur déjà existant", "success": False},
        )
    create_user(email=email, passwd=password, admin=is_admin)
    return templates.TemplateResponse(
        "user_created.html",
        {"request": request, "message": "Utilisateur créé avec succès", "success": True},
    )

# ------------------- DELETE USER -------------------
@router.get("/delete_user", response_class=HTMLResponse, dependencies=[Depends(require_login)])
def delete_user_page(request: Request):
    return templates.TemplateResponse("delete_user.html", {"request": request})

@router.get("/endpoint_delete_user", response_class=HTMLResponse, dependencies=[Depends(require_login)])
def process_delete_user(request: Request, email: str):
    if not user_exist(email):
        return templates.TemplateResponse(
            "user_created.html",
            {"request": request, "message": "Utilisateur n'existe pas", "success": False},
        )
    delete_user(email=email)
    return templates.TemplateResponse(
        "user_created.html",
        {"request": request, "message": "Utilisateur supprimé avec succès", "success": True},
    )

@router.get("/users", response_class=HTMLResponse, dependencies=[Depends(require_login)])
def viewusers(request: Request):
    users = get_all_users()  # récupère tous les utilisateurs
    return templates.TemplateResponse("view_users.html", {"request": request, "users": users})