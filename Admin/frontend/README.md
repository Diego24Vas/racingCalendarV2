n# Racing Calendar Frontend

Este es el frontend de la aplicación Racing Calendar, desarrollado con React y siguiendo los principios de Clean Architecture.

## Estructura del Proyecto

```
frontend/
├── src/
│   ├── domain/           # Entidades de dominio
│   ├── application/      # Casos de uso
│   ├── infrastructure/   # Implementaciones de infraestructura
│   ├── presentation/     # Componentes UI y páginas
│   └── shared/           # Recursos compartidos
├── package.json
├── vite.config.js
└── index.html
```

## Instalación y Ejecución

### Prerrequisitos
- Node.js (versión 16 o superior)
- npm o yarn

### Instalación
```bash
cd frontend
npm install
```

### Desarrollo
```bash
npm run dev
```
El servidor de desarrollo se ejecutará en http://localhost:3000

### Build de Producción
```bash
npm run build
```

### Preview del Build
```bash
npm run preview
```

## Arquitectura

El proyecto sigue los principios de Clean Architecture:

- **Domain**: Entidades de negocio puras
- **Application**: Casos de uso y lógica de aplicación
- **Infrastructure**: Implementaciones de servicios externos
- **Presentation**: Componentes React y páginas

## Tecnologías

- React 18
- Vite (build tool)
- CSS3 con gradientes y animaciones
- ESLint para linting
