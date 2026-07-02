"""
edge_extractor.py

Extracts individual edges from a TopoDS_Compound.
"""

from __future__ import annotations

from typing import List

from OCC.Core.TopoDS import TopoDS_Compound, TopoDS_Edge
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.TopAbs import TopAbs_EDGE
from OCC.Core.TopoDS import topods


class EdgeExtractor:
    """
    Converts a TopoDS_Compound into a list of TopoDS_Edge objects.
    """

    def extract(self, compound: TopoDS_Compound) -> List[TopoDS_Edge]:

        edges = []

        explorer = TopExp_Explorer(compound, TopAbs_EDGE)

        while explorer.More():

            edge = topods.Edge(explorer.Current())

            edges.append(edge)

            explorer.Next()

        return edges