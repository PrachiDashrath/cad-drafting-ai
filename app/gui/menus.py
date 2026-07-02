"""
app/gui/menus.py
Builds the menu bar from shared actions dict.
"""

from PySide6.QtWidgets import QMainWindow, QMenuBar


def build_menu_bar(window: QMainWindow, actions: dict) -> QMenuBar:
    mb = window.menuBar()

    # -- File ---------------------------------------------------------------
    file_menu = mb.addMenu("&File")
    file_menu.addAction(actions["open"])
    file_menu.addSeparator()
    file_menu.addAction(actions["screenshot"])
    file_menu.addSeparator()
    file_menu.addAction(actions["exit"])

    # -- View ---------------------------------------------------------------
    view_menu = mb.addMenu("&View")
    view_menu.addAction(actions["fit_all"])
    view_menu.addSeparator()
    view_menu.addAction(actions["front"])
    view_menu.addAction(actions["top"])
    view_menu.addAction(actions["right"])
    view_menu.addAction(actions["iso"])
    view_menu.addSeparator()
    view_menu.addAction(actions["wireframe"])
    view_menu.addAction(actions["shaded"])

    # -- Help ---------------------------------------------------------------
    help_menu = mb.addMenu("&Help")
    help_menu.addAction(actions["about"])

    return mb
