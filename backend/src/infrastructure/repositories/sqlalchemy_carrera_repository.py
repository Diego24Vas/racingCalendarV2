from typing import List, Optional
from sqlalchemy.orm import Session
from ...domain.entities.carrera import Carrera
from ...domain.repositories.carrera_repository import CarreraRepository
from ..database.models.carrera_model import CarreraModel


class SQLAlchemyCarreraRepository(CarreraRepository):
    """Implementación del repositorio de carreras usando SQLAlchemy"""
    
    def __init__(self, db: Session):
        self._db = db
    
    def crear(self, carrera: Carrera) -> Carrera:
        """Crear una nueva carrera"""
        carrera_db = CarreraModel(
            id=carrera.id,
            nombre=carrera.nombre,
            fecha=carrera.fecha,
            pais=carrera.pais,
            circuito=carrera.circuito,
            latitud=carrera.latitud,
            longitud=carrera.longitud,
            categoria_id=carrera.categoria_id
        )
        
        self._db.add(carrera_db)
        self._db.commit()
        self._db.refresh(carrera_db)
        
        return self._to_entity(carrera_db)
    
    def obtener_por_id(self, id: str) -> Optional[Carrera]:
        """Obtener una carrera por su ID"""
        carrera_db = self._db.query(CarreraModel).filter(
            CarreraModel.id == id
        ).first()
        
        if carrera_db:
            return self._to_entity(carrera_db)
        return None
    
    def obtener_todas(self) -> List[Carrera]:
        """Obtener todas las carreras"""
        carreras_db = self._db.query(CarreraModel).order_by(CarreraModel.fecha).all()
        return [self._to_entity(carrera_db) for carrera_db in carreras_db]
    
    def obtener_por_categoria(self, categoria_id: str) -> List[Carrera]:
        """Obtener todas las carreras de una categoría específica"""
        carreras_db = self._db.query(CarreraModel).filter(
            CarreraModel.categoria_id == categoria_id
        ).order_by(CarreraModel.fecha).all()
        
        return [self._to_entity(carrera_db) for carrera_db in carreras_db]
    
    def actualizar(self, carrera: Carrera) -> Carrera:
        """Actualizar una carrera existente"""
        carrera_db = self._db.query(CarreraModel).filter(
            CarreraModel.id == carrera.id
        ).first()
        
        if carrera_db:
            carrera_db.nombre = carrera.nombre
            carrera_db.fecha = carrera.fecha
            carrera_db.pais = carrera.pais
            carrera_db.circuito = carrera.circuito
            carrera_db.latitud = carrera.latitud
            carrera_db.longitud = carrera.longitud
            carrera_db.categoria_id = carrera.categoria_id
            
            self._db.commit()
            self._db.refresh(carrera_db)
            
            return self._to_entity(carrera_db)
        return None
    
    def eliminar(self, id: str) -> bool:
        """Eliminar una carrera por su ID"""
        carrera_db = self._db.query(CarreraModel).filter(
            CarreraModel.id == id
        ).first()
        
        if carrera_db:
            self._db.delete(carrera_db)
            self._db.commit()
            return True
        return False
    
    def _to_entity(self, carrera_db: CarreraModel) -> Carrera:
        """Convertir modelo de base de datos a entidad de dominio"""
        carrera = Carrera(
            nombre=carrera_db.nombre,
            fecha=carrera_db.fecha,
            pais=carrera_db.pais,
            circuito=carrera_db.circuito,
            latitud=carrera_db.latitud,
            longitud=carrera_db.longitud,
            categoria_id=carrera_db.categoria_id
        )
        carrera.asignar_id(carrera_db.id)
        return carrera
