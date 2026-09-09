from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from backend.app.core.config import settings

# Motor de conexión SQLAlchemy con reconexión automática (pool_pre_ping)
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=3600,
    echo=False
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db() -> Generator:
    """
    Generador de sesión de base de datos para inyección de dependencias en FastAPI.
    Garantiza el cierre adecuado de la sesión tras cada petición.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
