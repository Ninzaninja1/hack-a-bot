import os
os.environ["QT_QPA_PLATFORM"] = "xcb" 
import cv2
import numpy as np

def draw_grid(img, grid_shape, color=(0, 0, 255), thickness=1):
    h, w, _ = img.shape
    rows, cols = grid_shape
    dy, dx = h / rows, w / cols

    # draw vertical lines
    for x in np.linspace(start=dx, stop=w-dx, num=cols-1):
        x = int(round(x))
        cv2.line(img, (x, 0), (x, h), color=color, thickness=thickness)

    # draw horizontal lines
    for y in np.linspace(start=dy, stop=h-dy, num=rows-1):
        y = int(round(y))
        cv2.line(img, (0, y), (w, y), color=color, thickness=thickness)

    return img
import os
os.environ["QT_QPA_PLATFORM"] = "xcb" 
import cv2

web = cv2.VideoCapture(0)

arucoDict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_100)
arucoParams = cv2.aruco.DetectorParameters()

while True:
   
    ret, frame = web.read()
    if not ret:
        break
    
    # Create the ArUco detector
    detector = cv2.aruco.ArucoDetector(arucoDict, arucoParams)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    corners, ids, rejected = detector.detectMarkers(gray)
    
    num_detected_ids = len(corners)
    centers = [0] * num_detected_ids
    coords = [[0] * num_detected_ids] * 4
    
    for i in range(len(corners)):
    
        # isolate the 4 corners of the current marker
        marker_corners = corners[i][0] 
        coords[i] = corners[i][0]

        # average the x and y columns simultaneously 
        center_x, center_y = marker_corners.mean(axis=0)
        # cast them to integers if you plan to draw them on the frame
        center_x = int(center_x)
        center_y = int(center_y)
        centers[i] = [center_x, center_y]
        
    # Print the detected markers
    if ids is not None:
        print("Markers detected.")
        for i in range(len(ids)):
            print(ids[i], "center:", centers[i], "\ncorners: \n", coords[i], "\n")
    
    cv2.aruco.drawDetectedMarkers(frame, corners, ids)
    frame = draw_grid(frame, (50,50))
    cv2.imshow('Detected Markers', frame)

    if cv2.waitKey(1) & 0xff == ord('q'):
        break

web.release()
cv2.destroyAllWindows()