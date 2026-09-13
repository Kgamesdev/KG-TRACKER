import os
import config

from PySide6.QtCore import Qt, QSize, QVariantAnimation, QTimer
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
from core.steam_enricher import SteamEnricher


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
    self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
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
    if role == 'success':
        self.setStyleSheet(f'QPushButton {{ background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 {self._bg}, stop:1 {self._hover}); color: {self._fg}; border: 1px solid #34D399; border-radius: {self._radius}px; font-weight: bold; padding: 0 8px; }} QPushButton:hover {{ background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #34D399, stop:1 {self._bg}); }} QPushButton:pressed {{ background: #047857; padding-top: 2px; }}')
    elif role == 'secondary':
        self.setStyleSheet(f'QPushButton {{ background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #3A3B52, stop:1 #262738); color: {self._fg}; border: 1px solid #4E506B; border-radius: {self._radius}px; font-weight: bold; padding: 0 8px; }} QPushButton:hover {{ background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #4E506B, stop:1 #3A3B52); border: 1px solid #818CF8; color: #818CF8; }} QPushButton:pressed {{ background: #1E1F2E; padding-top: 2px; }}')
    else:
        self.setStyleSheet(f'QPushButton {{ background: {self._bg}; color: {self._fg}; border: 1px solid {self._border}; border-radius: {self._radius}px; padding: 0 8px; }}')


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
    from PySide6.QtGui import QPainter, QConicalGradient, QColor, QPen, QLinearGradient
    from PySide6.QtCore import Qt
    import math

    t_up = self.text().upper()
    if 'AHORRADO' in t_up or 'SAVED' in t_up:
      p = QPainter(self)
      p.setRenderHint(QPainter.RenderHint.Antialiasing)
      r = self.rect().toRectF()
      ab = 1.5
      r.adjust(ab / 2.0, ab / 2.0, -ab / 2.0, -ab / 2.0)

      bg_grad = QLinearGradient(0, 0, 0, self.height())
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
    
    # Margen interior de seguridad: evita que la línea inferior se corte
    desplazamiento_y = 1.5 if self.isDown() else 0.0
    r.adjust(1.0, 1.0 + desplazamiento_y, -1.0, -1.0)

    tema = config.THEMES.get(config.CURRENT_THEME, {})
    accent_light = tema.get("COLOR_ACCENT_LIGHT", COLOR_ACCENT_LIGHT)

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


class NeonFrame(QFrame):
    """QFrame con un haz de luz neón blanco autónomo animado que recorre el perímetro."""

    def __init__(self, parent=None, radius=12, border_width=1.5, speed_ms=4500):
        super().__init__(parent)
        self._radius = radius
        self._border_width = border_width
        self._ang = 0.0

        self._neon_anim = QVariantAnimation(self)
        self._neon_anim.setStartValue(0.0)
        self._neon_anim.setEndValue(360.0)
        self._neon_anim.setDuration(speed_ms)
        self._neon_anim.setLoopCount(-1)
        self._neon_anim.valueChanged.connect(self._on_neon_step)

    def _on_neon_step(self, val):
        self._ang = val
        self.update()

    def showEvent(self, event):
        super().showEvent(event)
        if hasattr(self, "_neon_anim") and self._neon_anim.state() != QVariantAnimation.State.Running:
            self._neon_anim.start()

    def hideEvent(self, event):
        if hasattr(self, "_neon_anim") and self._neon_anim.state() == QVariantAnimation.State.Running:
            self._neon_anim.pause()
        super().hideEvent(event)

    def paintEvent(self, event):
        super().paintEvent(event)
        from PySide6.QtGui import QPainter, QConicalGradient, QColor, QPen
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        r = self.rect().toRectF()
        r.adjust(0.75, 0.75, -0.75, -0.75)

        g = QConicalGradient(r.center(), self._ang)
        g.setColorAt(0.0, QColor("#FFFFFF"))          # Haz neón blanco puro
        g.setColorAt(0.05, QColor("#00F3FF"))         # Estela cian eléctrica
        g.setColorAt(0.12, QColor(129, 140, 248, 50)) # Halo índigo suave
        g.setColorAt(0.22, QColor(0, 0, 0, 0))         # Fondo transparente
        g.setColorAt(0.82, QColor(0, 0, 0, 0))
        g.setColorAt(0.95, QColor(0, 243, 255, 120))  # Destello frontal
        g.setColorAt(1.0, QColor("#FFFFFF"))          # Cierre incandescente

        pen = QPen(g, float(self._border_width))
        p.setPen(pen)
        p.setBrush(Qt.BrushStyle.NoBrush)
        p.drawRoundedRect(r, float(self._radius), float(self._radius))
        p.end()

class GameCard(NeonFrame):
  def __init__(self, owner, juego, nombre_tienda):
    super().__init__(owner.frame_lista, radius=12, border_width=1.5, speed_ms=5500)
    self.owner = owner
    self.juego = juego
    self.nombre_tienda = nombre_tienda
    self._imagen_cargada_con_exito = False
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

    meta_row = QHBoxLayout()
    meta_row.setSpacing(8)
    meta_row.setContentsMargins(0, 0, 0, 0)

    store = QLabel(nombre_tienda.upper())
    store.setObjectName("gameStore")
    meta_row.addWidget(store)

    self._steam_badge = QLabel("")
    self._steam_badge.setObjectName("steamBadge")
    self._steam_badge.hide()
    meta_row.addWidget(self._steam_badge)
    meta_row.addStretch()

    info.addLayout(meta_row)

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
      btn_reclamar.setToolTip(t("tooltip.claim"))
      actions.addWidget(btn_reclamar)

      # Fila inferior simétrica: [ ✔ ] (62px) + [ 🔗 ] (62px) = 128px exactos
      sub_row = QHBoxLayout()
      sub_row.setContentsMargins(0, 0, 0, 0)
      sub_row.setSpacing(4)

      btn_marcar = RoundedButton(
        self, text="✔",
        command=lambda checked=False, j=juego: owner._alternar_reclamado(j),
        width=62, height=32,
        bg=c_bg_card, hover_bg=c_hover,
        fg=c_accent_light, border=c_border, radius=10,
        font=("Segoe UI", 10, "bold"), role="secondary",
      )
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

  def _compartir_oferta(self):
    """Copia al portapapeles los datos de la oferta en formato Markdown para Discord/Redes."""
    from PySide6.QtWidgets import QApplication
    from PySide6.QtCore import QTimer

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
    """Muestra el nombre de la tienda en texto tipográfico limpio sin logotipos comerciales."""
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
      self._image_label.setPixmap(pixmap)
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
    if len(desc) > 170:
      desc = desc[:167] + "..."
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

    # Si la foto original de la tienda falló y Steam tiene carátula oficial de respaldo:
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
      bg_color = "rgba(16, 185, 129, 0.15)"
    elif percent >= 70:
      color_accent = "#38BDF8"
      bg_color = "rgba(56, 189, 248, 0.15)"
    else:
      color_accent = "#F59E0B"
      bg_color = "rgba(245, 158, 11, 0.15)"

    self._steam_badge.setText(f" Steam: {percent}% ({desc})")
    self._steam_badge.setStyleSheet(f"""
      QLabel#steamBadge {{
        background-color: {bg_color};
        color: {color_accent};
        border: 1px solid {color_accent};
        border-radius: 4px;
        padding: 1px 6px;
        font: bold 7pt "Segoe UI";
      }}
    """)
    self._steam_badge.show()
