from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routes import login, admin

app = FastAPI()

# 🔹 Servir le dossier static
app.mount("/static", StaticFiles(directory="static"), name="static")

# 🔹 Inclure tes routes
app.include_router(login.router)
app.include_router(admin.router)
