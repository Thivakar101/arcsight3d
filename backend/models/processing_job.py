from datetime import datetime
from backend.extensions import db

class ProcessingJob(db.Model):
    __tablename__ = 'processing_jobs'

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id', ondelete='CASCADE'), nullable=False)
    job_type = db.Column(db.String(100), nullable=False) # IMAGE_PREPROCESSING, CONTOUR_DETECTION, etc.
    status = db.Column(db.String(50), nullable=False, default='PENDING')
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime, nullable=True)
    processing_time_ms = db.Column(db.Integer, nullable=True)
    message = db.Column(db.Text, nullable=True)
    error_details = db.Column(db.Text, nullable=True)
    metrics = db.Column(db.JSON, nullable=True)

    project = db.relationship('Project', backref=db.backref('processing_jobs', lazy=True, cascade="all, delete-orphan"))
