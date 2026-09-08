# Changelog

Todas las notas de cambios notables en K GAME TRACKER se documentan en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/),
y este proyecto sigue [Semantic Versioning](https://semver.org/lang/es/).

---

## [Unreleased]

### Planeado para próximas versiones
- [ ] Soporte para macOS y Linux
- [ ] Base de datos local para historial de juegos reclamados
- [ ] Notificaciones del sistema
- [ ] Filtrado avanzado por género
- [ ] Exportar lista de juegos a CSV
- [ ] Integración con Discord webhook
- [ ] API propia para obtener datos históricos
- [ ] Tema personalizado por usuario

---

## [1.0.0] - 2024-08-29

### ✨ Agregado
- ✅ Interfaz gráfica completa con Tkinter
- ✅ Rastreo en tiempo real de juegos gratuitos
- ✅ Soporte para 9 plataformas diferentes:
  - Steam
  - Epic Games Store
  - GOG
  - Amazon Prime Gaming
  - Itch.io
  - Humble Store
  - Fanatical
  - IndieGala
  - Otras Plataformas
- ✅ Dos modos de búsqueda:
  - Solo Juegos (sin DLCs ni demostraciones)
  - Todo Gratis (incluye DLCs, bundles y demos)
- ✅ Tema claro y oscuro intercambiable
- ✅ Reproducción de música de fondo con control de volumen
- ✅ Insignias de notificación en burbujas de tiendas
- ✅ Acordeones expandibles por tienda
- ✅ Descarga y caché de thumbnails de juegos
- ✅ Pantalla de bienvenida (splash screen) con animación
- ✅ Sistema de logging centralizado
- ✅ Configuración de autostart en Windows
- ✅ Panel de ajustes:
  - Maximizar/restaurar ventana
  - Habilitar/deshabilitar autostart
- ✅ Botones directos para reclamar juegos en sus plataformas
- ✅ Documentación completa en README.md

### 🎨 Mejoras visuales
- Diseño moderno con paleta de colores cuidada
- Esquinas redondeadas en el splash screen
- Efecto sombra flotante en el splash
- Animaciones suaves (fade-in, zoom, fade-out)
- Iconos y emojis descriptivos
- Interfaz responsiva que se adapta al contenido

### 🔧 Infraestructura técnica
- Estructura modular con carpetas `core/` y `ui/`
- Separación de responsabilidades:
  - `config.py` - Configuración global
  - `logger.py` - Sistema de logging
  - `core/images.py` - Manejo de imágenes
  - `ui/main_window.py` - Ventana principal
  - `ui/splash_screen.py` - Pantalla de bienvenida
  - `ui/mode_selector.py` - Selector de modo
  - `ui/widgets.py` - Widgets reutilizables
  - `ui/store_panel.py` - Panel de tiendas
- Archivo `requirements.txt` con todas las dependencias
- Archivo `.gitignore` para Git
- Sistema de logging con archivos de log por fecha

### 🐛 Arreglado
- N/A (Primera versión)

### ⚠️ Conocidos
- El audio solo funciona en Windows (usa MCI)
- La transparencia del splash screen solo funciona en Windows
- El registro de Windows solo funciona en Windows
- Pueden haber ocasionales fallos de conexión a la API GamerPower
- Las imágenes pueden tardar en cargar en conexiones lentas

---

## Notas de versión

### Cómo interpretar los cambios

**✨ Agregado** - Nuevas funcionalidades  
**🎨 Mejoras visuales** - Cambios en la UI/UX  
**🔧 Cambios técnicos** - Refactoring, optimizaciones  
**🐛 Arreglado** - Bugs corregidos  
**⚠️ Cambios importantes** - Cambios breaking  
**⚠️ Conocidos** - Problemas/limitaciones actuales  

---

## Versiones futuras

### v1.1.0 (Planeado)
- Soporte para notificaciones del sistema
- Historial de juegos reclamados
- Búsqueda y filtrado avanzado
- Exportar lista a CSV

### v1.2.0 (Planeado)
- Base de datos SQLite local
- Integración con Discord webhook
- API propia para datos históricos
- Estadísticas de juegos por tienda

### v2.0.0 (Planeado)
- Soporte para macOS y Linux
- Tema personalizado por usuario
- Interfaz web alternativa
- App móvil acompañante

---

## Cómo contribuir

Si quieres reportar un bug o sugerir una mejora:

1. Abre un **Issue** en GitHub
2. Describe el problema/idea claramente
3. Incluye pasos para reproducir (si es un bug)
4. Espera feedback del equipo

---

## Soporte

¿Problemas? Revisa:
- 📖 [README.md](README.md) - Guía completa
- 🐛 [Issues](https://github.com/tu-usuario/k-game-tracker/issues) - Problemas reportados
- 📋 [Logs](logs/) - Archivos de log para debugging

---

**Generado por K GAME TRACKER**