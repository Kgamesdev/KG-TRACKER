"""Componentes visuales y tarjetas de juego para KG Tracker."""

import os
import re
import config
import datetime

from PySide6.QtCore import (
    QObject, Signal,
    Qt, QSize, QVariantAnimation, QTimer, QRectF, QPoint,
    QPropertyAnimation, QParallelAnimationGroup, QEasingCurve,
)
from PySide6.QtGui import (
    QIcon, QPixmap, QPainter, QPainterPath, QColor, QPen,
    QLinearGradient, QFont, QConicalGradient,
)
from PySide6.QtWidgets import (
    QScrollArea,
    QApplication, QFrame, QHBoxLayout, QLabel, QPushButton,
    QSizePolicy, QSlider, QScrollBar, QVBoxLayout, QWidget,
    QGraphicsOpacityEffect,
)

from config import (
    COLOR_BG_CARD, COLOR_HOVER, COLOR_BORDER, COLOR_ACCENT,
    COLOR_ACCENT_HOVER, COLOR_ACCENT_LIGHT, COLOR_SUCCESS,
    COLOR_SUCCESS_HOVER, COLOR_TEXT_PRIMARY,
)
from core.i18n import t, obtener_idioma
from core.translator import GameTranslator
from core.steam_enricher import SteamEnricher


def _limpiar_titulo_visual(titulo: str) -> str:
    """Limpia sufijos feos de giveaway o tienda dejando el título limpio y profesional."""
    t_str = str(titulo or "").strip()
    t_str = re.sub(
        r"\s*[\(\[](?:epic games|epic|steam|gog|itch\.io|itch|amazon prime|amazon|prime|pc|free|gratis|giveaway)[\)\]]",
        "", t_str, flags=re.IGNORECASE
    )
    for sufijo in (
        " - giveaway", " : giveaway", " giveaway",
        " free steam key", " steam key", " free key",
        " free on steam", " free on epic games", " free on gog",
        " free download", " free",
    ):
        if t_str.lower().endswith(sufijo):
            t_str = t_str[:-len(sufijo)].strip()
    return " ".join(t_str.split()).strip() or str(titulo)


def _redondear_pixmap(pixmap: QPixmap, radio: int = 8) -> QPixmap:
    """Recorta suavemente las esquinas de una carátula para un acabado moderno."""
    if pixmap.isNull():
        return pixmap
    out = QPixmap(pixmap.size())
    out.fill(Qt.GlobalColor.transparent)
    painter = QPainter(out)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
    path = QPainterPath()
    path.addRoundedRect(0, 0, pixmap.width(), pixmap.height(), radio, radio)
    painter.setClipPath(path)
    painter.drawPixmap(0, 0, pixmap)
    painter.end()
    return out


class FloatingRewardLabel(QLabel):
    """Etiqueta flotante efímera de recompensa (+$$ / +1) con elevación y desvanecimiento suave."""

    def __init__(self, parent, text: str, pos_inicial: QPoint):
        super().__init__(parent)
        self.setText(text)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet("""
            QLabel {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 rgba(16, 185, 129, 0.95), stop:1 rgba(5, 150, 105, 0.95));
                color: #FFFFFF;
                border: 1.5px solid #6EE7B7;
                border-radius: 8px;
                padding: 4px 10px;
                font: bold 9pt "Segoe UI";
            }
        """)
        self.adjustSize()
        self.move(pos_inicial)
        self.show()

        self._op_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self._op_effect)
        self._op_effect.setOpacity(1.0)

        self._anim_group = QParallelAnimationGroup(self)

        anim_pos = QPropertyAnimation(self, b"pos")
        anim_pos.setDuration(950)
        anim_pos.setStartValue(pos_inicial)
        anim_pos.setEndValue(QPoint(pos_inicial.x(), pos_inicial.y() - 48))
        anim_pos.setEasingCurve(QEasingCurve.Type.OutCubic)

        anim_fade = QPropertyAnimation(self._op_effect, b"opacity")
        anim_fade.setDuration(950)
        anim_fade.setStartValue(1.0)
        anim_fade.setEndValue(0.0)
        anim_fade.setEasingCurve(QEasingCurve.Type.InQuad)

        self._anim_group.addAnimation(anim_pos)
        self._anim_group.addAnimation(anim_fade)
        self._anim_group.finished.connect(self.deleteLater)
        self._anim_group.start()


