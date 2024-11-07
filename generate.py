import bpy
import mathutils
import json

def create_wall_from_line(start, end, height):
    """
    Create a 3D wall from a 2D line.
    
    Args:
        start (tuple): Starting point of the wall (x, y).
        end (tuple): Ending point of the wall (x, y).
        height (float): The height of the wall.
    """
    # Convert the 2D coordinates into 3D vectors
    start_vec = mathutils.Vector((start[0], start[1], 0))
    end_vec = mathutils.Vector((end[0], end[1], 0))
    
    # Define the vertices for the wall (four vertices)
    vertices = [
        (start_vec.x, start_vec.y, 0),  # Bottom-left
        (end_vec.x, end_vec.y, 0),      # Bottom-right
        (end_vec.x, end_vec.y, height), # Top-right
        (start_vec.x, start_vec.y, height)  # Top-left
    ]

    # Create a new mesh and link it to the object
    mesh = bpy.data.meshes.new("WallMesh")
    wall = bpy.data.objects.new("Wall", mesh)
    bpy.context.collection.objects.link(wall)

    # Define the faces of the wall
    faces = [(0, 1, 2, 3)]  # Single face for the wall

    # Create the mesh from the vertices and face
    mesh.from_pydata(vertices, [], faces)
    mesh.update()

def generate_walls_from_json(json_file_path, height):
    """
    Generate walls based on coordinates in a JSON file.
    
    Args:
        json_file_path (str): Path to the JSON file containing line coordinates.
        height (float): The height of the walls.
    """
    with open(json_file_path, 'r') as f:
        line_coordinates = json.load(f)
    
    # Create a wall for each line in the coordinates
    for line in line_coordinates:
        start, end = line
        create_wall_from_line(start, end, height)

# Example usage
json_file_path = r"C:\Users\Admin\Desktop\2dto3d\line_coordinates.json"
generate_walls_from_json(json_file_path, height=3.0)
