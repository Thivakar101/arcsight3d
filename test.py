import json
import cv2
import numpy as np

def process_blueprint(image_path):
    # Load the blueprint image
    image = cv2.imread(image_path)
    
    # Check if the image was loaded successfully
    if image is None:
        raise FileNotFoundError(f"Image not found at {image_path}")

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian Blur to reduce noise and improve edge detection
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Apply Canny edge detection
    edges = cv2.Canny(blurred, 50, 150)

    # Find lines using Hough Transform
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=50, minLineLength=50, maxLineGap=10)

    # Prepare a list to hold the detected line coordinates
    line_coordinates = []

    # Check if lines were detected
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            # Convert NumPy types to native Python int
            line_coordinates.append(((int(x1), int(y1)), (int(x2), int(y2))))
            print(f"Detected Line: Start ({x1}, {y1}), End ({x2}, {y2})")  # Print coordinates for verification
    else:
        print("No lines were detected.")

    # Save the line coordinates to a JSON file
    with open('line_coordinates.json', 'w') as f:
        json.dump(line_coordinates, f)  # This will now work since all data is native Python types

    return image, line_coordinates, edges  # Return the image, coordinates, and edges for visualization

# Example usage
image_path = 'print.png'
image, lines, edges = process_blueprint(image_path)

# Draw detected lines on the original image for visualization (optional)
if lines:
    for (start, end) in lines:
        cv2.line(image, start, end, (0, 255, 0), 2)  # Draw lines in green

# Show the original image with detected lines
cv2.imshow("Blueprint with Lines", image)
cv2.imshow("Edges", edges)
cv2.waitKey(0)
cv2.destroyAllWindows()