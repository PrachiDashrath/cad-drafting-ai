"""
app/core/document.py
CADDocument — central data model for a loaded CAD file.  Every module that
needs geometry or metadata reads from here instead of reloading the file.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


# ---------------------------------------------------------------------------
# Enumerations
# ---------------------------------------------------------------------------

class DisplayMode(Enum):
    WIREFRAME = 1
    SHADED    = 2
    SHADED_WITH_EDGES = 3


class ViewDirection(Enum):
    FRONT     = "front"
    BACK      = "back"
    TOP       = "top"
    BOTTOM    = "bottom"
    RIGHT     = "right"
    LEFT      = "left"
    ISO       = "iso"


# ---------------------------------------------------------------------------
# CADDocument
# ---------------------------------------------------------------------------

@dataclass
class CADDocument:
    """
    Central data model for one loaded CAD file.

    Milestone 1 populates: shape, filename, units, faces, edges, vertices,
    bounding_box, volume, surface_area.

    Later milestones will populate: projections, recognized_features,
    drawing_views, metadata.
    """

    # -- Geometry -----------------------------------------------------------
    shape: Any = None                         # OCC TopoDS_Shape
    filename: str = ""
    units: str = "mm"

    # -- Topology stats -----------------------------------------------------
    faces:    int = 0
    edges:    int = 0
    vertices: int = 0

    # -- Physical properties ------------------------------------------------
    bounding_box: Any = None                  # OCC Bnd_Box
    volume:        float = 0.0
    surface_area:  float = 0.0

    # -- Future milestones (pre-declared so data model is stable) -----------
    metadata:            dict[str, Any] = field(default_factory=dict)
    projections:         dict[str, Any] = field(default_factory=dict)
    recognized_features: list[Any]      = field(default_factory=list)
    drawing_views:       dict[str, Any] = field(default_factory=dict)

    # -- Convenience --------------------------------------------------------
    @property
    def is_loaded(self) -> bool:
        return self.shape is not None

    def summary(self) -> str:
        if not self.is_loaded:
            return "No model loaded"
        return (
            f"{self.filename}  |  "
            f"Faces: {self.faces}  Edges: {self.edges}  "
            f"Vertices: {self.vertices}  |  {self.units}"
        )
