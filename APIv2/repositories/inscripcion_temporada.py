from sqlalchemy.orm import Session
from db.models import InscripcionTemporada
from schemas.inscripcion_temporada import InscripcionTemporadaCreate, InscripcionTemporadaUpdate
from typing import List, Optional

def get_all(db: Session) -> List[InscripcionTemporada]:
    return db.query(InscripcionTemporada).all()

def get_by_id(db: Session, insc_id: int) -> Optional[InscripcionTemporada]:
    return db.query(InscripcionTemporada).filter(InscripcionTemporada.id == insc_id).first()

def create(db: Session, insc: InscripcionTemporadaCreate) -> InscripcionTemporada:
    db_insc = InscripcionTemporada(**insc.dict())
    db.add(db_insc)
    db.commit()
    db.refresh(db_insc)
    return db_insc

def update(db: Session, insc_id: int, insc: InscripcionTemporadaUpdate) -> Optional[InscripcionTemporada]:
    db_insc = get_by_id(db, insc_id)
    if not db_insc:
        return None
    for key, value in insc.dict(exclude_unset=True).items():
        setattr(db_insc, key, value)
    db.commit()
    db.refresh(db_insc)
    return db_insc

def delete(db: Session, insc_id: int) -> bool:
    db_insc = get_by_id(db, insc_id)
    if not db_insc:
        return False
    db.delete(db_insc)
    db.commit()
    return True
