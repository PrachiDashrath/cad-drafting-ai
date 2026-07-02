"""
coordinate_mapper.py

Maps engineering coordinates to screen coordinates.
"""

from dataclasses import dataclass

from app.projection.geometry2d import Point2D


@dataclass(slots=True)
class CoordinateMapper:
    scale: float = 8.0
    offset_x: float = 50.0
    offset_y: float = 50.0

    def map(self, point: Point2D) -> tuple[float, float]:
        """
        Convert engineering coordinates into Qt screen coordinates.
        """
        x = self.offset_x + point.x * self.scale

        # Qt Y-axis is inverted
        y = self.offset_y - point.y * self.scale

        return x, y