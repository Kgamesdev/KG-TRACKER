"""Coordinación de instancias de KG Tracker mediante sockets locales de Qt."""

import getpass
import hashlib
from pathlib import Path

from PySide6.QtCore import QObject, Signal
from PySide6.QtCore import QLockFile
from PySide6.QtNetwork import QLocalServer, QLocalSocket

from core.paths import USER_DATA_DIR


_ACTIVATE_MESSAGE = b"activate"


def _server_name():
    """Devuelve un nombre estable por usuario y compartido entre builds de la app."""
    user = getpass.getuser().casefold()
    user_hash = hashlib.sha256(user.encode("utf-8")).hexdigest()[:16]
    return f"kg_tracker_{user_hash}"


def _solicitar_activacion(nombre, timeout_ms=250):
    socket = QLocalSocket()
    socket.connectToServer(nombre)
    if not socket.waitForConnected(timeout_ms):
        return False

    socket.write(_ACTIVATE_MESSAGE)
    enviado = socket.waitForBytesWritten(timeout_ms)
    socket.disconnectFromServer()
    return enviado


class SingleInstance(QObject):
    """Mantiene el servidor local y notifica cuándo se solicita otra apertura."""

    activation_requested = Signal()

    def __init__(self, nombre=None, parent=None):
        super().__init__(parent)
        self.nombre = nombre or _server_name()
        lock_name = hashlib.sha256(self.nombre.encode("utf-8")).hexdigest()[:16]
        self.lock = QLockFile(str(Path(USER_DATA_DIR) / f"{lock_name}.lock"))
        self.server = QLocalServer(self)
        self.server.newConnection.connect(self._aceptar_conexiones)

        # QLocalServer puede aceptar listeners duplicados en Windows. El lock
        # del sistema de archivos es quien arbitra qué proceso es el principal.
        if not self.lock.tryLock(0):
            _solicitar_activacion(self.nombre)
            self.is_primary = False
            return

        if self.server.listen(self.nombre):
            self.is_primary = True
            return

        # El lock garantiza que ningún proceso vivo puede poseer este socket.
        # Si quedó un endpoint huérfano tras un cierre anómalo, se recrea.
        QLocalServer.removeServer(self.nombre)
        self.is_primary = self.server.listen(self.nombre)
        if not self.is_primary:
            self.lock.unlock()

    def _aceptar_conexiones(self):
        while self.server.hasPendingConnections():
            socket = self.server.nextPendingConnection()
            if socket is None:
                continue
            socket.readyRead.connect(
                lambda socket=socket: self._leer_peticion(socket)
            )
            if socket.bytesAvailable():
                self._leer_peticion(socket)

    def _leer_peticion(self, socket):
        mensaje = bytes(socket.readAll())
        if mensaje == _ACTIVATE_MESSAGE:
            self.activation_requested.emit()
        socket.disconnectFromServer()
        socket.deleteLater()

    def close(self):
        if self.is_primary:
            self.server.close()
            QLocalServer.removeServer(self.nombre)
            self.lock.unlock()
            self.is_primary = False
