"""
drawing_widget.py

Simple 2D engineering drawing viewer.
"""

from __future__ import annotations

from PySide6.QtCore import Qt

from PySide6.QtGui import (
    QColor,
    QPainter,
    QPen,
)

from PySide6.QtWidgets import QWidget

from app.drawing.coordinate_mapper import CoordinateMapper
from app.projection.geometry2d import Line2D
from app.projection.projected_view import ProjectedView


class DrawingWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setMinimumSize(500, 500)

        self.mapper = CoordinateMapper()

        self.view: ProjectedView | None = None

    # ---------------------------------------------------------

    def set_projected_view(self, view: ProjectedView):

        self.view = view

        self.update()

    # ---------------------------------------------------------

    def paintEvent(self, event):

        painter = QPainter(self)

        painter.fillRect(self.rect(), QColor(35, 35, 35))

        if self.view is None:
            return

        if self.view.bounding_box is not None:

            self.mapper.fit(
                self.view.bounding_box,
                self.width(),
                self.height(),
            )

        #
        # Hidden lines
        #

        hidden_pen = QPen(QColor(150, 150, 150))

        hidden_pen.setWidth(1)

        hidden_pen.setStyle(Qt.DashLine)

        painter.setPen(hidden_pen)

        for entity in self.view.hidden_geometry:

            if not isinstance(entity, Line2D):
                continue

            x1, y1 = self.mapper.map(entity.start)

            x2, y2 = self.mapper.map(entity.end)

            painter.drawLine(x1, y1, x2, y2)

        #
        # Visible lines
        #

        visible_pen = QPen(Qt.yellow)

        visible_pen.setWidth(2)

        painter.setPen(visible_pen)

        for entity in self.view.visible_geometry:

            if not isinstance(entity, Line2D):
                continue

            x1, y1 = self.mapper.map(entity.start)

            x2, y2 = self.mapper.map(entity.end)

            painter.drawLine(x1, y1, x2, y2)