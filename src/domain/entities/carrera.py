from typing import Optional
from datetime import datetime


class Carrera:
    """Entidad de dominio para Carrera"""
    
    def __init__(
        self, 
        nombre: str, 
        fecha: datetime, 
        pais: str, 
        circuito: str, 
        latitud: float, 
        longitud: float,
        categoria_id: str,
        id: Optional[str] = None
    ):
        self._id = id
        self._nombre = self._validate_nombre(nombre)
        self._fecha = self._validate_fecha(fecha)
        self._pais = self._validate_pais(pais)
        self._circuito = self._validate_circuito(circuito)
        self._latitud = self._validate_latitud(latitud)
        self._longitud = self._validate_longitud(longitud)
        self._categoria_id = self._validate_categoria_id(categoria_id)
    
    @property
    def id(self) -> Optional[str]:
        return self._id
    
    @property
    def nombre(self) -> str:
        return self._nombre
    
    @property
    def fecha(self) -> datetime:
        return self._fecha
    
    @property
    def pais(self) -> str:
        return self._pais
    
    @property
    def circuito(self) -> str:
        return self._circuito
    
    @property
    def latitud(self) -> float:
        return self._latitud
    
    @property
    def longitud(self) -> float:
        return self._longitud
    
    @property
    def categoria_id(self) -> str:
        return self._categoria_id
    
    def cambiar_nombre(self, nuevo_nombre: str) -> None:
        """Cambiar el nombre de la carrera"""
        self._nombre = self._validate_nombre(nuevo_nombre)
    
    def cambiar_fecha(self, nueva_fecha: datetime) -> None:
        """Cambiar la fecha de la carrera"""
        self._fecha = self._validate_fecha(nueva_fecha)
    
    def cambiar_ubicacion(self, nuevo_pais: str, nuevo_circuito: str, 
                         nueva_latitud: float, nueva_longitud: float) -> None:
        """Cambiar la ubicación de la carrera"""
        self._pais = self._validate_pais(nuevo_pais)
        self._circuito = self._validate_circuito(nuevo_circuito)
        self._latitud = self._validate_latitud(nueva_latitud)
        self._longitud = self._validate_longitud(nueva_longitud)
    
    def asignar_id(self, id: str) -> None:
        """Asignar un ID a la carrera"""
        if self._id is None:
            self._id = id
        else:
            raise ValueError("La carrera ya tiene un ID asignado")
    
    def _validate_nombre(self, nombre: str) -> str:
        """Validar que el nombre cumpla con las reglas de negocio"""
        if not nombre or not nombre.strip():
            raise ValueError("El nombre de la carrera no puede estar vacío")
        
        if len(nombre.strip()) < 2:
            raise ValueError("El nombre de la carrera debe tener al menos 2 caracteres")
        
        if len(nombre.strip()) > 200:
            raise ValueError("El nombre de la carrera no puede tener más de 200 caracteres")
        
        return nombre.strip()
    
    def _validate_fecha(self, fecha: datetime) -> datetime:
        """Validar que la fecha sea válida"""
        if not isinstance(fecha, datetime):
            raise ValueError("La fecha debe ser un objeto datetime")
        return fecha
    
    def _validate_pais(self, pais: str) -> str:
        """Validar que el país cumpla con las reglas de negocio"""
        if not pais or not pais.strip():
            raise ValueError("El país no puede estar vacío")
        
        if len(pais.strip()) < 2:
            raise ValueError("El país debe tener al menos 2 caracteres")
        
        if len(pais.strip()) > 100:
            raise ValueError("El país no puede tener más de 100 caracteres")
        
        return pais.strip()
    
    def _validate_circuito(self, circuito: str) -> str:
        """Validar que el circuito cumpla con las reglas de negocio"""
        if not circuito or not circuito.strip():
            raise ValueError("El circuito no puede estar vacío")
        
        if len(circuito.strip()) < 2:
            raise ValueError("El circuito debe tener al menos 2 caracteres")
        
        if len(circuito.strip()) > 200:
            raise ValueError("El circuito no puede tener más de 200 caracteres")
        
        return circuito.strip()
    
    def _validate_latitud(self, latitud: float) -> float:
        """Validar que la latitud esté en rango válido"""
        if not isinstance(latitud, (int, float)):
            raise ValueError("La latitud debe ser un número")
        
        if latitud < -90 or latitud > 90:
            raise ValueError("La latitud debe estar entre -90 y 90 grados")
        
        return float(latitud)
    
    def _validate_longitud(self, longitud: float) -> float:
        """Validar que la longitud esté en rango válido"""
        if not isinstance(longitud, (int, float)):
            raise ValueError("La longitud debe ser un número")
        
        if longitud < -180 or longitud > 180:
            raise ValueError("La longitud debe estar entre -180 y 180 grados")
        
        return float(longitud)
    
    def _validate_categoria_id(self, categoria_id: str) -> str:
        """Validar que el ID de categoría no esté vacío"""
        if not categoria_id or not categoria_id.strip():
            raise ValueError("El ID de categoría no puede estar vacío")
        
        return categoria_id.strip()
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Carrera):
            return False
        return (self._id == other._id and 
                self._nombre == other._nombre and
                self._fecha == other._fecha and
                self._categoria_id == other._categoria_id)
    
    def __str__(self) -> str:
        return f"Carrera(id={self._id}, nombre='{self._nombre}', fecha={self._fecha}, categoria_id='{self._categoria_id}')"
