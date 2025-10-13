from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from services.auth_user import auth_user
from itsdangerous import URLSafeSerializer

SECRET_KEY = "ma_cle_super_secrete"  # Change pour quelque chose de complexe
serializer = URLSafeSerializer(SECRET_KEY)

router = APIRouter(prefix="/login", tags=["Auth"])
templates = Jinja2Templates(directory="templates")

# Page de connexion
@router.get("/", response_class=HTMLResponse)
def show_login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

# Vérification du login
@router.post("/check", response_class=HTMLResponse)
def process_login(request: Request, email: str = Form(...), password: str = Form(...)):
    if auth_user(email, password):
        # Génère un token signé
        token = serializer.dumps({"email": email, "is_admin": True})
        response = RedirectResponse(url="/admin", status_code=303)
        response.set_cookie(key="auth", value=token, httponly=True)
        return response
    else:
        return templates.TemplateResponse(
            "login_error.html",
            {"request": request, "email": email},
        )

# Logout
@router.get("/logout")
def logout():
    response = RedirectResponse(url="/login", status_code=303)
    response.delete_cookie("auth")
    return response

