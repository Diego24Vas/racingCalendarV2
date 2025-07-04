class DomainException(Exception):
    """Excepción base para errores del dominio"""
    pass


class CategoriaNoEncontradaException(DomainException):
    """Excepción lanzada cuando no se encuentra una categoría"""
    
    def __init__(self, categoria_id: str):
        self.categoria_id = categoria_id
        super().__init__(f"La categoría con ID '{categoria_id}' no fue encontrada")


class CategoriaDuplicadaException(DomainException):
    """Excepción lanzada cuando se intenta crear una categoría con nombre duplicado"""
    
    def __init__(self, nombre: str):
        self.nombre = nombre
        super().__init__(f"Ya existe una categoría con el nombre '{nombre}'")


class CategoriaInvalidaException(DomainException):
    """Excepción lanzada cuando los datos de la categoría son inválidos"""
    pass


class CarreraNoEncontradaException(DomainException):
    """Excepción lanzada cuando no se encuentra una carrera"""
    
    def __init__(self, carrera_id: str):
        self.carrera_id = carrera_id
        super().__init__(f"La carrera con ID '{carrera_id}' no fue encontrada")


class CarreraInvalidaException(DomainException):
    """Excepción lanzada cuando los datos de la carrera son inválidos"""
    pass
