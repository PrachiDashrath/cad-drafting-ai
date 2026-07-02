from OCC.Core.STEPControl import STEPControl_Reader
from OCC.Core.IFSelect import IFSelect_RetDone

from app.projection.projection_engine import ProjectionEngine


reader = STEPControl_Reader()

status = reader.ReadFile("data/samples/sample_box.stp")

if status != IFSelect_RetDone:
    raise RuntimeError("Failed to load STEP")

reader.TransferRoots()

shape = reader.OneShape()

engine = ProjectionEngine()

view = engine.front(shape)

print("Visible:", len(view.visible_geometry))

print("Hidden:", len(view.hidden_geometry))