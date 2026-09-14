# POLÍTICA DE SEGURIDAD Y REPORTE DE VULNERABILIDADES

## Medidas de Seguridad Implementadas (v0.2.35)
* **Aislamiento de Código:** Ningún dato procedente de fuentes externas se ejecuta como código. Las notificaciones nativas de Windows utilizan deserialización JSON por STDIN sin comandos de consola dinámicos.
* **Validación de URLs:** Apertura estricta de dominios oficiales verificados bajo protocolo seguro HTTPS.
* **Persistencia Atómica:** Las escrituras en disco emplean reemplazo atómico para evitar corrupción de archivos.
* **Descargas Seguras:** Límites estrictos de tamaño (10MB) y timeouts en la obtención de recursos remotos.

## Reporte Responsable de Vulnerabilidades
Si descubres un problema de seguridad en KG Tracker, por favor abre una incidencia o ponte en contacto directo con el mantenedor del proyecto de forma privada antes de su divulgación pública.
