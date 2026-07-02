"""
projected_view.py

Represents a single 2D engineering drawing view generated from a
3D CAD model.

Examples:
- Front View
- Top View
- Right View
- Isometric View

Each view contains visible and hidden geometry that later modules
(DXF export, dimensions, drawing sheet) will use.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import List

from app.projection.geometry2d import (
    Line2D,
    Arc2D,
    Circle2D,
    BoundingBox2D,
)


class ViewType(Enum):
    FRONT = "Front"
    TOP = "Top"
    RIGHT = "Right"
    ISOMETRIC = "Isometric"


@dataclass(slots=True)
class ProjectedView:
    """
    Represents one projected engineering view.
    """

    view_type: ViewType

    visible_lines: List[Line2D] = field(default_factory=list)
    hidden_lines: List[Line2D] = field(default_factory=list)

    visible_arcs: List[Arc2D] = field(default_factory=list)
    hidden_arcs: List[Arc2D] = field(default_factory=list)

    circles: List[Circle2D] = field(default_factory=list)

    bounding_box: BoundingBox2D | None = None

    scale: float = 1.0

    origin_x: float = 0.0
    origin_y: float = 0.0

    @property
    def total_entities(self) -> int:
        return (
            len(self.visible_lines)
            + len(self.hidden_lines)
            + len(self.visible_arcs)
            + len(self.hidden_arcs)
            + len(self.circles)
        )

    def clear(self) -> None:
        """Remove all projected entities."""

        self.visible_lines.clear()
        self.hidden_lines.clear()
        self.visible_arcs.clear()
        self.hidden_arcs.clear()
        self.circles.clear()