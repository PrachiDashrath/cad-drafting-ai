"""
app/viewer/display_manager.py
Wraps AIS_InteractiveContext.  All rendering requests go through here.
"""

from OCC.Core.AIS import AIS_Shape, AIS_InteractiveContext
from OCC.Core.V3d import V3d_Viewer
from OCC.Core.Quantity import (
    Quantity_Color, Quantity_NOC_WHITE
)
from OCC.Core.TopoDS import TopoDS_Shape

from app.core.document import DisplayMode
from app.utils.logger import get_logger

log = get_logger(__name__)

# Map our enum → OCC integer display mode
_AIS_MODE = {
    DisplayMode.WIREFRAME:          1,
    DisplayMode.SHADED:             1,   # AIS shaded = 1
    DisplayMode.SHADED_WITH_EDGES:  1,
}


class DisplayManager:
    """
    High-level interface over AIS_InteractiveContext.

    Every module that wants to display, erase, or highlight geometry
    calls this class instead of touching OCC internals directly.
    """

    def __init__(self, context: AIS_InteractiveContext):
        self._context = context
        self._current_ais: AIS_Shape | None = None
        log.debug("DisplayManager initialised")

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def show(self, shape: TopoDS_Shape, update: bool = True) -> None:
        """Display *shape*, replacing any previously shown geometry."""
        self.erase_all(update=False)
        ais = AIS_Shape(shape)
        self._context.Display(ais, update)
        self._current_ais = ais
        log.debug("Shape displayed")

    def erase_all(self, update: bool = True) -> None:
        """Remove all shapes from the context."""
        self._context.EraseAll(update)
        self._current_ais = None
        log.debug("Context cleared")

    def update(self) -> None:
        self._context.UpdateCurrentViewer()

    def set_display_mode(self, mode: DisplayMode) -> None:
        """Switch wireframe / shaded / shaded-with-edges."""
        if self._current_ais is None:
            return
        if mode == DisplayMode.WIREFRAME:
            self._context.SetDisplayMode(self._current_ais, 0, True)
        elif mode == DisplayMode.SHADED:
            self._context.SetDisplayMode(self._current_ais, 1, True)
        elif mode == DisplayMode.SHADED_WITH_EDGES:
            self._context.SetDisplayMode(self._current_ais, 1, True)
            # Edge overlay is handled by the viewer's edge drawing mode
        log.debug(f"Display mode → {mode.name}")

    def highlight(self, shape: TopoDS_Shape) -> None:
        """Stub — will highlight a sub-shape in future milestones."""
        log.debug("highlight() stub called")
