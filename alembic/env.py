# alembic/env.py
import os
from logging.config import fileConfig
from urllib.parse import quote_plus

from sqlalchemy import engine_from_config, pool
from alembic import context
from dotenv import load_dotenv

# Загружаем .env (нужно при локальном запуске без docker-compose)
load_dotenv(".env")

# Alembic config
config = context.config
fileConfig(config.config_file_name)

user = os.getenv("POSTGRES_USER", "wg_user")
password = quote_plus(os.getenv("POSTGRES_PASSWORD", ""))
host = os.getenv("POSTGRES_HOST", "127.0.0.1")
port = os.getenv("POSTGRES_PORT", "5432")
db = os.getenv("POSTGRES_DB", "wg_db")

db_url = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}"
config.set_main_option("sqlalchemy.url", db_url)


def run_migrations_offline():
    """Запуск миграций без подключения к БД (генерация SQL)."""
    context.configure(
        url=config.get_main_option("sqlalchemy.url"),
        literal_binds=True,
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Запуск миграций с подключением к БД."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
