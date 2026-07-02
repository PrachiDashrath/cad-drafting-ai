"""
app/viewer/selection.py
SelectionManager stub.  Milestone 1 only detects click; sub-shape picking
will be added in a later milestone when feature recognition is integrated.
"""

from app.utils.logger import get_logger

log = get_logger(__name__)


class SelectionManager:
    """Manages interactive selection of faces, edges, and vertices."""

    def __init__(self, context=None):
        self._context = context

    def select_face(self)   -> None: log.debug("select_face()   — stub")
    def select_edge(self)   -> None: log.debug("select_edge()   — stub")
    def select_vertex(self) -> None: log.debug("select_vertex() — stub")

    def clear_selection(self) -> None:
        if self._context:
            self._context.ClearSelected(True)
        log.debug("Selection cleared")
