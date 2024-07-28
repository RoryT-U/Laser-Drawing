import cv2
import pandas as pd
import numpy as np
from scipy.spatial import KDTree

def draw_acyclic_path_and_save(csv_file, output_image, output_csv, keep_ratio):
    # Read the CSV file
    df = pd.read_csv(csv_file)
    
    # Check if the CSV file contains 'X' and 'Y' columns
    if 'X' not in df.columns or 'Y' not in df.columns:
        raise ValueError("CSV file must contain 'X' and 'Y' columns")
    
    # Extract the coordinates
    points = df[['X', 'Y']].values
    
    # Randomly select a subset of points based on the keep_ratio
    total_points = len(points)
    num_points_to_keep = int(total_points * keep_ratio)
    if num_points_to_keep < 2:  # Ensure at least 2 points are kept
        raise ValueError("keep_ratio is too low, resulting in less than 2 points being kept")
    
    selected_indices = np.random.choice(total_points, num_points_to_keep, replace=False)
    selected_points = points[selected_indices]
    
    # Create a KDTree for finding the nearest neighbors efficiently
    tree = KDTree(selected_points)
    
    # Create a blank image
    max_x = selected_points[:, 0].max() + 10
    max_y = selected_points[:, 1].max() + 10
    image = 255 * np.ones((max_y, max_x, 3), dtype=np.uint8)
    
    # Initialize an array to keep track of visited points
    visited = np.zeros(len(selected_points), dtype=bool)
    
    # Initialize a list to store the path
    path = []

    # Function to find the closest unvisited point
    def find_closest_unvisited_point(current_index):
        distances, indices = tree.query(selected_points[current_index], k=len(selected_points))
        for idx in indices:
            if not visited[idx]:
                return idx
        return None

    # Start from the first point
    current_index = 0
    visited[current_index] = True
    path.append((selected_points[current_index][0], selected_points[current_index][1]))
    
    # Draw the first point
    start_point = (selected_points[current_index][0], selected_points[current_index][1])
    cv2.circle(image, start_point, 2, (0, 0, 255), -1)
    
    for _ in range(1, num_points_to_keep):
        next_index = find_closest_unvisited_point(current_index)
        if next_index is None:
            break
        
        end_point = (selected_points[next_index][0], selected_points[next_index][1])
        
        # Draw the line connecting the current point to the next point
        cv2.line(image, start_point, end_point, (0, 255, 0), 1)
        
        # Mark the next point as visited
        visited[next_index] = True
        path.append((selected_points[next_index][0], selected_points[next_index][1]))
        
        # Move to the next point
        start_point = end_point
        current_index = next_index
        
        # Draw the next point
        cv2.circle(image, start_point, 2, (0, 0, 255), -1)

    # Overlay the number of points
    text = f'Number of points: {num_points_to_keep}'
    cv2.putText(image, text, (10, max_y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)

    # Save or display the image
    cv2.imwrite(output_image, image)
    cv2.imshow('Image with Acyclic Path', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    # Save the path to a CSV file
    path_df = pd.DataFrame(path, columns=['X', 'Y'])
    path_df.to_csv(output_csv, index=False)

# Usage example
csv_file = 'outputs/raw_edge_coordinates.csv'
output_image = 'outputs/output_image.png'
output_csv = 'outputs/shortest_path.csv'
keep_ratio = 0.5  # 50% of the points will be preserved
draw_acyclic_path_and_save(csv_file, output_image, output_csv, keep_ratio)
