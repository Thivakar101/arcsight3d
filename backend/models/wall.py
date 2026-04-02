from backend.extensions import db

class Wall(db.Model):
    __tablename__ = 'walls'

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id', ondelete='CASCADE'), nullable=False)
    detected_object_id = db.Column(db.Integer, db.ForeignKey('detected_objects.id', ondelete='CASCADE'), nullable=True)
    start_x = db.Column(db.Float, nullable=False)
    start_y = db.Column(db.Float, nullable=False)
    end_x = db.Column(db.Float, nullable=False)
    end_y = db.Column(db.Float, nullable=False)
    pixel_length = db.Column(db.Float, nullable=True)
    real_length = db.Column(db.Float, nullable=True)
    thickness = db.Column(db.Float, nullable=True)
    height = db.Column(db.Float, nullable=True)
    orientation = db.Column(db.String(50), nullable=True)
    confidence = db.Column(db.Float, nullable=True)

    project = db.relationship('Project', backref=db.backref('walls', lazy=True, cascade="all, delete-orphan"))
    detected_object = db.relationship('DetectedObject')

    def to_dict(self):
        return {
            "id": self.id,
            "start_x": self.start_x,
            "start_y": self.start_y,
            "end_x": self.end_x,
            "end_y": self.end_y,
            "thickness": self.thickness,
            "height": self.height
        }
