from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PaisBase(BaseModel):
    nombre: str
    codigo_iso: Optional[str] = None

class PaisCreate(PaisBase):
    pass

class PaisUpdate(PaisBase):
    pass

class PaisOut(PaisBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
