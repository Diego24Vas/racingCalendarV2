from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models.categoria_model import Base
from .models.carrera_model import CarreraModel  # Importar para registrar el modelo
from ...shared.config.settings import settings

# Crear el motor de la base de datos
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False}  # Necesario para SQLite
)

# Crear la sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_tables():
    """Crear las tablas en la base de datos"""
    Base.metadata.create_all(bind=engine)


def get_db():
    """Dependency para obtener la sesión de la base de datos"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
