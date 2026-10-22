"""Controles reutilizables de la interfaz: botones, volumen y etiquetas efímeras."""

import math
import os
import re

import config
from config import (
    COLOR_BG_CARD, COLOR_BORDER, COLOR_HOVER,
)
from core.i18n import t
from ui.design_system import FONT_FAMILY, FONT_SIZE_BODY_PT
from PySide6.QtCore import (
    QEasingCurve, QParallelAnimationGroup, QPoint, QPropertyAnimation, QRectF,
    QSize, Qt,
    QTimer, QVariantAnimation,
)
from PySide6.QtGui import (
    QColor, QConicalGradient, QFont, QIcon, QLinearGradient, QPainter, QPen,
)
from PySide6.QtWidgets import (
    QGraphicsOpacityEffect, QLabel, QPushButton, QSlider,
)


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

        self.setFont(QFont(FONT_FAMILY, FONT_SIZE_BODY_PT, QFont.Weight.Bold))

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
                self.setStyleSheet(f'QPushButton {{ background: #C6D6EA; color: #354E76; border: 1px solid #AEBFD7; border-radius: {self._radius}px; font-weight: bold; padding: 0 8px; letter-spacing: 0.2px; }} QPushButton:hover {{ background: #B9CCE3; border: 1px solid #98AFCE; }} QPushButton:pressed {{ background: #AEC3DE; padding-top: 2px; }}')

        elif role == 'success':
            # 2. BOTÓN VERDE (RECLAMAR): Mismo verde esmeralda, versión menta luminosa
            if es_oscuro:
                self.setStyleSheet(f'QPushButton {{ background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 {self._bg}, stop:1 {self._hover}); color: {self._fg}; border: 1px solid #34D399; border-radius: {self._radius}px; font-weight: bold; padding: 0 8px; }} QPushButton:hover {{ background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #34D399, stop:1 {self._bg}); }} QPushButton:pressed {{ background: #047857; padding-top: 2px; }}')
            else:
                self.setStyleSheet(f'QPushButton {{ background: #C8E2D2; color: #35634B; border: 1px solid #AECFB9; border-radius: {self._radius}px; font-weight: bold; padding: 0 8px; }} QPushButton:hover {{ background: #BDDBC9; border: 1px solid #9FC6AD; }} QPushButton:pressed {{ background: #B1D3BE; padding-top: 2px; }}')

        elif role in ('secondary', 'sidebar'):
            # 3. BOTONES AZUL MARINO / PIZARRA (SIDEBAR, [✔], [🔗], RECLAMADOS, MUTE):
            # En tema claro: El mismo azul pizarra del tema oscuro, pero en tono acero claro satinado y visible
            if es_oscuro:
                bg_dark = "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #3A3B52, stop:1 #262738)" if role == 'secondary' else "qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #25263A, stop:1 #171827)"
                bd_dark = "#4E506B" if role == 'secondary' else "#3A3A50"
                self.setStyleSheet(f'QPushButton {{ background: {bg_dark}; color: #FFFFFF; border: 1px solid {bd_dark}; border-radius: {self._radius}px; font-weight: bold; padding: 0 8px; }} QPushButton:hover {{ background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #4E506B, stop:1 #3A3B52); border: 1px solid #818CF8; color: #818CF8; }} QPushButton:pressed {{ background: #1E1F2E; padding-top: 2px; }}')
            else:
                if role == 'sidebar':
                    bg_light, hover_light, pressed_light = "#D0DCEC", "#C4D4E8", "#B8CAE2"
                    fg_light, border_light, hover_border = "#3B5479", "#B2C2D8", "#9FB4D0"
                else:
                    bg_light, hover_light, pressed_light = "#DDE5EF", "#D0DCE9", "#C4D2E2"
                    fg_light, border_light, hover_border = "#38485D", "#C1CDDB", "#AEBED2"
                self.setStyleSheet(f'QPushButton {{ background: {bg_light}; color: {fg_light}; border: 1px solid {border_light}; border-radius: {self._radius}px; font-weight: bold; padding: 0 8px; }} QPushButton:hover {{ background: {hover_light}; border: 1px solid {hover_border}; color: {fg_light}; }} QPushButton:pressed {{ background: {pressed_light}; padding-top: 2px; }}')

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
                    bg_grad.setColorAt(0.0, QColor('#F2E5C3'))
                    bg_grad.setColorAt(1.0, QColor('#EEDFB2'))
                else:
                    bg_grad.setColorAt(0.0, QColor('#F0E1B8'))
                    bg_grad.setColorAt(1.0, QColor('#EBD8A6'))
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

            c_bd = '#DDC77F' if not (self._is_hover or self._flicker_state) else '#CFB965'
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

            p.setPen(QPen(QColor('#70591F') if not es_oscuro_ahorro else QColor('#FFFFFF')))
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
            if config.CURRENT_THEME == "light":
                g.setColorAt(0.0, QColor('#E7EDF6'))
                g.setColorAt(0.15, QColor('#BCCBDD'))
                g.setColorAt(0.50, QColor('#8299BD'))
                g.setColorAt(0.85, QColor('#BCCBDD'))
                g.setColorAt(1.0, QColor('#E7EDF6'))
            else:
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
            p.setFont(QFont('Segoe UI', 8, QFont.Weight.Bold))
            p.drawText(handle_rect, Qt.AlignmentFlag.AlignCenter, f"{self.value()}%")

        p.end()
