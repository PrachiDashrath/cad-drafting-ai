"""
First Hidden Line Removal experiment.

Loads a STEP file and performs HLR.

No GUI.
No exporters.
Pure OCCT test.
"""

from OCC.Core.STEPControl import STEPControl_Reader
from OCC.Core.IFSelect import IFSelect_RetDone

from OCC.Core.HLRBRep import (
    HLRBRep_Algo,
    HLRBRep_HLRToShape,
)

from OCC.Core.HLRAlgo import HLRAlgo_Projector

from OCC.Core.gp import gp_Ax2, gp_Dir, gp_Pnt


reader = STEPControl_Reader()

status = reader.ReadFile("data/samples/sample_box.stp")

if status != IFSelect_RetDone:
    raise RuntimeError("Failed to load STEP")

reader.TransferRoots()

shape = reader.OneShape()

print("STEP Loaded")


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


hlr = HLRBRep_HLRToShape(algo)

print("Visible Compound:", hlr.VCompound())

print("Hidden Compound:", hlr.HCompound())

print("SUCCESS")