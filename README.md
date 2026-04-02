# ArcSight 3D

ArcSight 3D is an automated pipeline designed to convert 2D architectural floor plans into fully explorable 3D models. 

By integrating computer vision and optical character recognition, ArcSight 3D aims to eliminate the manual labor of reconstructing a building's geometry from a flat blueprint. It reads the lines and text of a floor plan, uses those findings to procedurally generate a 3D scene in Blender, and exports the result for real-time visualization in Unity.

---

## How the System Works

The application follows a strictly defined, multi-step workflow. It is built as a distributed architecture consisting of a desktop client, a REST API backend, and an automated 3D modeling layer.

1. Upload and Ingestion: The user selects a 2D floor plan image (PNG or JPG format) using the PyQt5 desktop client. The client securely transmits the image to the Flask backend API.
2. Computer Vision Analysis: The backend triggers a processing pipeline that utilizes OpenCV. It applies noise reduction and thresholding, then searches for geometric contours and parallel lines to identify the location, length, and orientation of structural walls and doorways.
3. Optical Character Recognition: If enabled, Tesseract OCR analyzes the image to extract textual information. Custom parsers filter this data to identify room names and dimensional measurements.
4. Database Storage: The structural coordinates and text metadata are persisted into a PostgreSQL database, establishing a unified source of truth for the floor plan.
5. Headless 3D Generation: Upon request, the backend spawns a headless Blender process. A custom Blender Python script connects to the database output, calculates the appropriate 3D coordinates, and generates meshes for every detected wall and door.
6. Export and Visualization: Blender exports the completed scene as a GLB or FBX file. This file can be downloaded through the desktop client and directly imported into Unity for a first-person interactive walkthrough.

---

## Directory and File Breakdown

The project repository is strictly modularized to separate concerns across the frontend interface, backend logic, and game engine visualization.

### 1. Desktop Client (desktop/)
This directory contains the PyQt5 application that serves as the primary user interface.
* app.py: The main executable script. Running this file launches the desktop application.
* api_client.py: The networking layer. It handles all HTTP requests to the backend API, ensuring the UI remains decoupled from backend logic.
* workers.py: Contains background thread classes. These ensure that network requests and long-running generation tasks do not freeze the graphical interface.
* ui/main_window.py: Defines the structural layout, buttons, and progress bars of the user interface.
* ui/styles.qss: The Qt stylesheet that provides the dark-mode aesthetic for the application.

### 2. Backend Services (backend/)
This directory houses the Flask REST API and all data processing pipelines.
* app.py and config.py: These files initialize the Flask web server, handle environment variables, and configure the database connection.
* api/ and controllers/: These modules define the web endpoints (such as POST /api/v1/projects) and handle input validation and HTTP responses.
* services/: This layer contains the core business logic, orchestrating the flow between the API endpoints and the processing pipelines.
* models/: Contains SQLAlchemy schemas that map Python objects to PostgreSQL database tables.
* cv/: The computer vision engine. It includes preprocessing routines and detection algorithms for extracting geometry from the uploaded image.
* ocr/: The text extraction pipeline. It integrates Tesseract and includes specific parsers for identifying architectural dimensions and room labels.
* blender/: The 3D automation layer. It contains a runner script that manages the Blender subprocess, alongside the actual Blender Python script (generate_scene.py) that builds the meshes.

### 3. Unity Integration (unity/)
This directory contains C# scripts intended to be dropped into a Unity project for rendering the exported models.
* FirstPersonController.cs: A standard player movement script providing keyboard and mouse controls for navigating the 3D space.
* RuntimeModelLoader.cs and SceneBootstrap.cs: Scripts that automate the process of loading the exported GLB file into the Unity scene at runtime.

### 4. Legacy Code (legacy/)
This directory contains the original, monolithic prototype scripts. They are retained for historical reference and documentation purposes but are not executed by the current system.

---

## Installation and Setup

1. Clone the repository:
   git clone <repo-url>
   cd arcsight3d

2. Backend Setup:
   Create a virtual environment and install the required Python dependencies:
   python -m venv venv
   
   # For Windows:
   .\venv\Scripts\activate  
   
   # For Mac/Linux:
   source venv/bin/activate
   
   pip install -r requirements.txt

3. Environment Variables:
   Copy the .env.example file to a new file named .env. Ensure that the TESSERACT_CMD and BLENDER_EXECUTABLE variables point to the correct absolute paths on your system if they are not available in your global PATH.

4. Database Setup (PostgreSQL):
   If you have Docker installed, you can initialize the database using the provided compose file:
   docker-compose up -d postgres
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade

## Usage Guide

1. Start the Backend Server:
   Open a terminal, activate your virtual environment, and execute the following:
   set FLASK_APP=backend.app
   set FLASK_ENV=development
   flask run --host=0.0.0.0 --port=5000

2. Start the Desktop Client:
   Open a second terminal, activate the virtual environment, and execute:
   python -m desktop.app

3. Using the Interface:
   In the desktop application, provide a project name and select a blueprint image. Click "Upload & Process" to begin the computer vision analysis. Once the status indicates completion, click "Generate 3D Model" to trigger the Blender export. The final model will be saved in the exports/ directory.

---

## Limitations and Future Improvements

* Image Quality Dependency: The accuracy of the wall and door detection relies heavily on the clarity and contrast of the uploaded blueprint. Cluttered or heavily stylized hand-drawn plans may yield inaccurate geometry.
* OCR Reliability: Tesseract's ability to extract text is constrained by the resolution of the image and the orientation of the text within the blueprint.
* Unity GLB Loading: Unity does not natively support runtime loading of GLB files. We recommend installing the GLTFast package via the Unity Package Manager to ensure the runtime loader scripts function as intended.
* Future Roadmap: We plan to replace the geometric heuristic algorithms with machine learning models, such as YOLO, for more robust object classification, and to improve the detection of closed room polygons for automatic floor generation.
