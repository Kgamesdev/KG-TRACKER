\# K GAME TRACKER 🎮



Una aplicación de escritorio para rastrear y reclamar juegos gratuitos de múltiples plataformas en tiempo real.



!\[Python](https://img.shields.io/badge/Python-3.8+-blue)

!\[Tkinter](https://img.shields.io/badge/GUI-Tkinter-green)

!\[Licencia](https://img.shields.io/badge/Licencia-MIT-yellow)



\---



\## 📋 Características



✅ \*\*Rastreo en tiempo real\*\* - Obtiene ofertas de juegos gratuitos de la API GamerPower  

✅ \*\*Múltiples tiendas\*\* - Soporta Steam, Epic Games, GOG, Amazon Prime, Itch.io, Humble Store y más  

✅ \*\*Dos modos de búsqueda:\*\*

&#x20;  - 🎮 \*\*Solo Juegos\*\* - Filtra DLCs, demostraciones y contenido adicional

&#x20;  - 🎁 \*\*Todo Gratis\*\* - Incluye juegos, DLCs, bundles y demostraciones



✅ \*\*Interfaz moderna\*\* - Temas claro y oscuro  

✅ \*\*Música de fondo\*\* - Reproducción de audio con control de volumen  

✅ \*\*Insignias de notificación\*\* - Muestra cuántas ofertas hay en cada tienda  

✅ \*\*Acordeones expandibles\*\* - Oculta/muestra tiendas según necesites  

✅ \*\*Botones rápidos\*\* - Reclama juegos con un solo click  

✅ \*\*Inicio automático\*\* - Opción para ejecutar la app al encender el ordenador  



\---



\## 🚀 Instalación



\### Requisitos previos

\- \*\*Python 3.8+\*\* instalado

\- \*\*pip\*\* (gestor de paquetes de Python)

\- \*\*Windows\*\* (la app usa características específicas de Windows)



\### Pasos de instalación



1\. \*\*Clonar o descargar el proyecto\*\*

```bash

git clone https://github.com/tu-usuario/k-game-tracker.git

cd k-game-tracker

```



2\. \*\*Crear entorno virtual (recomendado)\*\*

```bash

python -m venv venv

venv\\Scripts\\activate  # En Windows

```



3\. \*\*Instalar dependencias\*\*

```bash

pip install -r requirements.txt

```



4\. \*\*Ejecutar la aplicación\*\*

```bash

python main.py

```



\---



\## 📁 Estructura del Proyecto



```

K GAME TRACKER/

│

├── core/                          # Módulo con funciones centrales

│   ├── \_\_init\_\_.py

│   └── images.py                  # Descarga y procesamiento de imágenes

│

├── ui/                            # Módulo con componentes gráficos

│   ├── \_\_init\_\_.py

│   ├── main\_window.py             # Ventana principal

│   ├── splash\_screen.py           # Pantalla de bienvenida

│   ├── mode\_selector.py           # Selector de modo (Solo Juegos / Todo Gratis)

│   ├── widgets.py                 # Widgets reutilizables

│   └── store\_panel.py             # Panel de tiendas

│

├── logs/                          # Carpeta de logs (se crea automáticamente)

│   └── kgametracker\_YYYY-MM-DD.log

│

├── assets/                        # Recursos gráficos

│   ├── logo.ico                   # Icono de la app

│   └── logo\_KG.png                # Logo principal

│

├── config.py                      # Configuración y constantes globales

├── logger.py                      # Sistema de logging

├── main.py                        # Punto de entrada

├── requirements.txt               # Dependencias de Python

├── .gitignore                     # Archivos a ignorar en Git

├── chill.mp3                      # Música de fondo

└── README.md                      # Este archivo

```



\---



\## 🎯 Cómo usar



\### Al iniciar la app



1\. Verás el \*\*splash screen\*\* con animación de entrada

2\. Se abrirá el \*\*selector de modo\*\*:

&#x20;  - Elige \*\*🎮 SOLO JUEGOS\*\* para ver solo juegos completos

&#x20;  - Elige \*\*🎁 TODO GRATIS\*\* para incluir DLCs, bundles y demos



\### En la ventana principal



1\. \*\*Selecciona tiendas\*\* - Haz click en las burbujas de tiendas para activarlas

2\. \*\*Haz click en "Buscar"\*\* - La app consultará la API

3\. \*\*Verás insignias rojas\*\* con el número de ofertas en cada tienda

4\. \*\*Expande/contrae tiendas\*\* - Haz click en los nombres para ver/ocultar juegos

5\. \*\*Reclama juegos\*\* - Haz click en 🚀 Reclamar para ir al sitio oficial



\### Controles adicionales



\- \*\*☀️ / 🌙\*\* - Alterna entre tema claro y oscuro

\- \*\*🔊 / 🔇\*\* - Controla el volumen de la música

\- \*\*⚙️\*\* - Abre configuración (pantalla completa, autostart)

\- \*\*⬅️ Volver\*\* - Vuelve al selector de modo



\---



\## 🔧 Configuración



Edita `config.py` para personalizar:



```python

\# Cambiar URL de API

API\_URL = "https://..."



\# Ajustar tamaño de thumbnails

THUMBNAIL\_SIZE = (110, 50)



\# Personalizar colores

THEMES = {

&#x20;   "dark": { ... },

&#x20;   "light": { ... }

}



\# Cambiar nombre de audio

AUDIO\_PATH = "tu\_musica.mp3"

```



\---



\## 📊 API utilizada



La app usa la \*\*\[API de GamerPower](https://www.gamerpower.com/api)\*\* para obtener datos de giveaways:



```

GET https://www.gamerpower.com/api/giveaways?type=game

```



Respuesta:

```json

\[

&#x20; {

&#x20;   "id": 1,

&#x20;   "title": "Nombre del Juego",

&#x20;   "description": "Descripción...",

&#x20;   "image": "https://...",

&#x20;   "open\_giveaway\_url": "https://...",

&#x20;   "platforms": "PC, Steam",

&#x20;   "store": "Steam",

&#x20;   "type": "Game"

&#x20; },

&#x20; ...

]

```



\---



\## 📝 Logging



La app registra todos los eventos en:

\- \*\*Archivo\*\*: `logs/kgametracker\_YYYY-MM-DD.log`

\- \*\*Consola\*\*: También se muestran los logs en la terminal



Ejemplos de logs:

```

2024-08-29 10:30:45 - INFO - KGameTracker - ℹ️  K GAME TRACKER - INICIADA

2024-08-29 10:30:50 - DEBUG - KGameTracker - 🔍 Modo seleccionado: Solo Juegos

2024-08-29 10:30:52 - INFO - KGameTracker - ℹ️  Búsqueda iniciada - Modo: Solo Juegos

2024-08-29 10:30:55 - INFO - KGameTracker - ✅ Se encontraron 42 juegos en 8 tiendas

```



\---



\## 🐛 Solución de problemas



\### La app no inicia

\- Verifica que Python 3.8+ esté instalado: `python --version`

\- Reinstala dependencias: `pip install -r requirements.txt --force-reinstall`



\### No hay imagen en las tarjetas de juegos

\- Verifica conexión a internet

\- Revisa los logs: `logs/kgametracker\_YYYY-MM-DD.log`

\- Comprueba que las URLs de imágenes sean válidas



\### El audio no funciona

\- Verifica que `chill.mp3` exista en la carpeta raíz

\- Asegúrate de que el archivo sea válido (pruébalo en tu reproductor)

\- En algunos sistemas, MCI puede no estar disponible



\### Error de importación

\- Verifica que `core/\_\_init\_\_.py` y `ui/\_\_init\_\_.py` existan

\- Asegúrate de estar en la carpeta raíz del proyecto

\- Reinstala dependencias: `pip install -r requirements.txt`



\---



\## 🔐 Características de Windows



La app utiliza características específicas de Windows:



\- \*\*Windows Registry\*\* - Para guardar configuración de autostart

\- \*\*MCI (Media Control Interface)\*\* - Para reproducción de audio

\- \*\*Transparencia de ventana\*\* - Efecto chroma key en el splash screen



Si usas \*\*Linux o macOS\*\*, algunos features podrían no funcionar correctamente.



\---



\## 📦 Dependencias



```

tkinter==0.0.1       # GUI (incluido con Python)

Pillow==10.0.0       # Procesamiento de imágenes

requests==2.31.0     # Solicitudes HTTP

numpy==1.24.3        # Procesamiento numérico

```



Para instalar: `pip install -r requirements.txt`



\---



\## 📄 Licencia



Este proyecto está bajo la licencia MIT. Ver `LICENSE` para más detalles.



\---



\## 🤝 Contribuciones



¿Encontraste un bug o tienes una idea de mejora?



1\. Abre un \*\*Issue\*\* describiendo el problema

2\. Haz un \*\*Fork\*\* del proyecto

3\. Crea una \*\*rama\*\* para tu feature: `git checkout -b feature/mi-feature`

4\. Haz \*\*commit\*\*: `git commit -m "Añade mi feature"`

5\. Haz \*\*push\*\*: `git push origin feature/mi-feature`

6\. Abre un \*\*Pull Request\*\*



\---



\## 👨‍💻 Autor



\*\*KuriBeatbox\*\* - Desarrollador



\---



\## ⭐ Agradecimientos



\- \[GamerPower](https://www.gamerpower.com/) - Por la API de giveaways

\- \[Pillow](https://python-pillow.org/) - Por el procesamiento de imágenes

\- \[Requests](https://docs.python-requests.org/) - Por las solicitudes HTTP



\---



\## 📞 Contacto



¿Preguntas o sugerencias?



\- 📧 Email: kurigamedeveloper@gmail.com
\- 💬 Discord: KuriBeatbox



\---



\## 🎉 ¡Disfruta cazando juegos gratis!



Recuerda: la mayoría de los giveaways tienen plazo limitado. ¡No te pierdas ninguno! 🚀



\---



\*\*Última actualización\*\*: 29 de Agosto de 2024

