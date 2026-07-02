"""
app/config.py
Application-wide constants.  Import from here instead of hardcoding values.
"""

from app.core.document import DisplayMode

# -- Window -----------------------------------------------------------------
APP_NAME    = "CAD Drafting AI"
APP_VERSION = "0.1.0"
WINDOW_W    = 1280
WINDOW_H    = 800

# -- Viewer -----------------------------------------------------------------
BACKGROUND_COLOR_TOP    = (0.15, 0.15, 0.20)   # dark navy top gradient
BACKGROUND_COLOR_BOTTOM = (0.05, 0.05, 0.08)   # near-black bottom gradient
DEFAULT_DISPLAY_MODE    = DisplayMode.SHADED_WITH_EDGES

# -- Units ------------------------------------------------------------------
DEFAULT_UNIT = "mm"

# -- UI ---------------------------------------------------------------------
THEME         = "dark"
GRID_ENABLED  = False
SNAP_ENABLED  = False

# -- File I/O ---------------------------------------------------------------
STEP_EXTENSIONS = ("*.stp", "*.step", "*.STP", "*.STEP")
STEP_FILTER     = "STEP Files (*.stp *.step *.STP *.STEP);;All Files (*)"

# -- Logging ----------------------------------------------------------------
LOG_LEVEL = "DEBUG"
