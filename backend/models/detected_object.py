from datetime import datetime
from backend.extensions import db

class DetectedObject(db.Model):
    __tablename__ = 'detected_objects'

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id', ondelete='CASCADE'), nullable=False)
    object_type = db.Column(db.String(50), nullable=False) # WALL, DOOR, WINDOW, ROOM, TEXT, UNKNOWN
    x = db.Column(db.Float, nullable=True)
    y = db.Column(db.Float, nullable=True)
    width = db.Column(db.Float, nullable=True)
    height = db.Column(db.Float, nullable=True)
    x1 = db.Column(db.Float, nullable=True)
    y1 = db.Column(db.Float, nullable=True)
    x2 = db.Column(db.Float, nullable=True)
    y2 = db.Column(db.Float, nullable=True)
    angle = db.Column(db.Float, nullable=True)
    confidence = db.Column(db.Float, nullable=True)
    metadata_ = db.Column('metadata', db.JSON, nullable=True) # Using metadata_ as attribute to avoid collision with SQLAlchemy's metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships to specific tables can be added if we use joined table inheritance,
    # but for simplicity we will just map them explicitly or use this as a base table
    # or just rely on this table as requested. Wait, the prompt lists Wall, Door, etc as separate tables.
    
    project = db.relationship('Project', backref=db.backref('detected_objects', lazy=True, cascade="all, delete-orphan"))
