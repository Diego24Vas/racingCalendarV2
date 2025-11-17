from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date

class PilotoBase(BaseModel):
    nombre: str
    apellido: str
    estatus: Optional[bool] = True
    id_pais: int
    fecha_nacimiento: Optional[date] = None
    numero: Optional[int] = None
    imagen_url: Optional[str] = None

class PilotoCreate(PilotoBase):
    pass

class PilotoUpdate(PilotoBase):
    pass

class PilotoOut(PilotoBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]
    class Config:
        from_attributes = True
