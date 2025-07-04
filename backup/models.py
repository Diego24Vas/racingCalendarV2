from pydantic import BaseModel
from typing import Optional

class Categoria(BaseModel):
    id: Optional[str] = None
    nombre: str

class CategoriaUpdate(BaseModel):
    nombre: str

class CategoriaResponse(BaseModel):
    id: str
    nombre: str

class MensajeResponse(BaseModel):
    mensaje: str
    categoria: Optional[CategoriaResponse] = None
