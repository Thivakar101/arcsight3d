import sys
import json
import cv2
import numpy as np
import pytesseract
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QFileDialog, QProgressBar, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QFont

class ProcessingThread(QThread):
    progress_updated = pyqtSignal(int)
    status_updated = pyqtSignal(str)

    def __init__(self, blueprint_path):
        super().__init__()
        self.blueprint_path = blueprint_path

    def run(self):
        try:
            self.status_updated.emit(f'Processing blueprint: {self.blueprint_path}... Hold onto your hats!')
            image, detected_objects = self.process_blueprint(self.blueprint_path)
            self.status_updated.emit("Done! I’ve detected objects like a pro. You're welcome.")
            for i in range(101):
                self.progress_updated.emit(i)
                QThread.msleep(10)
        except Exception as e:
            self.status_updated.emit(f'Whoops! Something went wrong: {str(e)}. Maybe I need more coffee?')

    def process_blueprint(self, image_path):
        image = cv2.imread(image_path)
        if image is None:
            raise FileNotFoundError(f"Uh-oh! Couldn't find the image at {image_path}. Did you hide it from me?")
        
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        text_mask = np.zeros_like(gray)
        ocr_results = pytesseract.image_to_boxes(gray)

        for box in ocr_results.splitlines():
            b = box.split(' ')
            x, y, w, h = int(b[1]), int(b[2]), int(b[3]), int(b[4])
            cv2.rectangle(text_mask, (x, y), (w, h), 255, -1)

        blurred = cv2.bitwise_and(blurred, cv2.bitwise_not(text_mask))
        thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                       cv2.THRESH_BINARY_INV, 11, 2)
        kernel = np.ones((5, 5), np.uint8)
        morphed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
        contours, _ = cv2.findContours(morphed, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        detected_objects = []

        for contour in contours:
            epsilon = 0.02 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)
            x, y, w, h = cv2.boundingRect(approx)

            if len(approx) >= 4 and w / h > 3 or h / w > 3:
                detected_objects.append({"class": "wall", "box": [x, y, w, h]})
            elif w >= 20 and h >= 20:
                detected_objects.append({"class": "door", "box": [x, y, w, h]})

        with open('detected_objects.json', 'w') as f:
            json.dump(detected_objects, f)

        return image, detected_objects

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Arc Sight 3D')
        self.setGeometry(100, 100, 1600, 1200)
        
        # Main layout and styling
        self.layout = QVBoxLayout()
        self.main_layout = QHBoxLayout()
        self.label_layout = QVBoxLayout()
        self.label_layout.addSpacing(20)

        # "ARC" and "SIGHT 3D" labels with new font and colors
        font = QFont("Arial", 100, QFont.Bold)
        self.arc_label = QLabel('ARC')
        self.arc_label.setFont(font)
        self.arc_label.setStyleSheet("color: white; margin-left: 20px;")
        self.sight_label = QLabel('SIGHT 3D')
        self.sight_label.setFont(font)
        self.sight_label.setStyleSheet("color: white; margin-left: 20px;")
        
        self.label_layout.addWidget(self.arc_label)
        self.label_layout.addWidget(self.sight_label)
        self.main_layout.addLayout(self.label_layout)
        self.layout.addLayout(self.main_layout)

        # Spacer for visual balance
        self.layout.addStretch(1)

        # Centered button layout
        button_layout = QVBoxLayout()
        
        # Spacer above buttons to push them towards the center
        button_layout.addSpacerItem(QSpacerItem(20, 200, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.select_button = QPushButton('Select Blueprint')
        self.select_button.clicked.connect(self.select_blueprint)
        self.select_button.setFixedWidth(400)
        
        self.process_button = QPushButton('Start Processing')
        self.process_button.clicked.connect(self.start_processing)
        self.process_button.setFixedWidth(400)
        
        button_layout.addWidget(self.select_button, alignment=Qt.AlignCenter)
        button_layout.addWidget(self.process_button, alignment=Qt.AlignCenter)

        # Progress bar and status label centered with buttons
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximum(100)
        self.progress_bar.setFixedHeight(40)
        
        self.status_label = QLabel('Ready to rock and roll! 🎸')
        self.status_label.setAlignment(Qt.AlignCenter)
        
        button_layout.addWidget(self.progress_bar, alignment=Qt.AlignCenter)
        button_layout.addWidget(self.status_label, alignment=Qt.AlignCenter)

        # Spacer below buttons to keep them at the center
        button_layout.addSpacerItem(QSpacerItem(20, 200, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.layout.addLayout(button_layout)
        
        self.container = QWidget()
        self.container.setLayout(self.layout)
        self.setCentralWidget(self.container)

        # Set the styles
        self.setStyleSheet(f"""
            QMainWindow {{ background-color: black; font-family: 'Arial', sans-serif; }}
            QPushButton {{ color: white; background-color: #8A00C4; border-radius: 30px; padding: 20px; font-size: 24pt; }}
            QPushButton:hover {{ background-color:#9966CC ; }}
            QProgressBar {{ color: white; background-color: #444; border-radius: 10px; font-size: 18pt; font-weight: bold; }}
            QProgressBar::chunk {{ background-color: #8A00C4; }}
            QLabel {{ color: white; font-family: 'Arial', sans-serif; }}
        """)

    def select_blueprint(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Blueprint", "", "Image Files (*.jpg *.png *.bmp)")
        if file_path:
            self.selected_file = file_path
            self.status_label.setText(f'Nice pick! You chose: {file_path}')
        else:
            self.status_label.setText("Aw, come on! Don't be shy. Pick a blueprint!")

    def start_processing(self):
        if hasattr(self, 'selected_file') and self.selected_file:
            self.processing_thread = ProcessingThread(self.selected_file)
            self.processing_thread.progress_updated.connect(self.update_progress)
            self.processing_thread.status_updated.connect(self.update_status)
            self.processing_thread.start()
        else:
            self.status_label.setText("You haven't chosen a blueprint yet. Don’t worry; I'll wait.")

    def update_progress(self, progress):
        self.progress_bar.setValue(progress)

    def update_status(self, status):
        self.status_label.setText(status)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
