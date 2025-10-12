from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routes import login, admin, index, articles_manage, articles

app = FastAPI()

#Servir le dossier static
app.mount("/static", StaticFiles(directory="static"), name="static")

#Inclure tes routes
app.include_router(login.router)
app.include_router(admin.router)
app.include_router(index.router)
app.include_router(articles_manage.router)
app.include_router(articles.router)