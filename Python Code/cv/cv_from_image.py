import cv2
import matplotlib.pyplot as plt

def nothing(x):
    pass

img = cv2.imread(r'C:\Users\zkevi\Dropbox\Kevin\Monash\Y6\FYP\Code\Laser-Drawing\Python Code\cv\victoria.png')

assert img is not None

res = cv2.resize(img, (800,400))
cv2.namedWindow('canny')
switch = '0 : OFF \n1 : ON'
cv2.createTrackbar(switch, 'canny', 0, 1, nothing)
cv2.createTrackbar('Lower', 'canny',0,255,nothing)
cv2.createTrackbar('Upper', 'canny',0,255,nothing)


while True:
    lower = cv2.getTrackbarPos('Lower','canny')
    upper = cv2.getTrackbarPos('Upper', 'canny')
    s = cv2.getTrackbarPos(switch,'canny')


    # Ensure upper >= lower
    if upper < lower:
        upper = lower
        cv2.setTrackbarPos('Upper', 'canny', upper)

    if s == 0:
        edges = res
    else:
        edges = cv2.Canny(res, lower, upper)
    
    cv2.imshow('canny',edges)
    key = cv2.waitKey(1) & 0xFF

    if key == 27: # press esc to stop
        break

cv2.destroyAllWindows()
