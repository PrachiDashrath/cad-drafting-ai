"""
app/gui/main_window.py
"""

from PySide6.QtWidgets import (
    QMainWindow,
    QMessageBox,
    QSplitter,
)
from PySide6.QtCore import Qt

from app.gui.occ_viewer import OccViewer
from app.drawing.drawing_widget import DrawingWidget

from app.gui.actions import build_actions
from app.gui.menus import build_menu_bar
from app.gui.toolbar import build_toolbar
from app.gui.status_bar import CADStatusBar

from app.core.document import CADDocument
from app.config import APP_NAME, APP_VERSION, WINDOW_W, WINDOW_H
from app.utils.logger import get_logger

log = get_logger(__name__)


class MainWindow(QMainWindow):

    def __init__(self, controller, parent=None):
        super().__init__(parent)

        self._controller = controller

        self.setWindowTitle(f"{APP_NAME} v{APP_VERSION}")
        self.resize(WINDOW_W, WINDOW_H)

        # ----------------------------------------------------------
        # Splitter
        # ----------------------------------------------------------

        splitter = QSplitter(Qt.Horizontal)

        self.viewer = OccViewer(self)
        self.drawing = DrawingWidget(self)

        splitter.addWidget(self.viewer)
        splitter.addWidget(self.drawing)

        splitter.setStretchFactor(0, 3)
        splitter.setStretchFactor(1, 2)

        self.setCentralWidget(splitter)

        # ----------------------------------------------------------
        # Actions
        # ----------------------------------------------------------

        self.actions = build_actions(self)

        self.status = CADStatusBar(self)
        self.setStatusBar(self.status)

        build_menu_bar(self, self.actions)
        build_toolbar(self, self.actions)

        self.actions["open"].triggered.connect(self._controller.open_file)
        self.actions["screenshot"].triggered.connect(self._controller.save_screenshot)
        self.actions["exit"].triggered.connect(self.close)

        self.actions["fit_all"].triggered.connect(self._controller.fit_all)
        self.actions["front"].triggered.connect(self._controller.view_front)
        self.actions["top"].triggered.connect(self._controller.view_top)
        self.actions["right"].triggered.connect(self._controller.view_right)
        self.actions["iso"].triggered.connect(self._controller.view_iso)

        self.actions["wireframe"].triggered.connect(self._controller.set_wireframe)
        self.actions["shaded"].triggered.connect(self._controller.set_shaded)

        self.actions["about"].triggered.connect(self._show_about)

        self.viewer.mouse_moved.connect(self.status.set_mouse_position)

        log.info("MainWindow ready")

    # --------------------------------------------------------------

    def on_document_loaded(self, doc: CADDocument):
        self.status.set_model_info(doc)

    def on_load_failed(self, message: str):
        self.status.set_error(message)
        QMessageBox.critical(self, "Load Error", message)

    def on_loading(self, filename: str):
        self.status.set_loading(filename)

    # --------------------------------------------------------------

    def _show_about(self):
        QMessageBox.about(
            self,
            f"About {APP_NAME}",
            f"<b>{APP_NAME}</b><br>"
            f"Version {APP_VERSION}<br><br>"
            "AI-powered CAD Drafting Software<br>"
            "Built with Open CASCADE + PySide6",
        )