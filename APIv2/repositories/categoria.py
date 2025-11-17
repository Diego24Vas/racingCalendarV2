from sqlalchemy.orm import Session
from db.models import Categoria
from schemas.categoria import CategoriaCreate, CategoriaUpdate
from typing import List, Optional

def get_all(db: Session) -> List[Categoria]:
    return db.query(Categoria).all()

def get_by_id(db: Session, categoria_id: int) -> Optional[Categoria]:
    return db.query(Categoria).filter(Categoria.id == categoria_id).first()

def create(db: Session, categoria: CategoriaCreate) -> Categoria:
    db_categoria = Categoria(**categoria.dict())
    db.add(db_categoria)
    db.commit()
    db.refresh(db_categoria)
    return db_categoria

def update(db: Session, categoria_id: int, categoria: CategoriaUpdate) -> Optional[Categoria]:
    db_categoria = get_by_id(db, categoria_id)
    if not db_categoria:
        return None
    for key, value in categoria.dict(exclude_unset=True).items():
        setattr(db_categoria, key, value)
    db.commit()
    db.refresh(db_categoria)
    return db_categoria

def delete(db: Session, categoria_id: int) -> bool:
    db_categoria = get_by_id(db, categoria_id)
    if not db_categoria:
        return False
    db.delete(db_categoria)
    db.commit()
    return True
