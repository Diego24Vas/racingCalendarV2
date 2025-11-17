from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CircuitoBase(BaseModel):
    nombre: str
    ciudad: str
    id_pais: int
    latitud: Optional[float] = None
    longitud: Optional[float] = None
    descripcion: Optional[str] = None
    imagen_url: Optional[str] = None

class CircuitoCreate(CircuitoBase):
    pass

class CircuitoUpdate(CircuitoBase):
    pass

class CircuitoOut(CircuitoBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]
    class Config:
        from_attributes = True
