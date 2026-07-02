# CAD Drafting AI

An AI-assisted Computer-Aided Design (CAD) drafting tool containerized with clean architecture.

## Directory Structure

```
cad_drafting_ai/
│
├── app/                  # Main application source code
│   ├── gui/              # Graphical User Interface components
│   ├── viewer/           # 2D/3D Renderer and Viewport modules
│   ├── geometry/         # Geometric primitives, math, transformations
│   ├── topology/         # Boundary representation (B-Rep), topological relations
│   ├── features/         # Parametric features (extrude, revolve, fillet, etc.)
│   ├── projection/       # 3D to 2D projection engine
│   ├── dimensions/       # Automated dimensioning and annotation tools
│   ├── drawing/          # Sheet layouts, title blocks, drawing standards
│   ├── exporters/        # DXF, STEP, IGES, SVG, PDF exporters
│   ├── utils/            # Shared helper functions
│   └── main.py           # Application entrypoint
│
├── data/                 # Sample drawings, templates, and reference standards
│   ├── samples/
│   └── templates/
│
├── tests/                # Unit and integration test suites
│
├── docs/                 # Developer and user documentation
│
├── requirements.txt      # Python dependencies
│
└── README.md             # This file
```

## Getting Started

1. Clone or download this project.
2. Initialize directory and environment:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python -m app.main
   ```
