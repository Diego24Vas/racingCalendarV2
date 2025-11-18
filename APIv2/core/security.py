from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
import jwt
from core.config import settings
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.base import get_db
from db.models import Usuario, RolUsuarioEnum

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt

# Dependencia para obtener el usuario actual desde el token JWT
def get_current_user(token: str = Depends(lambda: None), db: Session = Depends(get_db)):
    from fastapi.security import OAuth2PasswordBearer
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")
    if token is None:
        token = Depends(oauth2_scheme)
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except Exception:
        raise credentials_exception
    user = db.query(Usuario).filter(Usuario.id == user_id).first()
    if user is None or not user.activo:
        raise credentials_exception
    return user

# Dependencia para verificar que el usuario es admin
def require_admin(current_user: Usuario = Depends(get_current_user)):
    if current_user.rol != RolUsuarioEnum.admin:
        raise HTTPException(status_code=403, detail="No tienes permisos de administrador")
    return current_user
