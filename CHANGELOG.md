# Changelog

Los cambios relevantes de KG Game Tracker se documentan en este archivo.

## [En desarrollo]

### Cambiado

- El indicador de estado de búsqueda usa un pulso azul neón temporal mientras se consulta la API.

## [0.1.3] - 2026-09-11

### Corregido

- El botón `NO RECLAMADO` elimina correctamente el juego del historial persistente.
- La vista de Reclamados mantiene su estado y actualiza sus tarjetas tras modificar un juego.
- Se consolidó el guardado previo de cambios en el historial de reclamados.
- Se ajustó el comportamiento de la ventana en su modo expandido.

## [0.1.2] - 2026-09-10

### Mejorado

- Splash de inicio con transición cinematográfica.
- Reducción de parpadeos durante las transiciones de la interfaz.

## [0.1.1] - 2026-09-10

### Añadido

- Ondas de borde neón en la interfaz.

## [0.1.0] - 2026-09-10

### Añadido

- Primera versión estable de la interfaz Qt.

## [0.0.10] - 2026-09-11

### Corregido

- El indicador `LISTO` permanece visible al abrir Reclamados.
- El botón de Reclamados tiene espacio suficiente para mostrar su texto completo.

## [0.0.9] - 2026-09-11

### Mejorado

- Animación de búsqueda en el indicador de estado.
- Corrección del recorte lateral del efecto neón.
- Barra inferior anclada visualmente al borde inferior al maximizar o restaurar la ventana.

## [0.0.8] - 2026-09-10

### Mejorado

- Estabilidad y fluidez de la interfaz.
- Reducción de repintados, saltos visuales y parpadeos.

## [0.0.7] - 2026-09-10

### Cambiado

- División de `main_window.py` en módulos especializados de interfaz, tema, audio, juegos, historial, navegación y utilidades.

## [0.0.5] - 2026-09-10

### Cambiado

- Migración de los modales de Ko-fi y ajustes a PySide6.

## [0.0.4] y anteriores

### Cambiado

- Retirada progresiva de componentes heredados de Tkinter.
- Limpieza de imágenes y paneles obsoletos.
