from fastapi import APIRouter, Depends, HTTPException, status
from core.security import require_admin, get_current_user
from sqlalchemy.orm import Session
from schemas.equipo import EquipoOut, EquipoCreate, EquipoUpdate
from repositories import equipo as equipo_repo
from db.base import get_db
from typing import List

router = APIRouter(prefix="/equipos", tags=["equipos"])

@router.get("/", response_model=List[EquipoOut])
def list_equipos(db: Session = Depends(get_db)):
    return equipo_repo.get_all(db)

@router.get("/{equipo_id}", response_model=EquipoOut)
def get_equipo(equipo_id: int, db: Session = Depends(get_db)):
    equipo = equipo_repo.get_by_id(db, equipo_id)
    if not equipo:
        raise HTTPException(status_code=404, detail="Equipo no encontrado")
    return equipo

@router.post("/", response_model=EquipoOut, status_code=status.HTTP_201_CREATED)
def create_equipo(equipo: EquipoCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    require_admin(current_user)
    return equipo_repo.create(db, equipo)

@router.put("/{equipo_id}", response_model=EquipoOut)
def update_equipo(equipo_id: int, equipo: EquipoUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    require_admin(current_user)
    updated = equipo_repo.update(db, equipo_id, equipo)
    if not updated:
        raise HTTPException(status_code=404, detail="Equipo no encontrado")
    return updated

@router.delete("/{equipo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_equipo(equipo_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    require_admin(current_user)
    deleted = equipo_repo.delete(db, equipo_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Equipo no encontrado")
    return None
