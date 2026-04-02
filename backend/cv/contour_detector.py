import cv2

def detect_contours(morphed_image):
    contours, _ = cv2.findContours(morphed_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
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
        
        obj_data = {
            "x": int(x), "y": int(y), 
            "width": int(w), "height": int(h),
            "confidence": 0.8 # Placeholder confidence
        }
        
        if len(approx) >= 4 and aspect_ratio_wall:
            obj_data["object_type"] = "WALL"
            detected_objects.append(obj_data)
        elif w >= 20 and h >= 20:
            obj_data["object_type"] = "DOOR"
            detected_objects.append(obj_data)

    return detected_objects
