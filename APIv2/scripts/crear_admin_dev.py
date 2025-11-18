from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from db.models import Usuario, RolUsuarioEnum
from core.security import get_password_hash
from core.config import settings

# Configuración de conexión
engine = create_engine(settings.database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def crear_admin():
    db = SessionLocal()
    try:
        admin_email = "admin@dev.local"
        admin = db.query(Usuario).filter(Usuario.correo == admin_email).first()
        if not admin:
            admin = Usuario(
                nombre="Admin",
                apellido="Dev",
                correo=admin_email,
                password_hash=get_password_hash("admin1234"),
                rol=RolUsuarioEnum.admin,
                activo=True
            )
            db.add(admin)
            db.commit()
            print("Usuario admin creado: admin@dev.local / admin1234")
        else:
            print("El usuario admin ya existe.")
    finally:
        db.close()

if __name__ == "__main__":
    crear_admin()
