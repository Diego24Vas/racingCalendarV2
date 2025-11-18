from fastapi import APIRouter, Depends, HTTPException, status
from core.security import get_current_user, require_admin
from sqlalchemy.orm import Session
from schemas.usuario import UsuarioOut, UsuarioCreate, UsuarioUpdate
from repositories import usuario as usuario_repo
from db.base import get_db
from typing import List

router = APIRouter(prefix="/usuarios", tags=["usuarios"])

@router.get("/", response_model=List[UsuarioOut])
def list_usuarios(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return usuario_repo.get_all(db)


# Solo el usuario autenticado puede ver su propio perfil
@router.get("/me", response_model=UsuarioOut)
def get_profile(current_user=Depends(get_current_user)):
    return current_user

@router.get("/{usuario_id}", response_model=UsuarioOut)
def get_usuario(usuario_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    usuario = usuario_repo.get_by_id(db, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@router.post("/", response_model=UsuarioOut, status_code=status.HTTP_201_CREATED)
def create_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    require_admin(current_user)
    return usuario_repo.create(db, usuario)

@router.put("/{usuario_id}", response_model=UsuarioOut)
def update_usuario(usuario_id: int, usuario: UsuarioUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    require_admin(current_user)
    updated = usuario_repo.update(db, usuario_id, usuario)
    if not updated:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return updated

@router.delete("/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_usuario(usuario_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    require_admin(current_user)
    deleted = usuario_repo.delete(db, usuario_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return None