class RoundedButton(QPushButton):
    def __init__(self, parent=None, text='', command=None, width=120, height=42, bg=COLOR_BG_CARD, hover_bg=COLOR_HOVER, fg='white', radius=12, font=None, border=COLOR_BORDER, border_width=1, icon_path=None, icon_size=(20, 20), role='default'):
        super().__init__(text, parent)
        self._bg = bg
        self._hover = hover_bg
        self._fg = fg
        self._border = border
        self._border_width = border_width
        self._radius = radius
        self._icon_size = icon_size
        self._is_hover = False
        self._ang = 0.0
        self._flicker_count = 0
        self._flicker_state = False
        self._target_val = 0.0
        self._current_val = 0.0
        self._shine_pos = -60.0
        self._bloqueo_recursivo = False

        if 'AHORRADO' in text.upper() or 'SAVED' in text.upper():
            try:
                self._current_val = float(re.sub(r'[^0-9.-]', '', text.replace(',', '')))
                self._target_val = self._current_val
            except Exception:
                pass

        self.setText(text)
        self.setFixedSize(int(width), int(height))
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFlat(True)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setProperty('role', role)

        self.setFont(QFont('Segoe UI', 8, QFont.Weight.Bold) if role != 'secondary' else QFont('Segoe UI', 7, QFont.Weight.Bold))

        self._anim = QVariantAnimation(self)
        self._anim.setStartValue(0.0)
        self._anim.setEndValue(360.0)
        self._anim.setDuration(2200)
        self._anim.setLoopCount(-1)
        self._anim.valueChanged.connect(lambda v: (setattr(self, '_ang', v), setattr(self, '_shine_pos', -60.0 + (v / 360.0) * 240.0), self.update()))

        self._flicker_timer = QTimer(self)
        self._flicker_timer.setInterval(180)
        self._flicker_timer.timeout.connect(self._do_flicker)

        self._count_timer = QTimer(self)
        self._count_timer.setInterval(16)
        self._count_timer.timeout.connect(self._do_count)

        if 'AHORRADO' in text.upper() or 'SAVED' in text.upper():
            self._anim.start()
        self._role = role
        self.set_icon(icon_path)
        if callable(command):
            self.clicked.connect(command)
        self.aplicar_estilo_segun_rol()

    def aplicar_estilo_segun_rol(self):
        es_oscuro = (config.CURRENT_THEME == "dark")
        role = self.property("role") or getattr(self, "_role", "default")

        if role == 'accent':
            # 1. BOTÓN AZUL (BUSCAR JUEGOS): Mismo azul eléctrico, versión luminosa
            if es_oscuro:
                self.setStyleSheet(f'QPushButton {{ background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #6366F1, stop:1 #4F46E5); color: #FFFFFF; border: 1.2px solid #818CF8; border-radius: {self._radius}px; font-weight: bold; padding: 0 8px; letter-spacing: 0.5px; }} QPushButton:hover {{ background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #818CF8, stop:1 #6366F1); border: 1.2px solid #00F3FF; }} QPushButton:pressed {{ background: #4338CA; padding-top: 2px; }}')
            else:
                self.setStyleSheet(f'QPushButton {{ background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #4F46E5, stop:0.5 #6366F1, stop:1 #38BDF8); color: #FFFFFF; border: 1.5px solid #818CF8; border-radius: {self._radius}px; font-weight: bold; padding: 0 8px; letter-spacing: 0.5px; }} QPushButton:hover {{ background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #6366F1, stop:0.5 #818CF8, stop:1 #67E8F9); border: 1.5px solid #00F3FF; }} QPushButton:pressed {{ background: #3730A3; padding-top: 2px; }}')

        elif role == 'success':
            # 2. BOTÓN VERDE (RECLAMAR): Mismo verde esmeralda, versión menta luminosa
            if es_oscuro:
                self.setStyleSheet(f'QPushButton {{ background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 {self._bg}, stop:1 {self._hover}); color: {self._fg}; border: 1px solid #34D399; border-radius: {self._radius}px; font-weight: bold; padding: 0 8px; }} QPushButton:hover {{ background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #34D399, stop:1 {self._bg}); }} QPushButton:pressed {{ background: #047857; padding-top: 2px; }}')
            else:
                self.setStyleSheet(f'QPushButton {{ background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #34D399, stop:1 #10B981); color: #FFFFFF; border: 1.2px solid #6EE7B7; border-radius: {self._radius}px; font-weight: bold; padding: 0 8px; }} QPushButton:hover {{ background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #6EE7B7, stop:1 #34D399); color: #064E3B; border: 1.2px solid #A7F3D0; }} QPushButton:pressed {{ background: #059669; padding-top: 2px; }}')

        elif role in ('secondary', 'sidebar'):
            # 3. BOTONES AZUL MARINO / PIZARRA (SIDEBAR, [✔], [🔗], RECLAMADOS, MUTE):
            # En tema claro: El mismo azul pizarra del tema oscuro, pero en tono acero claro satinado y visible
            if es_oscuro:
                bg_dark = "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #3A3B52, stop:1 #262738)" if role == 'secondary' else "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #25263A, stop:1 #171827)"
                bd_dark = "#4E506B" if role == 'secondary' else "#3A3A50"
                self.setStyleSheet(f'QPushButton {{ background: {bg_dark}; color: #FFFFFF; border: 1px solid {bd_dark}; border-radius: {self._radius}px; font-weight: bold; padding: 0 8px; }} QPushButton:hover {{ background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #4E506B, stop:1 #3A3B52); border: 1px solid #818CF8; color: #818CF8; }} QPushButton:pressed {{ background: #1E1F2E; padding-top: 2px; }}')
            else:
                self.setStyleSheet(f'QPushButton {{ background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #636792, stop:1 #4D5175); color: #FFFFFF; border: 1.2px solid #878BB8; border-radius: {self._radius}px; font-weight: bold; padding: 0 8px; }} QPushButton:hover {{ background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #787CAE, stop:1 #5E628E); border: 1.2px solid #A5B4FC; color: #FFFFFF; }} QPushButton:pressed {{ background: #3C3F5E; padding-top: 2px; }}')

        else:
            b_bg = "#FFFFFF" if not es_oscuro else self._bg
            b_fg = "#0F172A" if not es_oscuro else self._fg
            b_border = "#CBD5E1" if not es_oscuro else self._border
            self.setStyleSheet(f'QPushButton {{ background: {b_bg}; color: {b_fg}; border: 1px solid {b_border}; border-radius: {self._radius}px; padding: 0 8px; }}')

    def set_icon(self, p):
        self._icon_path = p
        if p and os.path.exists(p):
            self.setIcon(QIcon(p))
            self.setIconSize(QSize(*self._icon_size))
        else:
            self.setIcon(QIcon())

    def set_colors(self, bg=None, hover=None, fg=None, border=None):
        if bg: self._bg = bg
        if hover: self._hover = hover
        if fg: self._fg = fg
        if border: self._border = border
        if self.property("role") in (None, "", "default"):
            self.setStyleSheet(f'QPushButton {{ background: {self._bg}; color: {self._fg}; border: none; border-radius: {self._radius}px; padding: 0 8px; }}')
        self.update()

    def enterEvent(self, e):
        self._is_hover = True
        t_up = self.text().upper()
        if 'AHORRADO' not in t_up and 'SAVED' not in t_up:
            self._anim.start()
        super().enterEvent(e)

    def leaveEvent(self, e):
        self._is_hover = False
        t_up = self.text().upper()
        if 'AHORRADO' not in t_up and 'SAVED' not in t_up:
            self._anim.stop()
        self.update()
        super().leaveEvent(e)

    def hideEvent(self, e):
        if hasattr(self, "_anim") and self._anim.state() == QVariantAnimation.State.Running:
            t_up = self.text().upper()
            if 'AHORRADO' in t_up or 'SAVED' in t_up:
                self._anim.pause()
            else:
                self._anim.stop()
        super().hideEvent(e)

    def showEvent(self, e):
        super().showEvent(e)
        t_up = self.text().upper()
        if 'AHORRADO' in t_up or 'SAVED' in t_up:
            if hasattr(self, "_anim") and self._anim.state() != QVariantAnimation.State.Running:
                if self._anim.state() == QVariantAnimation.State.Paused:
                    self._anim.resume()
                else:
                    self._anim.start()

    def paintEvent(self, e):
        import math
        t_up = self.text().upper()
        if 'AHORRADO' in t_up or 'SAVED' in t_up:
            p = QPainter(self)
            p.setRenderHint(QPainter.RenderHint.Antialiasing)
            r = self.rect().toRectF()
            ab = 1.5
            r.adjust(ab / 2.0, ab / 2.0, -ab / 2.0, -ab / 2.0)

            bg_grad = QLinearGradient(0, 0, 0, self.height())
            es_oscuro_ahorro = (config.CURRENT_THEME == "dark")
            if not es_oscuro_ahorro:
                if self._is_hover:
                    bg_grad.setColorAt(0.0, QColor('#FCD34D'))
                    bg_grad.setColorAt(1.0, QColor('#F59E0B'))
                else:
                    bg_grad.setColorAt(0.0, QColor('#FBBF24'))
                    bg_grad.setColorAt(1.0, QColor('#D97706'))
            else:
                if self._is_hover:
                    bg_grad.setColorAt(0.0, QColor('#F0B74E'))
                    bg_grad.setColorAt(1.0, QColor('#D4922A'))
                else:
                    bg_grad.setColorAt(0.0, QColor('#E5A93C'))
                    bg_grad.setColorAt(1.0, QColor('#C8861E'))

            p.setPen(Qt.PenStyle.NoPen)
            p.setBrush(bg_grad)
            p.drawRoundedRect(r, float(self._radius), float(self._radius))

            c_bd = '#FFD700' if not (self._is_hover or self._flicker_state) else '#FFFF80'
            p.setPen(QPen(QColor(c_bd), ab))
            p.setBrush(Qt.BrushStyle.NoBrush)
            p.drawRoundedRect(r, float(self._radius), float(self._radius))

            lg = QLinearGradient(self._shine_pos, 0, self._shine_pos + 35, self.height())
            lg.setColorAt(0.0, QColor(255, 255, 255, 0))
            lg.setColorAt(0.5, QColor(255, 255, 255, 120))
            lg.setColorAt(1.0, QColor(255, 255, 255, 0))
            p.setPen(Qt.PenStyle.NoPen)
            p.setBrush(lg)
            p.drawRoundedRect(r, float(self._radius), float(self._radius))

            p.setPen(QPen(QColor('#FFFFFF')))
            p.setFont(self.font())
            p.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, self.text())
            p.end()
            return

        super().paintEvent(e)
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        r = self.rect().toRectF()
        pulso = (math.sin(math.radians(self._ang * 2)) + 1.0) / 2.0
        ab = (2.0 + (pulso * 1.2)) if self._is_hover else float(self._border_width)
        
        desplazamiento_y = 1.5 if self.isDown() else 0.0
        r.adjust(1.0, 1.0 + desplazamiento_y, -1.0, -1.0)

        if self._is_hover:
            g = QConicalGradient(r.center(), self._ang)
            g.setColorAt(0.0, QColor('#FFFFFF'))
            g.setColorAt(0.15, QColor('#00F3FF'))
            g.setColorAt(0.50, QColor('#818CF8'))
            g.setColorAt(0.85, QColor('#00F3FF'))
            g.setColorAt(1.0, QColor('#FFFFFF'))
            pen = QPen(g, ab)
        else:
            pen = QPen(QColor(self._border), ab)

        p.setPen(pen)
        p.setBrush(Qt.BrushStyle.NoBrush)
        p.drawRoundedRect(r, float(self._radius) - 1.0, float(self._radius) - 1.0)
        p.end()

    def setText(self, text):
        t_str = str(text).upper()
        if ('AHORRADO' in t_str or 'SAVED' in t_str) and not getattr(self, '_bloqueo_recursivo', False):
            try:
                nv = float(re.sub(r'[^0-9.-]', '', str(text).replace(',', '')))
            except Exception:
                nv = 0.0
            if abs(nv - self._target_val) > 0.01:
                setattr(self, '_target_val', nv)
                setattr(self, '_flicker_count', 0)
                setattr(self, '_flicker_state', True)
                if not self._flicker_timer.isActive(): self._flicker_timer.start()
                if not self._count_timer.isActive(): self._count_timer.start()
                return
        super().setText(str(text))

    def _do_flicker(self):
        self._flicker_state = not self._flicker_state
        self._flicker_count += 1
        self.update()
        if self._flicker_count >= 6:
            self._flicker_timer.stop()
            self._flicker_state = False
            self.update()

    def _do_count(self):
        d = self._target_val - self._current_val
        if abs(d) < 0.05:
            self._current_val = self._target_val
            self._count_timer.stop()
        else:
            self._current_val += d * 0.12
        self._bloqueo_recursivo = True
        self.setText(t("saved.pill", amount=f"{self._current_val:,.2f}"))
        self._bloqueo_recursivo = False



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


