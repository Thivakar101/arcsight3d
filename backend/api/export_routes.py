from flask import Blueprint, request
from backend.controllers.export_controller import ExportController

export_bp = Blueprint('exports', __name__)

@export_bp.route('/<project_id>/generate', methods=['POST'])
def generate_model(project_id):
    return ExportController.generate_model(project_id, request)

@export_bp.route('/<project_id>/exports/<export_id>/download', methods=['GET'])
def download_export(project_id, export_id):
    return ExportController.download_export(project_id, export_id)
