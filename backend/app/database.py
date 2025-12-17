"""
Estoque Engenho - Database Connection
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
from app.config import settings
from app.models import Base

# Engine do SQLAlchemy
engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,  # Verifica conexão antes de usar
    pool_recycle=3600,   # Recicla conexões a cada hora
    echo=settings.API_DEBUG  # Log de queries em modo debug
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    """
    Dependency para obter sessão do banco de dados
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Inicializa o banco de dados criando todas as tabelas
    """
    Base.metadata.create_all(bind=engine)
    print("✅ Tabelas criadas com sucesso!")


def drop_db():
    """
    Remove todas as tabelas (CUIDADO!)
    """
    Base.metadata.drop_all(bind=engine)
    print("⚠️ Tabelas removidas!")
