"""
tests/test_projection.py

Test the complete HLR -> Edge Extraction -> Curve Conversion pipeline.
"""

from OCC.Core.STEPControl import STEPControl_Reader
from OCC.Core.IFSelect import IFSelect_RetDone

from OCC.Core.HLRBRep import (
    HLRBRep_Algo,
    HLRBRep_HLRToShape,
)

from OCC.Core.HLRAlgo import HLRAlgo_Projector
from OCC.Core.gp import gp_Ax2, gp_Dir, gp_Pnt

from app.projection.edge_extractor import EdgeExtractor
from app.projection.curve_converter import CurveConverter


# ------------------------------------------------------------
# Load STEP
# ------------------------------------------------------------

reader = STEPControl_Reader()

status = reader.ReadFile("data/samples/sample_box.stp")

if status != IFSelect_RetDone:
    raise RuntimeError("Failed to load STEP file.")

reader.TransferRoots()

shape = reader.OneShape()

print("STEP Loaded")


# ------------------------------------------------------------
# Run HLR
# ------------------------------------------------------------

projector = HLRAlgo_Projector(
    gp_Ax2(
        gp_Pnt(0, 0, 0),
        gp_Dir(0, 0, 1),
    )
)

algo = HLRBRep_Algo()

algo.Add(shape)
algo.Projector(projector)
algo.Update()
algo.Hide()

print("HLR Finished")


# ------------------------------------------------------------
# Convert HLR output to compounds
# ------------------------------------------------------------

hlr = HLRBRep_HLRToShape(algo)

visible_compound = hlr.VCompound()
hidden_compound = hlr.HCompound()

print("Visible Compound:", type(visible_compound))
print("Hidden Compound:", type(hidden_compound))


# ------------------------------------------------------------
# Extract edges
# ------------------------------------------------------------

extractor = EdgeExtractor()

visible_edges = extractor.extract(visible_compound)
hidden_edges = extractor.extract(hidden_compound)

print(f"Visible edges: {len(visible_edges)}")
print(f"Hidden edges: {len(hidden_edges)}")


# ------------------------------------------------------------
# Convert edges to Geometry2D
# ------------------------------------------------------------

converter = CurveConverter()

geometry = []

for edge in visible_edges:
    entity = converter.convert(edge)
    if entity is not None:
        geometry.append(entity)

print(f"Converted geometry: {len(geometry)}")

for entity in geometry:
    print(entity)

print("\nSUCCESS")