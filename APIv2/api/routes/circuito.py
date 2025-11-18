from fastapi import APIRouter, Depends, HTTPException, status
from core.security import require_admin, get_current_user
from fastapi.security import OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")
from sqlalchemy.orm import Session
from schemas.circuito import CircuitoOut, CircuitoCreate, CircuitoUpdate
from repositories import circuito as circuito_repo
from db.base import get_db
from typing import List

router = APIRouter(prefix="/circuitos", tags=["circuitos"])

@router.get("/", response_model=List[CircuitoOut])
def list_circuitos(db: Session = Depends(get_db)):
    return circuito_repo.get_all(db)

@router.get("/{circuito_id}", response_model=CircuitoOut)
def get_circuito(circuito_id: int, db: Session = Depends(get_db)):
    circuito = circuito_repo.get_by_id(db, circuito_id)
    if not circuito:
        raise HTTPException(status_code=404, detail="Circuito no encontrado")
    return circuito

@router.post("/", response_model=CircuitoOut, status_code=status.HTTP_201_CREATED)
def create_circuito(circuito: CircuitoCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    current_user = require_admin(get_current_user(token=token, db=db))
    return circuito_repo.create(db, circuito)

@router.put("/{circuito_id}", response_model=CircuitoOut)
def update_circuito(circuito_id: int, circuito: CircuitoUpdate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    current_user = require_admin(get_current_user(token=token, db=db))
    updated = circuito_repo.update(db, circuito_id, circuito)
    if not updated:
        raise HTTPException(status_code=404, detail="Circuito no encontrado")
    return updated

@router.delete("/{circuito_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_circuito(circuito_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    current_user = require_admin(get_current_user(token=token, db=db))
    deleted = circuito_repo.delete(db, circuito_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Circuito no encontrado")
    return None
