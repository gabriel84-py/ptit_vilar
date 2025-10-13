import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from pathlib import Path

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_DIR = os.path.join(BASE_DIR, "db_backend")
os.makedirs(DB_DIR, exist_ok=True)  # <-- crée le dossier s'il n'existe pas

BASE_DIR = Path(__file__).resolve().parent  # dossier du projet (ajuste si besoin)
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)               # crée le dossier si absent

DB_PATH = DATA_DIR / "app.db"               # D:\journal-local\ptit_vilar\data\app.db
DATABASE_URL = f"sqlite:///{DB_PATH.as_posix()}"  # <-- CHEMIN CORRECT AVEC "/"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()