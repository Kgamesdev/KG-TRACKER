# K GAME TRACKER

<p align="center">
  <img src="assets/LogoKG_transparente.png" alt="KG Tracker" width="132"/>
</p>

<p align="center"><strong>Encuentra juegos gratis para PC en distintas tiendas desde una sola app de Windows.</strong></p>

<p align="center">
  <a href="#inicio-rápido">Empezar</a> ·
  <a href="#características">Ver características</a> ·
  <a href="https://github.com/Kgamesdev/KG-TRACKER/issues">Proponer una idea o informar de un fallo</a> ·
  <a href="https://github.com/Kgamesdev/KG-TRACKER">Dar una estrella</a>
</p>

<p align="center">
  <a href="README.md"><strong>Read in English</strong></a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/version-v0.3.4-blue?style=for-the-badge" alt="Versión 0.3.4"/>
  <img src="https://img.shields.io/badge/Python-3.12%20probado-yellow?style=for-the-badge" alt="Python 3.12 probado"/>
  <img src="https://img.shields.io/badge/GUI-PySide6%20%2B%20Qt%206-41CD52?style=for-the-badge" alt="PySide6 y Qt 6"/>
  <img src="https://img.shields.io/badge/plataforma-Windows%2010%20%7C%2011-0078D6?style=for-the-badge" alt="Windows 10 y 11"/>
  <a href="LICENSE"><img src="https://img.shields.io/badge/licencia-No%20comercial-orange?style=for-the-badge" alt="Licencia no comercial"/></a>
</p>

<p align="center">
  <a href="https://github.com/Kgamesdev/KG-TRACKER/stargazers"><img src="https://img.shields.io/github/stars/Kgamesdev/KG-TRACKER?style=social" alt="Dar una estrella a KG Tracker en GitHub"/></a>
  <a href="https://github.com/Kgamesdev/KG-TRACKER/issues"><img src="https://img.shields.io/github/issues/Kgamesdev/KG-TRACKER" alt="Incidencias abiertas"/></a>
</p>

---

KG Tracker te ayuda a encontrar ofertas de juegos para PC por tiempo limitado sin tener que revisar cada tienda manualmente. Combina los listados de **GamerPower** con búsquedas en tiendas compatibles y reúne las ofertas en una sola aplicación.

## Características

- **Más oportunidades para encontrar juegos:** combina listados de ofertas y fuentes directas compatibles para ampliar la cobertura.
- **Resultados más limpios:** filtra muchos DLC y demos, y reduce duplicados aunque las tiendas muestren títulos distintos o en otros idiomas.
- **Información útil del juego:** muestra reseñas de Steam cuando están disponibles y traduce las descripciones en segundo plano.
- **No te pierdas una oferta:** consulta cuando quieras o activa búsquedas periódicas y notificaciones de Windows desde la bandeja del sistema.
- **Historial de reclamados:** guarda localmente los juegos que has reclamado y muestra el ahorro acumulado.
- **A tu gusto:** interfaz en español e inglés, temas claro y oscuro, ajustes persistentes de música y volumen, e inicio opcional con Windows.

KG Tracker está hecha para Windows 10 y 11 con Python y PySide6. Las ofertas pueden caducar o variar según la región, la cuenta y la tienda.

## Inicio rápido

### Requisitos

- Windows 10 u 11
- Python 3.12 (probado)

### Ejecutar desde el código fuente

```powershell
git clone https://github.com/Kgamesdev/KG-TRACKER.git
cd KG-TRACKER
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe main.py
```

## Ayuda a mejorar el proyecto

¿Has encontrado un fallo, echas en falta una tienda o tienes una idea? [Abre una incidencia](https://github.com/Kgamesdev/KG-TRACKER/issues) e indica qué esperabas y qué ocurrió. Si KG Tracker te resulta útil, [dale una estrella al repositorio](https://github.com/Kgamesdev/KG-TRACKER/stargazers); así otros jugadores podrán descubrirlo.

Las contribuciones son bienvenidas: haz un fork, prepara un cambio concreto y envía una pull request. Consulta la [licencia](LICENSE) antes de reutilizar el código; este proyecto es **no comercial**.

## Apoya el proyecto

KG Tracker es un proyecto personal de aprendizaje. Si quieres apoyar su desarrollo, puedes [invitarme a un café en Ko-fi](https://ko-fi.com/kurigamedeveloper).

## Créditos

Los datos de ofertas vienen de [GamerPower](https://www.gamerpower.com/). La app también muestra reseñas de la comunidad de Steam cuando están disponibles.
