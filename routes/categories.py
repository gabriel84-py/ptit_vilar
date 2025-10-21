# routes/categories.py
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from services.article_admin import get_all_articles

templates = Jinja2Templates(directory="templates")
router = APIRouter(prefix="/categories", tags=["Categories"])

@router.get("/", name="categories_page")
def categories_page(request: Request, category: str = "", search: str = ""):
    """
    Affiche tous les articles filtrés par catégorie et recherche.
    """
    all_articles = get_all_articles()

    # Filtrage par catégorie
    if category:
        all_articles = [a for a in all_articles if a.category == category]

    # Filtrage par recherche
    if search:
        search_lower = search.lower()
        all_articles = [a for a in all_articles if search_lower in a.title.lower() or search_lower in a.subtitle.lower()]

    categories_list = [
        "Vie du lycée", "Science et Progrès", "Culture et Arts",
        "Sport", "Un oeil sur le monde", "Autres", "Orientation"
    ]

    return templates.TemplateResponse(
        "categories.html",
        {"request": request, "articles": all_articles, "categories": categories_list, "selected_category": category, "search": search}
    )
