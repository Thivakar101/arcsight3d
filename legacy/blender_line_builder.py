import bpy
import mathutils
import json
import os

def get_json_path():
    """
    Attempts to locate 'line_coordinates.json' using multiple fallbacks:
    1. Relative to the current saved .blend file.
    2. In the current working directory.
    3. Relative to this script's path (if executed from disk).
    """
    # 1. Look relative to the saved blend file
    if bpy.data.is_saved:
        blend_dir = os.path.dirname(bpy.data.filepath)
        json_path = os.path.join(blend_dir, "line_coordinates.json")
        if os.path.exists(json_path):
            return json_path
    
    # 2. Look in the current working directory
    cwd_path = os.path.join(os.getcwd(), "line_coordinates.json")
    if os.path.exists(cwd_path):
        return cwd_path
        
    # 3. Look relative to the script location (if running from file)
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        script_path = os.path.join(script_dir, "line_coordinates.json")
        if os.path.exists(script_path):
            return script_path
    except NameError:
        pass
        
    return None

def create_wall_from_line(start, end, height, scale=0.05):
    """
    Create a 3D plane wall from a 2D line in Blender.
    """
    # Convert and scale the 2D coordinates into 3D vectors
    start_vec = mathutils.Vector((start[0] * scale, start[1] * scale, 0))
    end_vec = mathutils.Vector((end[0] * scale, end[1] * scale, 0))
    
    # Define the 4 vertices for the flat plane wall
    vertices = [
        (start_vec.x, start_vec.y, 0),       # Bottom-left
        (end_vec.x, end_vec.y, 0),           # Bottom-right
        (end_vec.x, end_vec.y, height),      # Top-right
        (start_vec.x, start_vec.y, height)   # Top-left
    ]

    mesh = bpy.data.meshes.new("WallMesh")
    wall = bpy.data.objects.new("Wall_Line", mesh)
    bpy.context.collection.objects.link(wall)

    # Single face for the wall
    faces = [(0, 1, 2, 3)]

    # Create the mesh
    mesh.from_pydata(vertices, [], faces)
    mesh.update()

def main():
    json_path = get_json_path()
    if not json_path:
        print("Error: Could not find 'line_coordinates.json'. Make sure the detector script was run.")
        return

    print(f"Loading line coordinates from: {json_path}")
    try:
        with open(json_path, 'r') as f:
            line_coordinates = json.load(f)
    except Exception as e:
        print(f"Error reading JSON file: {e}")
        return

    # Clear existing generated line walls
    bpy.ops.object.select_all(action='DESELECT')
    for obj in list(bpy.data.objects):
        if obj.type == 'MESH' and obj.name.startswith("Wall_Line"):
            bpy.data.objects.remove(obj, do_unlink=True)

    wall_height = 3.0  # Height of the walls in Blender units (meters)
    scale_factor = 0.05  # Downscales pixel coordinates to Blender-friendly units
    
    count = 0
    for line in line_coordinates:
        if len(line) == 2:
            start, end = line
            create_wall_from_line(start, end, wall_height, scale=scale_factor)
            count += 1

    print(f"Successfully generated {count} line walls in the scene.")

if __name__ == "__main__":
    main()
