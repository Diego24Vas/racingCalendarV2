from abc import ABC, abstractmethod
from typing import List, Optional
from ..entities.categoria import Categoria


class CategoriaRepository(ABC):
    """Interfaz abstracta para el repositorio de categorías"""
    
    @abstractmethod
    def obtener_todas(self) -> List[Categoria]:
        """Obtener todas las categorías"""
        pass
    
    @abstractmethod
    def obtener_por_id(self, categoria_id: str) -> Optional[Categoria]:
        """Obtener una categoría por su ID"""
        pass
    
    @abstractmethod
    def obtener_por_nombre(self, nombre: str) -> Optional[Categoria]:
        """Obtener una categoría por su nombre"""
        pass
    
    @abstractmethod
    def guardar(self, categoria: Categoria) -> Categoria:
        """Guardar una categoría (crear o actualizar)"""
        pass
    
    @abstractmethod
    def eliminar(self, categoria_id: str) -> bool:
        """Eliminar una categoría por su ID"""
        pass
    
    @abstractmethod
    def existe_nombre(self, nombre: str, excluir_id: Optional[str] = None) -> bool:
        """Verificar si existe una categoría con el nombre dado"""
        pass
