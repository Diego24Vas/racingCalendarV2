from sqlalchemy.orm import Session
from db.models import Carrera
from schemas.carrera import CarreraCreate, CarreraUpdate
from typing import List, Optional

def get_all(db: Session) -> List[Carrera]:
    return db.query(Carrera).all()

def get_by_id(db: Session, carrera_id: int) -> Optional[Carrera]:
    return db.query(Carrera).filter(Carrera.id == carrera_id).first()

def create(db: Session, carrera: CarreraCreate) -> Carrera:
    db_carrera = Carrera(**carrera.dict())
    db.add(db_carrera)
    db.commit()
    db.refresh(db_carrera)
    return db_carrera

def update(db: Session, carrera_id: int, carrera: CarreraUpdate) -> Optional[Carrera]:
    db_carrera = get_by_id(db, carrera_id)
    if not db_carrera:
        return None
    for key, value in carrera.dict(exclude_unset=True).items():
        setattr(db_carrera, key, value)
    db.commit()
    db.refresh(db_carrera)
    return db_carrera

def delete(db: Session, carrera_id: int) -> bool:
    db_carrera = get_by_id(db, carrera_id)
    if not db_carrera:
        return False
    db.delete(db_carrera)
    db.commit()
    return True
