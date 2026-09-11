import os
import config

from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import (
    QApplication, QFrame, QHBoxLayout, QLabel, QPushButton,
    QSizePolicy, QSlider, QVBoxLayout,
)

from config import (
    COLOR_BG_CARD, COLOR_HOVER, COLOR_BORDER, COLOR_ACCENT,
    COLOR_ACCENT_HOVER, COLOR_ACCENT_LIGHT, COLOR_SUCCESS,
    COLOR_SUCCESS_HOVER, COLOR_TEXT_PRIMARY,
)
from core.i18n import t, obtener_idioma
from core.translator import GameTranslator


class RoundedButton(QPushButton):
    def __init__(self, parent=None, text='', command=None, width=120, height=42, bg=COLOR_BG_CARD, hover_bg=COLOR_HOVER, fg='white', radius=12, font=None, border=COLOR_BORDER, border_width=1, icon_path=None, icon_size=(20,20), role='default'):
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
                import re
                self._current_val = float(re.sub(r'[^0-9.-]', '', text.replace(',', '')))
                self._target_val = self._current_val
            except Exception:
                pass
        
        self.setText(text)
        self.setFixedSize(int(width), int(height))
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFlat(True)
        self.setProperty('role', role)

        from PySide6.QtGui import QFont
        self.setFont(QFont('Segoe UI', 8, QFont.Weight.Bold) if role != 'secondary' else QFont('Segoe UI', 7, QFont.Weight.Bold))

        from PySide6.QtCore import QVariantAnimation, QTimer
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

        if role in (None, '', 'default'):
            self.setStyleSheet(f'QPushButton {{ background: {self._bg}; color: {self._fg}; border: none; border-radius: {self._radius}px; padding: 0 8px; }}')
        else:
            self.setStyleSheet(f'QPushButton {{ border: none; border-radius: {self._radius}px; padding: 0 8px; }}')

        self.set_icon(icon_path)
        if callable(command):
            self.clicked.connect(command)

    def set_icon(self, p):
        self._icon_path = p
        if p and os.path.exists(p):
            from PySide6.QtGui import QIcon
            self.setIcon(QIcon(p))
            self.setIconSize(QSize(*self._icon_size))
        else:
            from PySide6.QtGui import QIcon
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

    def paintEvent(self, e):
        super().paintEvent(e)
        from PySide6.QtGui import QPainter, QConicalGradient, QColor, QPen, QLinearGradient
        from PySide6.QtCore import Qt
        import math

        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        r = self.rect().toRectF()
        pulso = (math.sin(math.radians(self._ang * 2)) + 1.0) / 2.0
        ab = (2.0 + (pulso * 1.5)) if self._is_hover else float(self._border_width)
        r.adjust(ab / 2.0, ab / 2.0, -ab / 2.0, -ab / 2.0)

        t_up = self.text().upper()
        if 'AHORRADO' in t_up or 'SAVED' in t_up:
            c_bd = '#FFD700' if not (self._is_hover or self._flicker_state) else '#FFFF80'
            ab = 2.5 if (self._is_hover or self._flicker_state) else 1.2
            p.setPen(QPen(QColor(c_bd), ab))
            p.setBrush(Qt.BrushStyle.NoBrush)
            p.drawRoundedRect(r, float(self._radius), float(self._radius))

            lg = QLinearGradient(self._shine_pos, 0, self._shine_pos + 35, self.height())
            lg.setColorAt(0.0, QColor(255, 255, 255, 0))
            lg.setColorAt(0.5, QColor(255, 255, 255, 190))
            lg.setColorAt(1.0, QColor(255, 255, 255, 0))
            p.setPen(Qt.PenStyle.NoPen)
            p.setBrush(lg)
            p.drawRoundedRect(r, float(self._radius), float(self._radius))
            p.end()
            return

        tema = config.THEMES.get(config.CURRENT_THEME, {})
        accent_light = tema.get("COLOR_ACCENT_LIGHT", COLOR_ACCENT_LIGHT)

        if self._is_hover:
            g = QConicalGradient(r.center(), self._ang)
            g.setColorAt(0.0, QColor(self._hover))
            g.setColorAt(0.5, QColor(accent_light))
            g.setColorAt(1.0, QColor(self._hover))
            pen = QPen(g, ab)
        else:
            pen = QPen(QColor(self._border), ab)

        p.setPen(pen)
        p.setBrush(Qt.BrushStyle.NoBrush)
        p.drawRoundedRect(r, float(self._radius), float(self._radius))
        p.end()

    def setText(self, text):
        t_str = str(text).upper()
        if ('AHORRADO' in t_str or 'SAVED' in t_str) and not getattr(self, '_bloqueo_recursivo', False):
            try:
                import re
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
        self.setFixedHeight(22)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.valueChanged.connect(self._on_value_changed)

    def _on_value_changed(self, value):
        if callable(self._command):
            self._command(value)


