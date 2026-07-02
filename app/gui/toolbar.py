"""
app/gui/toolbar.py
Builds the main toolbar from shared actions dict.
"""

from PySide6.QtWidgets import QMainWindow, QToolBar
from PySide6.QtCore import Qt


def build_toolbar(window: QMainWindow, actions: dict) -> QToolBar:
    tb = QToolBar("Main Toolbar", window)
    tb.setMovable(False)
    tb.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
    window.addToolBar(Qt.TopToolBarArea, tb)

    tb.addAction(actions["open"])
    tb.addSeparator()
    tb.addAction(actions["fit_all"])
    tb.addAction(actions["front"])
    tb.addAction(actions["top"])
    tb.addAction(actions["right"])
    tb.addAction(actions["iso"])
    tb.addSeparator()
    tb.addAction(actions["wireframe"])
    tb.addAction(actions["shaded"])
    tb.addSeparator()
    tb.addAction(actions["screenshot"])

    return tb
