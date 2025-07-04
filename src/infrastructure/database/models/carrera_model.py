from sqlalchemy import Column, String, DateTime, Float, ForeignKey
from .categoria_model import Base


class CarreraModel(Base):
    """Modelo de SQLAlchemy para la tabla de carreras"""
    
    __tablename__ = "carreras"
    
    id = Column(String, primary_key=True, index=True)
    nombre = Column(String, nullable=False, index=True)
    fecha = Column(DateTime, nullable=False, index=True)
    pais = Column(String, nullable=False)
    circuito = Column(String, nullable=False)
    latitud = Column(Float, nullable=False)
    longitud = Column(Float, nullable=False)
    categoria_id = Column(String, ForeignKey("categorias.id"), nullable=False, index=True)
    
    # Relación con la categoría
    # categoria = relationship("CategoriaModel", back_populates="carreras")
