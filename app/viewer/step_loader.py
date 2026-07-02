"""
app/viewer/step_loader.py
Loads a STEP file, populates a CADDocument, and emits a Qt signal.
Runs synchronously; call from ApplicationController.
"""

import os
from PySide6.QtCore import QObject, Signal

from OCC.Core.STEPControl import STEPControl_Reader
from OCC.Core.IFSelect import IFSelect_RetDone
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.TopAbs import TopAbs_FACE, TopAbs_EDGE, TopAbs_VERTEX
from OCC.Core.BRep import BRep_Builder
from OCC.Core.BRepBndLib import brepbndlib
from OCC.Core.Bnd import Bnd_Box
from OCC.Core.GProp import GProp_GProps
from OCC.Core.BRepGProp import brepgprop

from app.core.document import CADDocument
from app.utils.logger import get_logger

log = get_logger(__name__)


class StepLoader(QObject):
    """Loads .step / .stp files and produces a CADDocument."""

    # Emitted on success with the populated document
    document_loaded = Signal(CADDocument)
    # Emitted on failure with an error message
    load_failed = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

    # ------------------------------------------------------------------
    def load(self, file_path: str) -> CADDocument | None:
        """
        Load *file_path*, populate a CADDocument, emit document_loaded.
        Returns the document on success, None on failure.
        """
        if not os.path.exists(file_path):
            msg = f"File not found: {file_path}"
            log.error(msg)
            self.load_failed.emit(msg)
            return None

        log.info(f"Reading STEP file: {file_path}")
        reader = STEPControl_Reader()
        status = reader.ReadFile(file_path)

        if status != IFSelect_RetDone:
            msg = f"Failed to parse STEP file: {file_path}"
            log.error(msg)
            self.load_failed.emit(msg)
            return None

        reader.TransferRoot()
        shape = reader.Shape()

        doc = CADDocument(
            shape    = shape,
            filename = os.path.basename(file_path),
            units    = "mm",
        )
        doc = _populate_stats(doc)

        log.info(doc.summary())
        self.document_loaded.emit(doc)
        return doc


# ------------------------------------------------------------------
def _count_topology(shape, topology_type) -> int:
    explorer = TopExp_Explorer(shape, topology_type)
    count = 0
    while explorer.More():
        count += 1
        explorer.Next()
    return count


def _populate_stats(doc: CADDocument) -> CADDocument:
    shape = doc.shape

    doc.faces    = _count_topology(shape, TopAbs_FACE)
    doc.edges    = _count_topology(shape, TopAbs_EDGE)
    doc.vertices = _count_topology(shape, TopAbs_VERTEX)

    # Bounding box
    bbox = Bnd_Box()
    brepbndlib.Add(shape, bbox)
    doc.bounding_box = bbox

    # Volume / surface area
    try:
        v_props = GProp_GProps()
        brepgprop.VolumeProperties(shape, v_props)
        doc.volume = v_props.Mass()

        s_props = GProp_GProps()
        brepgprop.SurfaceProperties(shape, s_props)
        doc.surface_area = s_props.Mass()
    except Exception as e:
        log.warning(f"Could not compute physical properties: {e}")

    return doc
