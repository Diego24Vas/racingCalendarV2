from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class CategoriaModel(Base):
    """Modelo de SQLAlchemy para la tabla de categorías"""
    
    __tablename__ = "categorias"
    
    id = Column(String, primary_key=True, index=True)
    nombre = Column(String, unique=True, index=True, nullable=False)
