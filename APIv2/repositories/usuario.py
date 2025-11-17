from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from db.models import Usuario
from schemas.usuario import UsuarioCreate, UsuarioUpdate
from core.security import get_password_hash
from typing import List, Optional
from fastapi import HTTPException

def get_all(db: Session) -> List[Usuario]:
    return db.query(Usuario).all()

def get_by_id(db: Session, usuario_id: int) -> Optional[Usuario]:
    return db.query(Usuario).filter(Usuario.id == usuario_id).first()

def get_by_email(db: Session, email: str) -> Optional[Usuario]:
    return db.query(Usuario).filter(Usuario.correo == email).first()

def create(db: Session, usuario: UsuarioCreate) -> Usuario:
    # Verificar si ya existe un usuario con ese email
    existing_user = db.query(Usuario).filter(Usuario.correo == usuario.correo).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Ya existe un usuario con este correo")
    
    # Crear el diccionario del usuario y hashear la contraseña
    usuario_dict = usuario.dict()
    password = usuario_dict.pop('password')
    usuario_dict['password_hash'] = get_password_hash(password)
    
    try:
        db_usuario = Usuario(**usuario_dict)
        db.add(db_usuario)
        db.commit()
        db.refresh(db_usuario)
        return db_usuario
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error al crear el usuario")

def update(db: Session, usuario_id: int, usuario: UsuarioUpdate) -> Optional[Usuario]:
    db_usuario = get_by_id(db, usuario_id)
    if not db_usuario:
        return None
    for key, value in usuario.dict(exclude_unset=True).items():
        setattr(db_usuario, key, value)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

def delete(db: Session, usuario_id: int) -> bool:
    db_usuario = get_by_id(db, usuario_id)
    if not db_usuario:
        return False
    db.delete(db_usuario)
    db.commit()
    return True
