from backend.models.project import Project
from backend.extensions import db

class ProjectRepository:
    @staticmethod
    def create(name, description=None):
        project = Project(name=name, description=description)
        db.session.add(project)
        db.session.commit()
        return project

    @staticmethod
    def get_by_public_id(public_id):
        return Project.query.filter_by(public_id=public_id).first()

    @staticmethod
    def list_projects(page=1, page_size=20):
        pagination = Project.query.order_by(Project.created_at.desc()).paginate(page=page, per_page=page_size, error_out=False)
        return pagination.items, pagination.total

    @staticmethod
    def delete(project):
        db.session.delete(project)
        db.session.commit()
