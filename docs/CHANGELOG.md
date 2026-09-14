# CHANGELOG — KG TRACKER

Todos los cambios notables en este proyecto se documentan en este archivo.

## [v0.2.33] - 2026-09-15
### Corregido
- **Concurrencia:** Aislamiento de señales en `_busqueda_thread` al cancelar/reiniciar búsquedas en segundo plano.
- **Codificación:** Normalización estricta UTF-8 en `config.py` eliminando residuos de caracteres Mojibake.

## [v0.2.32] - 2026-09-15
### Mejorado
- Rediseño profesional de `README.md` con formato estandarizado UTF-8.

## [v0.2.31] - 2026-09-14
### Pruebas
- Ampliación de cobertura de pruebas unitarias para i18n, enriquecedor de Steam y traductor.

## [v0.2.30] - 2026-09-13
### Persistencia
- Estandarización de persistencia atómica de configuración y cachés JSON con respaldos `.bak`.

## [v0.2.29] - 2026-09-12
### Mantenimiento
- Ignorar datos runtime del usuario en `.gitignore` y eliminación de scripts obsoletos.

## [v0.2.28] - 2026-09-11
### Seguridad y Concurrencia
- Aislamiento de sesiones HTTP concurrentes por scraper y escape de caracteres en notificaciones push de PowerShell.
