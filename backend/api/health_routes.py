from flask import Blueprint, jsonify

health_bp = Blueprint('health', __name__)

@health_bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        "success": True,
        "data": {
            "status": "healthy",
            "database": "connected", # In a real scenario, you'd check DB connection here
            "tesseract": "available", # Will implement actual checks later
            "blender": "available"    # Will implement actual checks later
        },
        "error": None,
        "meta": {}
    }), 200
