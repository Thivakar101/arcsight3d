from backend.services.project_service import ProjectService
from backend.utils.response import success_response, error_response

class ProjectController:
    @staticmethod
    def create_project(request):
        data = request.get_json()
        if not data:
            return error_response("INVALID_REQUEST", "Invalid or missing JSON payload")

        try:
            project_data = ProjectService.create_project(data)
            return success_response(data=project_data, status_code=201)
        except ValueError as e:
            return error_response("VALIDATION_ERROR", str(e))
        except Exception as e:
            return error_response("INTERNAL_ERROR", "Failed to create project", details={"error": str(e)}, status_code=500)

    @staticmethod
    def get_project(project_id):
        try:
            project_data = ProjectService.get_project(project_id)
            if not project_data:
                return error_response("NOT_FOUND", "Project not found", status_code=404)
            return success_response(data=project_data)
        except Exception as e:
            return error_response("INTERNAL_ERROR", "Failed to retrieve project", details={"error": str(e)}, status_code=500)

    @staticmethod
    def list_projects(request):
        try:
            page = int(request.args.get('page', 1))
            page_size = int(request.args.get('page_size', 20))
            
            projects, total = ProjectService.list_projects(page, page_size)
            meta = {
                "page": page,
                "page_size": page_size,
                "total": total
            }
            return success_response(data=projects, meta=meta)
        except ValueError:
            return error_response("VALIDATION_ERROR", "Invalid pagination parameters")
        except Exception as e:
            return error_response("INTERNAL_ERROR", "Failed to list projects", details={"error": str(e)}, status_code=500)

    @staticmethod
    def delete_project(project_id):
        try:
            success = ProjectService.delete_project(project_id)
            if not success:
                return error_response("NOT_FOUND", "Project not found", status_code=404)
            return success_response(data={"message": "Project deleted successfully"})
        except Exception as e:
            return error_response("INTERNAL_ERROR", "Failed to delete project", details={"error": str(e)}, status_code=500)

    @staticmethod
    def upload_blueprint(project_id, request):
        if 'file' not in request.files:
            return error_response("INVALID_REQUEST", "No file part in the request")
        
        file = request.files['file']
        
        try:
            from backend.services.blueprint_service import BlueprintService
            blueprint_data = BlueprintService.upload_blueprint(project_id, file)
            return success_response(data=blueprint_data, status_code=201)
        except ValueError as e:
            if "not found" in str(e).lower():
                return error_response("NOT_FOUND", str(e), status_code=404)
            return error_response("INVALID_IMAGE", str(e), status_code=400)
        except Exception as e:
            return error_response("INTERNAL_ERROR", "Failed to upload blueprint", details={"error": str(e)}, status_code=500)

    @staticmethod
    def get_detections(project_id, request):
        try:
            from backend.models.detected_object import DetectedObject
            from backend.extensions import db
            # In a real app, this should be in a service layer
            detections = DetectedObject.query.filter_by(project_id=project_id).all()
            
            data = []
            for d in detections:
                data.append({
                    "id": d.id,
                    "object_type": d.object_type,
                    "x": d.x, "y": d.y, "width": d.width, "height": d.height,
                    "x1": d.x1, "y1": d.y1, "x2": d.x2, "y2": d.y2,
                    "confidence": d.confidence
                })
            return success_response(data=data)
        except Exception as e:
            return error_response("INTERNAL_ERROR", "Failed to get detections", details={"error": str(e)}, status_code=500)

    @staticmethod
    def get_rooms(project_id):
        try:
            from backend.models.room import Room
            rooms = Room.query.filter_by(project_id=project_id).all()
            # Serialize logic here
            return success_response(data=[])
        except Exception as e:
            return error_response("INTERNAL_ERROR", "Failed to get rooms", details={"error": str(e)}, status_code=500)

    @staticmethod
    def get_jobs(project_id):
        try:
            from backend.models.processing_job import ProcessingJob
            jobs = ProcessingJob.query.filter_by(project_id=project_id).all()
            return success_response(data=[])
        except Exception as e:
            return error_response("INTERNAL_ERROR", "Failed to get jobs", details={"error": str(e)}, status_code=500)

    @staticmethod
    def get_ocr(project_id):
        try:
            from backend.models.ocr_text import OCRText
            ocr_records = OCRText.query.filter_by(project_id=project_id).all()
            data = []
            for r in ocr_records:
                data.append({
                    "id": r.id,
                    "text": r.text,
                    "normalized_text": r.normalized_text,
                    "text_type": r.text_type,
                    "x": r.x, "y": r.y, "width": r.width, "height": r.height,
                    "confidence": r.confidence,
                    "parsed_value": r.parsed_value
                })
            return success_response(data=data)
        except Exception as e:
            return error_response("INTERNAL_ERROR", "Failed to get OCR records", details={"error": str(e)}, status_code=500)
