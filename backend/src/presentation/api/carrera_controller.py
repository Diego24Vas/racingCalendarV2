from fastapi import APIRouter, HTTPException, Depends, status
from typing import List
from sqlalchemy.orm import Session

from ..schemas.carrera_schema import (
    CarreraSchema,
    CarreraUpdateSchema,
    CarreraResponseSchema,
    MensajeCarreraResponseSchema
)
from ...application.use_cases.carrera_use_case import CarreraUseCase, CarreraNotFoundException
from ...application.dtos.carrera_dto import (
    CrearCarreraDTO,
    ActualizarCarreraDTO
)
from ...infrastructure.repositories.sqlalchemy_carrera_repository import SQLAlchemyCarreraRepository
from ...infrastructure.repositories.sqlalchemy_categoria_repository import SQLAlchemyCategoriaRepository
from ...infrastructure.database.connection import get_db
from ...shared.exceptions.domain_exceptions import (
    CategoriaNoEncontradaException
)

router = APIRouter(prefix="/carreras", tags=["carreras"])


def get_carrera_use_case(db: Session = Depends(get_db)) -> CarreraUseCase:
    """Dependency para obtener el caso de uso de carreras"""
    carrera_repository = SQLAlchemyCarreraRepository(db)
    categoria_repository = SQLAlchemyCategoriaRepository(db)
    return CarreraUseCase(carrera_repository, categoria_repository)


@router.post("/", response_model=MensajeCarreraResponseSchema, status_code=status.HTTP_201_CREATED)
def crear_carrera(
    carrera_data: CarreraSchema,
    use_case: CarreraUseCase = Depends(get_carrera_use_case)
):
    """Crear una nueva carrera"""
    try:
        dto = CrearCarreraDTO(
            nombre=carrera_data.nombre,
            fecha=carrera_data.fecha,
            pais=carrera_data.pais,
            circuito=carrera_data.circuito,
            latitud=carrera_data.latitud,
            longitud=carrera_data.longitud,
            categoria_id=carrera_data.categoria_id
        )
        resultado = use_case.crear_carrera(dto)
        
        return MensajeCarreraResponseSchema(
            mensaje=resultado.mensaje,
            carrera=CarreraResponseSchema(
                id=resultado.carrera.id,
                nombre=resultado.carrera.nombre,
                fecha=resultado.carrera.fecha,
                pais=resultado.carrera.pais,
                circuito=resultado.carrera.circuito,
                latitud=resultado.carrera.latitud,
                longitud=resultado.carrera.longitud,
                categoria_id=resultado.carrera.categoria_id
            )
        )
    except CategoriaNoEncontradaException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/", response_model=List[CarreraResponseSchema])
def obtener_carreras(
    use_case: CarreraUseCase = Depends(get_carrera_use_case)
):
    """Obtener todas las carreras"""
    carreras = use_case.obtener_todas_carreras()
    return [
        CarreraResponseSchema(
            id=carrera.id,
            nombre=carrera.nombre,
            fecha=carrera.fecha,
            pais=carrera.pais,
            circuito=carrera.circuito,
            latitud=carrera.latitud,
            longitud=carrera.longitud,
            categoria_id=carrera.categoria_id
        )
        for carrera in carreras
    ]


@router.get("/{carrera_id}", response_model=CarreraResponseSchema)
def obtener_carrera(
    carrera_id: str,
    use_case: CarreraUseCase = Depends(get_carrera_use_case)
):
    """Obtener una carrera por ID"""
    try:
        carrera = use_case.obtener_carrera_por_id(carrera_id)
        return CarreraResponseSchema(
            id=carrera.id,
            nombre=carrera.nombre,
            fecha=carrera.fecha,
            pais=carrera.pais,
            circuito=carrera.circuito,
            latitud=carrera.latitud,
            longitud=carrera.longitud,
            categoria_id=carrera.categoria_id
        )
    except CarreraNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.get("/categoria/{categoria_id}", response_model=List[CarreraResponseSchema])
def obtener_carreras_por_categoria(
    categoria_id: str,
    use_case: CarreraUseCase = Depends(get_carrera_use_case)
):
    """Obtener todas las carreras de una categoría específica"""
    try:
        carreras = use_case.obtener_carreras_por_categoria(categoria_id)
        return [
            CarreraResponseSchema(
                id=carrera.id,
                nombre=carrera.nombre,
                fecha=carrera.fecha,
                pais=carrera.pais,
                circuito=carrera.circuito,
                latitud=carrera.latitud,
                longitud=carrera.longitud,
                categoria_id=carrera.categoria_id
            )
            for carrera in carreras
        ]
    except CategoriaNoEncontradaException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.put("/{carrera_id}", response_model=MensajeCarreraResponseSchema)
def actualizar_carrera(
    carrera_id: str,
    carrera_data: CarreraUpdateSchema,
    use_case: CarreraUseCase = Depends(get_carrera_use_case)
):
    """Actualizar una carrera existente"""
    try:
        dto = ActualizarCarreraDTO(
            nombre=carrera_data.nombre,
            fecha=carrera_data.fecha,
            pais=carrera_data.pais,
            circuito=carrera_data.circuito,
            latitud=carrera_data.latitud,
            longitud=carrera_data.longitud,
            categoria_id=carrera_data.categoria_id
        )
        resultado = use_case.actualizar_carrera(carrera_id, dto)
        
        return MensajeCarreraResponseSchema(
            mensaje=resultado.mensaje,
            carrera=CarreraResponseSchema(
                id=resultado.carrera.id,
                nombre=resultado.carrera.nombre,
                fecha=resultado.carrera.fecha,
                pais=resultado.carrera.pais,
                circuito=resultado.carrera.circuito,
                latitud=resultado.carrera.latitud,
                longitud=resultado.carrera.longitud,
                categoria_id=resultado.carrera.categoria_id
            )
        )
    except CarreraNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except CategoriaNoEncontradaException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/{carrera_id}", response_model=MensajeCarreraResponseSchema)
def eliminar_carrera(
    carrera_id: str,
    use_case: CarreraUseCase = Depends(get_carrera_use_case)
):
    """Eliminar una carrera"""
    try:
        resultado = use_case.eliminar_carrera(carrera_id)
        
        return MensajeCarreraResponseSchema(
            mensaje=resultado.mensaje,
            carrera=CarreraResponseSchema(
                id=resultado.carrera.id,
                nombre=resultado.carrera.nombre,
                fecha=resultado.carrera.fecha,
                pais=resultado.carrera.pais,
                circuito=resultado.carrera.circuito,
                latitud=resultado.carrera.latitud,
                longitud=resultado.carrera.longitud,
                categoria_id=resultado.carrera.categoria_id
            )
        )
    except CarreraNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
