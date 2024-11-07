import bpy
import json
import bmesh

def create_mesh(location, width, height, thickness, name):
    # Create a new mesh and object
    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)

    # Create a bmesh to hold the mesh data
    bm = bmesh.new()

    # Define the four bottom vertices
    p1 = bm.verts.new((location[0] - width / 2, location[1] - height / 2, 0))  # Bottom left
    p2 = bm.verts.new((location[0] + width / 2, location[1] - height / 2, 0))  # Bottom right
    p3 = bm.verts.new((location[0] + width / 2, location[1] + height / 2, 0))  # Top right
    p4 = bm.verts.new((location[0] - width / 2, location[1] + height / 2, 0))  # Top left

    # Define the four top vertices at the specified thickness
    p1_top = bm.verts.new((p1.co.x, p1.co.y, thickness))
    p2_top = bm.verts.new((p2.co.x, p2.co.y, thickness))
    p3_top = bm.verts.new((p3.co.x, p3.co.y, thickness))
    p4_top = bm.verts.new((p4.co.x, p4.co.y, thickness))

    # Create faces for the bottom
    bm.faces.new((p1, p2, p3, p4))  # Bottom face

    # Create faces for the sides (removing the top face)
    bm.faces.new((p1, p2, p2_top, p1_top))  # Side 1
    bm.faces.new((p2, p3, p3_top, p2_top))  # Side 2
    bm.faces.new((p3, p4, p4_top, p3_top))  # Side 3
    bm.faces.new((p4, p1, p1_top, p4_top))  # Side 4

    # Finish the mesh and update it
    bm.to_mesh(mesh)
    bm.free()

def main():
    # Load detected objects from JSON using absolute path
    try:
        with open(r'C:\koduu\metacrafters01-main\detected_objects.json', 'r') as f:
            detected_objects = json.load(f)
    except FileNotFoundError:
        print("Error: The JSON file was not found.")
        return
    except json.JSONDecodeError:
        print("Error: Failed to decode JSON.")
        return

    for obj in detected_objects:
        if "box" in obj:
            box = obj["box"]
            x, y, width, height = box
            
            # Skip lines if needed
            if obj["class"] == "detected line":
                continue  # Skip lines for now
            
            # Calculate location for the mesh
            location = (x + width / 2.0, y + height / 2.0, 0)  # Center the mesh

            thickness = 10.0  # Set the desired thickness here
            create_mesh(location, width, height, thickness, obj.get("class", "Mesh"))

# Clear existing objects in the scene
bpy.ops.object.select_all(action='DESELECT')
bpy.ops.object.select_by_type(type='MESH')
bpy.ops.object.delete(use_global=False)

# Run the main function
main()