class GameCard(QFrame):
    def __init__(self, owner, juego, nombre_tienda):
        super().__init__(owner.frame_lista)
        self.owner = owner
        self.juego = juego
        self.nombre_tienda = nombre_tienda
        self.setObjectName("gameCard")

        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 10, 12, 10)
        layout.setSpacing(10)

        image_box = QLabel()
        image_box.setObjectName("gameImage")
        image_box.setFixedSize(190, 104)
        image_box.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._image_label = image_box
        layout.addWidget(image_box)

        info = QVBoxLayout()
        info.setSpacing(4)

        title = QLabel(str(juego.get("title", "Elemento sin título")))
        title.setObjectName("gameTitle")
        title.setWordWrap(True)
        info.addWidget(title)

        desc_raw = str(juego.get("description") or "").strip()
        self._desc_original = desc_raw
        texto_inicial = desc_raw if desc_raw else t("card.no_desc")
        self._desc_label = QLabel(texto_inicial[:167] + ("..." if len(texto_inicial) > 170 else ""))
        self._desc_label.setObjectName("gameDescription")
        self._desc_label.setWordWrap(True)
        info.addWidget(self._desc_label)

        store = QLabel(nombre_tienda.upper())
        store.setObjectName("gameStore")
        info.addWidget(store)

        valor = owner._valor_juego(juego)
        if valor > 0:
            worth = QLabel(t("card.estimated_worth", worth=f"{valor:,.2f}"))
            worth.setObjectName("gameWorth")
            info.addWidget(worth)

        info.addStretch()
        layout.addLayout(info, 1)

        actions = QVBoxLayout()
        actions.setAlignment(Qt.AlignmentFlag.AlignVCenter)

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
            actions.addWidget(btn_reclamar)
            btn_marcar = RoundedButton(
                self, text=t("card.claimed"),
                command=lambda checked=False, j=juego: owner._alternar_reclamado(j),
                width=128, height=32,
                bg=c_bg_card, hover_bg=c_hover,
                fg=c_accent_light, border=c_border, radius=10,
                font=("Segoe UI", 7, "bold"), role="secondary",
            )
            actions.addWidget(btn_marcar)

        layout.addLayout(actions)

        # Cargar miniatura de forma asíncrona
        self._load_image(juego.get("image") or juego.get("thumbnail"))

        # Traducir descripción si el idioma activo es distinto a inglés
        self._traducir_descripcion()

    def _load_image(self, url_img):
        if not url_img:
            self._image_label.setText(t("card.no_thumbnail"))
            return

        self._current_url = url_img
        self._image_label.setText(t("card.loading_thumbnail"))

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
            self._image_label.setText("")
            self._image_label.setPixmap(pixmap)
        else:
            self._image_label.setText(t("card.no_thumbnail"))

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
        if len(desc) > 170:
            desc = desc[:167] + "..."
        self._desc_label.setText(desc)
