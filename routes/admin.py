from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from services.user_exist import user_exist
from services.create_user import create_user

router = APIRouter(prefix="/admin", tags=["Auth"])

#On configure les templates
templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
def dashboard(request: Request):
    return templates.TemplateResponse("admin_dashboard.html", {"request": request})


@router.get("/create_user", response_class=HTMLResponse)
def create_user_page(request: Request):
    return templates.TemplateResponse("create_user.html", {"request": request})


@router.get("/endpoint_create_user", response_class=HTMLResponse)
def process_login(request: Request, email: str, password: str, is_admin: bool):
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

@router.get("/delete_user", response_class=HTMLResponse)
def create_user_page(request: Request):
    return templates.TemplateResponse("delete_user.html", {"request": request})