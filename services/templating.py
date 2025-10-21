# services/templating.py
from fastapi.templating import Jinja2Templates
import markdown as md
from markupsafe import Markup

templates = Jinja2Templates(directory="templates")

def markdown_filter(text: str | None):
    html = md.markdown(text or "", extensions=["extra", "sane_lists", "nl2br"])
    return Markup(html)

# Enregistrer le filtre UNE seule fois, ici
templates.env.filters["markdown"] = markdown_filter