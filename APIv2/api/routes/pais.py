from fastapi import APIRouter, Depends, HTTPException, status
from core.security import require_admin, get_current_user
from sqlalchemy.orm import Session
from schemas.pais import PaisOut, PaisCreate, PaisUpdate
from repositories import pais as pais_repo
from db.base import get_db
from typing import List

router = APIRouter(prefix="/paises", tags=["paises"])

@router.get("/", response_model=List[PaisOut])
def list_paises(db: Session = Depends(get_db)):
    return pais_repo.get_all(db)

@router.get("/{pais_id}", response_model=PaisOut)
def get_pais(pais_id: int, db: Session = Depends(get_db)):
    pais = pais_repo.get_by_id(db, pais_id)
    if not pais:
        raise HTTPException(status_code=404, detail="País no encontrado")
    return pais

@router.post("/", response_model=PaisOut, status_code=status.HTTP_201_CREATED)
def create_pais(pais: PaisCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    require_admin(current_user)
    return pais_repo.create(db, pais)

@router.put("/{pais_id}", response_model=PaisOut)
def update_pais(pais_id: int, pais: PaisUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    require_admin(current_user)
    updated = pais_repo.update(db, pais_id, pais)
    if not updated:
        raise HTTPException(status_code=404, detail="País no encontrado")
    return updated

@router.delete("/{pais_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_pais(pais_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    require_admin(current_user)
    deleted = pais_repo.delete(db, pais_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="País no encontrado")
    return None
