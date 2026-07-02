"""
edge_classifier.py

Utilities for classifying projected edges.
Future versions will classify edges into visible, hidden,
silhouette, tangent, section, etc.
"""

from __future__ import annotations

from enum import Enum
from dataclasses import dataclass


class EdgeType(Enum):
    VISIBLE = "Visible"
    HIDDEN = "Hidden"
    SILHOUETTE = "Silhouette"
    TANGENT = "Tangent"
    SECTION = "Section"


@dataclass(slots=True)
class EdgeClassification:
    """
    Classification information attached to a projected edge.
    """

    edge_type: EdgeType
    line_weight: float = 0.25
    line_style: str = "Continuous"

    @property
    def is_hidden(self) -> bool:
        return self.edge_type == EdgeType.HIDDEN

    @property
    def is_visible(self) -> bool:
        return self.edge_type == EdgeType.VISIBLE