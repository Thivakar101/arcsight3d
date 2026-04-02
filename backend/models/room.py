from backend.extensions import db

class Room(db.Model):
    __tablename__ = 'rooms'

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id', ondelete='CASCADE'), nullable=False)
    name = db.Column(db.String(255), nullable=True)
    polygon = db.Column(db.JSON, nullable=True)
    center_x = db.Column(db.Float, nullable=True)
    center_y = db.Column(db.Float, nullable=True)
    area_pixels = db.Column(db.Float, nullable=True)
    estimated_area = db.Column(db.Float, nullable=True)
    width = db.Column(db.Float, nullable=True)
    length = db.Column(db.Float, nullable=True)
    confidence = db.Column(db.Float, nullable=True)

    project = db.relationship('Project', backref=db.backref('project_rooms', lazy=True, cascade="all, delete-orphan"))
