from pydantic_settings import BaseSettings
from typing import List
import os
from pathlib import Path

class Settings(BaseSettings):
    # Database
    database_url: str
    
    # Security
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # API Settings
    api_title: str = "RacingCalendar API"
    api_description: str = "API para gestionar eventos de carreras"
    api_version: str = "0.1.0"
    debug: bool = True
    
    # CORS - Se parseará automáticamente desde el .env
    cors_origins: str = "http://localhost:3000,http://localhost:8080,http://127.0.0.1:3000"
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Convierte la string de CORS origins en una lista"""
        return [origin.strip() for origin in self.cors_origins.split(",")]
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        env_file_encoding = 'utf-8'

# Buscar el archivo .env en el directorio actual y en directorios padre
def find_env_file():
    current_path = Path.cwd()
    for path in [current_path] + list(current_path.parents):
        env_file = path / ".env"
        if env_file.exists():
            return str(env_file)
    return ".env"  # fallback

settings = Settings(_env_file=find_env_file())