from datetime import datetime
from backend.extensions import db

class ExportedModel(db.Model):
    __tablename__ = 'exported_models'

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id', ondelete='CASCADE'), nullable=False)
    format = db.Column(db.String(10), nullable=False)
    file_path = db.Column(db.String(512), nullable=False)
    file_size = db.Column(db.Integer, nullable=False)
    generated_at = db.Column(db.DateTime, default=datetime.utcnow)
    blender_version = db.Column(db.String(50), nullable=True)
    metadata_ = db.Column('metadata', db.JSON, nullable=True)

    project = db.relationship('Project', backref=db.backref('exported_models', lazy=True, cascade="all, delete-orphan"))

    def to_dict(self):
        return {
            "id": self.id,
            "format": self.format,
            "file_size": self.file_size,
            "generated_at": self.generated_at.isoformat() if self.generated_at else None
        }
