"""
app/controller.py

Application controller.
"""

import os

from PySide6.QtWidgets import QFileDialog
from PySide6.QtCore import QObject

from app.viewer.step_loader import StepLoader
from app.viewer.display_manager import DisplayManager
from app.viewer.camera_controller import CameraController
from app.viewer.selection import SelectionManager

from app.projection.projection_service import ProjectionService

from app.core.document import CADDocument, DisplayMode
from app.config import STEP_FILTER
from app.utils.logger import get_logger

log = get_logger(__name__)


class ApplicationController(QObject):

    def __init__(self, parent=None):
        super().__init__(parent)

        self._window = None
        self._doc = None

        self._loader = None
        self._display = None
        self._camera = None
        self._selection = None

        # NEW
        self._projection = ProjectionService()

    # ------------------------------------------------------------

    def set_window(self, window):

        self._window = window

        display = window.viewer.occ_display

        self._display = DisplayManager(display.Context)
        self._camera = CameraController(display.View)
        self._selection = SelectionManager(display.Context)

        self._loader = StepLoader(self)

        self._loader.document_loaded.connect(
            self._on_document_loaded
        )

        self._loader.load_failed.connect(
            self._on_load_failed
        )

        log.info("ApplicationController ready.")

    # ------------------------------------------------------------

    def open_file(self):

        path, _ = QFileDialog.getOpenFileName(
            self._window,
            "Open STEP File",
            "",
            STEP_FILTER,
        )

        if not path:
            return

        self._window.on_loading(os.path.basename(path))

        self._loader.load(path)

    # ------------------------------------------------------------

    def save_screenshot(self):

        path, _ = QFileDialog.getSaveFileName(
            self._window,
            "Save Screenshot",
            "screenshot.png",
            "PNG (*.png)"
        )

        if path:
            self._window.viewer.occ_display.View.Dump(path)

    # ------------------------------------------------------------

    def fit_all(self):
        self._camera.fit_all()

    def view_front(self):
        self._camera.front()

    def view_top(self):
        self._camera.top()

    def view_right(self):
        self._camera.right()

    def view_iso(self):
        self._camera.iso()

    # ------------------------------------------------------------

    def set_wireframe(self):

        self._display.set_display_mode(DisplayMode.WIREFRAME)

        self._window.viewer.set_display_mode(
            DisplayMode.WIREFRAME
        )

    def set_shaded(self):

        self._display.set_display_mode(
            DisplayMode.SHADED_WITH_EDGES
        )

        self._window.viewer.set_display_mode(
            DisplayMode.SHADED_WITH_EDGES
        )

    # ------------------------------------------------------------

    def _on_document_loaded(self, doc: CADDocument):

    	self._doc = doc

    	#
    	# Display 3D model
    	#

    	self._window.viewer.erase_all()

    	self._window.viewer.display_shape(doc.shape)

    	self._camera.fit_all()

    	#
    	# Generate complete drawing sheet
    	#

    	try:

        	sheet = self._projection.generate_sheet(
            	doc.shape
        	)

        	self._window.drawing.set_drawing_sheet(sheet)

        	log.info("Drawing sheet generated.")

    	except Exception as e:

        	log.exception(e)

    	self._window.on_document_loaded(doc)

    # ------------------------------------------------------------

    def _on_load_failed(self, message):

        self._window.on_load_failed(message)