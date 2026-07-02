"""
projection_engine.py

High-level interface for generating engineering drawing views.
"""

from __future__ import annotations

from OCC.Core.TopoDS import TopoDS_Shape

from app.projection.hlr_engine import HLREngine
from app.projection.projected_view import ProjectedView, ViewType


class ProjectionEngine:
    """Facade over the HLR engine."""

    def __init__(self):
        self._hlr = HLREngine()

    def front(self, shape: TopoDS_Shape) -> ProjectedView:
        return self._hlr.generate(shape, ViewType.FRONT)

    def top(self, shape: TopoDS_Shape) -> ProjectedView:
        return self._hlr.generate(shape, ViewType.TOP)

    def right(self, shape: TopoDS_Shape) -> ProjectedView:
        return self._hlr.generate(shape, ViewType.RIGHT)

    def isometric(self, shape: TopoDS_Shape) -> ProjectedView:
        return self._hlr.generate(shape, ViewType.ISOMETRIC)