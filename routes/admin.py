from fastapi import APIRouter, Request, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from services.delete_user import delete_user
from services.user_exist import user_exist
from services.create_user import create_user

router = APIRouter(prefix="/admin", tags=["Auth"])

# Templates
templates = Jinja2Templates(directory="templates")

# Dépendance pour vérifier la connexion
def require_login(request: Request):
    auth_cookie = request.cookies.get("auth")
    if auth_cookie != "true":
        # Redirection vers /login si non connecté
        raise HTTPException(status_code=status.HTTP_302_FOUND, headers={"Location": "/login"})

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
    else:
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
    else:
        delete_user(email=email)
        return templates.TemplateResponse(
            "user_created.html",
            {"request": request, "message": "Utilisateur supprimé avec succès", "success": True},
        )
