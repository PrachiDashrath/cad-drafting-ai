"""
drawing_sheet.py

Represents a complete engineering drawing sheet.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from app.projection.projected_view import ProjectedView


@dataclass(slots=True)
class DrawingSheet:
    """
    Container for all projected views that belong to
    one engineering drawing.
    """

    front: ProjectedView | None = None
    top: ProjectedView | None = None
    right: ProjectedView | None = None
    isometric: ProjectedView | None = None

    title: str = ""

    scale: float = 1.0

    units: str = "mm"

    views: list[ProjectedView] = field(default_factory=list)

    def add_view(self, view: ProjectedView):

        self.views.append(view)

    def clear(self):

        self.views.clear()

        self.front = None
        self.top = None
        self.right = None
        self.isometric = None