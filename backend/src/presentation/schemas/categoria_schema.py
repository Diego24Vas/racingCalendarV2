from pydantic import BaseModel, Field
from typing import Optional


class CategoriaSchema(BaseModel):
    """Schema para crear una nueva categoría"""
    nombre: str = Field(..., min_length=2, max_length=100, description="Nombre de la categoría")


class CategoriaUpdateSchema(BaseModel):
    """Schema para actualizar una categoría"""
    nombre: str = Field(..., min_length=2, max_length=100, description="Nuevo nombre de la categoría")


class CategoriaResponseSchema(BaseModel):
    """Schema para la respuesta de una categoría"""
    id: str = Field(..., description="ID único de la categoría")
    nombre: str = Field(..., description="Nombre de la categoría")


class MensajeResponseSchema(BaseModel):
    """Schema para respuestas con mensaje"""
    mensaje: str = Field(..., description="Mensaje de respuesta")
    categoria: Optional[CategoriaResponseSchema] = Field(None, description="Datos de la categoría")
