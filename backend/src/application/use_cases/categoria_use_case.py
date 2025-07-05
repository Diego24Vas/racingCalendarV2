from typing import List
import uuid
from ..dtos.categoria_dto import CrearCategoriaDTO, ActualizarCategoriaDTO, CategoriaDTO, MensajeRespuestaDTO
from ...domain.entities.categoria import Categoria
from ...domain.repositories.categoria_repository import CategoriaRepository
from ...shared.exceptions.domain_exceptions import (
    CategoriaNoEncontradaException,
    CategoriaDuplicadaException
)


class CategoriaUseCase:
    """Casos de uso para la gestión de categorías"""
    
    def __init__(self, categoria_repository: CategoriaRepository):
        self._categoria_repository = categoria_repository
    
    def obtener_todas_categorias(self) -> List[CategoriaDTO]:
        """Obtener todas las categorías"""
        categorias = self._categoria_repository.obtener_todas()
        return [CategoriaDTO.from_entity(categoria) for categoria in categorias]
    
    def obtener_categoria_por_id(self, categoria_id: str) -> CategoriaDTO:
        """Obtener una categoría por su ID"""
        categoria = self._categoria_repository.obtener_por_id(categoria_id)
        if not categoria:
            raise CategoriaNoEncontradaException(categoria_id)
        
        return CategoriaDTO.from_entity(categoria)
    
    def crear_categoria(self, dto: CrearCategoriaDTO) -> MensajeRespuestaDTO:
        """Crear una nueva categoría"""
        # Verificar si ya existe una categoría con el mismo nombre
        if self._categoria_repository.existe_nombre(dto.nombre):
            raise CategoriaDuplicadaException(dto.nombre)
        
        # Crear la entidad de dominio
        categoria = Categoria(nombre=dto.nombre)
        
        # Asignar un ID único
        categoria.asignar_id(str(uuid.uuid4()))
        
        # Guardar en el repositorio
        categoria_guardada = self._categoria_repository.guardar(categoria)
        
        return MensajeRespuestaDTO(
            mensaje="Categoría creada exitosamente",
            categoria=CategoriaDTO.from_entity(categoria_guardada)
        )
    
    def actualizar_categoria(self, categoria_id: str, dto: ActualizarCategoriaDTO) -> MensajeRespuestaDTO:
        """Actualizar una categoría existente"""
        # Verificar que la categoría existe
        categoria = self._categoria_repository.obtener_por_id(categoria_id)
        if not categoria:
            raise CategoriaNoEncontradaException(categoria_id)
        
        # Verificar si ya existe otra categoría con el mismo nombre
        if self._categoria_repository.existe_nombre(dto.nombre, excluir_id=categoria_id):
            raise CategoriaDuplicadaException(dto.nombre)
        
        # Actualizar la entidad
        categoria.cambiar_nombre(dto.nombre)
        
        # Guardar cambios
        categoria_actualizada = self._categoria_repository.guardar(categoria)
        
        return MensajeRespuestaDTO(
            mensaje="Categoría actualizada exitosamente",
            categoria=CategoriaDTO.from_entity(categoria_actualizada)
        )
    
    def eliminar_categoria(self, categoria_id: str) -> MensajeRespuestaDTO:
        """Eliminar una categoría"""
        # Verificar que la categoría existe
        categoria = self._categoria_repository.obtener_por_id(categoria_id)
        if not categoria:
            raise CategoriaNoEncontradaException(categoria_id)
        
        # Eliminar la categoría
        eliminado = self._categoria_repository.eliminar(categoria_id)
        if not eliminado:
            raise CategoriaNoEncontradaException(categoria_id)
        
        return MensajeRespuestaDTO(
            mensaje="Categoría eliminada exitosamente",
            categoria=CategoriaDTO.from_entity(categoria)
        )
