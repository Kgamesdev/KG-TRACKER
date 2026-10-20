"""
core/validators.py
Validador centralizado de URLs externas y esquemas de red.

Toda apertura de un enlace en el navegador del sistema debe pasar por
`abrir_url_externa_segura`, que exige HTTPS, un host dentro de la lista blanca
y rechaza credenciales embebidas y puertos no estándar.
"""

import logging
import urllib.parse
import webbrowser
from typing import Optional, Set

logger = logging.getLogger("KGTracker.Validators")

# Lista blanca de dominios de tiendas y servicios oficiales de confianza
TIENDAS_PERMITIDAS: Set[str] = {
    "store.steampowered.com",
    "steampowered.com",
    "store.epicgames.com",
    "epicgames.com",
    "gog.com",
    "www.gog.com",
    "itch.io",
    "www.itch.io",
    "amazon.com",
    "www.amazon.com",
    "gaming.amazon.com",
    "humblebundle.com",
    "www.humblebundle.com",
    "fanatical.com",
    "www.fanatical.com",
    "indiegala.com",
    "www.indiegala.com",
    "gamerpower.com",
    "www.gamerpower.com",
    "ko-fi.com",
    "www.ko-fi.com",
}

# Dominios permitidos para el enlace de descarga de actualizaciones.
DOMINIOS_GITHUB: Set[str] = {"github.com"}


def es_url_segura(url: str, dominios_permitidos: Optional[Set[str]] = None) -> bool:
    """
    Valida que la URL:
    1. Utilice estrictamente el esquema HTTPS.
    2. Tenga un hostname válido dentro de la lista blanca de dominios de confianza.
    3. No incluya credenciales embebidas (usuario:clave@) ni puertos no estándar.
    4. No contenga esquemas peligrosos (javascript:, file:, data:, etc.).
    """
    if not url or not isinstance(url, str):
        return False

    url_str = url.strip()

    # Caracteres de control o espacios internos: no son URLs legítimas.
    if any(ord(c) < 0x21 or ord(c) == 0x7F for c in url_str):
        return False

    try:
        parsed = urllib.parse.urlparse(url_str)
        puerto = parsed.port  # puede lanzar ValueError si es inválido
    except Exception:
        return False

    if parsed.scheme.lower() != "https":
        return False

    if parsed.username is not None or parsed.password is not None:
        return False

    if puerto not in (None, 443):
        return False

    hostname = (parsed.hostname or "").lower().strip().rstrip(".")
    if not hostname:
        return False

    allowlist = dominios_permitidos if dominios_permitidos is not None else TIENDAS_PERMITIDAS

    # Hostname exacto o subdominio legítimo de un dominio de la lista blanca
    for dominio in allowlist:
        if hostname == dominio or hostname.endswith("." + dominio):
            return True

    return False


def abrir_url_externa_segura(
    url: str,
    dominios_permitidos: Optional[Set[str]] = None,
    nueva_pestana: bool = False,
) -> bool:
    """
    Valida la URL antes de enviarla al navegador predeterminado del sistema operativo.
    Retorna True si la URL era válida y se envió al navegador; False en caso contrario.
    """
    if not es_url_segura(url, dominios_permitidos):
        logger.warning("Apertura de URL no verificada bloqueada: %r", str(url)[:200])
        return False

    try:
        if nueva_pestana:
            webbrowser.open_new_tab(url.strip())
        else:
            webbrowser.open(url.strip())
        return True
    except Exception as e:
        logger.warning("No se pudo abrir la URL en el navegador: %s", e)
        return False
