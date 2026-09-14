# K GAME TRACKER (KG Tracker)

<p align="center">
  <img src="assets/LogoKG_transparente.png" alt="KG Tracker Logo" width="130"/>
</p>

<p align="center">
  <strong>Centro de control de escritorio para rastrear, centralizar y reclamar videojuegos gratuitos por tiempo limitado para PC.</strong>
</p>

<p align="center">
  <a href="README.md"><strong>English / Versión en Inglés</strong></a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/version-v0.2.35-blue?style=for-the-badge" alt="Version"/>
  <img src="https://img.shields.io/badge/python-3.14+-yellow?style=for-the-badge" alt="Python Version"/>
  <img src="https://img.shields.io/badge/framework-PySide6%20(Qt%206)-41CD52?style=for-the-badge" alt="PySide6"/>
  <img src="https://img.shields.io/badge/platform-Windows%2010%20%7C%2011-0078D6?style=for-the-badge" alt="Platform"/>
  <img src="https://img.shields.io/badge/license-Non--Commercial-orange?style=for-the-badge" alt="License"/>
</p>

---

## Descripción del Proyecto

**KG Tracker** es una aplicación de escritorio nativa para Windows desarrollada en **Python** y **PySide6 (Qt 6)**. Su objetivo es mantener a los usuarios informados sobre todas las ofertas de juegos 100% gratuitos y por tiempo limitado en las principales tiendas digitales de PC, filtrando automáticamente DLCs, demos, pases de temporada o bandas sonoras.

Cuenta con un motor de enriquecimiento de datos en tiempo real que cruza cada oferta con las **reseñas comunitarias de Steam** y traduce las descripciones dinámicamente en segundo plano.

---

## Características Principales

- **Rastreo Multitienda Centralizado:** Monitorea ofertas de Epic Games, Steam, GOG, Amazon Prime Gaming, Itch.io, Humble Store, Fanatical e IndieGala mediante la API de GamerPower.
- **Filtrado Inteligente:** Elimina automáticamente expansiones, skins, demos, betas y contenido secundario, mostrando exclusivamente videojuegos completos.
- **Cruce con Steam API en Vivo:** Muestra la puntuación comunitaria y el porcentaje de críticas positivas de Steam (ej. `Steam: 95% (Muy positivas)`) incluso en ofertas regaladas por Epic Games, GOG o Prime Gaming.
- **Traductor Dinámico de Descripciones:** Motor asíncrono con fallback multicanal (Google Mobile Web + MyMemory) que traduce las descripciones en segundo plano sin congelar la interfaz.
- **Internacionalización Completa (i18n):** Soporte bilingüe en caliente (Español / English) para botones, estados, modales, menús contextuales y notificaciones.
- **Arquitectura de Alto Rendimiento (60 FPS):** Carga y renderizado asíncrono de carátulas (`QThreadPool` + `QRunnable`) con caché multinivel en RAM y disco para un desplazamiento fluido.
- **Integración con System Tray de Windows:** Minimiza al área de notificación junto al reloj con notificaciones push nativas bilingües y temporizador de barrido periódico configurable (2h, 4h, 8h, 24h).
- **Historial de Reclamados y Cálculo de Ahorro:** Guarda localmente con I/O atómico seguro los juegos obtenidos y calcula el valor total acumulado en dólares (`$ AHORRADO`).
- **Hilo Musical Configurable:** Reproducción de audio de fondo con transiciones suaves (*Fade Out* al minimizar, *Fade In* al restaurar).

---

## Sobre el Autor

> Este proyecto personal ha sido realizado por mí, un enfermero que nunca ha tenido demasiado tiempo para estudiar programación, y siempre ha tenido unas ganas atroces de aprender. He desarrollado este proyecto ayudado únicamente de la investigación y de la IA. Espero que disfrutéis las horas y cariño que le he puesto.

---

## Arquitectura y Stack Tecnológico

| Componente | Tecnología |
| :--- | :--- |
| **Lenguaje** | Python 3.14 |
| **Interfaz Gráfica (GUI)** | PySide6 (Qt 6.x) con hojas de estilo dinámicas (QSS) |
| **Procesamiento de Imágenes** | Pillow (`PIL`) |
| **Consumo de APIs y Red** | `requests` con manejo de sesiones concurrentes |
| **Motor de Audio** | `pygame-ce` |
| **Persistencia** | JSON transaccional con escritura atómica (`fsync` + reemplazo seguro) |

---

## Licencia

Este proyecto está bajo una **Licencia No Comercial** (Non-Commercial License). Consulta el archivo [**LICENSE**](LICENSE) para más información.
