from fastapi import APIRouter, Depends, HTTPException, status
from core.security import require_admin, get_current_user
from sqlalchemy.orm import Session
from schemas.inscripcion_temporada import InscripcionTemporadaOut, InscripcionTemporadaCreate, InscripcionTemporadaUpdate
from repositories import inscripcion_temporada as insc_repo
from db.base import get_db
from typing import List

router = APIRouter(prefix="/inscripciones", tags=["inscripcion_temporada"])

@router.get("/", response_model=List[InscripcionTemporadaOut])
def list_inscripciones(db: Session = Depends(get_db)):
    return insc_repo.get_all(db)

@router.get("/{insc_id}", response_model=InscripcionTemporadaOut)
def get_inscripcion(insc_id: int, db: Session = Depends(get_db)):
    insc = insc_repo.get_by_id(db, insc_id)
    if not insc:
        raise HTTPException(status_code=404, detail="Inscripción no encontrada")
    return insc

@router.post("/", response_model=InscripcionTemporadaOut, status_code=status.HTTP_201_CREATED)
def create_inscripcion(insc: InscripcionTemporadaCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    require_admin(current_user)
    return insc_repo.create(db, insc)

@router.put("/{insc_id}", response_model=InscripcionTemporadaOut)
def update_inscripcion(insc_id: int, insc: InscripcionTemporadaUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    require_admin(current_user)
    updated = insc_repo.update(db, insc_id, insc)
    if not updated:
        raise HTTPException(status_code=404, detail="Inscripción no encontrada")
    return updated

@router.delete("/{insc_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_inscripcion(insc_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    require_admin(current_user)
    deleted = insc_repo.delete(db, insc_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Inscripción no encontrada")
    return None
