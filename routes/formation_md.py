from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/formation", tags=["md"])

# configure les templates
templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
def dashboard(request: Request):
    return templates.TemplateResponse("formation_md.html", {"request": request})