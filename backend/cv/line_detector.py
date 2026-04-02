import cv2
import numpy as np
import math

def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def detect_lines(blurred_image, min_distance=15.0):
    edges = cv2.Canny(blurred_image, 50, 150)
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=50, minLineLength=50, maxLineGap=10)
    
    detected_objects = []
    
    if lines is not None:
        raw_coords = []
        for line in lines:
            x1, y1, x2, y2 = line[0]
            raw_coords.append(((int(x1), int(y1)), (int(x2), int(y2))))
        
        filtered_lines = []
        for (p1, p2) in raw_coords:
            x1, y1 = p1
            x2, y2 = p2
            
            duplicate = False
            for (fp1, fp2) in filtered_lines:
                fx1, fy1 = fp1
                fx2, fy2 = fp2
                
                line1_vec = (x2 - x1, y2 - y1)
                line2_vec = (fx2 - fx1, fy2 - fy1)
                
                mag1 = math.sqrt(line1_vec[0]**2 + line1_vec[1]**2)
                mag2 = math.sqrt(line2_vec[0]**2 + line2_vec[1]**2)
                
                if mag1 > 0 and mag2 > 0:
                    cross_product = abs(line1_vec[0]*line2_vec[1] - line1_vec[1]*line2_vec[0])
                    sine_angle = cross_product / (mag1 * mag2)
                    
                    if sine_angle < 0.05: 
                        if distance(p1, fp1) < min_distance and distance(p2, fp2) < min_distance:
                            duplicate = True
                            break
            
            if not duplicate:
                filtered_lines.append((p1, p2))
                
                angle = math.atan2(y2 - y1, x2 - x1)
                length = distance(p1, p2)
                
                detected_objects.append({
                    "object_type": "WALL", # Lines are assumed to be walls
                    "x1": x1, "y1": y1,
                    "x2": x2, "y2": y2,
                    "x": min(x1, x2), "y": min(y1, y2),
                    "width": abs(x2 - x1), "height": abs(y2 - y1),
                    "angle": angle,
                    "length": length,
                    "confidence": 0.9 # Placeholder
                })
                
    return detected_objects
