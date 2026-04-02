import pytesseract
from pytesseract import Output
import cv2

class TesseractEngine:
    @staticmethod
    def setup(tesseract_cmd=None):
        if tesseract_cmd:
            pytesseract.pytesseract.tesseract_cmd = tesseract_cmd

    @staticmethod
    def extract_text(image_path):
        image = cv2.imread(image_path)
        if image is None:
            raise FileNotFoundError("Could not read image for OCR")
            
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        results = pytesseract.image_to_data(gray, output_type=Output.DICT)
        
        extracted = []
        for i in range(len(results["text"])):
            text = results["text"][i].strip()
            conf = int(results["conf"][i])
            
            if text and conf > 30: # Filter out low confidence and empty text
                extracted.append({
                    "text": text,
                    "x": results["left"][i],
                    "y": results["top"][i],
                    "width": results["width"][i],
                    "height": results["height"][i],
                    "confidence": conf / 100.0
                })
        
        return extracted
