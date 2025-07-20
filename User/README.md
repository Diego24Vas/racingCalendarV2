# Racing Calendar - Vista de Usuario

Esta es la aplicación frontend para usuarios del Racing Calendar, desarrollada con React y Vite.

## 🚀 Características

- **Interfaz moderna y responsiva** con React 18
- **Bienvenida personalizada** con saludo según la hora del día
- **Reloj en tiempo real** con fecha y hora actual
- **Diseño moderno** con gradientes y animaciones
- **Routing** preparado para futuras páginas
- **Arquitectura limpia** siguiendo principios de Clean Architecture

## 📋 Requisitos

- Node.js (versión 16 o superior)
- npm o yarn

## 🛠️ Instalación

1. Navega a la carpeta del frontend:
```bash
cd User/frontend
```

2. Instala las dependencias:
```bash
npm install
```

## 🎮 Comandos disponibles

- **Desarrollo**: `npm run dev` - Inicia el servidor de desarrollo en el puerto 3001
- **Build**: `npm run build` - Construye la aplicación para producción
- **Preview**: `npm run preview` - Vista previa de la build de producción
- **Lint**: `npm run lint` - Verifica el código con ESLint

## 🚀 Iniciar la aplicación

Para iniciar el servidor de desarrollo:

```bash
npm run dev
```

La aplicación estará disponible en: `http://localhost:3001`

## 📁 Estructura del proyecto

```
src/
├── App.jsx                 # Componente principal
├── main.jsx               # Punto de entrada
├── presentation/
│   ├── components/        # Componentes reutilizables
│   │   └── WelcomeComponent.jsx
│   └── pages/            # Páginas de la aplicación
│       └── HomePage.jsx
└── shared/
    └── styles/           # Estilos globales
        ├── App.css
        └── index.css
```

## 🎨 Características de la interfaz

- **Saludo dinámico**: Cambia según la hora del día
- **Reloj en tiempo real**: Muestra la hora y fecha actual
- **Diseño responsivo**: Se adapta a diferentes tamaños de pantalla
- **Animaciones suaves**: Para una mejor experiencia de usuario
- **Tema moderno**: Con gradientes y efectos visuales

## 🔮 Próximas características

- Visualización del calendario de carreras
- Filtros por categorías
- Vista detallada de eventos
- Notificaciones de carreras próximas

---

Desarrollado para el proyecto Racing Calendar V2
