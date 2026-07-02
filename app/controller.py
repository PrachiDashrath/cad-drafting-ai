"""
app/controller.py
ApplicationController.  Owns the application workflow: file loading,
screenshot saving, camera operations, display mode changes.

MainWindow owns the UI; this class owns the logic.
"""

import os
from PySide6.QtWidgets import QFileDialog, QMessageBox
from PySide6.QtCore import QObject

from app.viewer.step_loader import StepLoader
from app.viewer.display_manager import DisplayManager
from app.viewer.camera_controller import CameraController
from app.viewer.selection import SelectionManager
from app.core.document import CADDocument, DisplayMode
from app.config import STEP_FILTER, DEFAULT_DISPLAY_MODE
from app.utils.logger import get_logger

log = get_logger(__name__)


class ApplicationController(QObject):
    """
    Coordinates the application workflow.

    Flow for loading a file:
        open_file()
          → MainWindow.on_loading()
          → StepLoader.load()
            → StepLoader.document_loaded (Signal)
              → _on_document_loaded()
                → DisplayManager.show()
                → CameraController.fit_all()
                → MainWindow.on_document_loaded()
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self._window       = None   # set in set_window()
        self._doc: CADDocument | None = None

        # Viewer-layer services (populated in set_window once viewer exists)
        self._loader   : StepLoader        | None = None
        self._display  : DisplayManager    | None = None
        self._camera   : CameraController  | None = None
        self._selection: SelectionManager  | None = None

    # ------------------------------------------------------------------
    def set_window(self, window) -> None:
        """Call after MainWindow is constructed — wires up the viewer services."""
        from app.gui.main_window import MainWindow
        self._window = window

        display_obj = window.viewer.occ_display

        self._display   = DisplayManager(display_obj.Context)
        self._camera    = CameraController(display_obj.View)
        self._selection = SelectionManager(display_obj.Context)

        self._loader = StepLoader(self)
        self._loader.document_loaded.connect(self._on_document_loaded)
        self._loader.load_failed.connect(self._on_load_failed)

        log.info("ApplicationController wired to MainWindow")

    # ------------------------------------------------------------------
    # --- File actions --------------------------------------------------
    # ------------------------------------------------------------------

    def open_file(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self._window, "Open STEP File", "",
            STEP_FILTER,
        )
        if not path:
            return
        self._window.on_loading(os.path.basename(path))
        self._loader.load(path)

    def save_screenshot(self) -> None:
        path, _ = QFileDialog.getSaveFileName(
            self._window, "Save Screenshot", "screenshot.png",
            "PNG Images (*.png);;All Files (*)"
        )
        if not path:
            return
        self._window.viewer.occ_display.View.Dump(path)
        log.info(f"Screenshot saved: {path}")

    # ------------------------------------------------------------------
    # --- Camera actions ------------------------------------------------
    # ------------------------------------------------------------------

    def fit_all(self)    -> None: self._camera and self._camera.fit_all()
    def view_front(self) -> None: self._camera and self._camera.front()
    def view_top(self)   -> None: self._camera and self._camera.top()
    def view_right(self) -> None: self._camera and self._camera.right()
    def view_iso(self)   -> None: self._camera and self._camera.iso()

    # ------------------------------------------------------------------
    # --- Display mode --------------------------------------------------
    # ------------------------------------------------------------------

    def set_wireframe(self) -> None:
        self._display and self._display.set_display_mode(DisplayMode.WIREFRAME)
        self._window.viewer.set_display_mode(DisplayMode.WIREFRAME)

    def set_shaded(self) -> None:
        self._display and self._display.set_display_mode(DisplayMode.SHADED_WITH_EDGES)
        self._window.viewer.set_display_mode(DisplayMode.SHADED_WITH_EDGES)

    # ------------------------------------------------------------------
    # --- Signal handlers -----------------------------------------------
    # ------------------------------------------------------------------

    def _on_document_loaded(self, doc: CADDocument) -> None:
        self._doc = doc
        # Replace previously shown geometry cleanly
        self._window.viewer.erase_all()
        self._window.viewer.display_shape(doc.shape)
        self._camera.fit_all()
        self._window.on_document_loaded(doc)
        log.info(f"Model loaded: {doc.summary()}")

    def _on_load_failed(self, message: str) -> None:
        self._window.on_load_failed(message)
