# API de Categorías

Una API simple en Python usando FastAPI para gestionar categorías, diseñada con una arquitectura modular y escalable.

## Estructura del Proyecto

```
racingCalendarV2/
├── main.py              # Punto de entrada de la aplicación
├── models.py            # Modelos de datos (Pydantic)
├── routes.py            # Rutas y endpoints de la API
├── database.py          # Lógica de acceso a datos (SQLAlchemy)
├── db_config.py         # Configuración de la base de datos SQLite
├── config.py            # Configuración de la aplicación
├── requirements.txt     # Dependencias del proyecto
├── README.md           # Documentación
├── __init__.py         # Archivo de paquete Python
└── categorias.db       # Base de datos SQLite (se crea automáticamente)
```

## Arquitectura

La aplicación está dividida en capas para facilitar el mantenimiento y escalabilidad:

- **main.py**: Configuración principal de FastAPI y punto de entrada
- **models.py**: Definición de modelos de datos usando Pydantic
- **routes.py**: Definición de endpoints y rutas de la API
- **database.py**: Lógica de acceso y manipulación de datos usando SQLAlchemy
- **db_config.py**: Configuración de SQLite y modelos de base de datos
- **config.py**: Configuración centralizada de la aplicación

## Base de Datos

La aplicación utiliza **SQLite** como base de datos, que se almacena en el archivo `categorias.db`. Las ventajas de SQLite son:

- ✅ **Sin configuración**: No requiere instalación de servidor de base de datos
- ✅ **Portabilidad**: El archivo de base de datos es completamente portable
- ✅ **Rendimiento**: Excelente para aplicaciones pequeñas y medianas
- ✅ **ACID**: Transacciones completamente ACID
- ✅ **Persistencia**: Los datos se mantienen entre reinicios de la aplicación

### Esquema de la Base de Datos

**Tabla: categorias**
- `id` (STRING, PRIMARY KEY): Identificador único UUID
- `nombre` (STRING, UNIQUE): Nombre de la categoría

## Instalación

1. Instalar las dependencias:
```bash
pip install -r requirements.txt
```

## Ejecutar la API

```bash
python main.py
```

La API estará disponible en: http://localhost:8001

## Documentación

FastAPI genera automáticamente documentación interactiva:
- Swagger UI: http://localhost:8001/docs
- ReDoc: http://localhost:8001/redoc

## Endpoints disponibles

### GET /
- Mensaje de bienvenida

### POST /categorias/
- Crear una nueva categoría
- Body: `{"nombre": "Nombre de la categoría"}`

### GET /categorias/
- Obtener todas las categorías

### GET /categorias/{categoria_id}
- Obtener una categoría específica por ID

### PUT /categorias/{categoria_id}
- Actualizar una categoría existente
- Body: `{"nombre": "Nuevo nombre"}`

### DELETE /categorias/{categoria_id}
- Eliminar una categoría

## Ejemplos de uso

### Crear categoría
```bash
curl -X POST "http://localhost:8001/categorias/" \
     -H "Content-Type: application/json" \
     -d '{"nombre": "Deportes"}'
```

### Obtener todas las categorías
```bash
curl -X GET "http://localhost:8001/categorias/"
```

### Actualizar categoría
```bash
curl -X PUT "http://localhost:8001/categorias/{id}" \
     -H "Content-Type: application/json" \
     -d '{"nombre": "Deportes Modificado"}'
```

### Eliminar categoría
```bash
curl -X DELETE "http://localhost:8001/categorias/{id}"
```

## Ventajas de la Estructura Modular

1. **Separación de responsabilidades**: Cada archivo tiene una función específica
2. **Facilidad de mantenimiento**: Cambios en una capa no afectan las otras
3. **Escalabilidad**: Fácil agregar nuevos modelos, rutas o servicios
4. **Testabilidad**: Cada módulo puede ser probado de forma independiente
5. **Reutilización**: Los componentes pueden ser reutilizados en otros proyectos
6. **Persistencia de datos**: SQLite garantiza que los datos se mantengan entre sesiones

## Tecnologías utilizadas

- **FastAPI**: Framework web moderno y rápido
- **SQLAlchemy**: ORM para manejo de base de datos
- **SQLite**: Base de datos ligera y sin servidor
- **Pydantic**: Validación de datos y serialización
- **Uvicorn**: Servidor ASGI de alto rendimiento

## Próximos pasos para escalar

- Migrar a PostgreSQL o MySQL para producción
- Implementar autenticación y autorización
- Agregar logging y monitoreo
- Implementar tests unitarios y de integración
- Dockerizar la aplicación
- Agregar migraciones de base de datos con Alembic
