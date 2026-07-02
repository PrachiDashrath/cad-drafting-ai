"""
app/gui/actions.py
Shared QAction objects. Both menus and toolbar reference the same actions —
no duplication, consistent keyboard shortcuts and icons everywhere.
"""

from PySide6.QtGui import QAction, QKeySequence
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt


def build_actions(parent: QWidget) -> dict[str, QAction]:
    """
    Create and return all application actions keyed by string.

    Usage:
        actions = build_actions(self)
        toolbar.addAction(actions["fit_all"])
        menu_view.addAction(actions["fit_all"])
    """
    def action(text, shortcut=None, tip=None, checkable=False) -> QAction:
        a = QAction(text, parent)
        if shortcut:
            a.setShortcut(QKeySequence(shortcut))
        if tip:
            a.setStatusTip(tip)
        if checkable:
            a.setCheckable(True)
        return a

    return {
        # File
        "open":       action("&Open STEP…",       "Ctrl+O",  "Open a STEP file"),
        "screenshot": action("Save &Screenshot…",  "Ctrl+P",  "Save viewport as PNG"),
        "exit":       action("E&xit",              "Ctrl+Q",  "Quit the application"),

        # View — camera
        "fit_all":    action("Fit &All",           "F",       "Fit all geometry to view"),
        "front":      action("Fro&nt",             "Num+1",   "Front view"),
        "top":        action("&Top",               "Num+7",   "Top view"),
        "right":      action("R&ight",             "Num+3",   "Right view"),
        "iso":        action("&Isometric",         "Num+0",   "Isometric view"),

        # View — display mode
        "wireframe":  action("&Wireframe",         "W",       "Wireframe display mode", checkable=True),
        "shaded":     action("&Shaded",            "S",       "Shaded display mode",    checkable=True),

        # Help
        "about":      action("&About",             None,      "About CAD Drafting AI"),
    }
