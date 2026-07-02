"""
app/main.py
Application entry point.
"""

import sys
from PySide6.QtWidgets import QApplication

from app.controller import ApplicationController
from app.gui.main_window import MainWindow
from app.config import APP_NAME
from app.utils.logger import get_logger

log = get_logger(__name__)


def main():
    log.info(f"Starting {APP_NAME}")
    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)

    # Wire controller ↔ window
    controller = ApplicationController()
    window = MainWindow(controller)
    controller.set_window(window)

    window.show()
    log.info("MainWindow shown")
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
