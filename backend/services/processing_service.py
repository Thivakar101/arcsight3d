from backend.database.repositories.project_repository import ProjectRepository
from backend.database.repositories.blueprint_repository import BlueprintRepository
from backend.cv.detection_pipeline import DetectionPipeline

class ProcessingService:
    @staticmethod
    def start_processing(public_id, config):
        project = ProjectRepository.get_by_public_id(public_id)
        if not project:
            raise ValueError(f"Project {public_id} not found")
            
        blueprint = BlueprintRepository.get_by_project_id(project.id)
        if not blueprint:
            raise ValueError(f"No blueprint uploaded for project {public_id}")
            
        project.status = 'PROCESSING'
        from backend.extensions import db
        db.session.commit()
        
        mode = config.get("detection_mode", "auto")
        
        try:
            from backend.database.repositories.object_repository import ObjectRepository
            from backend.ocr.ocr_pipeline import OCRPipeline
            from flask import current_app
            
            # Synchronous processing for now
            detected_objects = DetectionPipeline.process(blueprint.file_path, mode)
            
            # Save to database
            ObjectRepository.save_detected_objects(project.id, detected_objects)
            
            ocr_count = 0
            if config.get("run_ocr", False):
                ocr_results = OCRPipeline.process(project.id, blueprint.file_path, current_app.config)
                ocr_count = len(ocr_results)
            
            project.status = 'DETECTED'
            db.session.commit()
            
            return {
                "message": "Processing complete",
                "detected_objects": len(detected_objects),
                "ocr_records": ocr_count
            }
        except Exception as e:
            project.status = 'FAILED'
            db.session.commit()
            raise e
