import os

from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon, QPixmap, QColor, QPainter, QPen
from PySide6.QtWidgets import (
    QApplication, QFrame, QHBoxLayout, QLabel, QPushButton,
    QSizePolicy, QSlider, QVBoxLayout,
)

from config import (
    COLOR_BG_CARD, COLOR_HOVER, COLOR_BORDER, COLOR_ACCENT,
    COLOR_ACCENT_HOVER, COLOR_ACCENT_LIGHT, COLOR_SUCCESS,
    COLOR_SUCCESS_HOVER, COLOR_TEXT_PRIMARY,
)


class StoreWidget(QFrame):
    """Burbuja de tienda con la geometría visual de la versión Tk original."""

    def __init__(self, owner, store, icon_filename):
        super().__init__(owner.store_panel)
        self.owner = owner
        self.store = store
        self.setObjectName("storeBubble")
        self.setProperty("active", False)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFixedHeight(140)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(6, 10, 6, 12)
        layout.setSpacing(4)

        self.icon_box = QFrame()
        self.icon_box.setObjectName("storeIconBox")
        self.icon_box.setFixedSize(80, 80)
        icon_layout = QVBoxLayout(self.icon_box)
        icon_layout.setContentsMargins(0, 0, 0, 0)
        icon_layout.setSpacing(0)

        icon = QLabel()
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        path = owner._store_icon_path(icon_filename)
        pixmap = owner._load_store_icon(path, 64)
        if pixmap is not None:
            icon.setPixmap(pixmap)
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
        layout.addWidget(label)
        self.label = label

    def _refresh_state(self):
        for widget in (self, self.icon_box, self.label):
            widget.style().unpolish(widget)
            widget.style().polish(widget)

    def enterEvent(self, event):
        self.setProperty("hovering", True)
        self._refresh_state()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.setProperty("hovering", False)
        self._refresh_state()
        super().leaveEvent(event)

    def set_count(self, count):
        self.badge.setText(str(count))
        self.badge.setVisible(int(count) > 0)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.owner._toggle_tienda(self.store)
        super().mousePressEvent(event)

