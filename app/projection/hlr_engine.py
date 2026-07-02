"""
hlr_engine.py

Wrapper around Open CASCADE's Hidden Line Removal (HLR) algorithms.

This module converts a 3D TopoDS_Shape into a ProjectedView
containing visible and hidden 2D entities.

(Currently only the class skeleton is implemented.)
"""

from __future__ import annotations

from OCC.Core.TopoDS import TopoDS_Shape

from app.projection.projected_view import ProjectedView, ViewType


class HLREngine:
    """
    Hidden Line Removal engine.

    Future implementation will use:
    - HLRBRep_Algo
    - HLRAlgo_Projector
    """

    def __init__(self):
        pass

    def generate(
        self,
        shape: TopoDS_Shape,
        view_type: ViewType,
    ) -> ProjectedView:
        """
        Generate one projected engineering view.

        Parameters
        ----------
        shape
            OCC solid

        view_type
            Front / Top / Right / Isometric

        Returns
        -------
        ProjectedView
        """

        # Implementation comes in Sprint 2.5
        return ProjectedView(view_type=view_type)