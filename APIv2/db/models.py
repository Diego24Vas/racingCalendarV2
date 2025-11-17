from db.base import Base
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, DECIMAL, Time, Date, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

class EstadoCarreraEnum(enum.Enum):
    programada = 'programada'
    en_curso = 'en_curso'
    finalizada = 'finalizada'
    cancelada = 'cancelada'

class RolUsuarioEnum(enum.Enum):
    usuario = 'usuario'
    admin = 'admin'

class Categoria(Base):
    __tablename__ = "categoria"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text)
    imagen_url = Column(String(255))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    
    # Relaciones
    carreras = relationship("Carrera", back_populates="categoria")
    inscripciones = relationship("InscripcionTemporada", back_populates="categoria")

class Pais(Base):
    __tablename__ = "pais"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False, unique=True)
    codigo_iso = Column(String(2))
    created_at = Column(DateTime, server_default=func.now())
    
    # Relaciones
    circuitos = relationship("Circuito", back_populates="pais")
    usuarios = relationship("Usuario", back_populates="pais")
    equipos = relationship("Equipo", back_populates="pais")
    pilotos = relationship("Piloto", back_populates="pais")

class Circuito(Base):
    __tablename__ = "circuito"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(150), nullable=False)
    ciudad = Column(String(100), nullable=False)
    id_pais = Column(Integer, ForeignKey("pais.id"), nullable=False)
    latitud = Column(DECIMAL(10, 8))
    longitud = Column(DECIMAL(11, 8))
    descripcion = Column(Text)
    imagen_url = Column(String(255))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    
    # Relaciones
    pais = relationship("Pais", back_populates="circuitos")
    carreras = relationship("Carrera", back_populates="circuito")

class Temporada(Base):
    __tablename__ = "temporada"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    año = Column(Integer, nullable=False)
    activa = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())
    
    # Relaciones
    carreras = relationship("Carrera", back_populates="temporada")
    inscripciones = relationship("InscripcionTemporada", back_populates="temporada")

class Carrera(Base):
    __tablename__ = "carrera"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(200), nullable=False)
    fecha = Column(Date, nullable=False)
    hora = Column(Time)
    id_categoria = Column(Integer, ForeignKey("categoria.id"), nullable=False)
    id_circuito = Column(Integer, ForeignKey("circuito.id"), nullable=False)
    id_temporada = Column(Integer, ForeignKey("temporada.id"), nullable=False)
    estado = Column(Enum(EstadoCarreraEnum), default=EstadoCarreraEnum.programada)
    numero_vueltas = Column(Integer)
    distancia_total = Column(DECIMAL(8, 2))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    
    # Relaciones
    categoria = relationship("Categoria", back_populates="carreras")
    circuito = relationship("Circuito", back_populates="carreras")
    temporada = relationship("Temporada", back_populates="carreras")

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100))
    correo = Column(String(150), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)
    id_pais = Column(Integer, ForeignKey("pais.id"))
    rol = Column(Enum(RolUsuarioEnum), default=RolUsuarioEnum.usuario)
    activo = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    
    # Relaciones
    pais = relationship("Pais", back_populates="usuarios")

class Equipo(Base):
    __tablename__ = "equipo"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(150), nullable=False)
    id_pais = Column(Integer, ForeignKey("pais.id"))
    fundacion = Column(Integer)
    imagen_url = Column(String(255))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    
    # Relaciones
    pais = relationship("Pais", back_populates="equipos")
    inscripciones = relationship("InscripcionTemporada", back_populates="equipo")

class Piloto(Base):
    __tablename__ = "piloto"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    estatus = Column(Boolean, default=True)
    id_pais = Column(Integer, ForeignKey("pais.id"), nullable=False)
    fecha_nacimiento = Column(Date)
    numero = Column(Integer)
    imagen_url = Column(String(255))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    
    # Relaciones
    pais = relationship("Pais", back_populates="pilotos")
    inscripciones = relationship("InscripcionTemporada", back_populates="piloto")

class InscripcionTemporada(Base):
    __tablename__ = "inscripcion_temporada"
    id = Column(Integer, primary_key=True, index=True)
    id_piloto = Column(Integer, ForeignKey("piloto.id"), nullable=False)
    id_categoria = Column(Integer, ForeignKey("categoria.id"), nullable=False)
    id_temporada = Column(Integer, ForeignKey("temporada.id"), nullable=False)
    id_equipo = Column(Integer, ForeignKey("equipo.id"), nullable=False)
    activo = Column(Boolean, default=True)
    puntos_actuales = Column(DECIMAL(6, 2), default=0)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    
    # Relaciones
    piloto = relationship("Piloto", back_populates="inscripciones")
    categoria = relationship("Categoria", back_populates="inscripciones")
    temporada = relationship("Temporada", back_populates="inscripciones")
    equipo = relationship("Equipo", back_populates="inscripciones")
