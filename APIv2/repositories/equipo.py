from sqlalchemy.orm import Session
from db.models import Equipo
from schemas.equipo import EquipoCreate, EquipoUpdate
from typing import List, Optional

def get_all(db: Session) -> List[Equipo]:
    return db.query(Equipo).all()

def get_by_id(db: Session, equipo_id: int) -> Optional[Equipo]:
    return db.query(Equipo).filter(Equipo.id == equipo_id).first()

def create(db: Session, equipo: EquipoCreate) -> Equipo:
    db_equipo = Equipo(**equipo.dict())
    db.add(db_equipo)
    db.commit()
    db.refresh(db_equipo)
    return db_equipo

def update(db: Session, equipo_id: int, equipo: EquipoUpdate) -> Optional[Equipo]:
    db_equipo = get_by_id(db, equipo_id)
    if not db_equipo:
        return None
    for key, value in equipo.dict(exclude_unset=True).items():
        setattr(db_equipo, key, value)
    db.commit()
    db.refresh(db_equipo)
    return db_equipo

def delete(db: Session, equipo_id: int) -> bool:
    db_equipo = get_by_id(db, equipo_id)
    if not db_equipo:
        return False
    db.delete(db_equipo)
    db.commit()
    return True
