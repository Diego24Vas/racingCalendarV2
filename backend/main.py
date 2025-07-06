from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.presentation.api.categoria_controller import router as categorias_router
from src.presentation.api.carrera_controller import router as carreras_router
from src.shared.config.settings import settings
from src.infrastructure.database.connection import create_tables

# Crear las tablas de la base de datos al iniciar
create_tables()

app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
    version="2.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir las rutas
app.include_router(categorias_router)
app.include_router(carreras_router)


@app.get("/")
def read_root():
    return {
        "mensaje": "API de RacingCalendar",
        "version": "2.0.0",
        "arquitectura": "Clean Architecture",
        "estado": "operativo",
        "timestamp": "2025-07-05T00:00:00Z",
        "endpoints": {
            "categorias": "/categorias",
            "carreras": "/carreras",
            "documentacion": "/docs",
            "redoc": "/redoc"
        }
    }


if __name__ == "__main__":
    import uvicorn
    
    # Mostrar información útil en la consola
    print("\n" + "="*60)
    print("🏁 RACING CALENDAR API v2.0.0")
    print("="*60)
    print(f"🌐 Servidor ejecutándose en: http://{settings.HOST}:{settings.PORT}")
    print(f"📚 Documentación Swagger: http://{settings.HOST}:{settings.PORT}/docs")
    print(f"📖 Documentación ReDoc: http://{settings.HOST}:{settings.PORT}/redoc")
    print("="*60)
    print("Endpoints disponibles:")
    print(f"  • Categorías: http://{settings.HOST}:{settings.PORT}/Categorias")
    print(f"  • Carreras: http://{settings.HOST}:{settings.PORT}/Carreras")
    print("="*60 + "\n")
    
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
