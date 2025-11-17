from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class EquipoBase(BaseModel):
    nombre: str
    id_pais: Optional[int] = None
    fundacion: Optional[int] = None
    imagen_url: Optional[str] = None

class EquipoCreate(EquipoBase):
    pass

class EquipoUpdate(EquipoBase):
    pass

class EquipoOut(EquipoBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]
    class Config:
        from_attributes = True
