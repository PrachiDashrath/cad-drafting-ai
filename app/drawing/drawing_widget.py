"""
drawing_widget.py

Displays one or more projected engineering drawing views.
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

        self.sheet: DrawingSheet | None = None

    # ---------------------------------------------------------

    def set_drawing_sheet(self, sheet: DrawingSheet):

        self.sheet = sheet

        print("DrawingSheet received")

        if sheet is not None:
            print("Views:", len(sheet.views))

        self.update()

    # ---------------------------------------------------------

    def paintEvent(self, event):

        painter = QPainter(self)

        painter.fillRect(self.rect(), QColor(35, 35, 35))

        if self.sheet is None:
            return

        margin = 20

        w = self.width()
        h = self.height()

        #
        # Layout
        #

        self._draw_view(
            painter,
            self.sheet.front,
            margin,
            h // 2,
            w // 2 - 2 * margin,
            h // 2 - 2 * margin,
        )

        self._draw_view(
            painter,
            self.sheet.top,
            margin,
            margin,
            w // 2 - 2 * margin,
            h // 3,
        )

        self._draw_view(
            painter,
            self.sheet.right,
            w // 2,
            h // 2,
            w // 2 - 2 * margin,
            h // 2 - 2 * margin,
        )

        self._draw_view(
            painter,
            self.sheet.isometric,
            w // 2,
            margin,
            w // 2 - 2 * margin,
            h // 3,
        )

    # ---------------------------------------------------------

    def _draw_view(
        self,
        painter,
        view,
        x,
        y,
        width,
        height,
    ):

        if view is None:
            return

        if view.bounding_box is None:
            return

        mapper = CoordinateMapper()

        mapper.fit(
            view.bounding_box,
            width,
            height,
        )

        mapper.offset_x += x
        mapper.offset_y += y

        #
        # Hidden lines
        #

        hidden_pen = QPen(QColor(150, 150, 150))
        hidden_pen.setStyle(Qt.DashLine)
        hidden_pen.setWidth(1)

        painter.setPen(hidden_pen)

        for entity in view.hidden_geometry:

            if not isinstance(entity, Line2D):
                continue

            x1, y1 = mapper.map(entity.start)
            x2, y2 = mapper.map(entity.end)

            painter.drawLine(x1, y1, x2, y2)

        #
        # Visible lines
        #

        visible_pen = QPen(Qt.yellow)
        visible_pen.setWidth(2)

        painter.setPen(visible_pen)

        for entity in view.visible_geometry:

            if not isinstance(entity, Line2D):
                continue

            x1, y1 = mapper.map(entity.start)
            x2, y2 = mapper.map(entity.end)

            painter.drawLine(x1, y1, x2, y2)