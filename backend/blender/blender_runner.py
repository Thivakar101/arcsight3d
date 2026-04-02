import os
import json
import subprocess
from flask import current_app

class BlenderRunner:
    @staticmethod
    def generate_scene(project, walls, doors, config):
        # 1. Create input JSON
        export_folder = current_app.config['EXPORT_FOLDER']
        temp_input = os.path.join(export_folder, f"temp_{project.public_id}.json")
        output_format = config.get("format", "glb").lower()
        output_file = os.path.join(export_folder, f"{project.public_id}.{output_format}")
        
        data = {
            "project_id": project.public_id,
            "scale_factor": config.get("scale_factor", current_app.config['DEFAULT_SCALE_FACTOR']),
            "wall_height": config.get("wall_height", current_app.config['DEFAULT_WALL_HEIGHT']),
            "wall_thickness": config.get("wall_thickness", current_app.config['DEFAULT_WALL_THICKNESS']),
            "walls": [w.to_dict() if hasattr(w, 'to_dict') else w for w in walls],
            "doors": [d.to_dict() if hasattr(d, 'to_dict') else d for d in doors],
            "windows": [],
            "rooms": []
        }
        
        with open(temp_input, 'w') as f:
            json.dump(data, f)
            
        script_path = os.path.join(os.path.dirname(__file__), 'scripts', 'generate_scene.py')
        blender_executable = current_app.config.get('BLENDER_EXECUTABLE', 'blender')
        
        # 2. Run Blender subprocess
        cmd = [
            blender_executable,
            "--background",
            "--python", script_path,
            "--",
            "--input", temp_input,
            "--output", output_file,
            "--format", output_format
        ]
        
        try:
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            # Log output if needed: current_app.logger.info(result.stdout)
        except subprocess.CalledProcessError as e:
            # We must handle the error properly, but for now we raise it
            raise RuntimeError(f"Blender failed: {e.stderr}")
        finally:
            if os.path.exists(temp_input):
                os.remove(temp_input)
                
        if not os.path.exists(output_file):
            raise FileNotFoundError("Blender script did not produce output file")
            
        file_size = os.path.getsize(output_file)
        if file_size == 0:
            os.remove(output_file)
            raise ValueError("Generated 3D model is empty")
            
        return output_file, output_format, file_size
