"""
drawing_widget.py
"""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPainter, QPen
from PySide6.QtWidgets import QWidget

from app.drawing.coordinate_mapper import CoordinateMapper
from app.drawing.drawing_sheet import DrawingSheet
from app.projection.geometry2d import Line2D


class DrawingWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setMinimumSize(500, 500)

        self.mapper = CoordinateMapper()

        self.sheet: DrawingSheet | None = None

    # ---------------------------------------------------------

    def set_drawing_sheet(self, sheet: DrawingSheet):

        self.sheet = sheet

        self.update()

    # ---------------------------------------------------------

    def paintEvent(self, event):

        painter = QPainter(self)

        painter.fillRect(self.rect(), QColor(35, 35, 35))

        if self.sheet is None:
            return

        #
        # Temporary:
        # draw only the front view from the sheet.
        #

        view = self.sheet.front

        if view is None:
            return

        if view.bounding_box is not None:

            self.mapper.fit(
                view.bounding_box,
                self.width(),
                self.height(),
            )

        #
        # Hidden lines
        #

        pen = QPen(QColor(150, 150, 150))
        pen.setStyle(Qt.DashLine)
        pen.setWidth(1)

        painter.setPen(pen)

        for entity in view.hidden_geometry:

            if not isinstance(entity, Line2D):
                continue

            x1, y1 = self.mapper.map(entity.start)
            x2, y2 = self.mapper.map(entity.end)

            painter.drawLine(x1, y1, x2, y2)

        #
        # Visible lines
        #

        pen = QPen(Qt.yellow)
        pen.setWidth(2)

        painter.setPen(pen)

        for entity in view.visible_geometry:

            if not isinstance(entity, Line2D):
                continue

            x1, y1 = self.mapper.map(entity.start)
            x2, y2 = self.mapper.map(entity.end)

            painter.drawLine(x1, y1, x2, y2)