class VolumeSlider(QSlider):
    def __init__(self, parent=None, from_=0, to=100, length=120, command=None, **kwargs):
        super().__init__(Qt.Orientation.Horizontal, parent)
        self._command = command
        self.setRange(int(from_), int(to))
        self.setFixedWidth(int(length))
        self.setFixedHeight(38)
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
        self.valueChanged.connect(self._on_value_changed)

    def _on_hover_step(self, val):
        self._hover_progress = val
        self.update()

    def _on_value_changed(self, value):
        self.update()
        if callable(self._command):
            self._command(value)

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

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._is_dragging = True
            self._actualizar_valor_por_pos(event.position().x())
            event.accept()
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self._is_dragging:
            self._actualizar_valor_por_pos(event.position().x())
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

    def _actualizar_valor_por_pos(self, mouse_x):
        ancho = self.width() - 16
        clamped_x = max(0, min(ancho, mouse_x - 8))
        nuevo_val = int(round((clamped_x / float(ancho)) * (self.maximum() - self.minimum()) + self.minimum()))
        if nuevo_val != self.value():
            self.setValue(nuevo_val)

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)

        ancho_util = self.width() - 16
        ratio = (self.value() - self.minimum()) / float(self.maximum() - self.minimum() or 1)
        handle_x = 8 + (ratio * ancho_util)
        centro_y = self.height() / 2.0

        groove_rect = QRectF(8, centro_y - 2.5, ancho_util, 5)
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(QColor(58, 58, 80, 180))
        p.drawRoundedRect(groove_rect, 2.5, 2.5)

        if ratio > 0.001:
            prog_w = ratio * ancho_util
            prog_rect = QRectF(8, centro_y - 2.5, prog_w, 5)
            grad = QLinearGradient(8, 0, 8 + prog_w, 0)
            grad.setColorAt(0.0, QColor('#6366F1'))
            grad.setColorAt(1.0, QColor('#00F3FF') if self._hover_progress > 0.3 else QColor('#818CF8'))
            p.setBrush(grad)
            p.drawRoundedRect(prog_rect, 2.5, 2.5)

        rx_base, ry_base = 6.0, 6.0
        rx_hover, ry_hover = 16.0, 9.0

        rx = rx_base + (self._hover_progress * (rx_hover - rx_base))
        ry = ry_base + (self._hover_progress * (ry_hover - ry_base))

        handle_cx = max(rx + 2.0, min(self.width() - rx - 2.0, handle_x))
        handle_rect = QRectF(handle_cx - rx, centro_y - ry, rx * 2.0, ry * 2.0)

        if self._hover_progress > 0.05:
            halo_alpha = int(self._hover_progress * 55)
            p.setBrush(QColor(0, 243, 255, halo_alpha))
            p.setPen(Qt.PenStyle.NoPen)
            p.drawRoundedRect(handle_rect.adjusted(-3, -3, 3, 3), ry + 3, ry + 3)

        if self._hover_progress < 0.2:
            p.setBrush(QColor('#FFFFFF'))
            p.setPen(QPen(QColor('#818CF8'), 1.8))
        else:
            bg_alpha = int(self._hover_progress * 255)
            p.setBrush(QColor(18, 19, 31, bg_alpha))
            p.setPen(QPen(QColor('#00F3FF'), 1.5))

        p.drawRoundedRect(handle_rect, ry, ry)

        if self._hover_progress > 0.25:
            txt_alpha = int(((self._hover_progress - 0.25) / 0.75) * 255)
            p.setPen(QColor(255, 255, 255, txt_alpha))
            p.setFont(QFont('Segoe UI', 7, QFont.Weight.Bold))
            p.drawText(handle_rect, Qt.AlignmentFlag.AlignCenter, f"{self.value()}%")

        p.end()


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
        from PySide6.QtWidgets import QGraphicsOpacityEffect
        self._bloquear_neon = True
        
        if not hasattr(self, "_efecto_opacidad") or self.graphicsEffect() is None:
            self._efecto_opacidad = QGraphicsOpacityEffect(self)
            self.setGraphicsEffect(self._efecto_opacidad)
            
        self._efecto_opacidad.setEnabled(True)
        self._efecto_opacidad.setOpacity(0.0)

    def animar_opacidad(self):
        from PySide6.QtCore import QPropertyAnimation, QEasingCurve
        
        if not hasattr(self, "_efecto_opacidad"):
            return
            
        if hasattr(self, "_anim_fade") and self._anim_fade.state() != 0:
            self._anim_fade.stop()
            
        self._anim_fade = QPropertyAnimation(self._efecto_opacidad, b"opacity", self)
        self._anim_fade.setDuration(450)
        self._anim_fade.setStartValue(0.0)
        self._anim_fade.setEndValue(1.0)
        self._anim_fade.setEasingCurve(QEasingCurve.Type.OutCubic)
        
        def _on_finish():
            self._bloquear_neon = False
            if hasattr(self, "_efecto_opacidad"):
                self._efecto_opacidad.setEnabled(False)
            self.update()
            
        self._anim_fade.finished.connect(_on_finish)
        self._anim_fade.start()

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
        g.setColorAt(0.0, QColor("#FFFFFF"))
        g.setColorAt(0.05, QColor("#00F3FF"))
        g.setColorAt(0.12, QColor(129, 140, 248, 50))
        g.setColorAt(0.22, QColor(0, 0, 0, 0))
        g.setColorAt(0.82, QColor(0, 0, 0, 0))
        g.setColorAt(0.95, QColor(0, 243, 255, 120))
        g.setColorAt(1.0, QColor("#FFFFFF"))

        pen = QPen(g, float(self._border_width))
        p.setPen(pen)
        p.setBrush(Qt.BrushStyle.NoBrush)
        p.drawRoundedRect(r, float(self._radius), float(self._radius))
        p.end()

