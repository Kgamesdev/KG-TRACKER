import os
import sys
import json
import html
import subprocess
import threading
from PySide6.QtWidgets import QSystemTrayIcon, QMenu, QApplication
from PySide6.QtGui import QIcon, QPixmap, QColor, QPainter, QAction
from PySide6.QtCore import Qt, QTimer

from core.paths import (
    RESOURCE_DIR,
    ASSETS_DIR,
    SETTINGS_FILE,
    RECLAMADOS_FILE
)

from core.i18n import t
from logger import log_info, log_warning, log_error


def _obtener_icono_seguro():
    icon_path = str(ASSETS_DIR / "logo.ico")
    if os.path.exists(icon_path):
        icono = QIcon(icon_path)
        if not icono.isNull():
            return icono

    pixmap = QPixmap(32, 32)
    pixmap.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pixmap)
    painter.setBrush(QColor("#6366F1"))
    painter.setPen(Qt.PenStyle.NoPen)
    painter.drawRoundedRect(2, 2, 28, 28, 6, 6)
    painter.end()
    return QIcon(pixmap)


def _obtener_config():
    if SETTINGS_FILE.exists():
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def _obtener_dict_reclamados():
    if not RECLAMADOS_FILE.exists():
        return {}
    try:
        with open(RECLAMADOS_FILE, "r", encoding="utf-8") as f:
            d = json.load(f)
            if isinstance(d, dict):
                return d
    except Exception:
        pass
    return {}


def enviar_notificacion_windows(titulo: str, mensaje: str, icono_path: str = None, duracion_larga: bool = True):
    """Envía una notificación push nativa de Windows 10/11 sin inyección de código (SEC-01 fix):
    - Transmite el payload en JSON a través de STDIN a un script PowerShell estático.
    - 100% Silenciosa (sin ding de Windows).
    - Duración pausada y extendida para lectura tranquila.
    """
    def _worker():
        try:
            t_str = str(titulo or "K GAME TRACKER")
            m_str = str(mensaje or "")

            ruta_img = icono_path or str(ASSETS_DIR / "branding" / "KG LOGO.png")
            if not os.path.exists(ruta_img):
                ruta_img = str(ASSETS_DIR / "icons" / "KGLogo.png")

            uri_icono = ""
            if os.path.exists(ruta_img):
                uri_icono = "file:///" + os.path.abspath(ruta_img).replace("\\", "/")

            # Payload JSON seguro para STDIN
            payload = json.dumps({
                "titulo": t_str,
                "mensaje": m_str,
                "icono_uri": uri_icono,
                "duracion_larga": bool(duracion_larga)
            }, ensure_ascii=False)

            # Script PowerShell 100% estático - No contiene f-strings ni interpolaciones de usuario
            ps_script = r"""
$ErrorActionPreference = 'Stop'
$rawInput = [Console]::In.ReadLine()
if (-not $rawInput) { exit 0 }

$data = $rawInput | ConvertFrom-Json
$t_xml = [System.Security.SecurityElement]::Escape($data.titulo)
$m_xml = [System.Security.SecurityElement]::Escape($data.mensaje)

$imgTag = ""
if ($data.icono_uri) {
    $imgTag = "<image placement=`"appLogoOverride`" hint-crop=`"circle`" src=`"$($data.icono_uri)`" />"
}

$durAttr = if ($data.duracion_larga) { 'duration="long"' } else { 'duration="short"' }

[Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] | Out-Null
[Windows.Data.Xml.Dom.XmlDocument, Windows.Data.Xml.Dom.XmlCommands, ContentType = WindowsRuntime] | Out-Null

$xmlTemplate = @"
<toast $durAttr>
    <visual>
        <binding template="ToastGeneric">
            <text>$t_xml</text>
            <text>$m_xml</text>
            $imgTag
        </binding>
    </visual>
    <audio silent="true" />
</toast>
"@

$xml = New-Object Windows.Data.Xml.Dom.XmlDocument
$xml.LoadXml($xmlTemplate)
$toast = [Windows.UI.Notifications.ToastNotification]::new($xml)
[Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier("K GAME TRACKER").Show($toast)
"""
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = subprocess.SW_HIDE

            proc = subprocess.Popen(
                [
                    "powershell.exe",
                    "-NoProfile",
                    "-NonInteractive",
                    "-WindowStyle", "Hidden",
                    "-Command", ps_script,
                ],
                stdin=subprocess.PIPE,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                startupinfo=startupinfo,
                creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0,
                text=True,
                encoding="utf-8"
            )
            
            proc.communicate(input=payload, timeout=5)
            log_info(f"📢 Notificación push silenciosa enviada de forma segura: {titulo}")
        except Exception as e:
            log_error(f"Error en notificación push silenciosa: {e}")

    threading.Thread(target=_worker, daemon=True).start()


