# Informe de auditoría y correcciones — KG Tracker

Base auditada: commit `1c643ed` (v0.3.2). Revisión estática del código, la configuración de build y el contenido del repo.
No se ejecutó la aplicación en Windows ni se comprobaron CVEs de dependencias (lo cubre el job `pip-audit` de CI).

| # | Severidad | Hallazgo | Corrección |
|---|-----------|----------|------------|
| 1 | Alta | `core/validators.py` existía y tenía tests, pero ningún código de producción lo usaba: `webbrowser.open()` recibía URLs de la API sin validar (aceptaba `file:`, `http:`...). | `abrir_url_externa_segura` se usa en reclamación, `abrir_enlace`, banner de actualización (solo `github.com`) y Ko-fi. El validador rechaza además credenciales embebidas, puertos no estándar y caracteres de control. |
| 2 | Alta | `dist/`, `build/`, dos `.exe` y un zip de 65 MB versionados (~261 MB). 40 archivos basura en la raíz (fragmentos de `autostart.py` salidos de una redirección de shell). | Archivos basura eliminados; `build/`, `dist/`, `*.exe`, `*.zip` en `.gitignore`; los binarios se publican en Releases (ver `scripts/untrack_binarios.ps1`). |
| 3 | Media | `logger.py` creaba `logs/` junto al módulo sin `try` (fallo de arranque en carpetas sin permiso), ignoraba `LOGS_DIR`, siempre en DEBUG y sin rotación. | Usa `%LOCALAPPDATA%\KGTracker\logs`, con fallback a la carpeta temporal o solo consola, rotación 1 MB x 3 y nivel INFO. |
| 4 | Media-baja | Las redirecciones podían salir de HTTPS; sin límite de dimensiones (bomba de descompresión); `_load_thumbnail` (código muerto) evadía `network.py` y escribía en una carpeta relativa. | Redirecciones validadas a mano, límite de 4096 px / 12 Mpx antes de decodificar, función muerta eliminada. |
| 5 | Media-baja | Dos `.spec` (uno sin `assets`), UPX activado, `requirements.txt` en UTF-16 con dependencias sin usar (Pillow, numpy), sin CI. | Un único `KGameTracker.spec` (con `assets`, sin UPX); `requirements.txt` UTF-8 con dependencias directas y `requirements-lock.txt` completo; CI en GitHub Actions (tests + `pip-audit`) y Dependabot. |
| 6 | Baja | Documentación desfasada: versiones inconsistentes (0.2.35 / 0.3.1 / 0.3.2), `SECURITY.md` describía PowerShell, `.env.example` sin uso, `SyntaxWarning` en `core/paths.py`. | `SECURITY.md` reescrito, User-Agent con `APP_VERSION`, `.env.example` eliminado, docstring en cadena raw. |

## Revisión de la auditoría anterior
Algunos puntos de la fase 2 no eran vulnerabilidades reales de esta aplicación y no se han aplicado:
cifrado AES-256 de datos (solo hay ajustes y juegos reclamados, sin credenciales) y protección contra
DoS/Slowloris (es una aplicación cliente; ya usa timeouts en todas las peticiones).

## Pendiente (fuera del alcance de estos cambios)
* Firmar digitalmente el ejecutable.
* Ampliar los tests de la capa `ui/` (la suite actual cubre sobre todo `core/`).
* Reescribir el historial de git si se quiere eliminar el peso de los binarios antiguos (`git filter-repo`).
