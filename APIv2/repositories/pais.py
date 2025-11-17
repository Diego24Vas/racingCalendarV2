from sqlalchemy.orm import Session
from db.models import Pais
from schemas.pais import PaisCreate, PaisUpdate
from typing import List, Optional

def get_all(db: Session) -> List[Pais]:
    return db.query(Pais).all()

def get_by_id(db: Session, pais_id: int) -> Optional[Pais]:
    return db.query(Pais).filter(Pais.id == pais_id).first()

def create(db: Session, pais: PaisCreate) -> Pais:
    db_pais = Pais(**pais.dict())
    db.add(db_pais)
    db.commit()
    db.refresh(db_pais)
    return db_pais

def update(db: Session, pais_id: int, pais: PaisUpdate) -> Optional[Pais]:
    db_pais = get_by_id(db, pais_id)
    if not db_pais:
        return None
    for key, value in pais.dict(exclude_unset=True).items():
        setattr(db_pais, key, value)
    db.commit()
    db.refresh(db_pais)
    return db_pais

def delete(db: Session, pais_id: int) -> bool:
    db_pais = get_by_id(db, pais_id)
    if not db_pais:
        return False
    db.delete(db_pais)
    db.commit()
    return True
