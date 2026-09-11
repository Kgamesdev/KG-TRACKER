# K GAME TRACKER

Aplicación de escritorio para Windows que consulta ofertas gratuitas de juegos y las organiza por tienda.

## Funciones

- Consulta ofertas de juegos desde la API de GamerPower.
- Clasifica los resultados por Epic Games, Steam, GOG, Amazon Prime, Itch.io, Humble Store, Fanatical, IndieGala y otras plataformas.
- Filtra DLC, demos, bandas sonoras, expansiones y otros contenidos que no son juegos completos.
- Permite abrir la página de cada oferta y marcarla como reclamada.
- Guarda el historial de reclamados localmente en `data/reclamados.json`.
- Permite retirar un juego de Reclamados mediante el botón `NO RECLAMADO`.
- Incluye temas oscuro y claro, control de volumen, música de fondo y caché de imágenes.
- Incluye splash de inicio nativo y opción de inicio automático en Windows.

## Tecnología

- Python 3.14
- PySide6
- requests
- pygame-ce
- Pillow
- NumPy
- plyer

## Requisitos

- Windows
- Python 3.14
- Conexión a Internet

## Instalación y ejecución

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pip install PySide6
python main.py
```

## Estructura principal

- `main.py`: inicio de la aplicación, audio inicial y splash Qt.
- `ui/`: ventana principal, tarjetas de juegos, navegación, historial, tema y modales.
- `core/`: API, audio, imágenes e inicio automático.
- `assets/`: iconos, logotipo y recursos visuales.
- `data/`: datos persistentes, incluido el historial de reclamados.
- `logs/`: registros de ejecución.

## Desarrollo

KG Game Tracker es un proyecto personal de aprendizaje y desarrollo práctico.

## Licencia

MIT License.
