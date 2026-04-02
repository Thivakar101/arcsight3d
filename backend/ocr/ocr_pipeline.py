from backend.ocr.tesseract_engine import TesseractEngine
from backend.ocr.dimension_parser import DimensionParser
from backend.ocr.room_name_parser import RoomNameParser
from backend.models.ocr_text import OCRText
from backend.extensions import db

class OCRPipeline:
    @staticmethod
    def process(project_id, image_path, app_config):
        TesseractEngine.setup(app_config.get('TESSERACT_CMD'))
        
        raw_texts = TesseractEngine.extract_text(image_path)
        
        ocr_results = []
        for item in raw_texts:
            text = item['text']
            
            parsed_dim = DimensionParser.parse(text)
            parsed_room = RoomNameParser.parse(text)
            
            text_type = 'UNKNOWN'
            parsed_value = None
            normalized = text
            
            if parsed_dim:
                text_type = 'DIMENSION'
                parsed_value = parsed_dim
            elif parsed_room:
                text_type = 'ROOM_NAME'
                parsed_value = parsed_room
                normalized = parsed_room['normalized']
            
            ocr_text = OCRText(
                project_id=project_id,
                text=text,
                normalized_text=normalized,
                text_type=text_type,
                x=item['x'],
                y=item['y'],
                width=item['width'],
                height=item['height'],
                confidence=item['confidence'],
                parsed_value=parsed_value
            )
            db.session.add(ocr_text)
            ocr_results.append(ocr_text)
            
        db.session.commit()
        return ocr_results
