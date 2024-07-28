import cv2

def nothing(x):
    pass

cap = cv2.VideoCapture(1)

if not cap.isOpened():
    print("Error: Could not open video stream.")
    exit()

cv2.namedWindow('canny', cv2.WINDOW_NORMAL)
cv2.resizeWindow('canny', 600, 400)  # Set the desired window size (width, height)
switch = '0 : OFF \n1 : ON'
cv2.createTrackbar(switch, 'canny', 0, 1, nothing)
cv2.createTrackbar('Lower', 'canny',0,255,nothing)
cv2.createTrackbar('Upper', 'canny',0,255,nothing)


while True:

    ret, frame = cap.read()

    if not ret:
        print("Error: Failed to capture image")
        break


    lower = cv2.getTrackbarPos('Lower','canny')
    upper = cv2.getTrackbarPos('Upper', 'canny')
    s = cv2.getTrackbarPos(switch,'canny')


    # Ensure upper >= lower
    if upper < lower:
        upper = lower
        cv2.setTrackbarPos('Upper', 'canny', upper)

    if s == 0:
        edges = frame
    else:
        edges = cv2.Canny(frame, lower, upper)
    
    cv2.imshow('canny',edges)
    key = cv2.waitKey(1) & 0xFF

    if key == 27: # press esc to stop
        break

cv2.destroyAllWindows()