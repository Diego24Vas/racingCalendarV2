from typing import List, Optional
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import uuid

from db_config import CategoriaDB

def obtener_todas_categorias(db: Session) -> List[dict]:
    """Obtener todas las categorías de la base de datos"""
    categorias = db.query(CategoriaDB).all()
    return [{"id": cat.id, "nombre": cat.nombre} for cat in categorias]

def obtener_categoria_por_id(db: Session, categoria_id: str) -> Optional[dict]:
    """Obtener una categoría específica por ID"""
    categoria = db.query(CategoriaDB).filter(CategoriaDB.id == categoria_id).first()
    if categoria:
        return {"id": categoria.id, "nombre": categoria.nombre}
    return None

def crear_nueva_categoria(db: Session, nombre: str) -> dict:
    """Crear una nueva categoría"""
    # Generar ID único
    categoria_id = str(uuid.uuid4())
    
    # Crear nueva categoría
    nueva_categoria = CategoriaDB(id=categoria_id, nombre=nombre)
    
    try:
        db.add(nueva_categoria)
        db.commit()
        db.refresh(nueva_categoria)
        return {"id": nueva_categoria.id, "nombre": nueva_categoria.nombre}
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Ya existe una categoría con ese nombre")

def actualizar_categoria_existente(db: Session, categoria_id: str, nuevo_nombre: str) -> dict:
    """Actualizar una categoría existente"""
    categoria = db.query(CategoriaDB).filter(CategoriaDB.id == categoria_id).first()
    
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    
    # Verificar si ya existe otra categoría con el mismo nombre
    categoria_existente = db.query(CategoriaDB).filter(
        CategoriaDB.nombre == nuevo_nombre,
        CategoriaDB.id != categoria_id
    ).first()
    
    if categoria_existente:
        raise HTTPException(status_code=400, detail="Ya existe una categoría con ese nombre")
    
    categoria.nombre = nuevo_nombre
    
    try:
        db.commit()
        db.refresh(categoria)
        return {"id": categoria.id, "nombre": categoria.nombre}
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error al actualizar la categoría")

def eliminar_categoria_por_id(db: Session, categoria_id: str) -> dict:
    """Eliminar una categoría por ID"""
    categoria = db.query(CategoriaDB).filter(CategoriaDB.id == categoria_id).first()
    
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    
    categoria_data = {"id": categoria.id, "nombre": categoria.nombre}
    db.delete(categoria)
    db.commit()
    
    return categoria_data
