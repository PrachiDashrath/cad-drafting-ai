"""
hlr_engine.py

Hidden Line Removal engine.

Generates ProjectedView objects from TopoDS_Shapes.
"""

from __future__ import annotations

from OCC.Core.HLRAlgo import HLRAlgo_Projector
from OCC.Core.HLRBRep import (
    HLRBRep_Algo,
    HLRBRep_HLRToShape,
)

from OCC.Core.gp import (
    gp_Ax2,
    gp_Dir,
    gp_Pnt,
)

from OCC.Core.TopoDS import TopoDS_Shape

from app.projection.edge_extractor import EdgeExtractor
from app.projection.curve_converter import CurveConverter
from app.projection.projected_view import (
    ProjectedView,
    ViewType,
)


class HLREngine:

    def __init__(self):

        self.extractor = EdgeExtractor()
        self.converter = CurveConverter()

    def generate(
        self,
        shape: TopoDS_Shape,
        view_type: ViewType,
    ) -> ProjectedView:

        projector = self._create_projector(view_type)

        algo = HLRBRep_Algo()

        algo.Add(shape)

        algo.Projector(projector)

        algo.Update()

        algo.Hide()

        hlr = HLRBRep_HLRToShape(algo)

        view = ProjectedView(view_type=view_type)

        # ---------- Visible Geometry ----------

        visible_edges = self.extractor.extract(
            hlr.VCompound()
        )

        for edge in visible_edges:

            geometry = self.converter.convert(edge)

            if geometry is not None:
                view.visible_geometry.append(geometry)

        # ---------- Hidden Geometry ----------

        hidden_edges = self.extractor.extract(
            hlr.HCompound()
        )

        for edge in hidden_edges:

            geometry = self.converter.convert(edge)

            if geometry is not None:
                view.hidden_geometry.append(geometry)

        return view

    def _create_projector(
        self,
        view_type: ViewType,
    ) -> HLRAlgo_Projector:

        directions = {
            ViewType.FRONT: (0, 0, 1),
            ViewType.TOP: (0, -1, 0),
            ViewType.RIGHT: (1, 0, 0),
            ViewType.ISOMETRIC: (1, 1, 1),
        }

        vx, vy, vz = directions[view_type]

        return HLRAlgo_Projector(
            gp_Ax2(
                gp_Pnt(0, 0, 0),
                gp_Dir(vx, vy, vz),
            )
        )