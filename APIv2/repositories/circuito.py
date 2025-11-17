from sqlalchemy.orm import Session
from db.models import Circuito
from schemas.circuito import CircuitoCreate, CircuitoUpdate
from typing import List, Optional

def get_all(db: Session) -> List[Circuito]:
    return db.query(Circuito).all()

def get_by_id(db: Session, circuito_id: int) -> Optional[Circuito]:
    return db.query(Circuito).filter(Circuito.id == circuito_id).first()

def create(db: Session, circuito: CircuitoCreate) -> Circuito:
    db_circuito = Circuito(**circuito.dict())
    db.add(db_circuito)
    db.commit()
    db.refresh(db_circuito)
    return db_circuito

def update(db: Session, circuito_id: int, circuito: CircuitoUpdate) -> Optional[Circuito]:
    db_circuito = get_by_id(db, circuito_id)
    if not db_circuito:
        return None
    for key, value in circuito.dict(exclude_unset=True).items():
        setattr(db_circuito, key, value)
    db.commit()
    db.refresh(db_circuito)
    return db_circuito

def delete(db: Session, circuito_id: int) -> bool:
    db_circuito = get_by_id(db, circuito_id)
    if not db_circuito:
        return False
    db.delete(db_circuito)
    db.commit()
    return True
