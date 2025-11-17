from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas.carrera import CarreraOut, CarreraCreate, CarreraUpdate
from repositories import carrera as carrera_repo
from db.base import get_db
from typing import List

router = APIRouter(prefix="/carreras", tags=["carreras"])

@router.get("/", response_model=List[CarreraOut])
def list_carreras(db: Session = Depends(get_db)):
    return carrera_repo.get_all(db)

@router.get("/{carrera_id}", response_model=CarreraOut)
def get_carrera(carrera_id: int, db: Session = Depends(get_db)):
    carrera = carrera_repo.get_by_id(db, carrera_id)
    if not carrera:
        raise HTTPException(status_code=404, detail="Carrera no encontrada")
    return carrera

@router.post("/", response_model=CarreraOut, status_code=status.HTTP_201_CREATED)
def create_carrera(carrera: CarreraCreate, db: Session = Depends(get_db)):
    return carrera_repo.create(db, carrera)

@router.put("/{carrera_id}", response_model=CarreraOut)
def update_carrera(carrera_id: int, carrera: CarreraUpdate, db: Session = Depends(get_db)):
    updated = carrera_repo.update(db, carrera_id, carrera)
    if not updated:
        raise HTTPException(status_code=404, detail="Carrera no encontrada")
    return updated

@router.delete("/{carrera_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_carrera(carrera_id: int, db: Session = Depends(get_db)):
    deleted = carrera_repo.delete(db, carrera_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Carrera no encontrada")
    return None
