from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class CarreraDTO:
    """DTO para transferir datos de carrera"""
    nombre: str
    fecha: datetime
    pais: str
    circuito: str
    latitud: float
    longitud: float
    categoria_id: str
    id: Optional[str] = None


@dataclass
class CrearCarreraDTO:
    """DTO para crear una nueva carrera"""
    nombre: str
    fecha: datetime
    pais: str
    circuito: str
    latitud: float
    longitud: float
    categoria_id: str


@dataclass
class ActualizarCarreraDTO:
    """DTO para actualizar una carrera existente"""
    nombre: Optional[str] = None
    fecha: Optional[datetime] = None
    pais: Optional[str] = None
    circuito: Optional[str] = None
    latitud: Optional[float] = None
    longitud: Optional[float] = None
    categoria_id: Optional[str] = None
