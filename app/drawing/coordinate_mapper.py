"""
coordinate_mapper.py

Maps engineering coordinates to screen coordinates.

Automatically:
- Computes drawing bounding box
- Scales to fit the widget
- Centers the drawing
- Keeps a margin
- Flips the Y-axis (CAD convention)
"""

from __future__ import annotations

from dataclasses import dataclass

from app.projection.geometry2d import Point2D, BoundingBox2D


@dataclass(slots=True)
class CoordinateMapper:

    margin: float = 30.0

    scale: float = 1.0

    offset_x: float = 0.0
    offset_y: float = 0.0

    # ---------------------------------------------------------

    def fit(
        self,
        bbox: BoundingBox2D,
        width: float,
        height: float,
    ) -> None:
        """
        Compute scale and translation so the drawing fits
        nicely inside the widget.
        """

        drawing_w = max(bbox.max_x - bbox.min_x, 1.0)
        drawing_h = max(bbox.max_y - bbox.min_y, 1.0)

        available_w = max(width - 2 * self.margin, 1.0)
        available_h = max(height - 2 * self.margin, 1.0)

        sx = available_w / drawing_w
        sy = available_h / drawing_h

        self.scale = min(sx, sy)

        self.offset_x = (
            (width - drawing_w * self.scale) / 2
            - bbox.min_x * self.scale
        )

        self.offset_y = (
            (height + drawing_h * self.scale) / 2
            + bbox.min_y * self.scale
        )

    # ---------------------------------------------------------

    def map(self, point: Point2D) -> tuple[float, float]:
        """
        Convert engineering coordinates to Qt screen coordinates.
        """

        x = self.offset_x + point.x * self.scale

        # Flip Y for Qt
        y = self.offset_y - point.y * self.scale

        return x, y