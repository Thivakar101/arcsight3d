class RoomNameParser:
    KNOWN_ROOMS = [
        "bedroom", "master bedroom", "kitchen", "living room", "hall", 
        "bathroom", "toilet", "dining room", "store room", "balcony", 
        "office", "garage", "closet", "bath", "living", "dining"
    ]

    @staticmethod
    def parse(text):
        normalized = text.lower().strip()
        
        # Simple fuzzy matching or direct inclusion check
        for room in RoomNameParser.KNOWN_ROOMS:
            if room in normalized:
                return {
                    "raw": text,
                    "normalized": room
                }
        return None
