# Racing Calendar API - Clean Architecture

Este proyecto implementa una API REST para gestión de categorías de carreras utilizando **Clean Architecture** (Arquitectura Limpia).

## 🚀 Instalación y Ejecución

1. Instalar dependencias:
```bash
pip install -r requirements.txt
```

2. Ejecutar la aplicación:
```bash
python main.py

# O usando uvicorn directamente
uvicorn main:app --host 0.0.0.0 --port 8001 --reload
```

## 📚 API Endpoints

### Categorías

- `GET /categorias/` - Obtener todas las categorías
- `GET /categorias/{id}` - Obtener categoría por ID
- `POST /categorias/` - Crear nueva categoría
- `PUT /categorias/{id}` - Actualizar categoría
- `DELETE /categorias/{id}` - Eliminar categoría

## 🏗️ Descripción de las Capas

### Domain (Dominio)
- **Entidades**: Objetos de negocio con reglas y validaciones
- **Repositorios**: Interfaces abstractas para acceso a datos
- No depende de ninguna capa externa

### Application (Aplicación)
- **Casos de Uso**: Lógica de aplicación y orquestación
- **DTOs**: Objetos para transferencia de datos
- Solo depende de la capa de Dominio

### Infrastructure (Infraestructura)
- **Base de Datos**: Configuración y modelos de SQLAlchemy
- **Repositorios**: Implementaciones concretas de las interfaces
- Implementa las interfaces definidas en el Dominio

### Presentation (Presentación)
- **Controladores**: Endpoints de la API REST
- **Schemas**: Validación y serialización con Pydantic
- Maneja la comunicación HTTP

### Shared (Compartido)
- **Configuración**: Settings de la aplicación
- **Excepciones**: Excepciones personalizadas
- Código utilizado por múltiples capas

## 🔄 Flujo de Datos

1. **Request** → Presentation Layer (Controller)
2. **Controller** → Application Layer (Use Case)
3. **Use Case** → Domain Layer (Entity/Repository Interface)
4. **Repository Interface** → Infrastructure Layer (Repository Implementation)
5. **Database** ← Infrastructure Layer
6. **Response** ← Presentation Layer

## 🧪 Testing

La arquitectura facilita el testing al permitir:
- Test unitarios de entidades de dominio
- Test de casos de uso con repositorios mock
- Test de integración de controladores
- Test de repositorios con base de datos en memoria

## 📝 Ejemplos de Uso

### Crear una categoría
```bash
curl -X POST "http://localhost:8001/categorias/" \
     -H "Content-Type: application/json" \
     -d '{"nombre": "Fórmula 1"}'
```

### Obtener todas las categorías
```bash
curl -X GET "http://localhost:8001/categorias/"
```

## 🔮 Extensiones Futuras

Esta arquitectura permite fácilmente:
- Agregar nuevas entidades (Carreras, Pilotos, etc.)
- Cambiar la base de datos (PostgreSQL, MongoDB, etc.)
- Agregar autenticación y autorización
- Implementar caché
- Agregar logging y métricas
- Crear diferentes interfaces (GraphQL, gRPC, etc.)

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request
