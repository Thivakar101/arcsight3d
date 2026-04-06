# Arc Sight 3D - 2D Floor Plan to 3D Blender Reconstructor

**Arc Sight 3D** is a lightweight toolset designed to bridge the gap between 2D architectural floor plan images (blueprints) and 3D scenes in Blender. Using computer vision (OpenCV) and Blender's Python API (`bpy` and `bmesh`), it extracts walls and doors from 2D images and reconstructs them in 3D space.

Whether you have a scanned JPEG/PNG of a blueprint or want to programmatically generate maps in Blender, this project provides clean pipelines to automate the heavy lifting.

---

## How It Works

Arc Sight 3D offers two main processing pipelines, plus a procedural layout demonstration:

### Pipeline 1: Contour-Based Detection (GUI)
*Best for floor plans with thick/filled walls.*
1. **Analyze:** Run the desktop application `detector_gui.py`. Select your blueprint image, and click **Start Processing**.
2. **Process:** The script performs adaptive thresholding, applies morphological closing to fill gaps, and extracts contours. It filters noise and classifies shapes as either `wall` or `door` based on aspect ratio and bounding box geometry.
3. **Save:** The detected elements are saved as a clean dataset in `detected_objects.json`.
4. **Build:** Open the Blender project, load `blender_contour_builder.py` into the text editor, and run it. It reads `detected_objects.json` and builds solid 3D walls and doors matching the plan.

### Pipeline 2: Line-Based Vector Extraction (CLI)
*Best for wireframes and thin single-line blueprints.*
1. **Analyze:** Run `line_detector.py` from your command line, pointing to a blueprint image.
2. **Process:** It runs a Gaussian blur, Canny edge detection, and a Hough Lines Transform. The script then applies an angle/distance filter to merge redundant parallel lines into clean single-line vectors.
3. **Save:** The line segments are saved as starting/ending coordinate pairs in `line_coordinates.json`.
4. **Build:** Run `blender_line_builder.py` inside Blender to instantiate flat 3D plane walls along those line vectors.

### Bonus: Procedural Map Level Designer
*Demonstrates manual 3D generation.*
* Running `blender_procedural_map.py` inside Blender procedurally generates a game-like level layout (walls and door cutouts) using coordinate arrays. It showcases how to use Blender's Boolean modifier to carve door gaps out of solid wall meshes.

---

## File Directory

```
arcsight3d/
├── samples/                       # Sample blueprint images for testing
│   ├── 0001.jpg
│   ├── blue.png
│   ├── print.png
│   └── typical.jpg (etc.)
├── detector_gui.py                # Desktop GUI for contour detection (PyQt5 + OpenCV)
├── line_detector.py               # Command-line line detector (OpenCV)
├── blender_contour_builder.py     # Blender script to build 3D mesh walls from contours
├── blender_line_builder.py        # Blender script to build 3D plane walls from line vectors
├── blender_procedural_map.py      # Blender script for procedural map generation with doors
├── 3D.blend                       # Main Blender project template
└── README.md                      # This documentation
```

---

## Prerequisites & Installation

To run the analysis scripts (`detector_gui.py` and `line_detector.py`), you need Python 3 installed with a few dependencies.

1. **Install dependencies:**
   ```bash
   pip install opencv-python numpy PyQt5
   ```

*(Note: The Blender scripts run entirely within Blender's built-in Python environment, which already includes `bpy`, `bmesh`, `math`, and `json`. You do not need to install anything special inside Blender!)*

---

## Usage Guide

### Step 1: Detect Structural Elements

#### Option A: Using the GUI (Contours)
1. Run the GUI:
   ```bash
   python detector_gui.py
   ```
2. Click **Select Blueprint** and choose one of the blueprints from the `samples/` directory (e.g. `samples/print.png` or your own floor plan).
3. Click **Start Processing**. When complete, it generates `detected_objects.json` in the project folder.

#### Option B: Using the CLI (Lines)
1. Run the script (defaults to `samples/print.png` if no argument is passed):
   ```bash
   python line_detector.py path/to/your/blueprint.png
   ```
2. It processes the image and outputs `line_coordinates.json` in the project folder.

---

### Step 2: Reconstruct in Blender

1. Open your Blender application.
2. Open `3D.blend` or create a new empty file and save it in the `arcsight3d` folder (saving is important so Blender knows where to look for the JSON files!).
3. Switch your Blender workspace layout to **Scripting**.
4. Click **Open** in the Text Editor and select either `blender_contour_builder.py` or `blender_line_builder.py`.
5. Click the **Run Script** button (play icon) at the top right of the Text Editor.
6. The script clears any previous run meshes and automatically populates your scene with the 3D reconstructed geometry.

*Tip: To view the procedural map layout example, load and run `blender_procedural_map.py` instead.*

---

## Customization & Parameters

You can open the scripts in any editor to fine-tune the parameters:
* **Scale Factor (`scale`):** Both Blender scripts downscale pixel units to Blender meters (default is `scale = 0.05`, meaning 20 pixels = 1 Blender meter). Adjust this if your model is too large or too small.
* **Canny Thresholds:** In `line_detector.py`, edit the `cv2.Canny(blurred, 50, 150)` thresholds to capture more or fewer edges.
* **Aspect Ratio Classification:** In `detector_gui.py`, change `w / h > 3.0` to adjust how strict the aspect ratio is when distinguishing long walls from square door enclosures.
