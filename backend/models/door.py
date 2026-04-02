from backend.extensions import db

class Door(db.Model):
    __tablename__ = 'doors'

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id', ondelete='CASCADE'), nullable=False)
    detected_object_id = db.Column(db.Integer, db.ForeignKey('detected_objects.id', ondelete='CASCADE'), nullable=True)
    center_x = db.Column(db.Float, nullable=False)
    center_y = db.Column(db.Float, nullable=False)
    width = db.Column(db.Float, nullable=False)
    height = db.Column(db.Float, nullable=False)
    orientation = db.Column(db.String(50), nullable=True)
    parent_wall_id = db.Column(db.Integer, db.ForeignKey('walls.id', ondelete='SET NULL'), nullable=True)
    confidence = db.Column(db.Float, nullable=True)

    project = db.relationship('Project', backref=db.backref('doors', lazy=True, cascade="all, delete-orphan"))
    detected_object = db.relationship('DetectedObject')
    parent_wall = db.relationship('Wall')

    def to_dict(self):
        return {
            "id": self.id,
            "center_x": self.center_x,
            "center_y": self.center_y,
            "width": self.width,
            "height": self.height
        }
