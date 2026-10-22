"""Scroll cinético y controles de desplazamiento con estilo KG Tracker."""

import config
from PySide6.QtCore import (
    QEasingCurve, QObject, QPropertyAnimation, QRectF, Qt, QTimer,
    QVariantAnimation, Signal,
)
from PySide6.QtGui import QColor, QLinearGradient, QPainter, QPen
from PySide6.QtWidgets import QScrollArea, QScrollBar


class NeonMasterClock(QObject):
    """Reloj maestro sincronizado a 45 FPS: elimina la sobrecarga de múltiples animaciones."""
    _instancia = None
    angulo_actualizado = Signal(float)

    @classmethod
    def instance(cls):
        if cls._instancia is None:
            cls._instancia = cls()
        return cls._instancia

    def __init__(self):
        super().__init__()
        self._ang = 0.0
        self._timer = QTimer(self)
        self._timer.setInterval(22)
        self._timer.timeout.connect(self._tick)
        self._subscriptores = 0

    def suscribir(self):
        self._subscriptores += 1
        if self._subscriptores == 1 and not self._timer.isActive():
            self._timer.start()

    def desuscribir(self):
        self._subscriptores = max(0, self._subscriptores - 1)
        if self._subscriptores == 0 and self._timer.isActive():
            self._timer.stop()

    def _tick(self):
        self._ang = (self._ang + 1.8) % 360.0
        self.angulo_actualizado.emit(self._ang)

class SmoothScrollArea(QScrollArea):
    """ScrollArea con desplazamiento cinético interpolado y amortiguación sedosa."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._target_value = 0.0
        self._anim_scroll = None

    def _obtener_animacion(self):
        bar = self.verticalScrollBar()
        if self._anim_scroll is None or self._anim_scroll.targetObject() != bar:
            self._anim_scroll = QPropertyAnimation(bar, b"value", self)
            self._anim_scroll.setDuration(180)
            self._anim_scroll.setEasingCurve(QEasingCurve.Type.OutCubic)
        return self._anim_scroll

    def wheelEvent(self, event):
        delta = event.angleDelta().y()
        if delta == 0:
            delta = event.pixelDelta().y()

        if delta != 0:
            bar = self.verticalScrollBar()
            paso = -(delta / 120.0) * 85.0
            min_v = float(bar.minimum())
            max_v = float(bar.maximum())
            anim = self._obtener_animacion()

            if anim.state() == QPropertyAnimation.State.Running:
                self._target_value = max(min_v, min(max_v, self._target_value + paso))
            else:
                self._target_value = max(min_v, min(max_v, float(bar.value()) + paso))

            anim.stop()
            anim.setStartValue(bar.value())
            anim.setEndValue(int(self._target_value))
            anim.start()
            event.accept()
        else:
            super().wheelEvent(event)

class NeonScrollBar(QScrollBar):
    def __init__(self, orientation=Qt.Orientation.Vertical, parent=None):
        super().__init__(orientation, parent)
        self.setFixedWidth(14)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setMouseTracking(True)
        self.setAttribute(Qt.WidgetAttribute.WA_Hover, True)

        self._hover_progress = 0.0
        self._is_hover = False
        self._is_dragging = False

        self._anim_hover = QVariantAnimation(self)
        self._anim_hover.setDuration(160)
        self._anim_hover.setEasingCurve(QEasingCurve.Type.OutCubic)
        self._anim_hover.valueChanged.connect(self._on_hover_step)

    def _on_hover_step(self, val):
        self._hover_progress = val
        self.update()

    def enterEvent(self, event):
        self._is_hover = True
        self._anim_hover.stop()
        self._anim_hover.setStartValue(self._hover_progress)
        self._anim_hover.setEndValue(1.0)
        self._anim_hover.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._is_hover = False
        if not self._is_dragging:
            self._anim_hover.stop()
            self._anim_hover.setStartValue(self._hover_progress)
            self._anim_hover.setEndValue(0.0)
            self._anim_hover.start()
        super().leaveEvent(event)

    def _actualizar_valor_por_pos(self, mouse_y):
        altura_disp = max(1.0, float(self.height() - 16.0))
        clamped_y = max(0.0, min(altura_disp, float(mouse_y - 8.0)))
        ratio = clamped_y / altura_disp
        min_v = self.minimum()
        max_v = self.maximum()
        nuevo_val = int(round(min_v + (ratio * (max_v - min_v))))
        if nuevo_val != self.value():
            self.setValue(nuevo_val)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._is_dragging = True
            y = event.position().y() if hasattr(event, "position") else event.pos().y()
            self._actualizar_valor_por_pos(y)
            event.accept()
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self._is_dragging:
            y = event.position().y() if hasattr(event, "position") else event.pos().y()
            self._actualizar_valor_por_pos(y)
            event.accept()
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._is_dragging = False
            if not self._is_hover:
                self._anim_hover.stop()
                self._anim_hover.setStartValue(self._hover_progress)
                self._anim_hover.setEndValue(0.0)
                self._anim_hover.start()
            event.accept()
        else:
            super().mouseReleaseEvent(event)

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)

        min_v = self.minimum()
        max_v = self.maximum()
        val = self.value()
        page = self.pageStep()

        if max_v <= min_v:
            p.end()
            return

        centro_x = self.width() / 2.0
        altura_disp = self.height() - 16.0

        groove_rect = QRectF(centro_x - 2.5, 8.0, 5.0, altura_disp)
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(QColor(58, 58, 80, 160) if config.CURRENT_THEME == "dark" else QColor(203, 213, 225, 180))
        p.drawRoundedRect(groove_rect, 2.5, 2.5)

        total_range = (max_v - min_v) + page
        thumb_h = max(32.0, min(altura_disp * 0.75, (page / float(total_range or 1)) * altura_disp))
        recorrido_disp = altura_disp - thumb_h
        ratio = (val - min_v) / float(max_v - min_v or 1)
        thumb_y = 8.0 + (ratio * recorrido_disp)

        ancho_base, ancho_hover = 6.0, 10.0
        ancho_actual = ancho_base + (self._hover_progress * (ancho_hover - ancho_base))
        radio_esquina = ancho_actual / 2.0

        thumb_rect = QRectF(centro_x - (ancho_actual / 2.0), thumb_y, ancho_actual, thumb_h)

        if self._hover_progress > 0.05:
            halo_alpha = int(self._hover_progress * 55)
            p.setBrush(QColor(0, 243, 255, halo_alpha))
            p.setPen(Qt.PenStyle.NoPen)
            p.drawRoundedRect(thumb_rect.adjusted(-3, -2, 3, 2), radio_esquina + 2, radio_esquina + 2)

        grad = QLinearGradient(0, thumb_y, 0, thumb_y + thumb_h)
        if self._hover_progress > 0.4:
            grad.setColorAt(0.0, QColor('#818CF8'))
            grad.setColorAt(1.0, QColor('#00F3FF'))
            border_color = QColor('#00F3FF')
        else:
            grad.setColorAt(0.0, QColor('#6366F1'))
            grad.setColorAt(1.0, QColor('#818CF8'))
            border_color = QColor(129, 140, 248, 180)

        p.setBrush(grad)
        p.setPen(QPen(border_color, 1.2))
        p.drawRoundedRect(thumb_rect, radio_esquina, radio_esquina)
        p.end()
