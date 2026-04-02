from backend.extensions import db

class OCRText(db.Model):
    __tablename__ = 'ocr_texts'

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id', ondelete='CASCADE'), nullable=False)
    text = db.Column(db.String(512), nullable=False)
    normalized_text = db.Column(db.String(512), nullable=True)
    text_type = db.Column(db.String(50), nullable=True) # ROOM_NAME, DIMENSION, ANNOTATION, UNKNOWN
    x = db.Column(db.Float, nullable=True)
    y = db.Column(db.Float, nullable=True)
    width = db.Column(db.Float, nullable=True)
    height = db.Column(db.Float, nullable=True)
    confidence = db.Column(db.Float, nullable=True)
    parsed_value = db.Column(db.JSON, nullable=True)

    project = db.relationship('Project', backref=db.backref('ocr_texts', lazy=True, cascade="all, delete-orphan"))
