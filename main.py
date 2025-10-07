from fastapi import FastAPI
from routes import login, admin
from database import engine, Base

app = FastAPI()

app.include_router(login.router)
app.include_router(admin.router)