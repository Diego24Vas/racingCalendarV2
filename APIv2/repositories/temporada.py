from sqlalchemy.orm import Session
from db.models import Temporada
from schemas.temporada import TemporadaCreate, TemporadaUpdate
from typing import List, Optional
from fastapi import HTTPException

def get_all(db: Session) -> List[Temporada]:
    return db.query(Temporada).all()

def get_by_id(db: Session, temporada_id: int) -> Optional[Temporada]:
    return db.query(Temporada).filter(Temporada.id == temporada_id).first()

def create(db: Session, temporada: TemporadaCreate) -> Temporada:
    # Verificar si ya existe una temporada para ese año
    existing_temporada = db.query(Temporada).filter(
        Temporada.año == temporada.año,
        Temporada.nombre == temporada.nombre
    ).first()
    if existing_temporada:
        raise HTTPException(
            status_code=400, 
            detail=f"Ya existe una temporada '{temporada.nombre}' para el año {temporada.año}"
        )
    
    # Si se marca como activa, desactivar otras temporadas
    if temporada.activa:
        db.query(Temporada).update({Temporada.activa: False})
    
    db_temporada = Temporada(**temporada.dict())
    db.add(db_temporada)
    db.commit()
    db.refresh(db_temporada)
    return db_temporada

def update(db: Session, temporada_id: int, temporada: TemporadaUpdate) -> Optional[Temporada]:
    db_temporada = get_by_id(db, temporada_id)
    if not db_temporada:
        return None
    for key, value in temporada.dict(exclude_unset=True).items():
        setattr(db_temporada, key, value)
    db.commit()
    db.refresh(db_temporada)
    return db_temporada

def delete(db: Session, temporada_id: int) -> bool:
    db_temporada = get_by_id(db, temporada_id)
    if not db_temporada:
        return False
    db.delete(db_temporada)
    db.commit()
    return True
