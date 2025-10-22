from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

import os
import sys

# --- Ajout du chemin du projet pour les imports ---
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# --- Importation de ta base et de tes modèles ---
from database import Base  # Ton fichier database.py doit définir Base = declarative_base()
      # Importe tous les modèles (articles, users, etc.)
from models.article import Article
from models.user import User
from models.visitors import Visitor
# --- Configuration Alembic ---
config = context.config

# Lecture du fichier alembic.ini pour les logs
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# C’est ici qu’Alembic récupère la structure de ta base
target_metadata = Base.metadata


def run_migrations_offline():
    """Exécution des migrations en mode 'offline'."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Exécution des migrations en mode 'online'."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type = True
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
