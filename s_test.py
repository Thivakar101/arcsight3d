import json
import cv2
import numpy as np
import pytesseract

def process_blueprint(image_path):
    # Load the blueprint image
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Image not found at {image_path}")
    print("Image loaded successfully.")

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    print("Converted to grayscale.")

    # Apply Gaussian Blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    print("Applied Gaussian Blur.")

    # Use OCR to detect text and mask it out
    text_mask = np.zeros_like(gray)
    ocr_results = pytesseract.image_to_boxes(gray)
    print("OCR Results:", ocr_results)  # Debug OCR output

    for box in ocr_results.splitlines():
        b = box.split(' ')
        x, y, w, h = int(b[1]), int(b[2]), int(b[3]), int(b[4])
        cv2.rectangle(text_mask, (x, y), (w, h), 255, -1)

    # Combine with the original image to remove text areas
    blurred = cv2.bitwise_and(blurred, cv2.bitwise_not(text_mask))
    print("Text areas masked.")

    # Adaptive threshold for shape detection
    thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY_INV, 11, 2)
    print("Applied adaptive threshold.")

    # Morphological operations to clean up the image
    kernel = np.ones((5, 5), np.uint8)
    morphed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    print("Morphological operations applied.")

    # Find contours for shapes
    contours, _ = cv2.findContours(morphed, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    detected_objects = []
    print(f"Found {len(contours)} contours.")

    for contour in contours:
        epsilon = 0.02 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)

        # Differentiate walls from other shapes based on geometry
        if len(approx) >= 4:  
            x, y, w, h = cv2.boundingRect(approx)
            
            # Skip if the contour is likely a door curve (small height or width)
            if w < 20 or h < 20:
                detected_objects.append({"class": "door", "box": [x, y, w, h]})
                continue

            # Identify walls as rectangular shapes with specific proportions
            if w / h > 3 or h / w > 3:
                detected_objects.append({"class": "wall", "box": [x, y, w, h]})
            else:
                detected_objects.append({"class": "detected shape", "box": [x, y, w, h]})

    # Save detected objects
    with open('detected_objects.json', 'w') as f:
        json.dump(detected_objects, f)
    print("Detected objects saved to JSON.")

    # Display processed image
    cv2.imshow("Processed Image", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return image, detected_objects

# Example usage
if _name_ == "_main_":
    image_path = "path/to/your/blueprint_image.jpg"  # Update this with your actual image path
    process_blueprint(image_path)