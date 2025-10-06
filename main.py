from fastapi import FastAPI
from routes import login
from database import engine, Base

app = FastAPI()

app.include_router(login.router)