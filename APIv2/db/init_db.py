from db.base import Base, engine
from db import models  # Importa todos los modelos para que se registren

def init_db():
    Base.metadata.create_all(bind=engine)
