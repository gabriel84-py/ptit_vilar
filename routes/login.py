from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from services.auth_user import auth_user

router = APIRouter(prefix="/login", tags=["Auth"])
templates = Jinja2Templates(directory="templates")

#Page de connexion
@router.get("/", response_class=HTMLResponse)
def show_login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

#Vérification du login
@router.post("/check", response_class=HTMLResponse)
def process_login(request: Request, email: str = Form(...), password: str = Form(...)):
    if auth_user(email, password):
        # Si ok → redirige vers le dashboard admin
        return RedirectResponse(url="/admin", status_code=303)
    else:
        # Sinon → affiche une erreur
        return templates.TemplateResponse(
            "login_error.html",
            {"request": request, "email": email},
        )