class StoreHeaderBanner(NeonFrame):
    """Banner de cabecera con efecto cristal (glassmorphism) y contorno neón resplandeciente."""

    def __init__(self, parent=None, text=""):
        super().__init__(parent, radius=11, border_width=1.5, speed_ms=3800)
        self.setObjectName("storeContextBanner")
        self.setFixedHeight(44)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 0, 16, 0)
        
        self.label = QLabel(text)
        self.label.setObjectName("storeContextTitle")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label)

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        r = self.rect().toRectF().adjusted(0.75, 0.75, -0.75, -0.75)
        radius = float(self._radius)

        # 1. Fondo base de cristal translúcido ahumado
        es_oscuro = config.CURRENT_THEME == "dark"
        bg_gradient = QLinearGradient(0, 0, 0, self.height())
        if es_oscuro:
            bg_gradient.setColorAt(0.0, QColor(42, 45, 72, 185))
            bg_gradient.setColorAt(1.0, QColor(22, 23, 38, 215))
        else:
            bg_gradient.setColorAt(0.0, QColor(255, 255, 255, 210))
            bg_gradient.setColorAt(1.0, QColor(215, 228, 245, 190))

        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(bg_gradient)
        p.drawRoundedRect(r, radius, radius)

        # 2. Reflejo especular superior de vidrio (sheen)
        sheen_h = self.height() * 0.48
        sheen_rect = QRectF(r.left(), r.top(), r.width(), sheen_h)
        sheen_grad = QLinearGradient(0, r.top(), 0, r.top() + sheen_h)
        if es_oscuro:
            sheen_grad.setColorAt(0.0, QColor(255, 255, 255, 45))
            sheen_grad.setColorAt(1.0, QColor(255, 255, 255, 0))
        else:
            sheen_grad.setColorAt(0.0, QColor(255, 255, 255, 120))
            sheen_grad.setColorAt(1.0, QColor(255, 255, 255, 0))

        path = QPainterPath()
        path.addRoundedRect(r, radius, radius)
        p.save()
        p.setClipPath(path)
        p.setBrush(sheen_grad)
        p.setPen(Qt.PenStyle.NoPen)
        p.drawRect(sheen_rect)
        p.restore()

        # 3. Bisel de cristal (borde fino interior)
        p.setBrush(Qt.BrushStyle.NoBrush)
        c_border = QColor(255, 255, 255, 55 if es_oscuro else 140)
        p.setPen(QPen(c_border, 1.0))
        p.drawRoundedRect(r.adjusted(0.5, 0.5, -0.5, -0.5), radius - 0.5, radius - 0.5)
        p.end()

        # 4. Superponer el haz neón perimetral animado heredado
        super().paintEvent(event)


