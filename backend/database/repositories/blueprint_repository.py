from backend.models.blueprint import Blueprint
from backend.extensions import db

class BlueprintRepository:
    @staticmethod
    def create(project_id, file_data):
        blueprint = Blueprint(
            project_id=project_id,
            original_filename=file_data['original_filename'],
            stored_filename=file_data['stored_filename'],
            file_path=file_data['file_path'],
            mime_type=file_data['mime_type'],
            file_size=file_data['file_size'],
            image_width=file_data['image_width'],
            image_height=file_data['image_height']
        )
        db.session.add(blueprint)
        db.session.commit()
        return blueprint

    @staticmethod
    def get_by_project_id(project_id):
        return Blueprint.query.filter_by(project_id=project_id).first()
