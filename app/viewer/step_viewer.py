import os
from OCC.Core.STEPControl import STEPControl_Reader
from OCC.Core.IFSelect import IFSelect_RetDone
from OCC.Display.SimpleGui import init_display

def load_and_display_step(file_path):
    """Loads a STEP file (.stp or .step) and displays it in a PySide-based 3D Viewport."""
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' does not exist.")
        return False
        
    print(f"Reading STEP file: {file_path}")
    reader = STEPControl_Reader()
    status = reader.ReadFile(file_path)
    
    if status == IFSelect_RetDone:
        # Transfer the model contents
        print("Transferring shape data to Open CASCADE kernel...")
        reader.TransferRoot()
        shape = reader.Shape()
        
        print("Launching 3D CAD Viewport...")
        # Initialize viewer window
        display, start_display, add_menu, add_function_to_menu = init_display()
        display.DisplayShape(shape, update=True)
        display.FitAll()
        start_display()
        return True
    else:
        print("Error: Failed to parse STEP file (invalid format or corrupted structure).")
        return False
