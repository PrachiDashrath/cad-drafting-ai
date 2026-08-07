"""
projection_service.py

High-level projection service.
"""

from OCC.Core.TopoDS import TopoDS_Shape

from app.drawing.drawing_sheet import DrawingSheet
from app.projection.projection_engine import ProjectionEngine


class ProjectionService:

    def __init__(self):

        self.engine = ProjectionEngine()

    # ---------------------------------------------------------

    def generate_sheet(
        self,
        shape: TopoDS_Shape,
    ) -> DrawingSheet:

        sheet = DrawingSheet()

        #
        # Generate views
        #

        sheet.front = self.engine.front(shape)
        sheet.top = self.engine.top(shape)
        sheet.right = self.engine.right(shape)
        sheet.isometric = self.engine.isometric(shape)

        #
        # Store all views
        #

        sheet.views = [
            sheet.front,
            sheet.top,
            sheet.right,
            sheet.isometric,
        ]

        return sheet

    # ---------------------------------------------------------

    def generate_front_view(
        self,
        shape: TopoDS_Shape,
    ):
        return self.engine.front(shape)