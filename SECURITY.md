# Política de seguridad

## Medidas implementadas
* **Apertura de enlaces:** toda URL que se abre en el navegador pasa por `core/validators.py`
  (`abrir_url_externa_segura`): solo HTTPS, host en lista blanca de tiendas oficiales, sin
  credenciales embebidas (`usuario@`) ni puertos distintos de 443. El enlace de actualización
  solo admite `github.com`.
* **Descargas de recursos:** `core/network.py` exige HTTPS también en cada redirección (máx. 3),
  limita el tamaño a 10 MB, aplica timeouts y no propaga excepciones. `core/image_loader.py`
  rechaza imágenes de más de 4096 px por lado o 12 Mpx antes de decodificarlas.
* **Notificaciones:** se envían con `plyer`; ningún dato externo se ejecuta como comando.
* **Persistencia atómica:** las escrituras usan archivo temporal + `fsync` + `os.replace`, con copia `.bak`.
* **Datos del usuario:** se guardan en `%LOCALAPPDATA%\KGTracker` (ajustes, juegos reclamados, cachés y logs).
  La aplicación no almacena credenciales ni datos personales.
* **Logs:** nivel INFO por defecto, rotación automática (1 MB x 3) y las librerías HTTP en WARNING para no
  registrar URLs completas. Para depurar: variable de entorno `KGT_DEBUG=1`.
* **Cadena de suministro:** CI con tests y `pip-audit`, Dependabot semanal, dependencias fijadas en
  `requirements-lock.txt`. Los ejecutables se publican solo en GitHub Releases junto a su SHA256
  (`build.py` lo genera).

## Limitaciones conocidas
* El ejecutable no está firmado digitalmente, por lo que Windows SmartScreen puede mostrar un aviso.
* Se aceptan todos los subdominios de los dominios de la lista blanca (p. ej. páginas de creadores en `*.itch.io`).

## Reporte responsable de vulnerabilidades
Si descubres un problema de seguridad en KG Tracker, abre un *security advisory* privado en la pestaña
**Security** del repositorio o contacta con el mantenedor de forma privada antes de su divulgación pública.
