from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class PaisBase(BaseModel):
    nombreES: str
    nombreEN: str
    iso2: Optional[str] = None
    iso3: Optional[str] = None
    phoneCode: Optional[int] = None

class PaisCreate(PaisBase):
    pass

class PaisUpdate(PaisBase):
    pass

class PaisOut(PaisBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
