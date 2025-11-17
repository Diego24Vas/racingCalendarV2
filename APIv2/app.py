from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from api.routes.auth import router as auth_router
from api.routes.categoria import router as categoria_router
from api.routes.pais import router as pais_router
from api.routes.circuito import router as circuito_router
from api.routes.temporada import router as temporada_router
from api.routes.carrera import router as carrera_router
from api.routes.usuario import router as usuario_router
from api.routes.equipo import router as equipo_router
from api.routes.piloto import router as piloto_router
from api.routes.inscripcion_temporada import router as inscripcion_temporada_router
from db.init_db import init_db
from contextlib import asynccontextmanager
from core.config import settings

@asynccontextmanager
async def lifespan(app):
    init_db()
    yield

app = FastAPI(
    title=settings.api_title,
    description=settings.api_description,
    version=settings.api_version,
    lifespan=lifespan
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(auth_router, tags=["auth"])
app.include_router(categoria_router)
app.include_router(pais_router)
app.include_router(circuito_router)
app.include_router(temporada_router)
app.include_router(carrera_router)
app.include_router(usuario_router)
app.include_router(equipo_router)
app.include_router(piloto_router)
app.include_router(inscripcion_temporada_router)


if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
