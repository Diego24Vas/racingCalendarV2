from fastapi import APIRouter, HTTPException, Depends, status
from typing import List
from sqlalchemy.orm import Session

from ..schemas.categoria_schema import (
    CategoriaSchema,
    CategoriaUpdateSchema,
    CategoriaResponseSchema,
    MensajeResponseSchema
)
from ...application.use_cases.categoria_use_case import CategoriaUseCase
from ...application.dtos.categoria_dto import (
    CrearCategoriaDTO,
    ActualizarCategoriaDTO,
    CategoriaDTO
)
from ...infrastructure.repositories.sqlalchemy_categoria_repository import SQLAlchemyCategoriaRepository
from ...infrastructure.database.connection import get_db
from ...shared.exceptions.domain_exceptions import (
    CategoriaNoEncontradaException,
    CategoriaDuplicadaException,
    CategoriaInvalidaException
)

router = APIRouter(prefix="/categorias", tags=["categorias"])


def get_categoria_use_case(db: Session = Depends(get_db)) -> CategoriaUseCase:
    """Dependency para obtener el caso de uso de categorías"""
    categoria_repository = SQLAlchemyCategoriaRepository(db)
    return CategoriaUseCase(categoria_repository)


@router.post("/", response_model=MensajeResponseSchema, status_code=status.HTTP_201_CREATED)
def crear_categoria(
    categoria_data: CategoriaSchema,
    use_case: CategoriaUseCase = Depends(get_categoria_use_case)
):
    """Crear una nueva categoría"""
    try:
        dto = CrearCategoriaDTO(nombre=categoria_data.nombre)
        resultado = use_case.crear_categoria(dto)
        
        return MensajeResponseSchema(
            mensaje=resultado.mensaje,
            categoria=CategoriaResponseSchema(
                id=resultado.categoria.id,
                nombre=resultado.categoria.nombre
            )
        )
    except CategoriaDuplicadaException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except CategoriaInvalidaException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/", response_model=List[CategoriaResponseSchema])
def obtener_categorias(
    use_case: CategoriaUseCase = Depends(get_categoria_use_case)
):
    """Obtener todas las categorías"""
    categorias = use_case.obtener_todas_categorias()
    return [
        CategoriaResponseSchema(id=cat.id, nombre=cat.nombre)
        for cat in categorias
    ]


@router.get("/{categoria_id}", response_model=CategoriaResponseSchema)
def obtener_categoria(
    categoria_id: str,
    use_case: CategoriaUseCase = Depends(get_categoria_use_case)
):
    """Obtener una categoría por ID"""
    try:
        categoria = use_case.obtener_categoria_por_id(categoria_id)
        return CategoriaResponseSchema(
            id=categoria.id,
            nombre=categoria.nombre
        )
    except CategoriaNoEncontradaException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.put("/{categoria_id}", response_model=MensajeResponseSchema)
def actualizar_categoria(
    categoria_id: str,
    categoria_data: CategoriaUpdateSchema,
    use_case: CategoriaUseCase = Depends(get_categoria_use_case)
):
    """Actualizar una categoría existente"""
    try:
        dto = ActualizarCategoriaDTO(nombre=categoria_data.nombre)
        resultado = use_case.actualizar_categoria(categoria_id, dto)
        
        return MensajeResponseSchema(
            mensaje=resultado.mensaje,
            categoria=CategoriaResponseSchema(
                id=resultado.categoria.id,
                nombre=resultado.categoria.nombre
            )
        )
    except CategoriaNoEncontradaException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except CategoriaDuplicadaException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except CategoriaInvalidaException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/{categoria_id}", response_model=MensajeResponseSchema)
def eliminar_categoria(
    categoria_id: str,
    use_case: CategoriaUseCase = Depends(get_categoria_use_case)
):
    """Eliminar una categoría"""
    try:
        resultado = use_case.eliminar_categoria(categoria_id)
        
        return MensajeResponseSchema(
            mensaje=resultado.mensaje,
            categoria=CategoriaResponseSchema(
                id=resultado.categoria.id,
                nombre=resultado.categoria.nombre
            )
        )
    except CategoriaNoEncontradaException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
