from abc import ABC, abstractmethod
from typing import List, Optional
from ..entities.carrera import Carrera


class CarreraRepository(ABC):
    """Interfaz del repositorio para carreras"""
    
    @abstractmethod
    def crear(self, carrera: Carrera) -> Carrera:
        """Crear una nueva carrera"""
        pass
    
    @abstractmethod
    def obtener_por_id(self, id: str) -> Optional[Carrera]:
        """Obtener una carrera por su ID"""
        pass
    
    @abstractmethod
    def obtener_todas(self) -> List[Carrera]:
        """Obtener todas las carreras"""
        pass
    
    @abstractmethod
    def obtener_por_categoria(self, categoria_id: str) -> List[Carrera]:
        """Obtener todas las carreras de una categoría específica"""
        pass
    
    @abstractmethod
    def actualizar(self, carrera: Carrera) -> Carrera:
        """Actualizar una carrera existente"""
        pass
    
    @abstractmethod
    def eliminar(self, id: str) -> bool:
        """Eliminar una carrera por su ID"""
        pass
