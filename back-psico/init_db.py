"""
Script para inicializar la base de datos
"""
from config import engine, Base
from models import Paciente


def crear_tablas():
    """Crear todas las tablas en la base de datos"""
    print("Creando tablas...")
    Base.metadata.create_all(bind=engine)
    print("✓ Tablas creadas exitosamente")


if __name__ == "__main__":
    crear_tablas()
