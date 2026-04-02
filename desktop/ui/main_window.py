import sys
import os
from PyQt5.QtWidgets import (QMainWindow, QPushButton, QVBoxLayout, 
                             QHBoxLayout, QWidget, QLabel, QFileDialog, QProgressBar, 
                             QSpacerItem, QSizePolicy, QLineEdit, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from desktop.api_client import ApiClient
from desktop.workers import UploadAndProcessWorker, GenerationWorker

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.api = ApiClient()
        self.project_id = None
        self.selected_file = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('ArcSight 3D')
        self.setGeometry(100, 100, 800, 600)
        
        layout = QVBoxLayout()
        
        # Header
        header = QLabel('ARC SIGHT 3D')
        header.setFont(QFont("Arial", 36, QFont.Bold))
        header.setStyleSheet("color: #EFB11D;")
        layout.addWidget(header, alignment=Qt.AlignCenter)
        
        layout.addSpacing(20)
        
        # Project Input
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Project Name")
        layout.addWidget(self.name_input)
        
        self.desc_input = QLineEdit()
        self.desc_input.setPlaceholderText("Project Description")
        layout.addWidget(self.desc_input)
        
        layout.addSpacing(20)
        
        # File Selection
        self.select_btn = QPushButton('Select Blueprint')
        self.select_btn.clicked.connect(self.select_file)
        layout.addWidget(self.select_btn)
        
        self.file_label = QLabel('No file selected')
        layout.addWidget(self.file_label)
        
        layout.addSpacing(20)
        
        # Process Button
        self.process_btn = QPushButton('Upload & Process')
        self.process_btn.clicked.connect(self.start_processing)
        layout.addWidget(self.process_btn)
        
        # Generation Button
        self.generate_btn = QPushButton('Generate 3D Model (GLB)')
        self.generate_btn.clicked.connect(self.generate_model)
        self.generate_btn.setEnabled(False)
        layout.addWidget(self.generate_btn)
        
        layout.addSpacing(20)
        
        # Progress and Status
        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_bar)
        
        self.status_label = QLabel('Ready')
        layout.addWidget(self.status_label)
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Blueprint", "", "Images (*.png *.jpg *.jpeg)")
        if file_path:
            self.selected_file = file_path
            self.file_label.setText(os.path.basename(file_path))
            
    def start_processing(self):
        if not self.selected_file or not self.name_input.text():
            QMessageBox.warning(self, "Error", "Please provide a name and select a blueprint.")
            return
            
        try:
            # Create project first (synchronously for simplicity here)
            proj = self.api.create_project(self.name_input.text(), self.desc_input.text())
            self.project_id = proj['data']['id']
            
            self.process_btn.setEnabled(False)
            config = {"detection_mode": "auto", "run_ocr": True}
            
            self.worker = UploadAndProcessWorker(self.project_id, self.selected_file, config)
            self.worker.progress.connect(self.progress_bar.setValue)
            self.worker.status.connect(self.status_label.setText)
            self.worker.finished.connect(self.on_processing_done)
            self.worker.error.connect(self.on_error)
            self.worker.start()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to create project: {e}")

    def on_processing_done(self, result):
        self.process_btn.setEnabled(True)
        self.generate_btn.setEnabled(True)
        QMessageBox.information(self, "Success", "Processing complete!")
        
    def generate_model(self):
        if not self.project_id:
            return
            
        self.generate_btn.setEnabled(False)
        config = {"format": "glb"}
        self.gen_worker = GenerationWorker(self.project_id, config)
        self.gen_worker.progress.connect(self.progress_bar.setValue)
        self.gen_worker.status.connect(self.status_label.setText)
        self.gen_worker.finished.connect(self.on_generation_done)
        self.gen_worker.error.connect(self.on_error)
        self.gen_worker.start()
        
    def on_generation_done(self, result):
        self.generate_btn.setEnabled(True)
        export_id = result['data']['id']
        QMessageBox.information(self, "Success", f"Model generated! Ready to download export ID: {export_id}")
        
    def on_error(self, err_msg):
        self.process_btn.setEnabled(True)
        self.generate_btn.setEnabled(True)
        self.status_label.setText("Error occurred")
        QMessageBox.critical(self, "Error", err_msg)
