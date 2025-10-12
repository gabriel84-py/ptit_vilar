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

@router.post("/check", response_class=HTMLResponse)
def process_login(request: Request, email: str = Form(...), password: str = Form(...)):
    if auth_user(email, password):
        response = RedirectResponse(url="/admin", status_code=303)
        response.set_cookie(key="auth", value="true")  # ✅ cookie de session
        return response
    else:
        return templates.TemplateResponse(
            "login_error.html",
            {"request": request, "email": email},
        )

