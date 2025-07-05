from typing import List, Optional
from sqlalchemy.orm import Session
from ...domain.entities.categoria import Categoria
from ...domain.repositories.categoria_repository import CategoriaRepository
from ..database.models.categoria_model import CategoriaModel


class SQLAlchemyCategoriaRepository(CategoriaRepository):
    """Implementación del repositorio de categorías usando SQLAlchemy"""
    
    def __init__(self, db: Session):
        self._db = db
    
    def obtener_todas(self) -> List[Categoria]:
        """Obtener todas las categorías"""
        categorias_db = self._db.query(CategoriaModel).all()
        return [self._to_entity(categoria_db) for categoria_db in categorias_db]
    
    def obtener_por_id(self, categoria_id: str) -> Optional[Categoria]:
        """Obtener una categoría por su ID"""
        categoria_db = self._db.query(CategoriaModel).filter(
            CategoriaModel.id == categoria_id
        ).first()
        
        if categoria_db:
            return self._to_entity(categoria_db)
        return None
    
    def obtener_por_nombre(self, nombre: str) -> Optional[Categoria]:
        """Obtener una categoría por su nombre"""
        categoria_db = self._db.query(CategoriaModel).filter(
            CategoriaModel.nombre == nombre
        ).first()
        
        if categoria_db:
            return self._to_entity(categoria_db)
        return None
    
    def guardar(self, categoria: Categoria) -> Categoria:
        """Guardar una categoría (crear o actualizar)"""
        categoria_db = self._db.query(CategoriaModel).filter(
            CategoriaModel.id == categoria.id
        ).first()
        
        if categoria_db:
            # Actualizar categoría existente
            categoria_db.nombre = categoria.nombre
        else:
            # Crear nueva categoría
            categoria_db = CategoriaModel(
                id=categoria.id,
                nombre=categoria.nombre
            )
            self._db.add(categoria_db)
        
        self._db.commit()
        self._db.refresh(categoria_db)
        
        return self._to_entity(categoria_db)
    
    def eliminar(self, categoria_id: str) -> bool:
        """Eliminar una categoría por su ID"""
        categoria_db = self._db.query(CategoriaModel).filter(
            CategoriaModel.id == categoria_id
        ).first()
        
        if categoria_db:
            self._db.delete(categoria_db)
            self._db.commit()
            return True
        return False
    
    def existe_nombre(self, nombre: str, excluir_id: Optional[str] = None) -> bool:
        """Verificar si existe una categoría con el nombre dado"""
        query = self._db.query(CategoriaModel).filter(CategoriaModel.nombre == nombre)
        
        if excluir_id:
            query = query.filter(CategoriaModel.id != excluir_id)
        
        return query.first() is not None
    
    def _to_entity(self, categoria_db: CategoriaModel) -> Categoria:
        """Convertir modelo de base de datos a entidad de dominio"""
        categoria = Categoria(nombre=categoria_db.nombre)
        categoria.asignar_id(categoria_db.id)
        return categoria
