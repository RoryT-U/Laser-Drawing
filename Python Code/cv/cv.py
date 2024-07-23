import cv2

# Initialize the camera
cap = cv2.VideoCapture(1)

if not cap.isOpened():
    print("Error: Could not open video stream.")
    exit()

show_outline = True  # Flag to toggle between views

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    if not ret:
        print("Error: Failed to capture image")
        break

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Use Canny edge detection
    edges = cv2.Canny(gray, 100, 200)

    if show_outline:
        # Convert edges to a 3-channel image
        edges_colored = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

        # Display the resulting frame with edges overlaid
        cv2.imshow('Edges Overlay', edges_colored)
    else:
        # Display the original frame
        cv2.imshow('Edges Overlay', frame)

    # Wait for a key press and check if it's 'q' or 'w'
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('w'):
        show_outline = not show_outline  # Toggle the view mode

# Release the camera and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
