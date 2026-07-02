"""
app/utils/logger.py
Central logging factory.  All modules call get_logger(__name__).
"""

import logging
import sys

_FMT = "%(asctime)s  %(levelname)-8s  %(name)s  —  %(message)s"
_DATE = "%H:%M:%S"

# Configure root logger once
logging.basicConfig(
    stream=sys.stdout,
    level=logging.DEBUG,
    format=_FMT,
    datefmt=_DATE,
)


def get_logger(name: str) -> logging.Logger:
    """Return a named logger.  Usage: log = get_logger(__name__)"""
    return logging.getLogger(name)
