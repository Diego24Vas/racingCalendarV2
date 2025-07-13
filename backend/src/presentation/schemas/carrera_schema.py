from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class CarreraSchema(BaseModel):
    """Schema para crear una nueva carrera"""
    nombre: str = Field(..., min_length=2, max_length=200, description="Nombre de la carrera")
    fecha: datetime = Field(..., description="Fecha y hora de la carrera")
    pais: str = Field(..., min_length=2, max_length=100, description="País donde se realiza la carrera")
    circuito: str = Field(..., min_length=2, max_length=200, description="Nombre del circuito")
    latitud: float = Field(..., ge=-90, le=90, description="Latitud del circuito (-90 a 90)")
    longitud: float = Field(..., ge=-180, le=180, description="Longitud del circuito (-180 a 180)")
    categoria_id: str = Field(..., description="ID de la categoría a la que pertenece")


class CarreraUpdateSchema(BaseModel):
    """Schema para actualizar una carrera"""
    nombre: Optional[str] = Field(None, min_length=2, max_length=200, description="Nuevo nombre de la carrera")
    fecha: Optional[datetime] = Field(None, description="Nueva fecha y hora de la carrera")
    pais: Optional[str] = Field(None, min_length=2, max_length=100, description="Nuevo país donde se realiza la carrera")
    circuito: Optional[str] = Field(None, min_length=2, max_length=200, description="Nuevo nombre del circuito")
    latitud: Optional[float] = Field(None, ge=-90, le=90, description="Nueva latitud del circuito (-90 a 90)")
    longitud: Optional[float] = Field(None, ge=-180, le=180, description="Nueva longitud del circuito (-180 a 180)")
    categoria_id: Optional[str] = Field(None, description="Nuevo ID de la categoría")


class CarreraResponseSchema(BaseModel):
    """Schema para la respuesta de una carrera"""
    id: str = Field(..., description="ID único de la carrera")
    nombre: str = Field(..., description="Nombre de la carrera")
    fecha: datetime = Field(..., description="Fecha y hora de la carrera")
    pais: str = Field(..., description="País donde se realiza la carrera")
    circuito: str = Field(..., description="Nombre del circuito")
    latitud: float = Field(..., description="Latitud del circuito")
    longitud: float = Field(..., description="Longitud del circuito")
    categoria_id: str = Field(..., description="ID de la categoría a la que pertenece")


class MensajeCarreraResponseSchema(BaseModel):
    """Schema para respuestas con mensaje y carrera"""
    mensaje: str = Field(..., description="Mensaje de respuesta")
    carrera: Optional[CarreraResponseSchema] = Field(None, description="Datos de la carrera")
