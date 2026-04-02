from PyQt5.QtCore import QThread, pyqtSignal
from desktop.api_client import ApiClient

class UploadAndProcessWorker(QThread):
    progress = pyqtSignal(int)
    status = pyqtSignal(str)
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)
    
    def __init__(self, project_id, file_path, config):
        super().__init__()
        self.project_id = project_id
        self.file_path = file_path
        self.config = config
        self.client = ApiClient()
        
    def run(self):
        try:
            self.status.emit("Uploading blueprint...")
            self.progress.emit(20)
            self.client.upload_blueprint(self.project_id, self.file_path)
            
            self.status.emit("Processing image...")
            self.progress.emit(50)
            result = self.client.process_project(self.project_id, self.config)
            
            self.status.emit("Done!")
            self.progress.emit(100)
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))

class GenerationWorker(QThread):
    progress = pyqtSignal(int)
    status = pyqtSignal(str)
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)
    
    def __init__(self, project_id, config):
        super().__init__()
        self.project_id = project_id
        self.config = config
        self.client = ApiClient()
        
    def run(self):
        try:
            self.status.emit("Generating 3D model with Blender...")
            self.progress.emit(50)
            result = self.client.generate_model(self.project_id, self.config)
            
            self.status.emit("Model generated!")
            self.progress.emit(100)
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))
