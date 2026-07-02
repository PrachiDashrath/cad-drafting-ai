"""
projection_service.py

High-level service used by the GUI.

The GUI never talks directly to HLR or ProjectionEngine.
"""

from OCC.Core.TopoDS import TopoDS_Shape

from app.projection.projection_engine import ProjectionEngine
from app.projection.projected_view import ProjectedView


class ProjectionService:

    def __init__(self):

        self.engine = ProjectionEngine()

    def generate_front_view(
        self,
        shape: TopoDS_Shape,
    ) -> ProjectedView:

        return self.engine.front(shape)