from pydantic import BaseModel, validator, Field
from typing import Optional
from datetime import datetime, date, time
from enum import Enum

class EstadoCarreraEnum(str, Enum):
    programada = 'programada'
    en_curso = 'en_curso'
    finalizada = 'finalizada'
    cancelada = 'cancelada'

class CarreraBase(BaseModel):
    nombre: str = Field(..., min_length=3, max_length=200, description="Nombre de la carrera")
    fecha: date = Field(..., description="Fecha de la carrera")
    hora: Optional[time] = None
    id_categoria: int = Field(..., gt=0, description="ID de la categoría")
    id_circuito: int = Field(..., gt=0, description="ID del circuito")
    id_temporada: int = Field(..., gt=0, description="ID de la temporada")
    estado: Optional[EstadoCarreraEnum] = EstadoCarreraEnum.programada
    numero_vueltas: Optional[int] = Field(None, gt=0, description="Número de vueltas")
    distancia_total: Optional[float] = Field(None, gt=0, description="Distancia total en km")
    
    @validator('fecha')
    def validar_fecha(cls, v):
        if v < date.today():
            raise ValueError('La fecha de la carrera no puede ser en el pasado')
        return v
    
    @validator('numero_vueltas')
    def validar_vueltas(cls, v):
        if v is not None and v <= 0:
            raise ValueError('El número de vueltas debe ser mayor a 0')
        return v

class CarreraCreate(CarreraBase):
    pass

class CarreraUpdate(CarreraBase):
    pass

class CarreraOut(CarreraBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]
    class Config:
        from_attributes = True
