from fastapi import APIRouter, Depends, HTTPException, status
from core.security import require_admin, get_current_user
from fastapi.security import OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")
from sqlalchemy.orm import Session
from schemas.piloto import PilotoOut, PilotoCreate, PilotoUpdate
from repositories import piloto as piloto_repo
from db.base import get_db
from typing import List

router = APIRouter(prefix="/pilotos", tags=["pilotos"])

@router.get("/", response_model=List[PilotoOut])
def list_pilotos(db: Session = Depends(get_db)):
    return piloto_repo.get_all(db)

@router.get("/{piloto_id}", response_model=PilotoOut)
def get_piloto(piloto_id: int, db: Session = Depends(get_db)):
    piloto = piloto_repo.get_by_id(db, piloto_id)
    if not piloto:
        raise HTTPException(status_code=404, detail="Piloto no encontrado")
    return piloto

@router.post("/", response_model=PilotoOut, status_code=status.HTTP_201_CREATED)
def create_piloto(piloto: PilotoCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    current_user = require_admin(get_current_user(token=token, db=db))
    return piloto_repo.create(db, piloto)

@router.put("/{piloto_id}", response_model=PilotoOut)
def update_piloto(piloto_id: int, piloto: PilotoUpdate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    current_user = require_admin(get_current_user(token=token, db=db))
    updated = piloto_repo.update(db, piloto_id, piloto)
    if not updated:
        raise HTTPException(status_code=404, detail="Piloto no encontrado")
    return updated

@router.delete("/{piloto_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_piloto(piloto_id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    current_user = require_admin(get_current_user(token=token, db=db))
    deleted = piloto_repo.delete(db, piloto_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Piloto no encontrado")
    return None