class GameCard(NeonFrame):
    """Tarjeta de juego con cápsulas uniformes para Tienda, Reseñas Steam y Precio."""

    def __init__(self, owner, juego, nombre_tienda):
        super().__init__(owner.frame_lista, radius=12, border_width=1.5, speed_ms=5500)
        self.owner = owner
        self.juego = juego
        self.nombre_tienda = nombre_tienda
        self._imagen_cargada_con_exito = False
        self.setObjectName("gameCard")
        self.setMouseTracking(True)
        self.setFixedHeight(124)

        self._hover_progress = 0.0
        self._anim_scale = QVariantAnimation(self)
        self._anim_scale.setDuration(230)
        self._anim_scale.setEasingCurve(QEasingCurve.Type.OutQuart)
        self._anim_scale.valueChanged.connect(self._on_scale_step)

        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 10, 14, 10)
        layout.setSpacing(14)

        image_box = QLabel()
        image_box.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        image_box.setObjectName("gameImage")
        image_box.setFixedSize(184, 104)
        image_box.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._image_label = image_box
        layout.addWidget(image_box)

        info = QVBoxLayout()
        info.setSpacing(5)

        titulo_limpio = _limpiar_titulo_visual(juego.get("title", "Elemento sin título"))
        title = QLabel(titulo_limpio)
        title.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        title.setObjectName("gameTitle")
        title.setWordWrap(True)
        info.addWidget(title)

        desc_raw = str(juego.get("description") or "").strip()
        self._desc_original = desc_raw
        texto_inicial = desc_raw if desc_raw else t("card.no_desc")
        self._desc_label = QLabel(texto_inicial[:145] + ("..." if len(texto_inicial) > 148 else ""))
        self._desc_label.setObjectName("gameDescription")
        self._desc_label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        self._desc_label.setWordWrap(True)
        info.addWidget(self._desc_label)

        meta_row = QHBoxLayout()
        meta_row.setSpacing(8)
        meta_row.setContentsMargins(0, 3, 0, 0)

        store = QLabel(nombre_tienda.upper())
        store.setObjectName("gameStore")
        store.setStyleSheet("""
            QLabel#gameStore {
                background-color: rgba(99, 102, 241, 0.18);
                color: #A5B4FC;
                border: 1px solid #818CF8;
                border-radius: 6px;
                padding: 2px 8px;
                font: bold 7.5pt "Segoe UI";
            }
        """)
        meta_row.addWidget(store)

        self._steam_badge = QLabel("")
        self._steam_badge.setObjectName("steamBadge")
        self._steam_badge.hide()
        meta_row.addWidget(self._steam_badge)

        valor = owner._valor_juego(juego)
        if valor > 0:
            worth = QLabel(f"Antes: ${valor:,.2f}")
            worth.setObjectName("gameWorth")
            es_oscuro_chip = (config.CURRENT_THEME == "dark")
            if es_oscuro_chip:
                worth.setStyleSheet("""
                    QLabel#gameWorth {
                        background-color: rgba(245, 158, 11, 0.18);
                        color: #FCD34D;
                        border: 1px solid #F59E0B;
                        border-radius: 6px;
                        padding: 2px 8px;
                        font: bold 7.5pt "Segoe UI";
                    }
                """)
            else:
                worth.setStyleSheet("""
                    QLabel#gameWorth {
                        background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #FEF3C7, stop:1 #FDE68A);
                        color: #92400E;
                        border: 1.2px solid #F59E0B;
                        border-radius: 6px;
                        padding: 2px 8px;
                        font: bold 7.5pt "Segoe UI";
                    }
                """)
            meta_row.addWidget(worth)

        # -- NUEVO: CHIP DE TIEMPO RESTANTE --
        end_date_str = juego.get("end_date")
        if end_date_str and end_date_str.upper() != "N/A":
            try:
                dt_str = end_date_str.split("+")[0].strip()
                if "T" in dt_str:
                    dt_str = dt_str.replace("T", " ")
                if len(dt_str) == 10:
                    dt_str += " 23:59:59"
                    
                end_dt = datetime.datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
                now = datetime.datetime.now()
                
                if end_dt > now:
                    diff = end_dt - now
                    if diff.days > 0:
                        txt_time = t("card.ends_in_days", d=diff.days)
                    elif diff.seconds > 3600:
                        txt_time = t("card.ends_in_hours", h=diff.seconds // 3600)
                    else:
                        txt_time = t("card.ends_today")
                        
                    time_label = QLabel(txt_time)
                    time_label.setObjectName("gameTimeLeft")
                    es_oscuro_chip = (config.CURRENT_THEME == "dark")
                    
                    if es_oscuro_chip:
                        time_label.setStyleSheet("""
                            QLabel#gameTimeLeft {
                                background-color: rgba(236, 72, 153, 0.18);
                                color: #F472B6;
                                border: 1px solid #EC4899;
                                border-radius: 6px;
                                padding: 2px 8px;
                                font: bold 7.5pt "Segoe UI";
                            }
                        """)
                    else:
                        time_label.setStyleSheet("""
                            QLabel#gameTimeLeft {
                                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #FCE7F3, stop:1 #FBCFE8);
                                color: #9D174D;
                                border: 1.2px solid #EC4899;
                                border-radius: 6px;
                                padding: 2px 8px;
                                font: bold 7.5pt "Segoe UI";
                            }
                        """)
                    meta_row.addWidget(time_label)
            except Exception:
                pass
        # ------------------------------------

        meta_row.addStretch()
        info.addLayout(meta_row)

        info.addStretch()
        layout.addLayout(info, 1)

        actions = QVBoxLayout()
        actions.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        actions.setSpacing(6)

        tema = config.THEMES.get(config.CURRENT_THEME, {})
        c_bg_card = tema.get("COLOR_BG_CARD", COLOR_BG_CARD)
        c_border = tema.get("COLOR_BORDER", COLOR_BORDER)
        c_hover = tema.get("COLOR_HOVER", COLOR_HOVER)
        c_accent = tema.get("COLOR_ACCENT", COLOR_ACCENT)
        c_accent_hover = tema.get("COLOR_ACCENT_HOVER", COLOR_ACCENT_HOVER)
        c_accent_light = tema.get("COLOR_ACCENT_LIGHT", COLOR_ACCENT_LIGHT)
        c_success = tema.get("COLOR_SUCCESS", COLOR_SUCCESS)
        c_success_hover = tema.get("COLOR_SUCCESS_HOVER", COLOR_SUCCESS_HOVER)
        c_text = tema.get("COLOR_TEXT_PRIMARY", COLOR_TEXT_PRIMARY)

        if owner._esta_reclamado(juego):
            if getattr(owner, 'mostrando_reclamados', False):
                btn = RoundedButton(
                    self, text=t("card.unclaimed"),
                    command=lambda checked=False, j=juego: owner._alternar_reclamado(j),
                    width=128, height=38,
                    bg=c_bg_card, hover_bg=c_hover,
                    fg=c_text, border=c_border, radius=11,
                    font=("Segoe UI", 8, "bold"), role="secondary",
                )
            else:
                btn = RoundedButton(
                    self, text=t("card.claimed"),
                    command=lambda checked=False, j=juego: owner._alternar_reclamado(j),
                    width=128, height=38,
                    bg=c_accent, hover_bg=c_accent_hover,
                    fg="white", border=c_accent, radius=11,
                    font=("Segoe UI", 8, "bold"), role="accent",
                )
            actions.addWidget(btn)
        else:
            btn_reclamar = RoundedButton(
                self, text=t("card.claim"),
                command=lambda checked=False, u=str(juego.get("open_giveaway_url") or ""): owner._abrir_reclamacion(u),
                width=128, height=36,
                bg=c_success, hover_bg=c_success_hover,
                fg="white", border=c_success, radius=11,
                font=("Segoe UI", 8, "bold"), role="success",
            )
            btn_reclamar.setToolTip(t("tooltip.claim"))
            actions.addWidget(btn_reclamar)

            sub_row = QHBoxLayout()
            sub_row.setContentsMargins(0, 0, 0, 0)
            sub_row.setSpacing(4)

            btn_marcar = RoundedButton(
                self, text="✔",
                width=62, height=32,
                bg=c_bg_card, hover_bg=c_hover,
                fg=c_accent_light, border=c_border, radius=10,
                font=("Segoe UI", 10, "bold"), role="secondary",
            )
            btn_marcar.clicked.connect(lambda checked=False, j=juego, b=btn_marcar: (
                self._lanzar_recompensa_flotante(b),
                owner._alternar_reclamado(j)
            ))
            btn_marcar.setToolTip(t("card.check_tooltip"))

            self._btn_compartir = RoundedButton(
                self, text="🔗",
                command=lambda checked=False: self._compartir_oferta(),
                width=62, height=32,
                bg=c_bg_card, hover_bg=c_hover,
                fg=c_accent_light, border=c_border, radius=10,
                font=("Segoe UI", 10, "bold"), role="secondary",
            )
            self._btn_compartir.setToolTip(t("card.share_tooltip"))

            sub_row.addWidget(btn_marcar)
            sub_row.addWidget(self._btn_compartir)
            actions.addLayout(sub_row)

        layout.addLayout(actions)

        self._load_image(juego.get("image") or juego.get("thumbnail"))
        self._traducir_descripcion()
        self._consultar_steam()

    def _on_scale_step(self, val):
        self._hover_progress = val
        # Elevación vertical fluida
        self.setFixedHeight(int(124 + (val * 12)))
        self._border_width = 1.5 + (val * 0.8)
        self.update()

    def enterEvent(self, event):
        self._anim_scale.stop()
        self._anim_scale.setStartValue(self._hover_progress)
        self._anim_scale.setEndValue(1.0)
        self._anim_scale.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._anim_scale.stop()
        self._anim_scale.setStartValue(self._hover_progress)
        self._anim_scale.setEndValue(0.0)
        self._anim_scale.start()
        super().leaveEvent(event)

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        prog = self._hover_progress
        r = self.rect().toRectF().adjusted(1.0, 1.0, -1.0, -1.0)
        radius = float(self._radius)
        es_oscuro = config.CURRENT_THEME == "dark"

        # 1. Sombra ambiental difusa de elevación tridimensional (Z-Lift)
        if prog > 0.03:
            s_alpha = int(prog * 48)
            p.setPen(Qt.PenStyle.NoPen)
            # Capa de penumbra exterior
            p.setBrush(QColor(0, 0, 0, s_alpha // 2) if es_oscuro else QColor(15, 23, 42, s_alpha // 3))
            p.drawRoundedRect(r.adjusted(-3, 1, 3, 5), radius + 2, radius + 2)
            # Capa de sombra cercana de oclusión
            p.setBrush(QColor(0, 0, 0, s_alpha) if es_oscuro else QColor(15, 23, 42, s_alpha // 2))
            p.drawRoundedRect(r.adjusted(-1, 0, 1, 3), radius + 1, radius + 1)

        # 2. Fondo continuo interpolado orgánicamente
        if es_oscuro:
            c_top_r = int(45 + (prog * 9))
            c_top_g = int(45 + (prog * 11))
            c_top_b = int(63 + (prog * 16))
            c_bot_r = int(28 + (prog * 4))
            c_bot_g = int(29 + (prog * 4))
            c_bot_b = int(46 + (prog * 5))
        else:
            c_top_r = int(255 - (prog * 6))
            c_top_g = int(255 - (prog * 6))
            c_top_b = int(255 - (prog * 4))
            c_bot_r = int(241 - (prog * 8))
            c_bot_g = int(245 - (prog * 8))
            c_bot_b = int(249 - (prog * 6))

        bg = QLinearGradient(0, 0, 0, self.height())
        bg.setColorAt(0.0, QColor(c_top_r, c_top_g, c_top_b))
        bg.setColorAt(1.0, QColor(c_bot_r, c_bot_g, c_bot_b))

        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(bg)
        p.drawRoundedRect(r, radius, radius)

        # 3. Borde reactivo orgánico (halo cian suave proporcional a la elevación)
        p.setBrush(Qt.BrushStyle.NoBrush)
        if prog > 0.05:
            c_neon = QColor(0, 243, 255, int(prog * 200))
            p.setPen(QPen(c_neon, 1.2 + (prog * 0.6)))
        else:
            p.setPen(QPen(QColor(COLOR_BORDER if es_oscuro else "#CBD5E1"), 1.0))
        p.drawRoundedRect(r, radius, radius)
        p.end()

        # 4. Superponer el haz neón orbital animado
        super().paintEvent(event)

    def _lanzar_recompensa_flotante(self, widget_origen=None):
        try:
            ventana_raiz = self.window()
            if not ventana_raiz:
                return

            valor = self.owner._valor_juego(self.juego)
            texto = f"+${valor:,.2f}" if valor > 0 else "¡Reclamado! ✨"

            origen = widget_origen or self
            pos_global = origen.mapToGlobal(QPoint(0, 0))
            pos_en_ventana = ventana_raiz.mapFromGlobal(pos_global)

            pos_inicial = QPoint(pos_en_ventana.x() - 10, pos_en_ventana.y() - 14)
            FloatingRewardLabel(ventana_raiz, texto, pos_inicial)
        except Exception:
            pass

    def _compartir_oferta(self):
        titulo = str(self.juego.get("title", "Juego gratuito"))
        tienda = str(self.nombre_tienda or "PC")
        url = str(self.juego.get("open_giveaway_url") or "")
        valor = self.owner._valor_juego(self.juego)
        valor_txt = f" (Antes: ${valor:,.2f})" if valor > 0 else ""

        texto = (
            f"🎮 **¡JUEGO GRATIS!** — {titulo}\n"
            f"🏪 **Tienda:** {tienda}{valor_txt}\n"
            f"🔗 **Reclámalo aquí:** {url}\n"
            f"✨ *Compartido desde KG Tracker*"
        )

        portapapeles = QApplication.clipboard()
        if portapapeles:
            portapapeles.setText(texto)

        if hasattr(self, "_btn_compartir") and self._btn_compartir:
            self._btn_compartir.setText("✓")
            self._btn_compartir.setToolTip(t("card.share_copied"))
            QTimer.singleShot(1500, lambda: (
                self._btn_compartir.setText("🔗"),
                self._btn_compartir.setToolTip(t("card.share_tooltip"))
            ))

    def _mostrar_placeholder_tienda(self):
        self._image_label.setPixmap(QPixmap())
        self._image_label.setText(str(self.nombre_tienda).upper())

    def _load_image(self, url_img):
        if not url_img:
            self._mostrar_placeholder_tienda()
            return

        self._current_url = url_img
        self._mostrar_placeholder_tienda()

        from core.image_loader import ImageLoader
        ImageLoader.get_instance().cargar(
            url_img,
            self._on_miniatura_cargada,
            (self._image_label.width(), self._image_label.height()),
        )

    def _on_miniatura_cargada(self, url, pixmap):
        if getattr(self, "_current_url", None) != url:
            return
        if pixmap is not None and not pixmap.isNull():
            self._imagen_cargada_con_exito = True
            self._image_label.setText("")
            redondeado = _redondear_pixmap(pixmap, 8)
            self._image_label.setPixmap(redondeado)
        else:
            self._imagen_cargada_con_exito = False
            self._mostrar_placeholder_tienda()

    def _traducir_descripcion(self):
        idioma = obtener_idioma()
        if idioma == "en" or not self._desc_original:
            return

        GameTranslator.get_instance().traducir_async(
            self._desc_original,
            idioma,
            self._al_recibir_traduccion,
        )

    def _al_recibir_traduccion(self, texto_traducido):
        if not texto_traducido or texto_traducido == self._desc_original:
            return
        desc = " ".join(texto_traducido.split())
        if len(desc) > 148:
            desc = desc[:145] + "..."
        self._desc_label.setText(desc)

    def _consultar_steam(self):
        titulo = str(self.juego.get("title") or "")
        if not titulo:
            return

        SteamEnricher.get_instance().obtener_resenas_async(
            titulo,
            self._al_recibir_datos_steam,
        )

    def _al_recibir_datos_steam(self, datos):
        if not datos:
            return

        banner = datos.get("banner_url")
        if banner and not getattr(self, "_imagen_cargada_con_exito", False):
            self._load_image(banner)

        if not datos.get("found") or not datos.get("percent"):
            return

        percent = datos.get("percent", 0)
        idioma = obtener_idioma()
        desc = datos.get("desc_es") if idioma == "es" else datos.get("desc_en")

        if percent >= 80:
            color_accent = "#10B981"
            bg_color = "rgba(16, 185, 129, 0.16)"
        elif percent >= 70:
            color_accent = "#38BDF8"
            bg_color = "rgba(56, 189, 248, 0.16)"
        else:
            color_accent = "#F59E0B"
            bg_color = "rgba(245, 158, 11, 0.16)"

        self._steam_badge.setText(f"★ Steam: {percent}% ({desc})")
        self._steam_badge.setStyleSheet(f"""
            QLabel#steamBadge {{
                background-color: {bg_color};
                color: {color_accent};
                border: 1px solid {color_accent};
                border-radius: 6px;
                padding: 2px 8px;
                font: bold 7.5pt "Segoe UI";
            }}
        """)
        self._steam_badge.show()
