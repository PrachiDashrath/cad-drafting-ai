"""
curve_converter.py

Converts Open CASCADE edges into internal Geometry2D objects.
Version 1 supports straight lines only.
"""

from __future__ import annotations

from OCC.Core.BRepAdaptor import BRepAdaptor_Curve
from OCC.Core.GeomAbs import GeomAbs_Line
from OCC.Core.TopoDS import TopoDS_Edge

from app.projection.geometry2d import Line2D, Point2D


class CurveConverter:

    def convert(self, edge: TopoDS_Edge):

        curve = BRepAdaptor_Curve(edge)

        curve_type = curve.GetType()

        if curve_type == GeomAbs_Line:

            first = curve.FirstParameter()
            last = curve.LastParameter()

            p1 = curve.Value(first)
            p2 = curve.Value(last)

            return Line2D(
                start=Point2D(p1.X(), p1.Y()),
                end=Point2D(p2.X(), p2.Y()),
            )

        return None