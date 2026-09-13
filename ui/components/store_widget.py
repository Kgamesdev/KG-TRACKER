import os
from PySide6.QtCore import Qt, QSize, QVariantAnimation, QEasingCurve, QEvent
from PySide6.QtGui import QIcon, QPixmap, QPainter, QTransform
from PySide6.QtWidgets import (
    QApplication, QFrame, QHBoxLayout, QLabel, QPushButton,
    QSizePolicy, QVBoxLayout,
)

class StoreWidget(QFrame):
    """Burbuja de tienda con efecto Paper Tilt dinámico mediante Event Filter."""

    def __init__(self, owner, store, icon_filename):
        super().__init__(owner.store_panel)
        self.owner = owner
        self.store = store
        self.setObjectName("storeBubble")
        self.setProperty("active", False)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFixedHeight(140)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        
        self.setMouseTracking(True)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(6, 10, 6, 12)
        layout.setSpacing(4)

        self.icon_box = QFrame()
        self.icon_box.setObjectName("storeIconBox")
        self.icon_box.setFixedSize(80, 80)
        self.icon_box.setMouseTracking(True)
        
        icon_layout = QVBoxLayout(self.icon_box)
        icon_layout.setContentsMargins(0, 0, 0, 0)
        icon_layout.setSpacing(0)

        icon = QLabel()
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon.setMouseTracking(True)
        
        path = owner._store_icon_path(icon_filename)
        self._pixmap_base = owner._load_store_icon(path, 64)
        self._current_angle = 0.0

        if self._pixmap_base is not None:
            icon.setPixmap(self._pixmap_base)
        
        icon_layout.addWidget(icon)
        self.icon_label = icon

        layout.addWidget(self.icon_box, 0, Qt.AlignmentFlag.AlignHCenter)

        self.badge = QLabel("0", self.icon_box)
        self.badge.setObjectName("storeBadge")
        self.badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.badge.setGeometry(62, 6, 16, 16)
        self.badge.hide()

        label = QLabel(store)
        label.setObjectName("storeLabel")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setMouseTracking(True)
        layout.addWidget(label)
        self.label = label

        # Instalar filtro de eventos en los hijos para capturar el movimiento global
        self.icon_box.installEventFilter(self)
        self.icon_label.installEventFilter(self)
        self.label.installEventFilter(self)

        # Animación de retorno suave
        self._anim_reset = QVariantAnimation(self)
        self._anim_reset.setDuration(250)
        self._anim_reset.setEasingCurve(QEasingCurve.Type.OutCubic)
        self._anim_reset.valueChanged.connect(self._aplicar_transformacion)

    def eventFilter(self, obj, event):
        """Filtra eventos de los hijos para procesar el movimiento del ratón y la inclinación."""
        if event.type() == QEvent.Type.MouseMove:
            if self.property("hovering"):
                # Mapear la posición global del ratón a coordenadas locales del StoreWidget
                global_pos = event.globalPosition().toPoint() if hasattr(event, 'globalPosition') else event.globalPos()
                local_pos = self.mapFromGlobal(global_pos)

                centro_x = self.width() / 2
                offset_x = (local_pos.x() - centro_x) / centro_x
                offset_x = max(-1.0, min(1.0, offset_x))

                angulo_objetivo = offset_x * 14.0 # Inclinación máxima de 14 grados
                self._aplicar_transformacion(angulo_objetivo)

        elif event.type() == QEvent.Type.Enter:
            if not self.property("hovering"):
                self.setProperty("hovering", True)
                self._refresh_state()

        elif event.type() == QEvent.Type.Leave:
            # Comprobar si el ratón realmente salió del widget principal
            if not self.rect().contains(self.mapFromGlobal(QApplication.cursor().pos())):
                if self.property("hovering"):
                    self.setProperty("hovering", False)
                    self._refresh_state()
                    self._anim_reset.stop()
                    self._anim_reset.setStartValue(self._current_angle)
                    self._anim_reset.setEndValue(0.0)
                    self._anim_reset.start()

        return super().eventFilter(obj, event)

    def _aplicar_transformacion(self, angulo):
        self._current_angle = angulo
        if self._pixmap_base is not None and not self._pixmap_base.isNull():
            escala = 1.18 if self.property("hovering") else 1.0
            
            transform = QTransform()
            transform.scale(escala, escala)
            transform.rotate(angulo)
            
            pixmap_transformado = self._pixmap_base.transformed(
                transform,
                Qt.TransformationMode.SmoothTransformation
            )
            self.icon_label.setPixmap(pixmap_transformado)

    def mouseMoveEvent(self, event):
        global_pos = event.globalPosition().toPoint() if hasattr(event, 'globalPosition') else event.globalPos()
        local_pos = self.mapFromGlobal(global_pos)
        centro_x = self.width() / 2
        offset_x = (local_pos.x() - centro_x) / centro_x
        offset_x = max(-1.0, min(1.0, offset_x))
        self._aplicar_transformacion(offset_x * 14.0)
        super().mouseMoveEvent(event)

    def enterEvent(self, event):
        self.setProperty("hovering", True)
        self._refresh_state()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.setProperty("hovering", False)
        self._refresh_state()
        self._anim_reset.stop()
        self._anim_reset.setStartValue(self._current_angle)
        self._anim_reset.setEndValue(0.0)
        self._anim_reset.start()
        super().leaveEvent(event)

    def _refresh_state(self):
        for widget in (self, self.icon_box, self.label):
            widget.style().unpolish(widget)
            widget.style().polish(widget)

    def set_count(self, count):
        self.badge.setText(str(count))
        self.badge.setVisible(int(count) > 0)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.owner._toggle_tienda(self.store)
        super().mousePressEvent(event)
