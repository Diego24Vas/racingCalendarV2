from fastapi import APIRouter, HTTPException, Depends
from typing import List
from sqlalchemy.orm import Session
from models import Categoria, CategoriaUpdate, MensajeResponse, CategoriaResponse
from database import (
    obtener_todas_categorias,
    obtener_categoria_por_id,
    crear_nueva_categoria,
    actualizar_categoria_existente,
    eliminar_categoria_por_id
)
from db_config import get_db

router = APIRouter(prefix="/categorias", tags=["categorias"])

@router.post("/", response_model=MensajeResponse)
def crear_categoria(categoria: Categoria, db: Session = Depends(get_db)):
    """Crear una nueva categoría"""
    nueva_categoria = crear_nueva_categoria(db, categoria.nombre)
    categoria_response = CategoriaResponse(**nueva_categoria)
    
    return MensajeResponse(
        mensaje="Categoría creada exitosamente",
        categoria=categoria_response
    )

@router.get("/", response_model=List[CategoriaResponse])
def obtener_categorias(db: Session = Depends(get_db)):
    """Obtener todas las categorías"""
    categorias = obtener_todas_categorias(db)
    return [CategoriaResponse(**categoria) for categoria in categorias]

@router.get("/{categoria_id}", response_model=CategoriaResponse)
def obtener_categoria(categoria_id: str, db: Session = Depends(get_db)):
    """Obtener una categoría por ID"""
    categoria = obtener_categoria_por_id(db, categoria_id)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    
    return CategoriaResponse(**categoria)

@router.put("/{categoria_id}", response_model=MensajeResponse)
def actualizar_categoria(categoria_id: str, categoria_update: CategoriaUpdate, db: Session = Depends(get_db)):
    """Actualizar una categoría existente"""
    categoria_actualizada = actualizar_categoria_existente(db, categoria_id, categoria_update.nombre)
    categoria_response = CategoriaResponse(**categoria_actualizada)
    
    return MensajeResponse(
        mensaje="Categoría actualizada exitosamente",
        categoria=categoria_response
    )

@router.delete("/{categoria_id}", response_model=MensajeResponse)
def eliminar_categoria(categoria_id: str, db: Session = Depends(get_db)):
    """Eliminar una categoría"""
    categoria_eliminada = eliminar_categoria_por_id(db, categoria_id)
    categoria_response = CategoriaResponse(**categoria_eliminada)
    
    return MensajeResponse(
        mensaje="Categoría eliminada exitosamente",
        categoria=categoria_response
    )
