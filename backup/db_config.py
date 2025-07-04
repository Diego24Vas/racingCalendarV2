from sqlalchemy import create_engine, Column, String, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Configuración de la base de datos SQLite
DATABASE_URL = "sqlite:///./calendarRacing.db"

# Crear el motor de la base de datos
engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False}  # Necesario para SQLite
)

# Crear la sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para los modelos
Base = declarative_base()

# Modelo de la tabla Categoria
class CategoriaDB(Base):
    __tablename__ = "categorias"
    
    id = Column(String, primary_key=True, index=True)
    nombre = Column(String, unique=True, index=True, nullable=False)

# Crear las tablas en la base de datos
def create_tables():
    Base.metadata.create_all(bind=engine)

# Dependency para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
