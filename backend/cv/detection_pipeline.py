from backend.cv.preprocessing import preprocess_image
from backend.cv.contour_detector import detect_contours
from backend.cv.line_detector import detect_lines

class DetectionPipeline:
    @staticmethod
    def process(image_path, mode="auto"):
        # Auto-selection logic could be added here. For now, default to contour
        if mode == "auto":
            mode = "contour"
            
        original, gray, blurred, morphed = preprocess_image(image_path)
        
        if mode == "contour":
            objects = detect_contours(morphed)
        elif mode == "line":
            objects = detect_lines(blurred)
        else:
            raise ValueError(f"Unknown detection mode: {mode}")
            
        return objects
