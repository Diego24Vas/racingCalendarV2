from typing import Optional


class Categoria:
    """Entidad de dominio para Categoria"""
    
    def __init__(self, nombre: str, id: Optional[str] = None):
        self._id = id
        self._nombre = self._validate_nombre(nombre)
    
    @property
    def id(self) -> Optional[str]:
        return self._id
    
    @property
    def nombre(self) -> str:
        return self._nombre
    
    def cambiar_nombre(self, nuevo_nombre: str) -> None:
        """Cambiar el nombre de la categoría"""
        self._nombre = self._validate_nombre(nuevo_nombre)
    
    def asignar_id(self, id: str) -> None:
        """Asignar un ID a la categoría"""
        if self._id is None:
            self._id = id
        else:
            raise ValueError("La categoría ya tiene un ID asignado")
    
    def _validate_nombre(self, nombre: str) -> str:
        """Validar que el nombre cumpla con las reglas de negocio"""
        if not nombre or not nombre.strip():
            raise ValueError("El nombre de la categoría no puede estar vacío")
        
        if len(nombre.strip()) < 2:
            raise ValueError("El nombre de la categoría debe tener al menos 2 caracteres")
        
        if len(nombre.strip()) > 100:
            raise ValueError("El nombre de la categoría no puede tener más de 100 caracteres")
        
        return nombre.strip()
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Categoria):
            return False
        return self._id == other._id and self._nombre == other._nombre
    
    def __str__(self) -> str:
        return f"Categoria(id={self._id}, nombre='{self._nombre}')"
    
    def __repr__(self) -> str:
        return self.__str__()
