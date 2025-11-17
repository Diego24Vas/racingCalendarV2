from sqlalchemy.orm import Session
from db.models import Piloto
from schemas.piloto import PilotoCreate, PilotoUpdate
from typing import List, Optional

def get_all(db: Session) -> List[Piloto]:
    return db.query(Piloto).all()

def get_by_id(db: Session, piloto_id: int) -> Optional[Piloto]:
    return db.query(Piloto).filter(Piloto.id == piloto_id).first()

def create(db: Session, piloto: PilotoCreate) -> Piloto:
    db_piloto = Piloto(**piloto.dict())
    db.add(db_piloto)
    db.commit()
    db.refresh(db_piloto)
    return db_piloto

def update(db: Session, piloto_id: int, piloto: PilotoUpdate) -> Optional[Piloto]:
    db_piloto = get_by_id(db, piloto_id)
    if not db_piloto:
        return None
    for key, value in piloto.dict(exclude_unset=True).items():
        setattr(db_piloto, key, value)
    db.commit()
    db.refresh(db_piloto)
    return db_piloto

def delete(db: Session, piloto_id: int) -> bool:
    db_piloto = get_by_id(db, piloto_id)
    if not db_piloto:
        return False
    db.delete(db_piloto)
    db.commit()
    return True
