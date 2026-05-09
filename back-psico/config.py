"""
Configuración de la base de datos
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Base de datos SQLite local
DATABASE_URL = "sqlite:///./pacientes.db"

# Crear motor de la base de datos
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False, "timeout": 30},
    echo=False,  # Desactivar para producción
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True
)

# Crear sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para los modelos
Base = declarative_base()

def get_db():
    """Obtener sesión de base de datos"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
