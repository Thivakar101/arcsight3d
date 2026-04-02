import bpy
import json
import sys
import argparse
import math

def setup_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

def build_wall(wall, config):
    start_x = wall['start_x'] * config['scale_factor']
    start_y = -wall['start_y'] * config['scale_factor'] # Negate Y
    end_x = wall['end_x'] * config['scale_factor']
    end_y = -wall['end_y'] * config['scale_factor'] # Negate Y
    
    cx = (start_x + end_x) / 2
    cy = (start_y + end_y) / 2
    cz = config['wall_height'] / 2
    
    length = math.sqrt((end_x - start_x)**2 + (end_y - start_y)**2)
    angle = math.atan2(end_y - start_y, end_x - start_x)
    
    bpy.ops.mesh.primitive_cube_add(location=(cx, cy, cz))
    obj = bpy.context.object
    obj.name = f"Wall_{wall.get('id', 'unknown')}"
    obj.scale = (length / 2, config['wall_thickness'] / 2, config['wall_height'] / 2)
    obj.rotation_euler[2] = angle
    
def build_door(door, config):
    cx = door['center_x'] * config['scale_factor']
    cy = -door['center_y'] * config['scale_factor']
    cz = config['door_height'] / 2
    
    width = door.get('width', 20) * config['scale_factor']
    
    bpy.ops.mesh.primitive_cube_add(location=(cx, cy, cz))
    obj = bpy.context.object
    obj.name = f"Door_{door.get('id', 'unknown')}"
    # Make door blocks slightly thinner than walls for visibility
    obj.scale = (width / 2, config['wall_thickness'] / 4, config['door_height'] / 2)
    # If orientation is known, rotate. For now, simple box.

def export_scene(output_path, format="glb"):
    if format.lower() == "glb":
        bpy.ops.export_scene.gltf(filepath=output_path, export_format='GLB')
    elif format.lower() == "fbx":
        bpy.ops.export_scene.fbx(filepath=output_path)
    else:
        # Default GLB
        bpy.ops.export_scene.gltf(filepath=output_path, export_format='GLB')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--format", default="glb")
    
    # Handle arguments passed after '--'
    if "--" in sys.argv:
        argv = sys.argv[sys.argv.index("--") + 1:]
    else:
        argv = []
        
    args, unknown = parser.parse_known_args(argv)
    
    with open(args.input, 'r') as f:
        data = json.load(f)
        
    config = {
        "scale_factor": data.get("scale_factor", 0.05),
        "wall_height": data.get("wall_height", 3.0),
        "wall_thickness": data.get("wall_thickness", 0.15),
        "door_height": 2.2
    }
    
    setup_scene()
    
    for wall in data.get('walls', []):
        build_wall(wall, config)
        
    for door in data.get('doors', []):
        build_door(door, config)
        
    # We could add floor builder from rooms here
    
    export_scene(args.output, args.format)
    print(f"Exported to {args.output}")

if __name__ == "__main__":
    main()
