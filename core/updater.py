"""Verificador asincrono de actualizaciones para K GAME TRACKER."""

import re
import logging
from typing import Optional, Tuple
import requests

from PySide6.QtCore import QObject, Signal, QRunnable, QThreadPool

from config import APP_VERSION, GITHUB_API_LATEST_RELEASE, GITHUB_RELEASES_URL

logger = logging.getLogger("KGTracker.Updater")


def parse_version(v_str: str) -> Tuple[int, ...]:
    """Extrae tupla numerica de una version como 'v0.2.36' -> (0, 2, 36)."""
    nums = re.findall(r"\d+", v_str)
    return tuple(map(int, nums)) if nums else (0, 0, 0)


class UpdateSignals(QObject):
    update_available = Signal(str, str)  # (version_tag, html_url)


class UpdateCheckTask(QRunnable):
    """Tarea asincrona de verificacion de version sin bloqueo."""

    def __init__(self, signals: UpdateSignals):
        super().__init__()
        self.signals = signals

    def run(self):
        try:
            headers = {
                "Accept": "application/vnd.github.v3+json",
                "User-Agent": f"KG-Tracker-{APP_VERSION}",
            }
            resp = requests.get(GITHUB_API_LATEST_RELEASE, headers=headers, timeout=4)
            if resp.status_code != 200:
                return

            data = resp.json()
            latest_tag = data.get("tag_name", "").strip()
            release_url = data.get("html_url", GITHUB_RELEASES_URL)

            if not latest_tag:
                return

            v_actual = parse_version(APP_VERSION)
            v_remota = parse_version(latest_tag)

            if v_remota > v_actual:
                logger.info(f"Nueva version disponible: {latest_tag} (Actual: {APP_VERSION})")
                self.signals.update_available.emit(latest_tag, release_url)
            else:
                logger.debug(f"KG Tracker esta actualizado (Actual: {APP_VERSION}, Remoto: {latest_tag})")

        except Exception as e:
            logger.debug(f"Verificacion de actualizacion omitida: {e}")


def verificar_actualizacion_asincrona(on_update_found) -> UpdateSignals:
    """Dispara chequeo de version en segundo plano via QThreadPool."""
    signals = UpdateSignals()
    signals.update_available.connect(on_update_found)
    task = UpdateCheckTask(signals)
    QThreadPool.globalInstance().start(task)
    return signals

