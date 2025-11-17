from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas.temporada import TemporadaOut, TemporadaCreate, TemporadaUpdate
from repositories import temporada as temporada_repo
from db.base import get_db
from typing import List

router = APIRouter(prefix="/temporadas", tags=["temporadas"])

@router.get("/", response_model=List[TemporadaOut])
def list_temporadas(db: Session = Depends(get_db)):
    return temporada_repo.get_all(db)

@router.get("/{temporada_id}", response_model=TemporadaOut)
def get_temporada(temporada_id: int, db: Session = Depends(get_db)):
    temporada = temporada_repo.get_by_id(db, temporada_id)
    if not temporada:
        raise HTTPException(status_code=404, detail="Temporada no encontrada")
    return temporada

@router.post("/", response_model=TemporadaOut, status_code=status.HTTP_201_CREATED)
def create_temporada(temporada: TemporadaCreate, db: Session = Depends(get_db)):
    return temporada_repo.create(db, temporada)

@router.put("/{temporada_id}", response_model=TemporadaOut)
def update_temporada(temporada_id: int, temporada: TemporadaUpdate, db: Session = Depends(get_db)):
    updated = temporada_repo.update(db, temporada_id, temporada)
    if not updated:
        raise HTTPException(status_code=404, detail="Temporada no encontrada")
    return updated

@router.delete("/{temporada_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_temporada(temporada_id: int, db: Session = Depends(get_db)):
    deleted = temporada_repo.delete(db, temporada_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Temporada no encontrada")
    return None
