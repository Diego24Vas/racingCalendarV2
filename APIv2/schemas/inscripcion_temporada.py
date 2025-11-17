from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class InscripcionTemporadaBase(BaseModel):
    id_piloto: int
    id_categoria: int
    id_temporada: int
    id_equipo: int
    activo: Optional[bool] = True
    puntos_actuales: Optional[float] = 0

class InscripcionTemporadaCreate(InscripcionTemporadaBase):
    pass

class InscripcionTemporadaUpdate(InscripcionTemporadaBase):
    pass

class InscripcionTemporadaOut(InscripcionTemporadaBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]
    class Config:
        from_attributes = True
