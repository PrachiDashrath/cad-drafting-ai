"""
hlr_engine.py

Hidden Line Removal (HLR) engine.

This module wraps Open CASCADE's HLR algorithms and converts a
TopoDS_Shape into a ProjectedView.
"""

from __future__ import annotations

from OCC.Core.TopoDS import TopoDS_Shape

from app.projection.projected_view import (
    ProjectedView,
    ViewType,
)


class HLREngine:
    """
    Wrapper around Open CASCADE Hidden Line Removal.
    """

    def __init__(self):
        print("HLR Engine initialized")

    def generate(
        self,
        shape: TopoDS_Shape,
        view_type: ViewType,
    ) -> ProjectedView:

        print(f"Generating {view_type.value} projection...")

        view = ProjectedView(view_type=view_type)

        # Actual HLR implementation comes next sprint.

        return view