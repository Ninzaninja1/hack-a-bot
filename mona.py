import os
os.environ["QT_QPA_PLATFORM"] = "xcb" 
import cv2

web = cv2.VideoCapture(0)

arucoDict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_100)
arucoParams = cv2.aruco.DetectorParameters()

i = 1
# test!

while True:
   
    ret, frame = web.read()
    if not ret:
        break
    
    # Create the ArUco detector
    detector = cv2.aruco.ArucoDetector(arucoDict, arucoParams)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    corners, ids, rejected = detector.detectMarkers(gray)

    for i in range(len(corners)):
    
        # isolate the 4 corners of the current marker
        marker_corners = corners[i][0] 

        # average the x and y columns simultaneously 
        center_x, center_y = marker_corners.mean(axis=0)

        # cast them to integers if you plan to draw them on the frame
        center_x = int(center_x)
        center_y = int(center_y)
        print(center_x)
        print(center_y)


    if ids is not None:
        ids = ids.flatten()
        if 8 in ids and 2 in ids:
            # cv2.line(frame, center_x)
            pass
    # Print the detected markers
    print("Detected markers:", ids)
    cv2.aruco.drawDetectedMarkers(frame, corners, ids)
    cv2.imshow('Detected Markers', frame)


    



    if cv2.waitKey(1) & 0xff == ord('q'):
        break

web.release()
cv2.destroyAllWindows()