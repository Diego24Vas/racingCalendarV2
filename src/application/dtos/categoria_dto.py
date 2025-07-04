from dataclasses import dataclass
from typing import Optional


@dataclass
class CrearCategoriaDTO:
    """DTO para crear una nueva categoría"""
    nombre: str


@dataclass
class ActualizarCategoriaDTO:
    """DTO para actualizar una categoría existente"""
    nombre: str


@dataclass
class CategoriaDTO:
    """DTO para representar una categoría"""
    id: str
    nombre: str
    
    @classmethod
    def from_entity(cls, categoria) -> 'CategoriaDTO':
        """Crear un DTO a partir de una entidad de dominio"""
        return cls(
            id=categoria.id,
            nombre=categoria.nombre
        )


@dataclass
class MensajeRespuestaDTO:
    """DTO para respuestas con mensaje"""
    mensaje: str
    categoria: Optional[CategoriaDTO] = None
