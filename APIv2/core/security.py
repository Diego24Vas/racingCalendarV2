from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
import jwt
from core.config import settings
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
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

# Dependencia para obtener el usuario actual desde el token JWT usando HTTPBearer
http_bearer = HTTPBearer()
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(http_bearer), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token = credentials.credentials
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except Exception:
        raise credentials_exception
    user = db.query(Usuario).filter(Usuario.correo == email).first()
    if user is None or not user.activo:
        raise credentials_exception
    return user

# Dependencia para verificar que el usuario es admin
def require_admin(current_user: Usuario = Depends(get_current_user)):
    if current_user.rol != RolUsuarioEnum.admin:
        raise HTTPException(status_code=403, detail="No tienes permisos de administrador")
    return current_user
