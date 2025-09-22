import os
from urllib.parse import quote_plus
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 1) Если задан DATABASE_URL — используем его как есть
database_url = os.getenv("DATABASE_URL")

# 2) Иначе собираем из частей (и ЭКРАНИРУЕМ пароль!)
if not database_url:
    user = os.getenv("POSTGRES_USER", "wg_user")
    password = os.getenv("POSTGRES_PASSWORD", "")
    host = os.getenv("POSTGRES_HOST", "127.0.0.1")
    port = os.getenv("POSTGRES_PORT", "5432")
    dbname = os.getenv("POSTGRES_DB", "wg_db")

    database_url = (
        f"postgresql+psycopg2://{user}:{quote_plus(password)}@{host}:{port}/{dbname}"
    )

engine = create_engine(database_url, future=True, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
