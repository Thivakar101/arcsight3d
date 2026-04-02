import os
import cv2
import uuid
from werkzeug.utils import secure_filename
from backend.config import config_by_name

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
ALLOWED_MIME_TYPES = {'image/png', 'image/jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def validate_image_file(file):
    if not file:
        raise ValueError("No file provided")
    if file.filename == '':
        raise ValueError("No file selected")
    if not allowed_file(file.filename):
        raise ValueError(f"Invalid file extension. Allowed: {ALLOWED_EXTENSIONS}")
    
    # We could do more thorough mimetype checking with python-magic, 
    # but for now we rely on extension and cv2 decoding.
    return True

def save_blueprint_image(file, project_id, app_config):
    original_filename = secure_filename(file.filename)
    extension = original_filename.rsplit('.', 1)[1].lower() if '.' in original_filename else 'png'
    stored_filename = f"{project_id}_{uuid.uuid4().hex}.{extension}"
    
    upload_folder = app_config['UPLOAD_FOLDER']
    os.makedirs(upload_folder, exist_ok=True)
    
    file_path = os.path.join(upload_folder, stored_filename)
    file.save(file_path)
    
    # Verify it's a valid image that OpenCV can read
    image = cv2.imread(file_path)
    if image is None:
        os.remove(file_path)
        raise ValueError("Uploaded file is not a valid or readable image")
        
    height, width = image.shape[:2]
    file_size = os.path.getsize(file_path)
    
    # MIME type derivation
    mime_type = "image/png" if extension == "png" else "image/jpeg"
    
    return {
        "original_filename": original_filename,
        "stored_filename": stored_filename,
        "file_path": file_path,
        "mime_type": mime_type,
        "file_size": file_size,
        "image_width": width,
        "image_height": height
    }
