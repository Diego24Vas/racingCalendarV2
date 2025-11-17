from pydantic import BaseModel, EmailStr, validator, Field
from typing import Optional
from datetime import datetime
from enum import Enum

class RolUsuarioEnum(str, Enum):
    usuario = 'usuario'
    admin = 'admin'

class UsuarioBase(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100, description="Nombre del usuario")
    apellido: Optional[str] = Field(None, max_length=100, description="Apellido del usuario")
    correo: EmailStr = Field(..., description="Correo electrónico válido")
    id_pais: Optional[int] = Field(None, gt=0, description="ID del país")
    rol: Optional[RolUsuarioEnum] = RolUsuarioEnum.usuario
    activo: Optional[bool] = True
    
    @validator('nombre')
    def validar_nombre(cls, v):
        if not v.strip():
            raise ValueError('El nombre no puede estar vacío')
        return v.strip().title()

class UsuarioCreate(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100)
    apellido: Optional[str] = Field(None, max_length=100)
    correo: EmailStr
    password: str = Field(..., min_length=8, description="Contraseña mínimo 8 caracteres")
    id_pais: Optional[int] = Field(None, gt=0)
    rol: Optional[RolUsuarioEnum] = RolUsuarioEnum.usuario
    activo: Optional[bool] = True
    
    @validator('password')
    def validar_password(cls, v):
        if len(v) < 8:
            raise ValueError('La contraseña debe tener al menos 8 caracteres')
        return v

class UsuarioUpdate(UsuarioBase):
    pass

class UsuarioOut(BaseModel):
    id: int
    nombre: str
    apellido: Optional[str] = None
    correo: EmailStr
    id_pais: Optional[int] = None
    rol: RolUsuarioEnum
    activo: bool
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True
