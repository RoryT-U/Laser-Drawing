import cv2

# Initialize the camera
cap = cv2.VideoCapture(1)

if not cap.isOpened():
    print("Error: Could not open video stream.")
    exit()

show_overlay = True  # Flag to toggle between views
threshold1 = 100  # Initial threshold1 value
threshold2 = 200  # Initial threshold2 value 

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    if not ret:
        print("Error: Failed to capture image")
        break

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Use Canny edge detection with dynamic thresholds
    edges = cv2.Canny(gray, threshold1, threshold2)

    if show_overlay:
        # Convert edges to a 3-channel image
        edges_colored = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

        # Overlay edges on the original frame
        overlay = cv2.addWeighted(frame, 0.1, edges_colored, 0.9, 0)

        # Display the resulting frame with edges overlaid
        frame_to_show = overlay
    else:
        # Display the original frame
        frame_to_show = frame

    # Display the threshold values on the frame
    text = f"Threshold1: {threshold1} Threshold2: {threshold2}"
    cv2.putText(frame_to_show, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Show the frame
    cv2.imshow('Edges Overlay', frame_to_show)

    # Wait for a key press and check if it's 'q', 'w', or arrow keys
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('w'):
        show_overlay = not show_overlay  # Toggle the view mode
    elif key == ord('i'):  # Up arrow key
        threshold1 += 5
    elif key == ord('k'):  # Down arrow key
        threshold1 -= 5
    elif key == ord('l'):  # Right arrow key
        threshold2 += 5
    elif key == ord('j'):  # Left arrow key
        threshold2 -= 5

    # Ensure threshold values are within valid range
    threshold1 = max(0, min(threshold1, threshold2))
    threshold2 = max(threshold1, min(threshold2, 255))

# Release the camera and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
