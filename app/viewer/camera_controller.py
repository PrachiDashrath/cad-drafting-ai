"""
app/viewer/camera_controller.py
Camera operations on an OCC V3d_View.
"""

from OCC.Core.V3d import V3d_View
from OCC.Core.gp import gp_Dir, gp_Ax3, gp_Pnt

from app.core.document import ViewDirection
from app.utils.logger import get_logger

log = get_logger(__name__)

# Projection vectors for each standard view
_VIEW_DIRS = {
    ViewDirection.FRONT:  gp_Dir( 0,  1,  0),
    ViewDirection.BACK:   gp_Dir( 0, -1,  0),
    ViewDirection.TOP:    gp_Dir( 0,  0, -1),
    ViewDirection.BOTTOM: gp_Dir( 0,  0,  1),
    ViewDirection.RIGHT:  gp_Dir(-1,  0,  0),
    ViewDirection.LEFT:   gp_Dir( 1,  0,  0),
    ViewDirection.ISO:    gp_Dir(-1, -1, -1),
}

_VIEW_UP = {
    ViewDirection.FRONT:  gp_Dir(0, 0, 1),
    ViewDirection.BACK:   gp_Dir(0, 0, 1),
    ViewDirection.TOP:    gp_Dir(0, 1, 0),
    ViewDirection.BOTTOM: gp_Dir(0, 1, 0),
    ViewDirection.RIGHT:  gp_Dir(0, 0, 1),
    ViewDirection.LEFT:   gp_Dir(0, 0, 1),
    ViewDirection.ISO:    gp_Dir( 0,  0,  1),
}


class CameraController:
    """Controls camera orientation and zoom for a V3d_View."""

    def __init__(self, view: V3d_View):
        self._view = view
        log.debug("CameraController initialised")

    # ------------------------------------------------------------------
    def fit_all(self) -> None:
        self._view.FitAll()
        self._view.ZFitAll()
        self._view.Redraw()
        log.debug("Camera: FitAll")

    def set_view(self, direction: ViewDirection) -> None:
        d = _VIEW_DIRS[direction]
        u = _VIEW_UP[direction]
        self._view.SetProj(d.X(), d.Y(), d.Z())
        self._view.SetUp(u.X(), u.Y(), u.Z())
        self._view.FitAll()
        self._view.Redraw()
        log.debug(f"Camera: {direction.name}")

    def front(self)  -> None: self.set_view(ViewDirection.FRONT)
    def back(self)   -> None: self.set_view(ViewDirection.BACK)
    def top(self)    -> None: self.set_view(ViewDirection.TOP)
    def bottom(self) -> None: self.set_view(ViewDirection.BOTTOM)
    def right(self)  -> None: self.set_view(ViewDirection.RIGHT)
    def left(self)   -> None: self.set_view(ViewDirection.LEFT)
    def iso(self)    -> None: self.set_view(ViewDirection.ISO)

    def zoom_in(self)  -> None:
        self._view.SetScale(self._view.Scale() * 1.2)
        self._view.Redraw()

    def zoom_out(self) -> None:
        self._view.SetScale(self._view.Scale() / 1.2)
        self._view.Redraw()

    def reset(self) -> None:
        self.iso()
