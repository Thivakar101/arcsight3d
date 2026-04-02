from flask import Blueprint, request, jsonify
from backend.controllers.project_controller import ProjectController

project_bp = Blueprint('projects', __name__)

@project_bp.route('', methods=['POST'])
def create_project():
    return ProjectController.create_project(request)

@project_bp.route('', methods=['GET'])
def list_projects():
    return ProjectController.list_projects(request)

@project_bp.route('/<project_id>', methods=['GET'])
def get_project(project_id):
    return ProjectController.get_project(project_id)

@project_bp.route('/<project_id>', methods=['DELETE'])
def delete_project(project_id):
    return ProjectController.delete_project(project_id)

@project_bp.route('/<project_id>/blueprint', methods=['POST'])
def upload_blueprint(project_id):
    return ProjectController.upload_blueprint(project_id, request)

@project_bp.route('/<project_id>/detections', methods=['GET'])
def get_detections(project_id):
    return ProjectController.get_detections(project_id, request)

@project_bp.route('/<project_id>/rooms', methods=['GET'])
def get_rooms(project_id):
    return ProjectController.get_rooms(project_id)

@project_bp.route('/<project_id>/jobs', methods=['GET'])
def get_jobs(project_id):
    return ProjectController.get_jobs(project_id)

@project_bp.route('/<project_id>/ocr', methods=['GET'])
def get_ocr(project_id):
    return ProjectController.get_ocr(project_id)
