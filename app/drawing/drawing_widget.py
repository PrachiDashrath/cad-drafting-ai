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
from app.drawing.layout_engine import LayoutEngine
from app.projection.geometry2d import Line2D


class DrawingWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setMinimumSize(500, 500)

        self.sheet: DrawingSheet | None = None

        self.layout_engine = LayoutEngine()

    # ---------------------------------------------------------

    def set_drawing_sheet(self, sheet: DrawingSheet):

        self.sheet = sheet
        self.update()

    # ---------------------------------------------------------

    def paintEvent(self, event):

        painter = QPainter(self)

        painter.fillRect(self.rect(), QColor(35, 35, 35))

        #
        # Sheet
        #

        sheet_margin = 20

        sheet_x = sheet_margin
        sheet_y = sheet_margin

        sheet_w = self.width() - 2 * sheet_margin
        sheet_h = self.height() - 2 * sheet_margin

        painter.setPen(QPen(Qt.white, 2))
        painter.drawRect(sheet_x, sheet_y, sheet_w, sheet_h)

        #
        # Title block
        #

        title_h = 90

        painter.drawLine(
            sheet_x,
            sheet_y + sheet_h - title_h,
            sheet_x + sheet_w,
            sheet_y + sheet_h - title_h,
        )

        painter.drawLine(
            sheet_x + sheet_w - 220,
            sheet_y + sheet_h - title_h,
            sheet_x + sheet_w - 220,
            sheet_y + sheet_h,
        )

        if self.sheet is None:
            return

        #
        # Automatic layout
        #

        layout = self.layout_engine.generate(
            self.sheet,
            sheet_w,
            sheet_h - title_h,
        )

        #
        # Draw all views
        #

        self._draw_view(
            painter,
            self.sheet.top,
            layout["top"].x + sheet_x,
            layout["top"].y + sheet_y,
            layout["top"].width,
            layout["top"].height,
        )

        self._draw_view(
            painter,
            self.sheet.front,
            layout["front"].x + sheet_x,
            layout["front"].y + sheet_y,
            layout["front"].width,
            layout["front"].height,
        )

        self._draw_view(
            painter,
            self.sheet.right,
            layout["right"].x + sheet_x,
            layout["right"].y + sheet_y,
            layout["right"].width,
            layout["right"].height,
        )

        self._draw_view(
            painter,
            self.sheet.isometric,
            layout["isometric"].x + sheet_x,
            layout["isometric"].y + sheet_y,
            layout["isometric"].width,
            layout["isometric"].height,
        )

        #
        # Labels
        #

        painter.setPen(Qt.white)

        painter.drawText(
            layout["top"].x + sheet_x + 10,
            layout["top"].y + sheet_y - 5,
            "TOP",
        )

        painter.drawText(
            layout["front"].x + sheet_x + 10,
            layout["front"].y + sheet_y - 5,
            "FRONT",
        )

        painter.drawText(
            layout["right"].x + sheet_x + 10,
            layout["right"].y + sheet_y - 5,
            "RIGHT",
        )

        painter.drawText(
            layout["isometric"].x + sheet_x + 10,
            layout["isometric"].y + sheet_y - 5,
            "ISOMETRIC",
        )

        #
        # Title block
        #

        painter.drawText(
            sheet_x + 20,
            sheet_y + sheet_h - 55,
            f"Units : {self.sheet.units}",
        )

        painter.drawText(
            sheet_x + 20,
            sheet_y + sheet_h - 30,
            f"Scale : {self.sheet.scale}",
        )

        painter.drawText(
            sheet_x + sheet_w - 200,
            sheet_y + sheet_h - 55,
            "CAD Drafting AI",
        )

        painter.drawText(
            sheet_x + sheet_w - 200,
            sheet_y + sheet_h - 30,
            "Sheet : A3",
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

            if isinstance(entity, Line2D):

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

            if isinstance(entity, Line2D):

                x1, y1 = mapper.map(entity.start)
                x2, y2 = mapper.map(entity.end)

                painter.drawLine(x1, y1, x2, y2)