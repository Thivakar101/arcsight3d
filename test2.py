import bpy
import math

# Scale factor to increase the overall size of the model
scale_factor = 2.0  # Adjust this value for different sizes

# Function to create walls with optional door gaps
def create_wall(start, end, height=3, door_position=None, door_width=1, door_height=2.5):
    # Scale the height
    scaled_height = height * scale_factor
    scaled_door_height = door_height * scale_factor
    scaled_door_width = door_width * scale_factor
    
    # Calculate center point
    cx = (start[0] + end[0]) / 2
    cy = (start[1] + end[1]) / 2
    
    # Calculate wall length and scale it
    length = math.sqrt((end[0] - start[0])*2 + (end[1] - start[1])*2) * scale_factor
    
    # Create the main wall
    bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(cx, cy, scaled_height / 2))
    wall = bpy.context.object
    wall.scale = (length / 2, 0.1 * scale_factor, scaled_height / 2)  # Scale to create a long, thin wall
    
    # Calculate rotation angle
    angle = math.atan2(end[1] - start[1], end[0] - start[0])
    wall.rotation_euler[2] = angle  # Rotate the wall to face the right direction
    
    # If a door position is specified, cut out a section of the wall
    if door_position:
        # Door center calculation
        door_cx = (start[0] + door_position[0]) / 2
        door_cy = (start[1] + door_position[1]) / 2

        # Create a smaller cube to subtract the door area from the wall
        bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=(door_cx, door_cy, scaled_door_height / 2))
        door_cut = bpy.context.object
        door_cut.scale = (scaled_door_width / 2, 0.1 * scale_factor, scaled_door_height / 2)

        # Set the boolean modifier to subtract the door space from the wall
        bool_mod = wall.modifiers.new(type="BOOLEAN", name="Door Cutout")
        bool_mod.object = door_cut
        bool_mod.operation = 'DIFFERENCE'
        bpy.context.view_layer.objects.active = wall
        bpy.ops.object.modifier_apply(modifier=bool_mod.name)
        
        # Remove the door object now that the cutout is done
        bpy.data.objects.remove(door_cut)

# Coordinates for walls with doors added for retail spaces
wall_coords = [
    # B Site (upper-left side of the map)
    [(0, 0), (15, 0), (7.5, 0)],  # Bottom wall with door
    [(15, 0), (15, 12), None],  # Right wall
    [(15, 12), (0, 12), None],  # Top wall
    [(0, 12), (0, 0), None],  # Left wall

    # B Boat House (above B Site)
    [(0, 12), (10, 12), (5, 12)],  # Bottom wall with door
    [(10, 12), (10, 18), None],  # Right wall
    [(10, 18), (0, 18), None],  # Top wall
    [(0, 18), (0, 12), None],  # Left wall

    # Mid Market
    [(15, 0), (25, 0), (20, 0)],  # Bottom wall with door
    [(25, 0), (25, 10), None],  # Right wall
    [(25, 10), (15, 10), None],  # Top wall
    [(15, 10), (15, 0), None],  # Left wall

    # Mid Plaza (center of the map)
    [(25, 0), (35, 0), (30, 0)],  # Bottom wall with door
    [(35, 0), (35, 15), None],  # Right wall
    [(35, 15), (25, 15), None],  # Top wall
    [(25, 15), (25, 0), None],  # Left wall

    # A Site (lower-right side of the map)
    [(35, 0), (45, 0), (40, 0)],  # Bottom wall with door
    [(45, 0), (45, 20), None],  # Right wall
    [(45, 20), (35, 20), None],  # Top wall
    [(35, 20), (35, 0), None],  # Left wall

    # A Rafters (upper-right side of A Site)
    [(45, 20), (55, 20), (50, 20)],  # Bottom wall with door
    [(55, 20), (55, 30), None],  # Right wall
    [(55, 30), (45, 30), None],  # Top wall
    [(45, 30), (45, 20), None],  # Left wall

    # Additional sections (like Mid Cubby, B Main, A Lobby) can be defined similarly
]

# Create walls with doors for the mall
for coord in wall_coords:
    create_wall(coord[0], coord[1], height=3, door_position=coord[2])  # Pass door position for walls with doors