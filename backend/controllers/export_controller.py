from backend.services.export_service import ExportService
from backend.utils.response import success_response, error_response
from flask import send_file
import os

class ExportController:
    @staticmethod
    def generate_model(project_id, request):
        config = request.get_json() or {}
        try:
            result = ExportService.generate_model(project_id, config)
            return success_response(data=result, status_code=201)
        except ValueError as e:
            return error_response("VALIDATION_ERROR", str(e))
        except Exception as e:
            return error_response("INTERNAL_ERROR", "Failed to generate 3D model", details={"error": str(e)}, status_code=500)

    @staticmethod
    def download_export(project_id, export_id):
        try:
            from backend.models.exported_model import ExportedModel
            export = ExportedModel.query.get(export_id)
            if not export or str(export.project.public_id) != str(project_id):
                return error_response("NOT_FOUND", "Export not found", status_code=404)
                
            if not os.path.exists(export.file_path):
                return error_response("NOT_FOUND", "Export file not found on disk", status_code=404)
                
            return send_file(export.file_path, as_attachment=True)
        except Exception as e:
            return error_response("INTERNAL_ERROR", "Failed to download export", details={"error": str(e)}, status_code=500)
