import os

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


class RoundedButton(QPushButton):
    def __init__(self, parent=None, text='', command=None, width=120, height=42, bg=COLOR_BG_CARD, hover_bg=COLOR_HOVER, fg='white', radius=12, font=None, border=COLOR_BORDER, border_width=1, icon_path=None, icon_size=(20,20), role='default'):
        super().__init__(text, parent); self._bg=bg; self._hover=hover_bg; self._fg=fg; self._border=border; self._border_width=border_width; self._radius=radius; self._icon_size=icon_size; self._is_hover=False; self._ang=0.0
        
        self.setText(text); self.setFixedSize(int(width), int(height)); self.setCursor(Qt.CursorShape.PointingHandCursor); self.setFlat(True); self.setProperty('role', role)
        from PySide6.QtGui import QFont; self.setFont(QFont('Segoe UI', 8, QFont.Weight.Bold) if role!='secondary' else QFont('Segoe UI', 7, QFont.Weight.Bold))
        from PySide6.QtCore import QVariantAnimation; self._anim=QVariantAnimation(self); self._anim.setStartValue(0.0); self._anim.setEndValue(360.0); self._anim.setDuration(2200); self._anim.setLoopCount(-1); self._anim.valueChanged.connect(lambda v: (setattr(self, '_ang', v), self.update()))
        self.setStyleSheet(f'QPushButton {{ background: {self._bg}; color: {self._fg}; border: none; border-radius: {self._radius}px; padding: 0 8px; }}')
        self.set_icon(icon_path); self.clicked.connect(command) if callable(command) else None
    def set_icon(self, p): self._icon_path=p; (self.setIcon(__import__('PySide6.QtGui', fromlist=['QIcon']).QIcon(p)), self.setIconSize(QSize(*self._icon_size))) if p and os.path.exists(p) else self.setIcon(__import__('PySide6.QtGui', fromlist=['QIcon']).QIcon())
    def set_colors(self, bg=None, hover=None, fg=None, border=None): self._bg=bg if bg else self._bg; self._hover=hover if hover else self._hover; self._fg=fg if fg else self._fg; self._border=border if border else self._border; self.setStyleSheet(f'QPushButton {{ background: {self._bg}; color: {self._fg}; border: none; border-radius: {self._radius}px; padding: 0 8px; }}')
    def enterEvent(self, e): self._is_hover=True; self._anim.start(); super().enterEvent(e)
    def leaveEvent(self, e): self._is_hover=False; self._anim.stop(); self.update(); super().leaveEvent(e)
    def paintEvent(self, e):
        super().paintEvent(e); p=__import__('PySide6.QtGui', fromlist=['QPainter']).QPainter(self); p.setRenderHint(p.RenderHint.Antialiasing)
        r=self.rect().toRectF(); import math; pulso=(math.sin(math.radians(self._ang*2))+1.0)/2.0; ab=(2.0+(pulso*1.5)) if self._is_hover else float(self._border_width)
        r.adjust(ab/2.0, ab/2.0, -ab/2.0, -ab/2.0)
        if self._is_hover:
            g=__import__('PySide6.QtGui', fromlist=['QConicalGradient']).QConicalGradient(r.center(), self._ang)
            g.setColorAt(0.0, __import__('PySide6.QtGui', fromlist=['QColor']).QColor(self._hover)); g.setColorAt(0.5, __import__('PySide6.QtGui', fromlist=['QColor']).QColor(COLOR_ACCENT_LIGHT)); g.setColorAt(1.0, __import__('PySide6.QtGui', fromlist=['QColor']).QColor(self._hover))
            pen=__import__('PySide6.QtGui', fromlist=['QPen']).QPen(g, ab)
        else: pen=__import__('PySide6.QtGui', fromlist=['QPen']).QPen(__import__('PySide6.QtGui', fromlist=['QColor']).QColor(self._border), ab)
        p.setPen(pen); p.setBrush(__import__('PySide6.QtCore', fromlist=['Qt']).Qt.BrushStyle.NoBrush); p.drawRoundedRect(r, float(self._radius), float(self._radius)); p.end()
    def config(self, **k):
        self.setText(k.pop('text')) if 'text' in k else None; self._bg=k.pop('bg') if 'bg' in k else self._bg; self._fg=k.pop('fg') if 'fg' in k else self._fg; self._hover=k.pop('activebackground') if 'activebackground' in k else self._hover
        self.setStyleSheet(f'QPushButton {{ background: {self._bg}; color: {self._fg}; border: none; border-radius: {self._radius}px; padding: 0 8px; }}')
        self.setEnabled(k.pop('enabled')) if k.get('enabled') is not None else None
        for key, v in k.items(): setattr(self, key, v) if hasattr(self, key) else None

