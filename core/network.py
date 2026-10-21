"""
core/network.py
Cliente HTTP seguro y centralizado para la descarga de recursos remotos.
Resuelve las vulnerabilidades SEC-03 (descargas seguras de imágenes) y NET-01 (concurrencia).
"""

import urllib.parse
import requests
from typing import Optional, Tuple
from config import APP_VERSION

MAX_IMAGE_SIZE_BYTES = 10 * 1024 * 1024  # Límite de 10 MB por imagen
TIMEOUT_CONEXION: Tuple[float, float] = (3.0, 5.0)  # (Connect, Read)

# CDNs usadas por las tiendas consultadas y por las imágenes de GamerPower.
# Cada redirección debe permanecer dentro de esta lista.
_DOMINIOS_IMAGENES_PERMITIDOS = frozenset({
    "gamerpower.com",
    "steamstatic.com",
    "steampowered.com",
    "epicgames.com",
    "unrealengine.com",
    "itch.zone",
    "itch.io",
    "gog-statics.com",
    "gog.com",
    "fanatical.com",
    "indiegala.com",
    "couchloot.com",
    "amazon.com",
    "media-amazon.com",
    "ssl-images-amazon.com",
})


def _url_imagen_permitida(url: str) -> bool:
    """Acepta solo HTTPS hacia CDNs conocidas, sin credenciales ni puertos alternativos."""
    try:
        parsed = urllib.parse.urlsplit(url)
        hostname = (parsed.hostname or "").lower().rstrip(".")
        puerto = parsed.port
    except (TypeError, ValueError):
        return False

    if (
        parsed.scheme.lower() != "https"
        or not hostname
        or parsed.username is not None
        or parsed.password is not None
        or puerto not in (None, 443)
    ):
        return False

    return any(
        hostname == dominio or hostname.endswith("." + dominio)
        for dominio in _DOMINIOS_IMAGENES_PERMITIDOS
    )


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
            f"Chrome/124.0.0.0 Safari/537.36 KGTracker/{APP_VERSION}"
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
    1. Esquema HTTPS y dominios de imagen permitidos.
    2. Límite estricto de tamaño recibido en streaming (previene ataques de agotamiento de memoria).
    3. Timeouts estrictos de conexión y lectura.
    4. Manejo seguro de errores sin propagar excepciones.
    """
    if not url or not isinstance(url, str):
        return None

    if not isinstance(max_size, int) or max_size <= 0:
        return None

    url_str = url.strip()
    if not _url_imagen_permitida(url_str):
        return None

    # Usar una sesión independiente por petición (evita race conditions de NET-01).
    # Seguir redirecciones manualmente para impedir una bajada de HTTPS a HTTP.
    with crear_sesion_http_segura() as session:
        resp = None
        try:
            current_url = url_str
            for redirect_count in range(6):
                if not _url_imagen_permitida(current_url):
                    return None

                resp = session.get(
                    current_url, timeout=timeout, stream=True, allow_redirects=False
                )
                if resp.status_code not in (301, 302, 303, 307, 308):
                    break

                location = resp.headers.get("Location")
                resp.close()
                resp = None
                if not location or redirect_count == 5:
                    return None
                current_url = urllib.parse.urljoin(current_url, location)

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
        finally:
            if resp is not None:
                resp.close()
