# Seguridad — KG Tracker

**Versión documentada:** 0.5.1
**Última revisión:** 23 de octubre de 2026

## Protecciones actuales

- Las peticiones de imágenes usan HTTPS, validan dominios permitidos, limitan el tamaño descargado y aplican tiempos máximos de conexión y lectura.
- Las respuestas externas se tratan como datos; no se ejecutan como código.
- La configuración, los juegos reclamados y la Wishlist se escriben mediante persistencia atómica. Si no se puede guardar un cambio de Wishlist, la interfaz informa del error y revierte cambios locales puntuales cuando corresponde.
- La compilación de release ejecuta la suite de pruebas y comprueba que el ejecutable generado carga Qt y construye la ventana principal antes de generar el checksum.
- La aplicación no gestiona credenciales de las tiendas.

## Reportar una vulnerabilidad

Abre una incidencia en el repositorio de KG Tracker con pasos de reproducción y el impacto observado. Para un problema que pueda comprometer datos de usuarios, contacta primero de forma privada con el mantenedor y evita publicar detalles explotables hasta que exista una corrección.
