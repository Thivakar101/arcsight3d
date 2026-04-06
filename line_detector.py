import sys
import os
import json
import cv2
import numpy as np
import math

def distance(p1, p2):
    """Calculate Euclidean distance between two 2D points."""
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def process_blueprint(image_path, min_distance=15.0):
    """
    Reads blueprint, runs Canny edge detection and Hough Transform to extract lines,
    then filters out closely spaced parallel duplicate lines.
    """
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Image not found at: {image_path}")

    print(f"Processing image: {image_path}")
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Gaussian blur to remove text and fine hatch markings
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Canny edge detection
    edges = cv2.Canny(blurred, 50, 150)
    
    # Hough Lines Transform
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=50, minLineLength=50, maxLineGap=10)
    
    line_coordinates = []
    if lines is not None:
        raw_coords = []
        for line in lines:
            x1, y1, x2, y2 = line[0]
            raw_coords.append(((int(x1), int(y1)), (int(x2), int(y2))))
        
        # Merge parallel lines that are too close
        filtered_lines = []
        for (p1, p2) in raw_coords:
            x1, y1 = p1
            x2, y2 = p2
            
            duplicate = False
            for (fp1, fp2) in filtered_lines:
                fx1, fy1 = fp1
                fx2, fy2 = fp2
                
                # Check cross product / orientation to see if they are roughly parallel
                line1_vec = (x2 - x1, y2 - y1)
                line2_vec = (fx2 - fx1, fy2 - fy1)
                
                # Normalize vectors to check parallelism
                mag1 = math.sqrt(line1_vec[0]**2 + line1_vec[1]**2)
                mag2 = math.sqrt(line2_vec[0]**2 + line2_vec[1]**2)
                
                if mag1 > 0 and mag2 > 0:
                    cross_product = abs(line1_vec[0]*line2_vec[1] - line1_vec[1]*line2_vec[0])
                    sine_angle = cross_product / (mag1 * mag2)
                    
                    # Parallel (sine close to 0) and close start/end points
                    if sine_angle < 0.05: 
                        if distance(p1, fp1) < min_distance and distance(p2, fp2) < min_distance:
                            duplicate = True
                            break
            
            if not duplicate:
                filtered_lines.append((p1, p2))
        
        line_coordinates = filtered_lines
        print(f"Detected {len(raw_coords)} lines, filtered down to {len(line_coordinates)} unique lines.")
    else:
        print("No lines detected.")
        
    return line_coordinates

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Allow inputting file path via command line argument, otherwise default to sample blueprint
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
    else:
        # Default to a sample image
        image_path = os.path.join(script_dir, "samples", "print.png")
        if not os.path.exists(image_path):
            # Try blue.png if print.png isn't there
            image_path = os.path.join(script_dir, "samples", "blue.png")

    if not os.path.exists(image_path):
        print(f"Error: Default sample image not found. Please provide an image path. Example:")
        print(f"python line_detector.py path/to/blueprint.png")
        return

    try:
        lines = process_blueprint(image_path)
        output_path = os.path.join(script_dir, "line_coordinates.json")
        
        with open(output_path, 'w') as f:
            json.dump(lines, f, indent=4)
        print(f"Saved lines coordinates to: {output_path}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
