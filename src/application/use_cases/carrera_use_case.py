from typing import List
import uuid
from ..dtos.carrera_dto import CrearCarreraDTO, ActualizarCarreraDTO, CarreraDTO
from ...domain.entities.carrera import Carrera
from ...domain.repositories.carrera_repository import CarreraRepository
from ...domain.repositories.categoria_repository import CategoriaRepository
from ...shared.exceptions.domain_exceptions import (
    CategoriaNoEncontradaException
)


class CarreraNotFoundException(Exception):
    """Excepción cuando no se encuentra una carrera"""
    def __init__(self, carrera_id: str):
        super().__init__(f"No se encontró la carrera con ID: {carrera_id}")


class MensajeRespuestaCarreraDTO:
    """DTO para respuestas con mensaje y carrera"""
    def __init__(self, mensaje: str, carrera: CarreraDTO = None):
        self.mensaje = mensaje
        self.carrera = carrera


class CarreraUseCase:
    """Casos de uso para la gestión de carreras"""
    
    def __init__(self, carrera_repository: CarreraRepository, categoria_repository: CategoriaRepository):
        self._carrera_repository = carrera_repository
        self._categoria_repository = categoria_repository
    
    def obtener_todas_carreras(self) -> List[CarreraDTO]:
        """Obtener todas las carreras"""
        carreras = self._carrera_repository.obtener_todas()
        return [self._entity_to_dto(carrera) for carrera in carreras]
    
    def obtener_carrera_por_id(self, carrera_id: str) -> CarreraDTO:
        """Obtener una carrera por su ID"""
        carrera = self._carrera_repository.obtener_por_id(carrera_id)
        if not carrera:
            raise CarreraNotFoundException(carrera_id)
        
        return self._entity_to_dto(carrera)
    
    def obtener_carreras_por_categoria(self, categoria_id: str) -> List[CarreraDTO]:
        """Obtener todas las carreras de una categoría específica"""
        # Verificar que la categoría existe
        categoria = self._categoria_repository.obtener_por_id(categoria_id)
        if not categoria:
            raise CategoriaNoEncontradaException(categoria_id)
        
        carreras = self._carrera_repository.obtener_por_categoria(categoria_id)
        return [self._entity_to_dto(carrera) for carrera in carreras]
    
    def crear_carrera(self, dto: CrearCarreraDTO) -> MensajeRespuestaCarreraDTO:
        """Crear una nueva carrera"""
        # Verificar que la categoría existe
        categoria = self._categoria_repository.obtener_por_id(dto.categoria_id)
        if not categoria:
            raise CategoriaNoEncontradaException(dto.categoria_id)
        
        # Crear la entidad de dominio
        carrera = Carrera(
            nombre=dto.nombre,
            fecha=dto.fecha,
            pais=dto.pais,
            circuito=dto.circuito,
            latitud=dto.latitud,
            longitud=dto.longitud,
            categoria_id=dto.categoria_id
        )
        
        # Asignar un ID único
        carrera.asignar_id(str(uuid.uuid4()))
        
        # Guardar en el repositorio
        carrera_guardada = self._carrera_repository.crear(carrera)
        
        return MensajeRespuestaCarreraDTO(
            mensaje="Carrera creada exitosamente",
            carrera=self._entity_to_dto(carrera_guardada)
        )
    
    def actualizar_carrera(self, carrera_id: str, dto: ActualizarCarreraDTO) -> MensajeRespuestaCarreraDTO:
        """Actualizar una carrera existente"""
        # Verificar que la carrera existe
        carrera = self._carrera_repository.obtener_por_id(carrera_id)
        if not carrera:
            raise CarreraNotFoundException(carrera_id)
        
        # Si se está cambiando la categoría, verificar que existe
        if dto.categoria_id and dto.categoria_id != carrera.categoria_id:
            categoria = self._categoria_repository.obtener_por_id(dto.categoria_id)
            if not categoria:
                raise CategoriaNoEncontradaException(dto.categoria_id)
        
        # Actualizar la entidad con los campos proporcionados
        if dto.nombre is not None:
            carrera.cambiar_nombre(dto.nombre)
        
        if dto.fecha is not None:
            carrera.cambiar_fecha(dto.fecha)
        
        if any([dto.pais, dto.circuito, dto.latitud is not None, dto.longitud is not None]):
            pais = dto.pais if dto.pais is not None else carrera.pais
            circuito = dto.circuito if dto.circuito is not None else carrera.circuito
            latitud = dto.latitud if dto.latitud is not None else carrera.latitud
            longitud = dto.longitud if dto.longitud is not None else carrera.longitud
            carrera.cambiar_ubicacion(pais, circuito, latitud, longitud)
        
        # Actualizar categoría si se proporcionó
        if dto.categoria_id is not None:
            # Crear nueva carrera con la nueva categoría (limitación del diseño actual)
            carrera_actualizada = Carrera(
                nombre=carrera.nombre,
                fecha=carrera.fecha,
                pais=carrera.pais,
                circuito=carrera.circuito,
                latitud=carrera.latitud,
                longitud=carrera.longitud,
                categoria_id=dto.categoria_id,
                id=carrera.id
            )
        else:
            carrera_actualizada = carrera
        
        # Guardar cambios
        carrera_guardada = self._carrera_repository.actualizar(carrera_actualizada)
        
        return MensajeRespuestaCarreraDTO(
            mensaje="Carrera actualizada exitosamente",
            carrera=self._entity_to_dto(carrera_guardada)
        )
    
    def eliminar_carrera(self, carrera_id: str) -> MensajeRespuestaCarreraDTO:
        """Eliminar una carrera"""
        # Verificar que la carrera existe
        carrera = self._carrera_repository.obtener_por_id(carrera_id)
        if not carrera:
            raise CarreraNotFoundException(carrera_id)
        
        # Eliminar la carrera
        eliminado = self._carrera_repository.eliminar(carrera_id)
        if not eliminado:
            raise CarreraNotFoundException(carrera_id)
        
        return MensajeRespuestaCarreraDTO(
            mensaje="Carrera eliminada exitosamente",
            carrera=self._entity_to_dto(carrera)
        )
    
    def _entity_to_dto(self, carrera: Carrera) -> CarreraDTO:
        """Convertir entidad a DTO"""
        return CarreraDTO(
            id=carrera.id,
            nombre=carrera.nombre,
            fecha=carrera.fecha,
            pais=carrera.pais,
            circuito=carrera.circuito,
            latitud=carrera.latitud,
            longitud=carrera.longitud,
            categoria_id=carrera.categoria_id
        )
