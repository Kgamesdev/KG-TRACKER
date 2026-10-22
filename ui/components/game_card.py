"""Componentes visuales y tarjetas de juego para KG Tracker."""

import re
import config
import datetime

from PySide6.QtCore import (
    Qt, QVariantAnimation, QTimer, QRectF, QPoint, QEasingCurve,
)
from PySide6.QtGui import (
    QPixmap, QPainter, QPainterPath, QColor, QPen, QLinearGradient,
)
from PySide6.QtWidgets import (
    QApplication, QFrame, QHBoxLayout, QLabel, QSizePolicy, QVBoxLayout,
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
from .controls import FloatingRewardLabel, RoundedButton, VolumeSlider
from .frames import NeonFrame
# Mantiene las importaciones históricas desde este módulo para compatibilidad.
from .scrolling import NeonMasterClock, NeonScrollBar, SmoothScrollArea


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
            bg_gradient.setColorAt(0.0, QColor(241, 243, 246, 245))
            bg_gradient.setColorAt(1.0, QColor(227, 232, 239, 240))

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
        self._imagen_fallo = False
        self._image_fallbacks = []
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
            txt_antes = "Antes" if obtener_idioma() == "es" else "Was"
            worth = QLabel(f"{txt_antes}: ${valor:,.2f}")
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
            c_top_r = int(250 - (prog * 5))
            c_top_g = int(249 - (prog * 5))
            c_top_b = int(246 - (prog * 4))
            c_bot_r = int(242 - (prog * 7))
            c_bot_g = int(240 - (prog * 7))
            c_bot_b = int(234 - (prog * 6))

        bg = QLinearGradient(0, 0, 0, self.height())
        bg.setColorAt(0.0, QColor(c_top_r, c_top_g, c_top_b))
        bg.setColorAt(1.0, QColor(c_bot_r, c_bot_g, c_bot_b))

        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(bg)
        p.drawRoundedRect(r, radius, radius)

        # 3. Borde reactivo orgánico (halo cian suave proporcional a la elevación)
        p.setBrush(Qt.BrushStyle.NoBrush)
        if prog > 0.05:
            c_neon = QColor(0, 243, 255, int(prog * 200)) if es_oscuro else QColor(95, 119, 170, int(prog * 100))
            p.setPen(QPen(c_neon, 1.2 + (prog * 0.6)))
        else:
            p.setPen(QPen(QColor(COLOR_BORDER if es_oscuro else "#CFD7E2"), 1.0))
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
            self._current_url = None
            self._imagen_fallo = True
            self._mostrar_placeholder_tienda()
            return

        self._current_url = url_img
        self._imagen_fallo = False
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
            if self._load_next_image_fallback():
                return
            self._imagen_fallo = True
            self._mostrar_placeholder_tienda()

    def _load_next_image_fallback(self):
        while self._image_fallbacks:
            fallback_url = self._image_fallbacks.pop(0)
            if fallback_url and fallback_url != getattr(self, "_current_url", None):
                self._load_image(fallback_url)
                return True
        return False

    def _traducir_descripcion(self):
        idioma = obtener_idioma()
        if not self._desc_original:
            return
        if idioma == "en":
            desc = " ".join(self._desc_original.split())
            if len(desc) > 148:
                desc = desc[:145] + "..."
            self._desc_label.setText(desc)
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

        # Steam solo aporta respaldos: no sustituir la imagen de la tienda
        # mientras sigue descargándose, porque el banner inferido puede ser 404.
        if not self._imagen_cargada_con_exito:
            candidatos = (datos.get("banner_url"), datos.get("fallback_image_url"))
            self._image_fallbacks = [
                url for url in candidatos
                if url and url != getattr(self, "_current_url", None)
            ]
            if self._imagen_fallo:
                self._load_next_image_fallback()

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

        self._steam_badge.setText(f"\u2605 Steam: {percent}% ({desc})")
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

