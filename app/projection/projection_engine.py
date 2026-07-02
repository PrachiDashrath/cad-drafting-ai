"""
projection_engine.py

High-level projection engine.

This class coordinates the entire projection pipeline:

STEP Shape
    ↓
HLR
    ↓
Edge Extraction
    ↓
Curve Conversion
    ↓
ProjectedView
"""

from OCC.Core.TopoDS import TopoDS_Shape

from app.projection.hlr_engine import HLREngine
from app.projection.edge_extractor import EdgeExtractor
from app.projection.curve_converter import CurveConverter
from app.projection.projected_view import (
    ProjectedView,
    ViewType,
)


class ProjectionEngine:

    def __init__(self):

        self.hlr = HLREngine()
        self.extractor = EdgeExtractor()
        self.converter = CurveConverter()

    def front(self, shape: TopoDS_Shape):

        return self._generate(shape, ViewType.FRONT)

    def top(self, shape: TopoDS_Shape):

        return self._generate(shape, ViewType.TOP)

    def right(self, shape: TopoDS_Shape):

        return self._generate(shape, ViewType.RIGHT)

    def isometric(self, shape: TopoDS_Shape):

        return self._generate(shape, ViewType.ISOMETRIC)

    def _generate(self, shape, view_type):

        view = self.hlr.generate(shape, view_type)

        return view