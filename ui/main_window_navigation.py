"""Interacción y navegación de la ventana principal."""

from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QSize
from PySide6.QtGui import QIcon, QPixmap, QColor, QPainter, QPen
from PySide6.QtWidgets import QApplication, QSizePolicy


def _crear_icono_seleccion(self, seleccionar_todas):
    """Crea un icono compacto para seleccionar o deseleccionar todas."""
    pixmap = QPixmap(28, 28)
    pixmap.fill(Qt.GlobalColor.transparent)

    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)

    if seleccionar_todas:
        color = QColor("#00F3FF")
        marcar = True
    else:
        color = QColor("#FF0055")
        marcar = False

    pen = QPen(color, 2)
    pen.setCapStyle(Qt.PenCapStyle.RoundCap)
    pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
    painter.setPen(pen)
    painter.setBrush(Qt.BrushStyle.NoBrush)

    for y in (5, 13, 21):
        painter.drawRect(3, y - 2, 6, 6)
        painter.drawLine(12, y + 1, 24, y + 1)
        if marcar:
            painter.drawLine(4, y + 1, 6, y + 3)
            painter.drawLine(6, y + 3, 9, y - 1)
        else:
            painter.drawLine(14, y - 2, 19, y + 3)
            painter.drawLine(19, y - 2, 14, y + 3)

    painter.end()
    return QIcon(pixmap)



def _ajustar_ventana_por_estado(self, expandida):
    """Expande la zona de juegos al 80% (640px de alto máximo) manteniendo la ventana fija en su lugar."""
    content_layout = self.content.layout()
    
    ancho_actual = self.width()
    alto_objetivo = 640 if expandida else 360
    ancho_objetivo = max(ancho_actual, 1120)

    if expandida:
        self.setMinimumSize(980, 540)
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
        self._anim_ventana.setDuration(260)
        self._anim_ventana.setStartValue(QSize(ancho_actual, self.height()))
        self._anim_ventana.setEndValue(QSize(ancho_objetivo, alto_objetivo))
        self._anim_ventana.setEasingCurve(QEasingCurve.Type.OutCubic)
        self._anim_ventana.start()
    else:
        self.resize(ancho_objetivo, alto_objetivo)



def _actualizar_visibilidad_atras(self):
    """Muestra Atrás solo cuando existe un estado que realmente se puede deshacer."""
    hay_filtros = any(self.active_filters.values())
    hay_todas = bool(self.todas_activado)
    hay_reclamados = bool(self.mostrando_reclamados)
    hay_estado = hay_filtros or hay_todas or hay_reclamados

    self.btn_side_todas.setVisible(hay_estado)
    self.btn_side_back.setVisible(hay_estado)

    self._ajustar_ventana_por_estado(hay_estado)



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
            self.btn_side_todas.setToolTip("Seleccionar todas")
        else:
            for s in self.active_filters:
                self.active_filters[s] = True
                self.acordeon_estados[s] = True
            self.todas_activado = True
            self.btn_side_todas.setIcon(self._crear_icono_seleccion(False))
            self.btn_side_todas.setToolTip("Deseleccionar todas")
        self._sync_store_states()
        self._actualizar_vista_juegos()
        self._actualizar_visibilidad_atras()
    finally:
        if root is not None:
            root.setUpdatesEnabled(True)
            root.update()



def _toggle_tienda(self, store):
    root = self.centralWidget()
    if root is not None:
        root.setUpdatesEnabled(False)
    try:
        if self.todas_activado:
            self.todas_activado = False
            self.btn_side_todas.setIcon(self._crear_icono_seleccion(True))
            self.btn_side_todas.setToolTip("Seleccionar todas")

        if self.active_filters[store]:
            self.active_filters[store] = False
            if store in self.acordeon_estados:
                self.acordeon_estados[store] = False
        else:
            for s in self.active_filters:
                self.active_filters[s] = False
            self.active_filters[store] = True
            self.acordeon_estados[store] = True

        self._sync_store_states()
        self._actualizar_vista_juegos()
        self._actualizar_visibilidad_atras()
    finally:
        if root is not None:
            root.setUpdatesEnabled(True)
            root.update()



def volver_atras(self):
    self.mostrando_reclamados = False
    self.btn_reclamados.setText("★ RECLAMADOS")
    self.btn_reclamados.setProperty("role", "secondary")
    self.btn_reclamados.style().unpolish(self.btn_reclamados)
    self.btn_reclamados.style().polish(self.btn_reclamados)

    for s in self.active_filters:
        self.active_filters[s] = False
    self.tienda_seleccionada = None
    self.todas_activado = False
    self.btn_side_todas.setIcon(self._crear_icono_seleccion(True))
    self.btn_side_todas.setToolTip("Seleccionar todas")
    self.btn_side_todas.hide()
    self._sync_store_states()

    self.juegos_cache_global = []
    self._actualizar_visibilidad_atras()
    self._actualizar_vista_juegos()
    self._set_status("● LISTO", "success")



def resetear_app(self):
    self.volver_atras()
    self.repaint()



def instalar_metodos(cls):

    cls._crear_icono_seleccion = _crear_icono_seleccion

    cls._ajustar_ventana_por_estado = _ajustar_ventana_por_estado

    cls._actualizar_visibilidad_atras = _actualizar_visibilidad_atras

    cls.toggle_todas = toggle_todas

    cls._toggle_tienda = _toggle_tienda

    cls.volver_atras = volver_atras

    cls.resetear_app = resetear_app
