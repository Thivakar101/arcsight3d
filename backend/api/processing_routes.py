from flask import Blueprint, request
from backend.services.processing_service import ProcessingService
from backend.utils.response import success_response, error_response

processing_bp = Blueprint('processing', __name__)

@processing_bp.route('/<project_id>/process', methods=['POST'])
def process_project(project_id):
    config = request.get_json() or {}
    
    try:
        result = ProcessingService.start_processing(project_id, config)
        return success_response(data=result)
    except ValueError as e:
        if "not found" in str(e).lower():
            return error_response("NOT_FOUND", str(e), status_code=404)
        return error_response("VALIDATION_ERROR", str(e), status_code=400)
    except Exception as e:
        return error_response("INTERNAL_ERROR", "Failed to process project", details={"error": str(e)}, status_code=500)
