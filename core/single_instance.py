"""Coordinación de instancias de KG Tracker mediante sockets locales de Qt."""

import getpass
import hashlib
import sys
from pathlib import Path

from PySide6.QtCore import QObject, Signal
from PySide6.QtCore import QLockFile
from PySide6.QtNetwork import QLocalServer, QLocalSocket

from core.paths import USER_DATA_DIR


_ACTIVATE_MESSAGE = b"activate"
_ACK_MESSAGE = b"ok"


def _server_name():
    """Devuelve un nombre estable por usuario y compartido entre builds de la app."""
    user = getpass.getuser().casefold()
    user_hash = hashlib.sha256(user.encode("utf-8")).hexdigest()[:16]
    return f"kg_tracker_{user_hash}"


def _solicitar_activacion(nombre, timeout_ms=1000):
    socket = QLocalSocket()
    socket.connectToServer(nombre)
    if not socket.waitForConnected(timeout_ms):
        return False

    if socket.write(_ACTIVATE_MESSAGE) != len(_ACTIVATE_MESSAGE):
        socket.abort()
        return False
    socket.flush()
    confirmado = socket.waitForReadyRead(timeout_ms)
    respuesta = bytes(socket.readAll()) if confirmado else b""
    socket.disconnectFromServer()
    return respuesta == _ACK_MESSAGE


class SingleInstance(QObject):
    """Mantiene el servidor local y notifica cuándo se solicita otra apertura."""

    activation_requested = Signal()

    def __init__(self, nombre=None, parent=None):
        super().__init__(parent)
        self.nombre = nombre or _server_name()
        self._mutex_handle = None
        self.lock = None
        self.server = QLocalServer(self)
        self.server.newConnection.connect(self._aceptar_conexiones)

        if not self._adquirir_bloqueo():
            self.activation_sent = _solicitar_activacion(self.nombre)
            self.is_primary = False
            return

        self.activation_sent = False
        if self.server.listen(self.nombre):
            self.is_primary = True
            return

        # El lock garantiza que ningún proceso vivo puede poseer este socket.
        # Si quedó un endpoint huérfano tras un cierre anómalo, se recrea.
        QLocalServer.removeServer(self.nombre)
        self.is_primary = self.server.listen(self.nombre)
        if not self.is_primary:
            self._liberar_bloqueo()

    def _adquirir_bloqueo(self):
        """Adquiere un bloqueo del sistema operativo, compartido entre procesos.

        En Windows el mutex nombrado se libera automáticamente si el proceso
        termina de forma abrupta. Un archivo de bloqueo puede quedar obsoleto
        o apuntar a perfiles de usuario distintos si cambia LOCALAPPDATA.
        """
        lock_name = hashlib.sha256(self.nombre.encode("utf-8")).hexdigest()[:24]
        if sys.platform == "win32":
            try:
                import ctypes
                from ctypes import wintypes

                kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
                create_mutex = kernel32.CreateMutexW
                create_mutex.argtypes = (wintypes.LPVOID, wintypes.BOOL, wintypes.LPCWSTR)
                create_mutex.restype = wintypes.HANDLE
                handle = create_mutex(None, False, f"Local\\KGTracker_{lock_name}")
                if not handle:
                    return False
                self._mutex_handle = handle
                already_exists = ctypes.get_last_error() == 183  # ERROR_ALREADY_EXISTS
                if already_exists:
                    self._liberar_bloqueo()
                    return False
                return True
            except (AttributeError, OSError):
                return False

        self.lock = QLockFile(str(Path(USER_DATA_DIR) / f"{lock_name}.lock"))
        return self.lock.tryLock(0)

    def _liberar_bloqueo(self):
        if self._mutex_handle is not None:
            try:
                import ctypes
                from ctypes import wintypes
                close_handle = ctypes.WinDLL("kernel32", use_last_error=True).CloseHandle
                close_handle.argtypes = (wintypes.HANDLE,)
                close_handle.restype = wintypes.BOOL
                close_handle(self._mutex_handle)
            except (AttributeError, OSError):
                pass
            self._mutex_handle = None
        if self.lock is not None and self.lock.isLocked():
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
            socket.write(_ACK_MESSAGE)
            socket.flush()
        socket.disconnectFromServer()
        socket.deleteLater()

    def close(self):
        if self.is_primary:
            self.server.close()
            QLocalServer.removeServer(self.nombre)
            self.is_primary = False
        self._liberar_bloqueo()
