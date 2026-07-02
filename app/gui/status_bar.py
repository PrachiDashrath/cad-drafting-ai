"""
app/gui/status_bar.py
Status bar showing model info, loading state, and mouse position.
"""

from PySide6.QtWidgets import QStatusBar, QLabel
from PySide6.QtCore import Qt

from app.core.document import CADDocument


class CADStatusBar(QStatusBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._main_label = QLabel("Ready")
        self._mouse_label = QLabel("")
        self._mouse_label.setAlignment(Qt.AlignRight)

        self.addWidget(self._main_label, stretch=1)
        self.addPermanentWidget(self._mouse_label)

    # ------------------------------------------------------------------
    def set_ready(self) -> None:
        self._main_label.setText("Ready")

    def set_loading(self, filename: str) -> None:
        self._main_label.setText(f"Loading  {filename} …")

    def set_model_info(self, doc: CADDocument) -> None:
        self._main_label.setText(
            f"  {doc.filename}   |   "
            f"Faces: {doc.faces}   "
            f"Edges: {doc.edges}   "
            f"Vertices: {doc.vertices}   |   "
            f"{doc.units}"
        )

    def set_error(self, message: str) -> None:
        self._main_label.setText(f"⚠  {message}")

    def set_mouse_position(self, x: float, y: float) -> None:
        self._mouse_label.setText(f"X: {x:.2f}   Y: {y:.2f}   ")
