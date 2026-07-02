"""
app/gui/occ_viewer.py

PySide6 wrapper around the Open CASCADE qtViewer3d widget.

Responsibilities:
- Initialize the OCC Qt backend
- Display 3D CAD models
- Expose a simple API for DisplayManager and CameraController
- Forward mouse movement for future status bar updates
"""

from PySide6.QtCore import Signal, QSize
from PySide6.QtGui import QMouseEvent

from OCC.Display.backend import load_backend

# IMPORTANT:
# Must be called BEFORE importing qtDisplay.
load_backend("pyside6")

from OCC.Display.qtDisplay import qtViewer3d

from app.core.document import DisplayMode
from app.utils.logger import get_logger

log = get_logger(__name__)


class OccViewer(qtViewer3d):
    """
    Wrapper around pythonOCC's qtViewer3d.

    qtViewer3d already provides:
    - V3d_Viewer
    - V3d_View
    - AIS_InteractiveContext
    - Mouse orbit / pan / zoom
    - Resize handling

    This class exposes a cleaner interface for the rest of the application.
    """

    # Emits current mouse position (screen coordinates)
    mouse_moved = Signal(float, float)

    def __init__(self, parent=None):
        super().__init__(parent)

        self._display_mode = DisplayMode.SHADED_WITH_EDGES

        log.debug("OccViewer initialized.")

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def display_shape(self, shape, update: bool = True) -> None:
        """Display a TopoDS_Shape."""
        self._display.DisplayShape(shape, update=update)

    def erase_all(self) -> None:
        """Remove all displayed shapes."""
        self._display.EraseAll()
        self._display.Repaint()

    def fit_all(self) -> None:
        """Fit the entire model inside the viewport."""
        self._display.FitAll()

    def set_view_direction(
        self,
        vx: float,
        vy: float,
        vz: float,
        ux: float = 0,
        uy: float = 0,
        uz: float = 1,
    ) -> None:
        """Set camera projection direction."""

        view = self._display.View

        view.SetProj(vx, vy, vz)
        view.SetUp(ux, uy, uz)
        view.FitAll()
        view.Redraw()

    def set_display_mode(self, mode: DisplayMode) -> None:
        """Switch between shaded and wireframe display."""

        self._display_mode = mode

        if mode == DisplayMode.WIREFRAME:
            self._display.SetModeWireFrame()
        else:
            self._display.SetModeShaded()

        log.debug(f"Display mode changed to {mode.name}")

    @property
    def occ_display(self):
        """Return the underlying OCC display object."""
        return self._display

    # ------------------------------------------------------------------
    # Qt Events
    # ------------------------------------------------------------------

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        """
        Forward mouse movement.

        Currently emits screen coordinates.
        Later milestones will emit world coordinates.
        """
        super().mouseMoveEvent(event)

        self.mouse_moved.emit(
            float(event.position().x()),
            float(event.position().y()),
        )

    def sizeHint(self) -> QSize:
        """Preferred initial viewer size."""
        return QSize(900, 600)