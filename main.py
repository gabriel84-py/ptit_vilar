#main.py
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from routes import login, admin, index, articles_manage, articles, categories, formation_md
from services.visitor_service import register_visitor
from database import Base, engine
from itsdangerous import URLSafeSerializer, BadSignature
from config import serializer

Base.metadata.create_all(bind=engine)

app = FastAPI()

#Servir le dossier static
app.mount("/static", StaticFiles(directory="static"), name="static")

#Inclure tes routes
@app.middleware("http")
async def count_unique_visitors(request: Request, call_next):
    client_ip = request.client.host
    user_agent = request.headers.get("user-agent", "unknown")

    # Enregistre uniquement si c’est une IP nouvelle
    register_visitor(client_ip, user_agent)

    response = await call_next(request)
    return response

@app.middleware("http")
async def load_user_from_cookie(request: Request, call_next):
    request.state.user = None
    token = request.cookies.get("auth")
    if token:
        try:
            request.state.user = serializer.loads(token)
        except BadSignature:
            pass
    return await call_next(request)

app.include_router(login.router)
app.include_router(admin.router)
app.include_router(index.router)
app.include_router(articles_manage.router)
app.include_router(articles.router)
app.include_router(categories.router)
app.include_router(formation_md.router)