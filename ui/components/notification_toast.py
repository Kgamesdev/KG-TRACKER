"""Notificación push flotante de escritorio estilo gaming para KG Tracker."""

import os
from PySide6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, QPoint, QRectF
from PySide6.QtGui import QIcon, QPixmap, QPainter, QPainterPath, QColor, QFont
from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QApplication

import config
from config import BASE_DIR, LOGO_PATH


class DesktopToast(QWidget):
    """Notificación push flotante en la esquina inferior derecha con animación suave y silenciosa."""

    def __init__(self, titulo: str, mensaje: str, ventana_principal=None):
        super().__init__(None)
        self.ventana_principal = ventana_principal

        # Configuración de ventana flotante sin robar foco
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.Tool
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.WindowDoesNotAcceptFocus
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating, True)

        self.setFixedSize(356, 88)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        es_oscuro = (config.CURRENT_THEME == "dark")
        self._es_oscuro = es_oscuro

        # Layout principal
        layout = QHBoxLayout(self)
        layout.setContentsMargins(14, 12, 12, 12)
        layout.setSpacing(12)

        # Icono / Logotipo de la app
        self.logo_label = QLabel()
        self.logo_label.setFixedSize(46, 46)
        self.logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        ruta_logo = os.path.join(BASE_DIR, "assets", "icons", "KGLogo.png")
        if not os.path.exists(ruta_logo):
            ruta_logo = LOGO_PATH

        if os.path.exists(ruta_logo):
            pix = QPixmap(ruta_logo).scaled(
                46, 46,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.logo_label.setPixmap(pix)

        layout.addWidget(self.logo_label)

        # Contenedor de textos
        text_layout = QVBoxLayout()
        text_layout.setContentsMargins(0, 0, 0, 0)
        text_layout.setSpacing(3)

        self.title_label = QLabel(titulo)
        c_title = "#00F3FF" if es_oscuro else "#4F46E5"
        self.title_label.setStyleSheet(f"color: {c_title}; font: bold 9pt 'Segoe UI';")
        text_layout.addWidget(self.title_label)

        self.desc_label = QLabel(mensaje)
        c_desc = "#E2E8F0" if es_oscuro else "#334155"
        self.desc_label.setStyleSheet(f"color: {c_desc}; font: 8.5pt 'Segoe UI';")
        self.desc_label.setWordWrap(True)
        text_layout.addWidget(self.desc_label)

        layout.addLayout(text_layout, 1)

        # Botón cerrar discreto (✕)
        self.btn_close = QPushButton("✕", self)
        self.btn_close.setFixedSize(20, 20)
        self.btn_close.setCursor(Qt.CursorShape.PointingHandCursor)
        c_btn = "#94A3B8" if es_oscuro else "#64748B"
        self.btn_close.setStyleSheet(f"""
            QPushButton {{
                background: transparent;
                color: {c_btn};
                border: none;
                font: bold 9pt 'Segoe UI';
                padding: 0;
            }}
            QPushButton:hover {{
                color: #EF4444;
            }}
        """)
        self.btn_close.clicked.connect(self._iniciar_salida)
        layout.addWidget(self.btn_close, 0, Qt.AlignmentFlag.AlignTop)

        # Temporizador de permanencia (8.5 segundos)
        self._timer_permanencia = QTimer(self)
        self._timer_permanencia.setSingleShot(True)
        self._timer_permanencia.setInterval(8500)
        self._timer_permanencia.timeout.connect(self._iniciar_salida)

        self._anim_pos = None

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        r = self.rect().toRectF().adjusted(1, 1, -1, -1)

        # Fondo según tema
        if self._es_oscuro:
            bg_color = QColor(26, 27, 43, 245)
            bd_color = QColor(129, 140, 248, 200)
        else:
            bg_color = QColor(255, 255, 255, 250)
            bd_color = QColor(129, 140, 248, 220)

        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(bg_color)
        p.drawRoundedRect(r, 13, 13)

        # Borde brillante
        p.setBrush(Qt.BrushStyle.NoBrush)
        p.setPen(bd_color)
        p.drawRoundedRect(r, 13, 13)
        p.end()

    def enterEvent(self, event):
        # Pausar temporizador si el usuario coloca el ratón encima
        if self._timer_permanencia.isActive():
            self._timer_permanencia.stop()
        super().enterEvent(event)

    def leaveEvent(self, event):
        # Reanudar con 3 segundos restantes al quitar el cursor
        self._timer_permanencia.setInterval(3000)
        self._timer_permanencia.start()
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            if self.ventana_principal:
                self.ventana_principal.showNormal()
                self.ventana_principal.raise_()
                self.ventana_principal.activateWindow()
                if hasattr(self.ventana_principal, "reanudar_musica_con_fade"):
                    self.ventana_principal.reanudar_musica_con_fade()
            self._iniciar_salida()
        super().mousePressEvent(event)

    def mostrar(self):
        screen = QApplication.primaryScreen()
        if not screen:
            return

        geo = screen.availableGeometry()
        ancho = self.width()
        alto = self.height()

        target_x = geo.right() - ancho - 18
        target_y = geo.bottom() - alto - 14
        start_y = geo.bottom() + 15

        self.move(target_x, start_y)
        self.show()

        # Animación pausada de entrada hacia arriba (650 ms)
        self._anim_pos = QPropertyAnimation(self, b"pos")
        self._anim_pos.setDuration(650)
        self._anim_pos.setStartValue(QPoint(target_x, start_y))
        self._anim_pos.setEndValue(QPoint(target_x, target_y))
        self._anim_pos.setEasingCurve(QEasingCurve.Type.OutCubic)
        self._anim_pos.finished.connect(self._timer_permanencia.start)
        self._anim_pos.start()

    def _iniciar_salida(self):
        if self._timer_permanencia.isActive():
            self._timer_permanencia.stop()

        screen = QApplication.primaryScreen()
        geo = screen.availableGeometry() if screen else self.rect()
        dest_y = geo.bottom() + 15

        self._anim_salida = QPropertyAnimation(self, b"pos")
        self._anim_salida.setDuration(420)
        self._anim_salida.setStartValue(self.pos())
        self._anim_salida.setEndValue(QPoint(self.x(), dest_y))
        self._anim_salida.setEasingCurve(QEasingCurve.Type.InCubic)
        self._anim_salida.finished.connect(self._cerrar_definitivo)
        self._anim_salida.start()

    def _cerrar_definitivo(self):
        self.close()
        self.deleteLater()