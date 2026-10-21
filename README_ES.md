# K GAME TRACKER (KG Tracker)

<p align="center">
  <img src="assets/LogoKG_transparente.png" alt="Logo de KG Tracker" width="150"/>
</p>

<p align="center"><strong>Encuentra y reclama juegos gratis para PC por tiempo limitado desde una sola app de Windows.</strong></p>

<p align="center">
  <a href="#características-principales">Características</a> · <a href="#inicio-rápido">Inicio rápido</a> · <a href="#créditos-y-fuentes-de-datos">Créditos</a> · <a href="https://github.com/Kgamesdev/KG-TRACKER/issues">Ideas y fallos</a>
</p>

<p align="center"><a href="README.md"><strong>🇬🇧 Read in English</strong></a></p>

<p align="center">
  <img src="https://img.shields.io/badge/version-v0.3.4-blue?style=for-the-badge" alt="Versión 0.3.4"/>
  <img src="https://img.shields.io/badge/Python-3.12%20probado-yellow?style=for-the-badge" alt="Python 3.12 probado"/>
  <img src="https://img.shields.io/badge/framework-PySide6%20%2B%20Qt%206-41CD52?style=for-the-badge" alt="PySide6 y Qt 6"/>
  <img src="https://img.shields.io/badge/plataforma-Windows%2010%20%7C%2011-0078D6?style=for-the-badge" alt="Windows 10 y 11"/>
  <a href="LICENSE"><img src="https://img.shields.io/badge/licencia-No%20comercial-orange?style=for-the-badge" alt="Licencia no comercial"/></a>
</p>

<p align="center">
  <a href="https://github.com/Kgamesdev/KG-TRACKER/stargazers"><img src="https://img.shields.io/github/stars/Kgamesdev/KG-TRACKER?style=social" alt="Dar una estrella a KG Tracker"/></a>
  <a href="https://github.com/Kgamesdev/KG-TRACKER/issues"><img src="https://img.shields.io/github/issues/Kgamesdev/KG-TRACKER" alt="Incidencias abiertas"/></a>
</p>

---

## 🎮 Descripción del Proyecto

**KG Tracker** es una aplicación de escritorio nativa para Windows, desarrollada en **Python** y **PySide6 (Qt 6)**. Te ayuda a encontrar ofertas de juegos para PC gratis y por tiempo limitado en distintas tiendas, desde un solo lugar. También añade reseñas de Steam cuando están disponibles y traduce las descripciones en segundo plano.

## ✨ Características Principales

- **Seguimiento multitienda:** combina los listados de GamerPower con búsquedas directas en Epic Games, Steam, GOG e itch.io.
- **Filtrado y deduplicación inteligente:** filtra muchas demos y complementos, y unifica ofertas duplicadas aunque los títulos estén en idiomas distintos.
- **Información útil del juego:** muestra reseñas de Steam cuando están disponibles y traduce descripciones en segundo plano.
- **Avisos y búsquedas en segundo plano:** busca cuando quieras o de forma periódica, con notificaciones de Windows desde la bandeja del sistema.
- **Historial de reclamados y ahorro:** guarda localmente los juegos reclamados y calcula su valor acumulado.
- **Ajustes personales:** interfaz en español e inglés, temas claro y oscuro, preferencias persistentes de música y volumen, e inicio opcional con Windows.
- **Interfaz ágil:** carga las imágenes en segundo plano y utiliza caché para que la navegación sea fluida.

## 🚀 Inicio Rápido

**Requisitos:** Windows 10 u 11 y Python 3.12.

```powershell
git clone https://github.com/Kgamesdev/KG-TRACKER.git
cd KG-TRACKER
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe main.py
```

## 👋 Sobre el Autor

> Este proyecto personal lo he creado yo, un enfermero que nunca ha tenido demasiado tiempo para estudiar programación, pero que siempre ha tenido unas ganas enormes de aprender. Lo he desarrollado a partir de investigación y con ayuda de la IA. Espero que disfrutéis las horas y el cariño que le he dedicado.

## 🧰 Arquitectura y Stack Tecnológico

| Componente | Tecnología |
| :--- | :--- |
| **Lenguaje** | Python 3.12 (probado) |
| **Interfaz Gráfica** | PySide6 (Qt 6.x) con hojas de estilo QSS |
| **Procesamiento de Imágenes** | Pillow (`PIL`) |
| **Conexiones de red** | `requests` y sesiones concurrentes |
| **Motor de Audio** | `pygame-ce` |
| **Persistencia** | JSON local con escrituras atómicas |

## 🔌 Créditos y Fuentes de Datos

KG Tracker utiliza los siguientes servicios y endpoints públicos. La disponibilidad y los datos de las ofertas dependen de sus proveedores.

- **[API de GamerPower](https://www.gamerpower.com/api/)** — listados y detalles de regalos.
- **[Epic Games Store](https://store-site-backend-static.ak.epicgames.com/)** — catálogo de promociones de juegos gratis.
- **[Steam Store](https://store.steampowered.com/)** — juegos destacados gratis o rebajados, búsqueda de juegos y reseñas de la comunidad; las imágenes se sirven desde la CDN de Steam.
- **[itch.io](https://itch.io/games/on-sale?format=json)** — listado de juegos en oferta.
- **[Catálogo de GOG](https://catalog.gog.com/)** — catálogo de juegos rebajados.
- **[Google Translate](https://translate.googleapis.com/)** — fuente principal para traducir descripciones.
- **[API de traducción MyMemory](https://mymemory.translated.net/)** — alternativa de traducción.
- **[API de GitHub Releases](https://docs.github.com/en/rest/releases/releases)** — consulta de nuevas versiones desde la app.

## ☕ Apoya el Proyecto

Si KG Tracker te resulta útil y quieres apoyar su desarrollo, puedes [invitarme a un café en Ko-fi](https://ko-fi.com/kurigamedeveloper).

## 📋 Novedades Recientes (v0.3.4)

- Más cobertura de juegos gratis al combinar listados de regalos con búsquedas directas en tiendas.
- Mejor detección de duplicados cuando un mismo juego aparece en distintos idiomas.
- Preferencias de música persistentes y controles de reproducción funcionales.
- Protección contra varias instancias y comportamiento más claro al cerrar o minimizar a la bandeja.

## 🤝 Ayuda a Mejorar el Proyecto

¿Has encontrado un fallo o tienes una idea? [Abre una incidencia](https://github.com/Kgamesdev/KG-TRACKER/issues). Las contribuciones son bienvenidas; consulta la [licencia no comercial](LICENSE) antes de reutilizar el código.

## Licencia

Este proyecto está bajo una **Licencia No Comercial**. Consulta [LICENSE](LICENSE) para más información.