class VolumeSlider(QSlider):
    """Slider Qt equivalente al control de volumen original."""

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

    def set_colors(self, bg=None, track_bg=None, fill_bg=None, knob_bg=None):
        self.setStyleSheet(
            f"QSlider {{ background: {bg or 'transparent'}; }}"
            f"QSlider::groove:horizontal {{ height: 5px; background: {track_bg or COLOR_BORDER}; border-radius: 2px; }}"
            f"QSlider::sub-page:horizontal {{ background: {fill_bg or COLOR_ACCENT}; border-radius: 2px; }}"
            f"QSlider::handle:horizontal {{ width: 14px; margin: -5px 0; border-radius: 7px; background: {knob_bg or COLOR_TEXT_PRIMARY}; border: 2px solid {fill_bg or COLOR_ACCENT}; }}"
        )


class GameCard(QFrame):
    """Tarjeta Qt de un juego."""

    def __init__(self, owner, juego, nombre_tienda):
        super().__init__(owner.frame_lista)
        self.owner = owner
        self.juego = juego
        self.nombre_tienda = nombre_tienda
        self.setObjectName("gameCard")

        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed,
        )

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

        title = QLabel(str(juego.get("title", "Elemento sin tÃ­tulo")))
        title.setObjectName("gameTitle")
        title.setWordWrap(True)
        info.addWidget(title)

        descripcion = " ".join(str(juego.get("description", "Sin descripciÃ³n disponible.")).split())
        if len(descripcion) > 170:
            descripcion = descripcion[:167] + "..."
        desc = QLabel(descripcion)
        desc.setObjectName("gameDescription")
        desc.setWordWrap(True)
        info.addWidget(desc)

        store = QLabel(nombre_tienda.upper())
        store.setObjectName("gameStore")
        info.addWidget(store)

        valor = owner._valor_juego(juego)
        if valor > 0:
            worth = QLabel(f"VALOR ESTIMADO: ${valor:,.2f}")
            worth.setObjectName("gameWorth")
            info.addWidget(worth)

        info.addStretch()
        layout.addLayout(info, 1)

        actions = QVBoxLayout()
        actions.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        if owner._esta_reclamado(juego):
            btn = RoundedButton(
                self, text="RECLAMADO",
                command=lambda checked=False, j=juego: owner._alternar_reclamado(j),
                width=128, height=38,
                bg=COLOR_ACCENT, hover_bg=COLOR_ACCENT_HOVER,
                fg="white", border=COLOR_ACCENT, radius=11,
                font=("Segoe UI", 8, "bold"), role="accent",
            )
            actions.addWidget(btn)
        else:
            btn_reclamar = RoundedButton(
                self, text="RECLAMAR",
                command=lambda checked=False, u=str(juego.get("open_giveaway_url") or ""): owner._abrir_reclamacion(u),
                width=128, height=36,
                bg=COLOR_SUCCESS, hover_bg=COLOR_SUCCESS_HOVER,
                fg="white", border=COLOR_SUCCESS, radius=11,
                font=("Segoe UI", 8, "bold"), role="success",
            )
            actions.addWidget(btn_reclamar)
            btn_marcar = RoundedButton(
                self, text="RECLAMADO",
                command=lambda checked=False, j=juego: owner._alternar_reclamado(j),
                width=128, height=32,
                bg=COLOR_BG_CARD, hover_bg=COLOR_HOVER,
                fg=COLOR_ACCENT_LIGHT, border=COLOR_BORDER, radius=10,
                font=("Segoe UI", 7, "bold"), role="secondary",
            )
            actions.addWidget(btn_marcar)

        layout.addLayout(actions)

        self._load_image(juego.get("image") or juego.get("thumbnail"))

    def _load_image(self, url_img):
        import requests
        pixmap = self.owner._load_thumbnail(url_img)
        if pixmap is not None and not pixmap.isNull():
            self._image_label.setPixmap(
                pixmap.scaled(
                    self._image_label.size(),
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )
            )
        else:
            self._image_label.setText("SIN\nMINIATURA")












