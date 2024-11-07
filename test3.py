import json
import cv2
import numpy as np
import math

screen_width=1920
screen_height=1080
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
        # Filter out double lines
        for line in lines:
            x1, y1, x2, y2 = line[0]
            line_coordinates.append(((int(x1), int(y1)), (int(x2), int(y2))))
        
        # Function to calculate distance between two points
        def distance(p1, p2):
            return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)
        
        # Filter lines by merging closely spaced, parallel lines
        filtered_lines = []
        min_distance = 10  # Minimum distance between lines to be considered unique
        for i, ((x1, y1), (x2, y2)) in enumerate(line_coordinates):
            duplicate = False
            for ((fx1, fy1), (fx2, fy2)) in filtered_lines:
                # Check if the line is parallel and close to an existing line
                if abs((y2 - y1)*(fx2 - fx1) - (fy2 - fy1)*(x2 - x1)) < 1e-2:  # Parallel lines
                    if distance((x1, y1), (fx1, fy1)) < min_distance and distance((x2, y2), (fx2, fy2)) < min_distance:
                        duplicate = True
                        break
            if not duplicate:
                filtered_lines.append(((x1, y1), (x2, y2)))
                print(f"Filtered Line: Start ({x1}, {y1}), End ({x2}, {y2})")  # Print for verification
        
        line_coordinates = filtered_lines

    else:
        print("No lines were detected.")

    # Save the line coordinates to a JSON file
    with open('line_coordinates.json', 'w') as f:
        json.dump(line_coordinates, f)

    return image, line_coordinates, edges  # Return the image, coordinates, and edges for visualization

# Example usage
image_path = '0001.jpg'
image, lines, edges = process_blueprint(image_path)

# Draw detected lines on the original image for visualization (optional)
if lines:
    for (start, end) in lines:
        cv2.line(image, start, end, (0, 255, 0), 2)  # Draw lines in green

# Show the original image with detected lines
resize_image=cv2.resize(image,(screen_width,screen_height))
resize_edges=cv2.resize(edges,(1900,1000))
cv2.imshow("Blueprint with Lines", resize_image)
cv2.imshow("Edges", resize_edges)
cv2.waitKey(0)
cv2.destroyAllWindows()