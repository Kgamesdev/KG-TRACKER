# Política de privacidad — KG Tracker

**Versión documentada:** 0.5.1
**Última revisión:** 23 de octubre de 2026

KG Tracker consulta catálogos y promociones públicas para mostrar ofertas. No requiere una cuenta de KG Tracker.

## Datos y almacenamiento

- La aplicación no solicita ni almacena contraseñas, cookies de tienda, tokens de acceso ni datos bancarios.
- No integra telemetría ni analítica de uso propia.
- Preferencias, juegos reclamados y Wishlist se guardan en el equipo, bajo `%LOCALAPPDATA%\KGTracker\` en Windows. La carpeta `cache` contiene imágenes y datos públicos de ofertas para acelerar la interfaz.
- La Wishlist guarda los identificadores y títulos elegidos, la carátula, el objetivo de precio, precios/ofertas consultados y la fecha de actualización. No contiene credenciales de las tiendas.
- El usuario puede borrar esos datos cerrando la aplicación y eliminando `%LOCALAPPDATA%\KGTracker\`.

## Conexiones de red

La aplicación hace peticiones HTTPS a servicios externos para sus funciones:

- **GamerPower** y las API públicas de **Epic Games**, **Steam** e **itch.io** para ofertas gratuitas.
- **CheapShark** para búsqueda de juegos, tiendas admitidas y ofertas/precios de Wishlist.
- Las API de **Steam** y el catálogo público de **GOG** para precios regionales de España en EUR cuando hay una coincidencia exacta.
- Catálogos/páginas públicas de **Fanatical**, **GOG**, **Amazon Luna** y otros proveedores usados por sus conectores; fuentes de imágenes de las tiendas y sus CDNs.
- **Google Translate** y **MyMemory** para traducir descripciones cuando hace falta.
- **GitHub Releases API** para comprobar si hay una versión nueva.

Los servicios externos reciben las peticiones necesarias para responder a la función solicitada, incluida la búsqueda de títulos. KG Tracker no garantiza su disponibilidad ni sus condiciones. La cobertura de precios de Wishlist depende de cada fuente: hoy se verifican precios regionales exactos para Steam y GOG; otras tiendas solo aparecen cuando CheapShark las lista y sus precios pueden no tener verificación regional en EUR. La aplicación no inventa ni convierte precios USD para presentarlos como precios españoles.

Los enlaces de compra y el enlace de Ko-fi se abren en el navegador solo como consecuencia de la acción del usuario.
