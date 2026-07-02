import os
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCC.Core.STEPControl import STEPControl_Writer, STEPControl_AsIs

def generate_sample_box(file_path, dx=10.0, dy=20.0, dz=30.0):
    """Generates a simple 3D cubic box and exports it as a STEP file."""
    # Ensure directory exists
    dir_name = os.path.dirname(file_path)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)
        
    print(f"Generating 3D box of dimensions {dx} x {dy} x {dz}...")
    # Use Open CASCADE to create a solid box
    box_shape = BRepPrimAPI_MakeBox(dx, dy, dz).Shape()
    
    # Write to STEP format
    writer = STEPControl_Writer()
    writer.Transfer(box_shape, STEPControl_AsIs)
    
    print(f"Writing shape to: {file_path}")
    status = writer.Write(file_path)
    print("STEP file generated successfully!")
    return file_path
