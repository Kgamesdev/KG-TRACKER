# Changelog

Los cambios relevantes de KG Game Tracker se documentan en este archivo.

## [En desarrollo]

## [0.1.10] - 2026-09-11

### Añadido
- Notificación al minimizar que informa en tiempo real las ofertas sin reclamar disponibles.
- Notificación al finalizar el barrido de ofertas (tanto periódico como manual desde el System Tray).

## [0.1.9] - 2026-09-11

### Añadido
- Modal de Ajustes 100% funcional con persistencia en data/settings.json.
- Selector de frecuencia de barrido de ofertas en segundo plano (2h, 4h, 8h, 24h, off).
- Interruptor para activar/desactivar notificaciones de escritorio.
- Opción de inicio voluntario con Windows vinculada al Registro.

## [0.1.8] - 2026-09-11

### Mejorado
- Notificación de bandeja silenciosa (sin el sonido estridente de alerta de Windows).
- La notificación ahora informa dinámicamente el número real de ofertas disponibles sin reclamar.

## [0.1.7] - 2026-09-11

### Añadido
- Módulo ui/main_window_tray.py para desacoplar el ciclo de vida del System Tray.
- Transición suave de audio (Fade Out) al minimizar al área de notificación de Windows.
- Transición suave de audio (Fade In) al restaurar la ventana desde el reloj.

## [0.1.6] - 2026-09-11

### Añadido
- Integración con la bandeja del sistema (System Tray) al pulsar cerrar.
- Notificación educativa nativa de Windows en el primer cierre explicando que la app sigue activa.
- Menú contextual en el icono del reloj para abrir la app o salir completamente.

## [0.1.5] - 2026-09-11

### Corregido
- Corregido el salto automático del scroll al fondo al pulsar 'NO RECLAMADO'.
- Preservada la posición exacta de visualización del usuario tras modificar el estado de un juego.

## [0.1.5] - 2026-09-11

### Corregido
- Corregido el salto automático del scroll al fondo al pulsar 'NO RECLAMADO'.
- Preservada la posición exacta de visualización del usuario tras modificar el estado de un juego.

## [0.1.4] - 2026-09-11

### Corregido
- Eliminado autostart forzado no consentido en el Registro de Windows.
- Optimizado subsistema de dependencias eliminando librerías innecesarias de audio.
- Resueltas inconsistencias de contraste WCAG AA en la paleta del modo claro.
- Implementada persistencia atómica con copias de seguridad automáticas en el historial.

### Cambiado

- El indicador de estado de bÃºsqueda usa un pulso azul neÃ³n temporal mientras se consulta la API.

## [0.1.3] - 2026-09-11

### Corregido

- El botÃ³n `NO RECLAMADO` elimina correctamente el juego del historial persistente.
- La vista de Reclamados mantiene su estado y actualiza sus tarjetas tras modificar un juego.
- Se consolidÃ³ el guardado previo de cambios en el historial de reclamados.
- Se ajustÃ³ el comportamiento de la ventana en su modo expandido.

## [0.1.2] - 2026-09-10

### Mejorado

- Splash de inicio con transiciÃ³n cinematogrÃ¡fica.
- ReducciÃ³n de parpadeos durante las transiciones de la interfaz.

## [0.1.1] - 2026-09-10

### AÃ±adido

- Ondas de borde neÃ³n en la interfaz.

## [0.1.0] - 2026-09-10

### AÃ±adido

- Primera versiÃ³n estable de la interfaz Qt.

## [0.0.10] - 2026-09-11

### Corregido

- El indicador `LISTO` permanece visible al abrir Reclamados.
- El botÃ³n de Reclamados tiene espacio suficiente para mostrar su texto completo.

## [0.0.9] - 2026-09-11

### Mejorado

- AnimaciÃ³n de bÃºsqueda en el indicador de estado.
- CorrecciÃ³n del recorte lateral del efecto neÃ³n.
- Barra inferior anclada visualmente al borde inferior al maximizar o restaurar la ventana.

## [0.0.8] - 2026-09-10

### Mejorado

- Estabilidad y fluidez de la interfaz.
- ReducciÃ³n de repintados, saltos visuales y parpadeos.

## [0.0.7] - 2026-09-10

### Cambiado

- DivisiÃ³n de `main_window.py` en mÃ³dulos especializados de interfaz, tema, audio, juegos, historial, navegaciÃ³n y utilidades.

## [0.0.5] - 2026-09-10

### Cambiado

- MigraciÃ³n de los modales de Ko-fi y ajustes a PySide6.

## [0.0.4] y anteriores

### Cambiado

- Retirada progresiva de componentes heredados de Tkinter.
- Limpieza de imÃ¡genes y paneles obsoletos.








