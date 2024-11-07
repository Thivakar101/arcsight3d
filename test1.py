import cv2
import numpy as np
import os

def save_coordinates_to_file(path, coordinates):
    # Saving the coordinates to a file in the same directory
    filename = os.path.join(os.path.dirname(path), 'coordinates.txt')
    with open(filename, 'w') as f:
        for coord in coordinates:
            f.write(f"{coord}\n")
    print(f"Coordinates saved to {filename}")

def get_blueprint_coordinates(image_path):
    # Load the blueprint image
    image = cv2.imread(image_path)

    if image is None:
        print("Image not found!")
        return

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Use Canny edge detection to detect the edges
    edges = cv2.Canny(gray, 50, 150)

    # Find contours from the edges
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    coordinates = []
    for contour in contours:
        for point in contour:
            coordinates.append(tuple(point[0]))

    # Save coordinates to a file
    save_coordinates_to_file(image_path, coordinates)

    return coordinates

if __name__ == "__main__":
    # Input the path of the blueprint
    blueprint_path = input("Enter the path of the blueprint image: ")
    
    # Get coordinates and save to file
    coordinates = get_blueprint_coordinates(blueprint_path)
    
    if coordinates:
        print("Coordinates extracted and saved.")