class GameTrackerTray:
    
    def mostrar_notificacion_push(self, titulo, cuerpo):
        try:
            from ui.components.notification_toast import DesktopToast
            if hasattr(self, "_toast_activo") and self._toast_activo is not None:
                try:
                    self._toast_activo.close()
                    self._toast_activo.deleteLater()
                except Exception:
                    pass
            self._toast_activo = DesktopToast(
                titulo=titulo,
                mensaje=cuerpo,
                ventana_principal=self.ventana
            )
            self._toast_activo.mostrar()
        except Exception as e:
            log_error(f"Error mostrando toast gaming: {e}")

    def __init__(self, ventana_principal):
        self.ventana = ventana_principal
        self.tray_icon = None
        self.icono_app = _obtener_icono_seguro()
        self.timer_busqueda = QTimer(ventana_principal)
        self.timer_busqueda.timeout.connect(self._ejecutar_barrido_segundo_plano)
        self._inicializar()
        self.actualizar_temporizador_busqueda()

    def _inicializar(self):
        if not QSystemTrayIcon.isSystemTrayAvailable():
            return

        self.tray_icon = QSystemTrayIcon(self.icono_app, self.ventana)
        self.tray_icon.setToolTip(t("tray.tooltip"))
        self.tray_icon.messageClicked.connect(self.mostrar_ventana)

        menu = QMenu()
        self.accion_abrir = QAction(t("tray.menu_open"), self.ventana)
        self.accion_abrir.triggered.connect(self.mostrar_ventana)
        menu.addAction(self.accion_abrir)

        self.accion_buscar = QAction(t("tray.menu_check"), self.ventana)
        self.accion_buscar.triggered.connect(self.ejecutar_barrido_manual)
        menu.addAction(self.accion_buscar)

        menu.addSeparator()

        self.accion_salir = QAction(t("tray.menu_exit"), self.ventana)
        self.accion_salir.triggered.connect(self.salir_definitivo)
        menu.addAction(self.accion_salir)

        self.tray_icon.setContextMenu(menu)
        self.tray_icon.activated.connect(self._on_activado)
        self.tray_icon.show()

    def actualizar_textos_menu(self):
        """Actualiza tooltip y opciones del menú de la bandeja en caliente."""
        if not self.tray_icon:
            return
        self.tray_icon.setToolTip(t("tray.tooltip"))
        if hasattr(self, "accion_abrir"):
            self.accion_abrir.setText(t("tray.menu_open"))
        if hasattr(self, "accion_buscar"):
            self.accion_buscar.setText(t("tray.menu_check"))
        if hasattr(self, "accion_salir"):
            self.accion_salir.setText(t("tray.menu_exit"))

    def _on_activado(self, reason):
        if reason in (QSystemTrayIcon.ActivationReason.Trigger, QSystemTrayIcon.ActivationReason.DoubleClick):
            self.mostrar_ventana()

    def mostrar_ventana(self):
        self.ventana.showNormal()
        self.ventana.raise_()
        self.ventana.activateWindow()
        if hasattr(self.ventana, "reanudar_musica_con_fade"):
            self.ventana.reanudar_musica_con_fade()

    def actualizar_temporizador_busqueda(self):
        cfg = _obtener_config()
        frecuencia = cfg.get("frecuencia_busqueda", "Cada 4 horas")
        self.timer_busqueda.stop()

        horas_map = {
            "Cada 2 horas": 2,
            "Cada 4 horas": 4,
            "Cada 8 horas": 8,
            "Una vez al día (24h)": 24,
            "Every 2 hours": 2,
            "Every 4 hours": 4,
            "Every 8 hours": 8,
            "Once a day (24h)": 24,
        }

        if frecuencia in horas_map:
            ms = horas_map[frecuencia] * 3600 * 1000
            self.timer_busqueda.setInterval(ms)
            self.timer_busqueda.start()
            log_info(f"[TRAY] Temporizador configurado a: {frecuencia}")

    def contar_ofertas_disponibles(self):
        try:
            juegos = getattr(self.ventana, "juegos_cache_global", []) or []
            if not juegos:
                return 0

            if hasattr(self.ventana, "_esta_reclamado"):
                disponibles = [j for j in juegos if not self.ventana._esta_reclamado(j)]
                return len(disponibles)

            reclamados_dict = getattr(self.ventana, "reclamados", None)
            if not isinstance(reclamados_dict, dict):
                reclamados_dict = _obtener_dict_reclamados()

            contador = 0
            for j in juegos:
                if not isinstance(j, dict):
                    continue
                titulo = str(j.get("title", "")).lower()
                coincide = any(titulo in k.lower() for k in reclamados_dict.keys())
                if not coincide:
                    contador += 1

            return contador
        except Exception as e:
            log_warning(f"[TRAY] Error calculando disponibles: {e}")
            return 0

    def notificar_al_minimizar(self):
        cfg = _obtener_config()
        if not cfg.get("notificaciones_activas", True):
            return

        cant = self.contar_ofertas_disponibles()
        if cant > 0:
            cuerpo = t("tray.minimized_body_offers", count=cant)
        else:
            cuerpo = t("tray.minimized_body_uptodate")

        self.mostrar_notificacion_push(t("tray.minimized_title"), cuerpo)

    def ejecutar_barrido_manual(self):
        log_info("[TRAY] Barrido manual solicitado por el usuario...")
        self._lanzar_busqueda(manual=True)

    def _ejecutar_barrido_segundo_plano(self):
        log_info("[TRAY] Ejecutando barrido automático programado...")
        self._lanzar_busqueda(manual=False)

    def _lanzar_busqueda(self, manual=False):
        try:
            if hasattr(self.ventana, "cargar_juegos_thread"):
                self.ventana.cargar_juegos_thread()
            elif hasattr(self.ventana, "actualizar_ofertas"):
                self.ventana.actualizar_ofertas()
            elif hasattr(self.ventana, "buscar_juegos"):
                self.ventana.buscar_juegos()

            QTimer.singleShot(2500, lambda: self._reportar_resultado_barrido(manual))
        except Exception as e:
            log_error(f"[TRAY] Error lanzando barrido: {e}")

    def _reportar_resultado_barrido(self, manual=False):
        cfg = _obtener_config()
        if not cfg.get("notificaciones_activas", True):
            return

        cant = self.contar_ofertas_disponibles()
        titulo = t("tray.sweep_manual_title") if manual else t("tray.sweep_auto_title")
        if cant > 0:
            cuerpo = t("tray.sweep_body_offers", count=cant)
        else:
            cuerpo = t("tray.sweep_body_none")

        self.mostrar_notificacion_push(titulo, cuerpo)

    def salir_definitivo(self):
        if self.tray_icon:
            self.tray_icon.hide()
        self.ventana._salida_forzada = True
        app = QApplication.instance()
        if app:
            app.quit()
