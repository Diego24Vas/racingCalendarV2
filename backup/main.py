from fastapi import FastAPI
from routes import router as categorias_router
from config import settings
from db_config import create_tables

# Crear las tablas de la base de datos al iniciar
create_tables()

app = FastAPI(
    title=settings.APP_NAME, 
    description=settings.APP_DESCRIPTION
)

# Incluir las rutas
app.include_router(categorias_router)

@app.get("/")
def read_root():
    return {"mensaje": "API de Categorías funcionando"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.HOST, 
        port=settings.PORT,
        reload=settings.DEBUG
    )
