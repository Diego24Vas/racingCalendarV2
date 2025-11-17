from pydantic import BaseModel, validator, Field
from typing import Optional
from datetime import datetime

class TemporadaBase(BaseModel):
    nombre: str = Field(..., min_length=3, max_length=100, description="Nombre de la temporada")
    año: int = Field(..., ge=2020, le=2030, description="Año de la temporada")
    activa: Optional[bool] = False
    
    @validator('nombre')
    def validar_nombre(cls, v):
        if not v.strip():
            raise ValueError('El nombre no puede estar vacío')
        return v.strip()
    
    @validator('año')
    def validar_año(cls, v):
        año_actual = datetime.now().year
        if v < 2020 or v > año_actual + 5:
            raise ValueError(f'El año debe estar entre 2020 y {año_actual + 5}')
        return v

class TemporadaCreate(TemporadaBase):
    pass

class TemporadaUpdate(TemporadaBase):
    pass

class TemporadaOut(TemporadaBase):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True
