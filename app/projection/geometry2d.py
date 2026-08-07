"""
geometry2d.py

Internal 2D geometry primitives used throughout the CAD Drafting AI
pipeline.

These classes are intentionally independent of Open CASCADE.
Every module (projection, dimensions, exporters, drawing engine)
communicates using these objects.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import sqrt

class Geometry2D:
    """
    Base class for every 2D geometry entity.
    """

    pass
# ---------------------------------------------------------------------
# Basic Geometry
# ---------------------------------------------------------------------

@dataclass(slots=True)
class Point2D:
    x: float
    y: float

    def distance_to(self, other: "Point2D") -> float:
        """Return Euclidean distance to another point."""
        return sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)


@dataclass(slots=True)
class Line2D(Geometry2D):
    start: Point2D
    end: Point2D

    @property
    def length(self) -> float:
        return self.start.distance_to(self.end)


@dataclass(slots=True)
class Circle2D(Geometry2D):
    center: Point2D
    radius: float


@dataclass(slots=True)
class Arc2D(Geometry2D):
    center: Point2D
    radius: float
    start_angle: float
    end_angle: float


@dataclass(slots=True)
class BoundingBox2D:
    min_x: float
    min_y: float
    max_x: float
    max_y: float

    @property
    def width(self) -> float:
        return self.max_x - self.min_x

    @property
    def height(self) -> float:
        return self.max_y - self.min_y

    @property
    def center(self) -> Point2D:
        return Point2D(
            (self.min_x + self.max_x) / 2,
            (self.min_y + self.max_y) / 2,
        )