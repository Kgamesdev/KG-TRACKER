"""
core/network.py
Cliente HTTP seguro y centralizado para la descarga de recursos remotos.
Resuelve las vulnerabilidades SEC-03 (descargas seguras de imágenes) y NET-01 (concurrencia).
"""

import logging
import urllib.parse
from typing import Optional, Tuple

import requests

from config import APP_VERSION

logger = logging.getLogger("KGTracker.Network")

MAX_IMAGE_SIZE_BYTES = 10 * 1024 * 1024  # Límite de 10 MB por imagen
MAX_REDIRECTS = 3
TIMEOUT_CONEXION: Tuple[float, float] = (3.0, 5.0)  # (Connect, Read)


def crear_sesion_http_segura() -> requests.Session:
    """
    Crea una instancia de requests.Session configurada con:
    - Verificación TLS obligatoria (verify=True).
    - User-Agent estandarizado con la versión real de la aplicación.
    """
    session = requests.Session()
    session.verify = True
    session.headers.update({
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            f"Chrome/124.0.0.0 Safari/537.36 KGTracker/{APP_VERSION}"
        )
    })
    return session


def _es_https(url: str) -> bool:
    try:
        return urllib.parse.urlparse(url).scheme.lower() == "https"
    except Exception:
        return False


def descargar_contenido_seguro(
    url: str,
    max_size: int = MAX_IMAGE_SIZE_BYTES,
    timeout: Tuple[float, float] = TIMEOUT_CONEXION
) -> Optional[bytes]:
    """
    Descarga el contenido de una URL garantizando:
    1. Esquema HTTPS obligatorio, también en cada redirección (máx. MAX_REDIRECTS).
    2. Límite estricto de tamaño recibido en streaming (previene agotamiento de memoria).
    3. Timeouts estrictos de conexión y lectura.
    4. Manejo seguro de errores sin propagar excepciones.
    """
    if not url or not isinstance(url, str):
        return None

    url_actual = url.strip()
    if not _es_https(url_actual):
        return None

    # Sesión independiente por petición (evita race conditions de NET-01)
    with crear_sesion_http_segura() as session:
        try:
            for _ in range(MAX_REDIRECTS + 1):
                # Las redirecciones se siguen a mano para validar HTTPS en cada salto.
                resp = session.get(url_actual, timeout=timeout, stream=True, allow_redirects=False)
                try:
                    if resp.status_code in (301, 302, 303, 307, 308):
                        destino = resp.headers.get("Location", "")
                        url_actual = urllib.parse.urljoin(url_actual, destino)
                        if not _es_https(url_actual):
                            logger.warning("Redirección no HTTPS bloqueada: %s", url_actual[:200])
                            return None
                        continue

                    if resp.status_code != 200:
                        return None

                    content_length = resp.headers.get("Content-Length")
                    if content_length and content_length.isdigit() and int(content_length) > max_size:
                        logger.warning("Recurso excede el tamaño máximo (%s bytes): %s", content_length, url_actual[:200])
                        return None

                    buffer = bytearray()
                    for chunk in resp.iter_content(chunk_size=8192):
                        buffer.extend(chunk)
                        if len(buffer) > max_size:
                            logger.warning("Descarga abortada por exceder %d bytes: %s", max_size, url_actual[:200])
                            return None

                    return bytes(buffer)
                finally:
                    resp.close()

            logger.warning("Demasiadas redirecciones: %s", url[:200])
            return None

        except Exception:
            return None
