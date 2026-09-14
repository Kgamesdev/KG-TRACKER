"""
core/validators.py
Validador centralizado de URLs externas y esquemas de red.
Resuelve la vulnerabilidad P1 (SEC-02) evitando la apertura de URLs no verificadas o maliciosas.
"""

import urllib.parse
import webbrowser
from typing import Optional, Set

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


def es_url_segura(url: str, dominios_permitidos: Optional[Set[str]] = None) -> bool:
    """
    Valida que la URL:
    1. Utilice estrictamente el esquema HTTPS.
    2. Tenga un hostname válido dentro de la lista blanca de dominios de confianza.
    3. No contenga esquemas peligrosos (javascript:, file:, data:, etc.).
    """
    if not url or not isinstance(url, str):
        return False

    url_str = url.strip()

    try:
        parsed = urllib.parse.urlparse(url_str)
    except Exception:
        return False

    # Exigir estrictamente HTTPS
    if parsed.scheme.lower() != "https":
        return False

    hostname = (parsed.hostname or "").lower().strip()
    if not hostname:
        return False

    allowlist = dominios_permitidos if dominios_permitidos is not None else TIENDAS_PERMITIDAS

    # Verificar si el hostname directo o su dominio raíz está en la lista blanca
    for dominio in allowlist:
        if hostname == dominio or hostname.endswith("." + dominio):
            return True

    return False


def abrir_url_externa_segura(url: str) -> bool:
    """
    Valida la URL antes de enviarla al navegador predeterminado del sistema operativo.
    Retorna True si la URL era válida y se envió al navegador; False en caso contrario.
    """
    if es_url_segura(url):
        try:
            webbrowser.open(url)
            return True
        except Exception:
            return False
    else:
        print(f"[SECURITY WARNING] Intento de abrir URL no verificada o insegura bloqueado: {url}")
        return False
