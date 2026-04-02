from backend.database.repositories.project_repository import ProjectRepository

class ProjectService:
    @staticmethod
    def create_project(data):
        name = data.get('name')
        description = data.get('description', '')

        if not name:
            raise ValueError("Project name is required")

        project = ProjectRepository.create(name=name, description=description)
        return project.to_dict()

    @staticmethod
    def get_project(public_id):
        project = ProjectRepository.get_by_public_id(public_id)
        if not project:
            return None
        
        data = project.to_dict()
        if project.blueprint:
            data['blueprint'] = project.blueprint.to_dict()
        else:
            data['blueprint'] = None
        
        return data

    @staticmethod
    def list_projects(page=1, page_size=20):
        projects, total = ProjectRepository.list_projects(page, page_size)
        return [p.to_dict() for p in projects], total

    @staticmethod
    def delete_project(public_id):
        project = ProjectRepository.get_by_public_id(public_id)
        if not project:
            return False
        ProjectRepository.delete(project)
        return True
