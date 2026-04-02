from backend.database.repositories.project_repository import ProjectRepository
from backend.models.wall import Wall
from backend.models.door import Door
from backend.models.exported_model import ExportedModel
from backend.blender.blender_runner import BlenderRunner
from backend.extensions import db

class ExportService:
    @staticmethod
    def generate_model(public_id, config):
        project = ProjectRepository.get_by_public_id(public_id)
        if not project:
            raise ValueError(f"Project {public_id} not found")
            
        walls = Wall.query.filter_by(project_id=project.id).all()
        doors = Door.query.filter_by(project_id=project.id).all()
        
        project.status = 'GENERATING_3D'
        db.session.commit()
        
        try:
            output_file, format, file_size = BlenderRunner.generate_scene(project, walls, doors, config)
            
            exported = ExportedModel(
                project_id=project.id,
                format=format,
                file_path=output_file,
                file_size=file_size
            )
            db.session.add(exported)
            
            project.status = 'EXPORTED'
            db.session.commit()
            
            return exported.to_dict()
            
        except Exception as e:
            project.status = 'FAILED'
            db.session.commit()
            raise e
