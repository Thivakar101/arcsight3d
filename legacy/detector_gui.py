import sys
import os
import json
import cv2
import numpy as np
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout, 
                             QHBoxLayout, QWidget, QLabel, QFileDialog, QProgressBar, 
                             QSpacerItem, QSizePolicy)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont

class ProcessingThread(QThread):
    progress_updated = pyqtSignal(int)
    status_updated = pyqtSignal(str)

    def __init__(self, blueprint_path):
        super().__init__()
        self.blueprint_path = blueprint_path

    def run(self):
        try:
            self.status_updated.emit(f"Processing blueprint: {os.path.basename(self.blueprint_path)}... Hang tight!")
            self.progress_updated.emit(10)
            
            image, detected_objects = self.process_blueprint(self.blueprint_path)
            self.progress_updated.emit(80)
            
            # Save output JSON relative to the script location
            script_dir = os.path.dirname(os.path.abspath(__file__))
            output_path = os.path.join(script_dir, 'detected_objects.json')
            
            with open(output_path, 'w') as f:
                json.dump(detected_objects, f, indent=4)
                
            self.progress_updated.emit(100)
            self.status_updated.emit(f"Done! Detected {len(detected_objects)} elements. Saved results to: detected_objects.json")
        except Exception as e:
            self.progress_updated.emit(0)
            self.status_updated.emit(f"Oops! Something went wrong: {str(e)}")

    def process_blueprint(self, image_path):
        # Load image
        image = cv2.imread(image_path)
        if image is None:
            raise FileNotFoundError(f"Could not load image at {image_path}")
        
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply Gaussian Blur to reduce noise
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Adaptive thresholding to handle uneven lighting and clear lines
        thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                       cv2.THRESH_BINARY_INV, 11, 2)
        
        # Morphological close to bridge small gaps
        kernel = np.ones((5, 5), np.uint8)
        morphed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
        
        # Find contours
        contours, _ = cv2.findContours(morphed, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        detected_objects = []

        for contour in contours:
            epsilon = 0.02 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)
            x, y, w, h = cv2.boundingRect(approx)

            # Avoid processing extremely small noise contours
            if w < 10 or h < 10:
                continue

            # Classify walls vs doors based on bounding box aspect ratio and geometry
            aspect_ratio_wall = (w / h > 3.0) or (h / w > 3.0)
            if len(approx) >= 4 and aspect_ratio_wall:
                detected_objects.append({
                    "class": "wall", 
                    "box": [int(x), int(y), int(w), int(h)]
                })
            elif w >= 20 and h >= 20:
                detected_objects.append({
                    "class": "door", 
                    "box": [int(x), int(y), int(w), int(h)]
                })

        return image, detected_objects

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.selected_file = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Arc Sight 3D - Blueprint Analyzer')
        self.setGeometry(100, 100, 800, 600)
        
        # Main layout
        self.layout = QVBoxLayout()
        self.main_layout = QHBoxLayout()
        
        # Branding Header
        self.label_layout = QVBoxLayout()
        self.label_layout.addSpacing(20)
        font = QFont("Arial", 48, QFont.Bold)
        
        self.arc_label = QLabel('ARC')
        self.arc_label.setFont(font)
        self.arc_label.setStyleSheet("color: #EFB11D; margin-left: 20px;")
        
        self.sight_label = QLabel('SIGHT 3D')
        self.sight_label.setFont(font)
        self.sight_label.setStyleSheet("color: white; margin-left: 20px;")
        
        self.label_layout.addWidget(self.arc_label)
        self.label_layout.addWidget(self.sight_label)
        self.main_layout.addLayout(self.label_layout)
        self.layout.addLayout(self.main_layout)

        self.layout.addStretch(1)

        # Centered action buttons and progress reporting
        button_layout = QVBoxLayout()
        button_layout.addSpacerItem(QSpacerItem(20, 50, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.select_button = QPushButton('Select Blueprint')
        self.select_button.clicked.connect(self.select_blueprint)
        self.select_button.setFixedWidth(400)
        
        self.process_button = QPushButton('Start Processing')
        self.process_button.clicked.connect(self.start_processing)
        self.process_button.setFixedWidth(400)
        
        button_layout.addWidget(self.select_button, alignment=Qt.AlignCenter)
        button_layout.addWidget(self.process_button, alignment=Qt.AlignCenter)

        # Progress elements
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximum(100)
        self.progress_bar.setFixedHeight(30)
        self.progress_bar.setFixedWidth(400)
        
        self.status_label = QLabel('Ready to analyze floor plan blueprints! 🚀')
        self.status_label.setAlignment(Qt.AlignCenter)
        
        button_layout.addWidget(self.progress_bar, alignment=Qt.AlignCenter)
        button_layout.addWidget(self.status_label, alignment=Qt.AlignCenter)

        button_layout.addSpacerItem(QSpacerItem(20, 50, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.layout.addLayout(button_layout)
        
        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

        # Sleek dark styling
        self.setStyleSheet("""
            QMainWindow { background-color: #121212; font-family: 'Arial', sans-serif; }
            QPushButton { 
                color: white; 
                background-color: #8A00C4; 
                border-radius: 20px; 
                padding: 12px; 
                font-size: 16pt; 
                font-weight: bold;
            }
            QPushButton:hover { background-color: #a124dc; }
            QProgressBar { 
                color: white; 
                background-color: #2D2D2D; 
                border-radius: 8px; 
                font-size: 12pt; 
                text-align: center;
                font-weight: bold; 
            }
            QProgressBar::chunk { background-color: #EFB11D; border-radius: 8px; }
            QLabel { color: white; font-family: 'Arial', sans-serif; font-size: 14pt; }
        """)

    def select_blueprint(self):
        # Open file dialog defaulting to the samples directory if it exists
        initial_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'samples')
        if not os.path.exists(initial_dir):
            initial_dir = ""
            
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open Blueprint Image", initial_dir, "Image Files (*.jpg *.png *.bmp *.webp)"
        )
        if file_path:
            self.selected_file = file_path
            self.status_label.setText(f"Selected: {os.path.basename(file_path)}")
            self.progress_bar.setValue(0)
        else:
            self.status_label.setText("No blueprint selected yet.")

    def start_processing(self):
        if self.selected_file:
            self.processing_thread = ProcessingThread(self.selected_file)
            self.processing_thread.progress_updated.connect(self.update_progress)
            self.processing_thread.status_updated.connect(self.update_status)
            self.processing_thread.start()
        else:
            self.status_label.setText("Please select a blueprint image first!")

    def update_progress(self, progress):
        self.progress_bar.setValue(progress)

    def update_status(self, status):
        self.status_label.setText(status)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
