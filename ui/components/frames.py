"""Marcos animados compartidos por tarjetas y cabeceras de tienda."""

import config
from PySide6.QtCore import QEasingCurve, QPropertyAnimation, Qt
from PySide6.QtGui import QColor, QConicalGradient, QPainter, QPen
from PySide6.QtWidgets import QFrame

from .scrolling import NeonMasterClock


class NeonFrame(QFrame):
    """QFrame con haz neón sincronizado por el reloj maestro ultraliviano."""

    def __init__(self, parent=None, radius=12, border_width=1.5, speed_ms=4500):
        super().__init__(parent)
        self._radius = radius
        self._border_width = border_width
        self._ang = 0.0
        self._conectado_clock = False
        self._bloquear_neon = False

    def _on_clock_tick(self, ang):
        if getattr(self, "_bloquear_neon", False):
            return
        self._ang = ang
        self.update()

    def preparar_animacion_cascada(self):
        self._bloquear_neon = False

    def obtener_animacion_baraja(self):
        from PySide6.QtCore import QPropertyAnimation, QEasingCurve
        if not hasattr(self, '_efecto_opacidad'):
            return None

        anim_fade = QPropertyAnimation(self._efecto_opacidad, b'opacity', self)
        anim_fade.setDuration(260)
        anim_fade.setStartValue(0.0)
        anim_fade.setEndValue(1.0)
        anim_fade.setEasingCurve(QEasingCurve.Type.OutCubic)

        def _on_finish():
            self._bloquear_neon = False
            if hasattr(self, '_efecto_opacidad'):
                self._efecto_opacidad.setOpacity(1.0)
            self.update()

        anim_fade.finished.connect(_on_finish)
        return anim_fade

    def showEvent(self, event):
        super().showEvent(event)
        if not self._conectado_clock:
            clock = NeonMasterClock.instance()
            clock.angulo_actualizado.connect(self._on_clock_tick)
            clock.suscribir()
            self._conectado_clock = True

    def hideEvent(self, event):
        if self._conectado_clock:
            clock = NeonMasterClock.instance()
            try:
                clock.angulo_actualizado.disconnect(self._on_clock_tick)
            except Exception:
                pass
            clock.desuscribir()
            self._conectado_clock = False
        super().hideEvent(event)

    def paintEvent(self, event):
        super().paintEvent(event)
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        r = self.rect().toRectF()
        r.adjust(0.75, 0.75, -0.75, -0.75)

        g = QConicalGradient(r.center(), self._ang)
        if config.CURRENT_THEME == "light":
            g.setColorAt(0.0, QColor(95, 119, 170, 28))
            g.setColorAt(0.05, QColor(95, 119, 170, 82))
            g.setColorAt(0.12, QColor(120, 142, 180, 24))
            g.setColorAt(0.95, QColor(95, 119, 170, 44))
        else:
            g.setColorAt(0.0, QColor("#FFFFFF"))
            g.setColorAt(0.05, QColor("#00F3FF"))
            g.setColorAt(0.12, QColor(129, 140, 248, 50))
            g.setColorAt(0.95, QColor(0, 243, 255, 120))
        g.setColorAt(0.22, QColor(0, 0, 0, 0))
        g.setColorAt(0.82, QColor(0, 0, 0, 0))
        g.setColorAt(1.0, QColor("#FFFFFF") if config.CURRENT_THEME == "dark" else QColor(95, 119, 170, 28))

        pen = QPen(g, float(self._border_width))
        p.setPen(pen)
        p.setBrush(Qt.BrushStyle.NoBrush)
        p.drawRoundedRect(r, float(self._radius), float(self._radius))
        p.end()
