import bpy
import json
import os
import bmesh

def get_json_path():
    """
    Attempts to locate 'detected_objects.json' using multiple fallbacks:
    1. Relative to the current saved .blend file.
    2. In the current working directory.
    3. Relative to this script's path (if executed from disk).
    """
    # 1. Look relative to the saved blend file
    if bpy.data.is_saved:
        blend_dir = os.path.dirname(bpy.data.filepath)
        json_path = os.path.join(blend_dir, "detected_objects.json")
        if os.path.exists(json_path):
            return json_path
    
    # 2. Look in the current working directory
    cwd_path = os.path.join(os.getcwd(), "detected_objects.json")
    if os.path.exists(cwd_path):
        return cwd_path
        
    # 3. Look relative to the script location (if running from file)
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        script_path = os.path.join(script_dir, "detected_objects.json")
        if os.path.exists(script_path):
            return script_path
    except NameError:
        pass
        
    return None

def create_mesh(location, width, height, thickness, name):
    """
    Creates a 3D block representing a wall or door in Blender.
    """
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)

    bm = bmesh.new()

    # Define the four bottom vertices (z = 0)
    # Note: Using small scale adjustments if needed, dividing width/height by a factor to make it fit Blender units.
    # Typically, image pixels are very large. Let's scale down by 100 to map pixels to Blender meters.
    scale = 0.05
    w_scaled = width * scale
    h_scaled = height * scale
    x_scaled = location[0] * scale
    y_scaled = location[1] * scale
    t_scaled = thickness

    p1 = bm.verts.new((x_scaled - w_scaled / 2, y_scaled - h_scaled / 2, 0))
    p2 = bm.verts.new((x_scaled + w_scaled / 2, y_scaled - h_scaled / 2, 0))
    p3 = bm.verts.new((x_scaled + w_scaled / 2, y_scaled + h_scaled / 2, 0))
    p4 = bm.verts.new((x_scaled - w_scaled / 2, y_scaled + h_scaled / 2, 0))

    # Define the four top vertices (z = thickness)
    p1_top = bm.verts.new((p1.co.x, p1.co.y, t_scaled))
    p2_top = bm.verts.new((p2.co.x, p2.co.y, t_scaled))
    p3_top = bm.verts.new((p3.co.x, p3.co.y, t_scaled))
    p4_top = bm.verts.new((p4.co.x, p4.co.y, t_scaled))

    # Create bottom face
    bm.faces.new((p1, p2, p3, p4))
    
    # Create top face (for solid walls, unlike the experimental hollow version)
    bm.faces.new((p1_top, p4_top, p3_top, p2_top))

    # Create side faces
    bm.faces.new((p1, p2, p2_top, p1_top))
    bm.faces.new((p2, p3, p3_top, p2_top))
    bm.faces.new((p3, p4, p4_top, p3_top))
    bm.faces.new((p4, p1, p1_top, p4_top))

    bm.to_mesh(mesh)
    bm.free()

def main():
    json_path = get_json_path()
    if not json_path:
        print("Error: Could not find 'detected_objects.json'. Ensure it is in the same directory as the .blend file.")
        return

    print(f"Loading objects from: {json_path}")
    try:
        with open(json_path, 'r') as f:
            detected_objects = json.load(f)
    except Exception as e:
        print(f"Error reading JSON: {e}")
        return

    # Clear existing wall/door meshes to allow clean re-generation
    bpy.ops.object.select_all(action='DESELECT')
    for obj in list(bpy.data.objects):
        if obj.type == 'MESH' and (obj.name.startswith("wall") or obj.name.startswith("door")):
            bpy.data.objects.remove(obj, do_unlink=True)

    wall_count = 0
    door_count = 0

    for obj_data in detected_objects:
        if "box" in obj_data:
            x, y, w, h = obj_data["box"]
            cls = obj_data.get("class", "wall").lower()
            
            # Skip noise or generic elements if needed
            if cls not in ["wall", "door"]:
                continue
                
            # Calculate center location
            location = (x + w / 2.0, y + h / 2.0)
            
            # Set structural parameters (thickness/height in Blender meters)
            # Walls are taller (e.g. 3m), doors are shorter (e.g. 2.2m)
            if cls == "wall":
                thickness = 3.0
                wall_count += 1
                name = f"wall_{wall_count}"
            else:
                thickness = 2.2
                door_count += 1
                name = f"door_{door_count}"

            create_mesh(location, w, h, thickness, name)

    print(f"Successfully generated {wall_count} walls and {door_count} doors.")

if __name__ == "__main__":
    main()
