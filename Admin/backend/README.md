# Racing Calendar Backend

API REST para gestión de categorías y carreras utilizando **Clean Architecture** con FastAPI.

## 🏗️ Estructura del Backend

```
backend/
├── src/
│   ├── domain/           # Entidades y repositorios abstractos
│   │   ├── entities/     # Objetos de negocio
│   │   └── repositories/ # Interfaces de repositorios
│   ├── application/      # Casos de uso y DTOs
│   │   ├── dtos/        # Data Transfer Objects
│   │   └── use_cases/   # Lógica de aplicación
│   ├── infrastructure/   # Implementaciones concretas
│   │   ├── database/    # Configuración de BD
│   │   └── repositories/ # Implementaciones de repositorios
│   ├── presentation/     # Controladores y schemas
│   │   ├── api/         # Controladores REST
│   │   └── schemas/     # Validación con Pydantic
│   └── shared/          # Configuración compartida
│       ├── config/      # Configuraciones
│       └── exceptions/  # Excepciones personalizadas
├── main.py              # Punto de entrada de la aplicación
├── requirements.txt     # Dependencias Python
└── README.md            # Documentación del backend
```

## 🚀 Instalación y Ejecución

### Prerrequisitos
- Python 3.8 o superior
- pip

### Instalación
```bash
cd backend
pip install -r requirements.txt
```

### Ejecución en Desarrollo
```bash
python main.py

# O usando uvicorn directamente
uvicorn main:app --host 0.0.0.0 --port 8001 --reload
```

La API estará disponible en: http://localhost:8001

### Documentación
- Swagger UI: http://localhost:8001/docs
- ReDoc: http://localhost:8001/redoc

## 📚 API Endpoints

### Categorías
- `GET /categorias/` - Obtener todas las categorías
- `GET /categorias/{id}` - Obtener categoría por ID
- `POST /categorias/` - Crear nueva categoría
- `PUT /categorias/{id}` - Actualizar categoría
- `DELETE /categorias/{id}` - Eliminar categoría

### Carreras
- `GET /carreras/` - Obtener todas las carreras
- `GET /carreras/{id}` - Obtener carrera por ID
- `POST /carreras/` - Crear nueva carrera
- `PUT /carreras/{id}` - Actualizar carrera
- `DELETE /carreras/{id}` - Eliminar carrera

## 🏗️ Arquitectura Limpia

### Domain (Dominio)
- **Entidades**: Objetos de negocio con reglas y validaciones
- **Repositorios**: Interfaces abstractas para acceso a datos
- **Independiente**: No depende de ninguna capa externa

### Application (Aplicación)
- **Casos de Uso**: Lógica de aplicación y orquestación
- **DTOs**: Objetos para transferencia de datos
- **Dependencia**: Solo depende de la capa de Dominio

### Infrastructure (Infraestructura)
- **Base de Datos**: Configuración y modelos de SQLAlchemy
- **Repositorios**: Implementaciones concretas de las interfaces
- **Implementación**: De las interfaces definidas en el Dominio

### Presentation (Presentación)
- **Controladores**: Endpoints de la API REST
- **Schemas**: Validación y serialización con Pydantic
- **Comunicación**: Maneja la comunicación HTTP

## 🛠️ Tecnologías

- **FastAPI**: Framework web moderno y rápido
- **SQLAlchemy**: ORM para Python
- **Pydantic**: Validación de datos con tipos
- **Uvicorn**: Servidor ASGI
- **SQLite**: Base de datos (por defecto)
