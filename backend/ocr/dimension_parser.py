import re

class DimensionParser:
    @staticmethod
    def parse(text):
        """
        Parses dimensions like '12x10', '12 ft x 10 ft', '3.5m x 4.2m'
        """
        text = text.lower().replace(" ", "")
        
        # Simple regex for width x height
        match = re.search(r'([\d.]+)(ft|m|mm|\'|)?(x|X|×)([\d.]+)(ft|m|mm|\'|)?', text)
        if match:
            width = float(match.group(1))
            length = float(match.group(4))
            unit = match.group(2) or match.group(5) or 'unknown'
            
            # Normalize ' to ft
            if unit == "'":
                unit = 'ft'
                
            return {
                "raw": text,
                "width": width,
                "length": length,
                "unit": unit
            }
        return None
