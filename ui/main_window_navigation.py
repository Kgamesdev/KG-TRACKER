import config
from core.i18n import t
"""Interacción y navegación de la ventana principal."""

from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QSize
from PySide6.QtGui import QIcon, QPixmap, QColor, QPainter, QPen, QBrush, QLinearGradient
from PySide6.QtWidgets import QApplication, QSizePolicy


def _crear_icono_seleccion(self, seleccionar_todas):
    """Dibuja un grupo de tiendas con un indicador claro de seleccionar/quitar."""
    pixmap = QPixmap(32, 32)
    pixmap.fill(Qt.GlobalColor.transparent)

    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)

    es_claro = config.CURRENT_THEME == "light"
    inicio = QColor("#536B9D" if es_claro else "#00F3FF")
    fin = QColor("#8A72D6" if es_claro else "#C45BFF")
    gradiente = QLinearGradient(4, 4, 27, 27)
    gradiente.setColorAt(0.0, inicio)
    gradiente.setColorAt(1.0, fin)

    # Cuatro pequeñas tarjetas representan el conjunto de tiendas, en línea
    # con el estilo luminoso de los iconos de la aplicación.
    painter.setBrush(Qt.BrushStyle.NoBrush)
    for x, y in ((3, 4), (14, 4), (3, 15), (14, 15)):
        glow = QPen(QColor(inicio.red(), inicio.green(), inicio.blue(), 48), 4.2)
        painter.setPen(glow)
        painter.drawRoundedRect(x, y, 9, 8, 2.5, 2.5)
        outline = QPen(QBrush(gradiente), 1.5)
        outline.setCapStyle(Qt.PenCapStyle.RoundCap)
        outline.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
        painter.setPen(outline)
        painter.drawRoundedRect(x, y, 9, 8, 2.5, 2.5)
        painter.setPen(QPen(QBrush(gradiente), 1.1))
        painter.drawLine(x + 2, y + 5.5, x + 7, y + 5.5)

    # El distintivo indica la acción disponible: añadir todas o quitar todas.
    badge_fill = QColor(config.THEMES[config.CURRENT_THEME]["COLOR_BG_CARD"])
    painter.setBrush(badge_fill)
    painter.setPen(QPen(QColor(inicio.red(), inicio.green(), inicio.blue(), 60), 4))
    painter.drawEllipse(17, 17, 13, 13)
    painter.setPen(QPen(QBrush(gradiente), 1.5))
    painter.drawEllipse(17, 17, 13, 13)
    painter.setPen(QPen(QBrush(gradiente), 1.8, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
    painter.drawLine(20.5, 23.5, 26.5, 23.5)
    if seleccionar_todas:
        painter.drawLine(23.5, 20.5, 23.5, 26.5)

    painter.end()
    return QIcon(pixmap)


def _ajustar_ventana_por_estado(self, expandida):
    """Expande la zona de juegos manteniendo la ventana fija en su lugar."""
    content_layout = self.content.layout()
    ancho_actual = self.width()

    # Ajuste fino: 675px (un 5% menos respecto a 710px) para un equilibrio visual exacto
    alto_objetivo = 675 if expandida else 360
    ancho_objetivo = max(ancho_actual, 1120)

    if expandida:
        self.setMinimumSize(980, 560)
        self.container.show()
        content_layout.setStretch(4, 1)
        self.content.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
    else:
        self.setMinimumSize(980, 360)
        content_layout.setStretch(4, 0)
        self.container.hide()
        self.content.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    if self.isVisible():
        if hasattr(self, "_anim_ventana") and self._anim_ventana.state() == QPropertyAnimation.State.Running:
            self._anim_ventana.stop()

        self._anim_ventana = QPropertyAnimation(self, b"size")
        self._anim_ventana.setDuration(440)
        self._anim_ventana.setStartValue(QSize(ancho_actual, self.height()))
        self._anim_ventana.setEndValue(QSize(ancho_objetivo, alto_objetivo))
        self._anim_ventana.setEasingCurve(QEasingCurve.Type.OutCubic)
        self._anim_ventana.start()
    else:
        self.resize(ancho_objetivo, alto_objetivo)


def _actualizar_visibilidad_atras(self):
    """Muestra Atrás solo cuando existe un estado que realmente se puede deshacer."""
    _actualizar_visibilidad_boton_busqueda(self)
    if getattr(self, "mostrando_wishlist", False):
        self.btn_side_todas.hide()
        self.btn_side_back.setVisible(True)
        self._ajustar_ventana_por_estado(True)
        return

    hay_filtros = any(self.active_filters.values())
    hay_todas = bool(self.todas_activado)
    hay_reclamados = bool(self.mostrando_reclamados)
    if hay_reclamados:
        self.btn_side_todas.setVisible(True)
        self.btn_side_back.setVisible(True)
        self._ajustar_ventana_por_estado(True)
        return
    hay_estado = hay_filtros or hay_todas
    self.btn_side_todas.setVisible(hay_estado)
    self.btn_side_back.setVisible(hay_estado)
    self._ajustar_ventana_por_estado(hay_estado)


def _actualizar_visibilidad_boton_busqueda(self):
    """Oculta la búsqueda global mientras hay una tienda concreta abierta."""
    hay_tienda_abierta = any(getattr(self, "active_filters", {}).values())
    mostrar = not hay_tienda_abierta and not getattr(self, "mostrando_wishlist", False)
    self.btn_actualizar.setVisible(mostrar)


def toggle_todas(self):
    root = self.centralWidget()
    if root is not None:
        root.setUpdatesEnabled(False)
    try:
        if self.todas_activado:
            for s in self.active_filters:
                self.active_filters[s] = False
            self.todas_activado = False
            self.btn_side_todas.setIcon(self._crear_icono_seleccion(True))
            self.btn_side_todas.setToolTip(t("sidebar.select_all"))
        else:
            for s in self.active_filters:
                self.active_filters[s] = True
            self.todas_activado = True
            self.btn_side_todas.setIcon(self._crear_icono_seleccion(False))
            self.btn_side_todas.setToolTip(t("sidebar.deselect_all"))
        self._sync_store_states()
        self._actualizar_vista_juegos()
        self._actualizar_visibilidad_atras()
    finally:
        if root is not None:
            root.setUpdatesEnabled(True)
            root.update()


def _toggle_tienda(self, store):
    if getattr(self, "mostrando_wishlist", False):
        self.alternar_wishlist()
    root = self.centralWidget()
    if root is not None:
        root.setUpdatesEnabled(False)
    try:
        if self.todas_activado:
            self.todas_activado = False
            self.btn_side_todas.setIcon(self._crear_icono_seleccion(True))
            self.btn_side_todas.setToolTip(t("sidebar.select_all"))

        if self.active_filters[store]:
            self.active_filters[store] = False
        else:
            for s in self.active_filters:
                self.active_filters[s] = False
            self.active_filters[store] = True

        self._sync_store_states()
        self._actualizar_vista_juegos()
        self._actualizar_visibilidad_atras()
    finally:
        if root is not None:
            root.setUpdatesEnabled(True)
            root.update()


def volver_atras(self):
    if getattr(self, "mostrando_wishlist", False):
        self.alternar_wishlist()
        self._set_status(t("status.ready"), "success")
        return
    self.mostrando_reclamados = False
    self.btn_reclamados.setText(t("claimed.btn"))
    self.btn_reclamados.setProperty("role", "secondary")
    self.btn_reclamados.style().unpolish(self.btn_reclamados)
    self.btn_reclamados.style().polish(self.btn_reclamados)

    for s in self.active_filters:
        self.active_filters[s] = False
    self.tienda_seleccionada = None
    self.todas_activado = False
    self.btn_side_todas.setIcon(self._crear_icono_seleccion(True))
    self.btn_side_todas.setToolTip(t("sidebar.select_all"))
    self.btn_side_todas.hide()
    self._sync_store_states()

    # Mantener las ofertas ya cargadas al cerrar una tienda. La vista se
    # oculta, pero los datos deben seguir disponibles para la siguiente
    # apertura sin obligar a ejecutar otra búsqueda.
    self._actualizar_visibilidad_atras()
    self._actualizar_vista_juegos()
    self._set_status(t("status.ready"), "success")


def resetear_app(self):
    self.volver_atras()
    self.repaint()


def instalar_metodos(cls):
    cls._crear_icono_seleccion = _crear_icono_seleccion
    cls._ajustar_ventana_por_estado = _ajustar_ventana_por_estado
    cls._actualizar_visibilidad_atras = _actualizar_visibilidad_atras
    cls._actualizar_visibilidad_boton_busqueda = _actualizar_visibilidad_boton_busqueda
    cls.toggle_todas = toggle_todas
    cls._toggle_tienda = _toggle_tienda
    cls.volver_atras = volver_atras
    cls.resetear_app = resetear_app
