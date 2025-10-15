from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="", tags=["racine"])

#On configure les templates
templates = Jinja2Templates(directory="templates")


@router.get("/categories", response_class=HTMLResponse)
def dashboard(request: Request):
    return templates.TemplateResponse("categories.html", {"request": request})