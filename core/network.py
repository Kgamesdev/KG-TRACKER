"""
core/network.py
Cliente HTTP seguro y centralizado para la descarga de recursos remotos.
Resuelve las vulnerabilidades SEC-03 (descargas seguras de imágenes) y NET-01 (concurrencia).
"""

import urllib.parse
import requests
from typing import Optional, Tuple

MAX_IMAGE_SIZE_BYTES = 10 * 1024 * 1024  # Límite de 10 MB por imagen
TIMEOUT_CONEXION: Tuple[float, float] = (3.0, 5.0)  # (Connect, Read)


def crear_sesion_http_segura() -> requests.Session:
    """
    Crea una instancia de requests.Session configurada con:
    - Verificación TLS obligatoria (verify=True).
    - User-Agent corporativo estandarizado.
    """
    session = requests.Session()
    session.verify = True
    session.headers.update({
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36 KGTracker/0.2.35"
        )
    })
    return session


def descargar_contenido_seguro(
    url: str,
    max_size: int = MAX_IMAGE_SIZE_BYTES,
    timeout: Tuple[float, float] = TIMEOUT_CONEXION
) -> Optional[bytes]:
    """
    Descarga el contenido de una URL garantizando:
    1. Esquema HTTPS obligatorio.
    2. Límite estricto de tamaño recibido en streaming (previene ataques de agotamiento de memoria).
    3. Timeouts estrictos de conexión y lectura.
    4. Manejo seguro de errores sin propagar excepciones.
    """
    if not url or not isinstance(url, str):
        return None

    url_str = url.strip()
    try:
        parsed = urllib.parse.urlparse(url_str)
        if parsed.scheme.lower() != "https":
            return None
    except Exception:
        return None

    # Usar una sesión independiente por petición (evita race conditions de NET-01)
    with crear_sesion_http_segura() as session:
        try:
            resp = session.get(url_str, timeout=timeout, stream=True, allow_redirects=True)
            if resp.status_code != 200:
                return None

            content_length = resp.headers.get("Content-Length")
            if content_length and content_length.isdigit():
                if int(content_length) > max_size:
                    print(f"[NETWORK SECURITY] Recurso {url} excede el tamaño máximo ({content_length} bytes)")
                    return None

            buffer = bytearray()
            for chunk in resp.iter_content(chunk_size=8192):
                buffer.extend(chunk)
                if len(buffer) > max_size:
                    print(f"[NETWORK SECURITY] Descarga abortada por exceder {max_size} bytes: {url}")
                    return None

            return bytes(buffer)

        except Exception:
            return None
