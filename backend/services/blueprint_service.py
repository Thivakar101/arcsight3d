from backend.database.repositories.project_repository import ProjectRepository
from backend.database.repositories.blueprint_repository import BlueprintRepository
from backend.utils.image_utils import validate_image_file, save_blueprint_image
from flask import current_app
import os

class BlueprintService:
    @staticmethod
    def upload_blueprint(public_id, file):
        # 1. Get project
        project = ProjectRepository.get_by_public_id(public_id)
        if not project:
            raise ValueError(f"Project with ID {public_id} not found")

        # 2. Validate file
        validate_image_file(file)
        
        # 3. Check if project already has a blueprint, if so delete old one
        existing = BlueprintRepository.get_by_project_id(project.id)
        if existing:
            # We don't delete the physical file right now for safety, but we could.
            pass

        # 4. Save to disk
        file_data = save_blueprint_image(file, project.id, current_app.config)

        # 5. Save to database
        blueprint = BlueprintRepository.create(project.id, file_data)
        
        # 6. Update project status
        project.status = 'UPLOADED'
        from backend.extensions import db
        db.session.commit()

        return blueprint.to_dict()
