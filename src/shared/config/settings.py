import os


class Settings:
    """Configuración de la aplicación"""
    
    APP_NAME: str = "API de Calendario de Carreras"
    APP_DESCRIPTION: str = "API simple para calendario de carreras con arquitectura limpia"
    HOST: str = "0.0.0.0"
    PORT: int = 8001
    DEBUG: bool = True
    
    # Base de datos
    DATABASE_URL: str = "sqlite:///./calendarRacing.db"
    
    def __init__(self):
        # Cargar variables de entorno si están disponibles
        self.APP_NAME = os.getenv("APP_NAME", self.APP_NAME)
        self.APP_DESCRIPTION = os.getenv("APP_DESCRIPTION", self.APP_DESCRIPTION)
        self.HOST = os.getenv("HOST", self.HOST)
        self.PORT = int(os.getenv("PORT", self.PORT))
        self.DEBUG = os.getenv("DEBUG", str(self.DEBUG)).lower() == "true"
        self.DATABASE_URL = os.getenv("DATABASE_URL", self.DATABASE_URL)


settings = Settings()
