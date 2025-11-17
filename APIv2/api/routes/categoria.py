from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas.categoria import CategoriaOut, CategoriaCreate, CategoriaUpdate
from repositories import categoria as categoria_repo
from db.base import get_db
from typing import List

router = APIRouter(prefix="/categorias", tags=["categorias"])

@router.get("/", response_model=List[CategoriaOut])
def list_categorias(db: Session = Depends(get_db)):
    return categoria_repo.get_all(db)

@router.get("/{categoria_id}", response_model=CategoriaOut)
def get_categoria(categoria_id: int, db: Session = Depends(get_db)):
    categoria = categoria_repo.get_by_id(db, categoria_id)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return categoria

@router.post("/", response_model=CategoriaOut, status_code=status.HTTP_201_CREATED)
def create_categoria(categoria: CategoriaCreate, db: Session = Depends(get_db)):
    return categoria_repo.create(db, categoria)

@router.put("/{categoria_id}", response_model=CategoriaOut)
def update_categoria(categoria_id: int, categoria: CategoriaUpdate, db: Session = Depends(get_db)):
    updated = categoria_repo.update(db, categoria_id, categoria)
    if not updated:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return updated

@router.delete("/{categoria_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_categoria(categoria_id: int, db: Session = Depends(get_db)):
    deleted = categoria_repo.delete(db, categoria_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return None
