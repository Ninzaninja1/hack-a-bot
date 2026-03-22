# link to medium website for source code: https://agneya.medium.com/color-detection-using-python-and-opencv-8305c29d4a42 

import os
# set this before importing cv2 to avoid wayland crashes
os.environ["QT_QPA_PLATFORM"] = "xcb"

import numpy as np
import cv2

totalRows, totalCols = 50, 50
pixelThresh = 0.3
gridMatrix = [totalRows][totalCols]


def main():

    # turn on cam
    webcam = cv2.VideoCapture(0)

    frame_width = webcam.get(cv2.CAP_PROP_FRAME_WIDTH)
    frame_height = webcam.get(cv2.CAP_PROP_FRAME_HEIGHT)

    # Set range for red color
    red_lower = np.array([136, 87, 111], np.uint8) # tobe changed
    red_upper = np.array([180, 255, 255], np.uint8)
    # green color
    green_lower = np.array([25, 52, 72], np.uint8)
    green_upper = np.array([65, 145, 108], np.uint8)
    # blue color
    blue_lower = np.array([94, 80, 2], np.uint8)
    blue_upper = np.array([120, 255, 255], np.uint8)

    while True:
        _, frame = webcam.read()

        # Convert BGR to HSV colorspace
        # final run
        frame = colordetect(frame, red_lower, red_upper, green_lower, green_upper, blue_lower, blue_upper)

        x, y = get_grid_cell(500, 120, frame_width, frame_height, totalRows, totalCols)

        print(f'{x}, {y}')
        cv2.imshow("Color Detection", frame)


        if cv2.waitKey(10) & 0xFF == ord('q'): # to quit from imshow, keyboard press q
            break
    webcam.release()
    cv2.destroyAllWindows()

def colordetect(imageFrame, red_lower, red_upper, green_lower, green_upper, blue_lower, blue_upper):
    # Convert BGR to HSV colorspace
    hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV)

    # define mask
    red_mask = cv2.inRange(hsvFrame, red_lower, red_upper)
    green_mask = cv2.inRange(hsvFrame, green_lower, green_upper)
    blue_mask = cv2.inRange(hsvFrame, blue_lower, blue_upper)

    # to detect only that particular color
    kernal = np.ones((5, 5), "uint8")

    # red color
    red_mask = cv2.dilate(red_mask, kernal)
    res_red = cv2.bitwise_and(imageFrame, imageFrame, mask=red_mask)

    # green color
    green_mask = cv2.dilate(green_mask, kernal)
    res_green = cv2.bitwise_and(imageFrame, imageFrame, mask=green_mask)

    # blue color
    blue_mask = cv2.dilate(blue_mask, kernal)
    res_blue = cv2.bitwise_and(imageFrame, imageFrame, mask=blue_mask)

    # Creating contour to track red color
    contours, hierarchy = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if (area > 300):
            x, y, w, h = cv2.boundingRect(contour)
            imageFrame = cv2.rectangle(imageFrame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.putText(imageFrame, "Red Colour", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255))

    # Creating contour to track green color
    contours, hierarchy = cv2.findContours(green_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if (area > 300):
            x, y, w, h = cv2.boundingRect(contour)
            imageFrame = cv2.rectangle(imageFrame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(imageFrame, "Green Colour", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0))

    # Creating contour to track blue color
    contours, hierarchy = cv2.findContours(blue_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if (area > 300):
            x, y, w, h = cv2.boundingRect(contour)
            imageFrame = cv2.rectangle(imageFrame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.putText(imageFrame, "Blue Colour", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 0, 0))

    for row in range(totalRows):
            for col in range(totalCols):
                
                # Find pixel boundaries for this cell
                top_y = int(row * cell_height)
                bottom_y = int((row + 1) * cell_height)
                left_x = int(col * cell_width)
                right_x = int((col + 1) * cell_width)

                # Extract just this cell's region from the mask
                cell_mask = red_mask[top_y:bottom_y, left_x:right_x]

                # Count the white (red) pixels in this cell
                active_pixel_count = cv2.countNonZero(cell_mask)

                # 4. Check against threshold
                if (active_pixel_count / pixels_per_cell) > THRESHOLD_PERCENTAGE:
                    grid_matrix[row][col] = 1
                    
                    # Draw a filled red rectangle on the overlay
                    cv2.rectangle(overlay, (left_x, top_y), (right_x, bottom_y), (0, 0, 255), -1)
    
    return imageFrame

def get_grid_cell(pixel_x, pixel_y, frame_width, frame_height, total_cols, total_rows):
    # Calculate how wide and tall one single cell is
    cell_width = frame_width / total_cols
    cell_height = frame_height / total_rows
    # print(f'{cell_width},{cell_height}')
    
    # Find the index by dividing the pixel location by the cell size
    column_index = int(pixel_x / cell_width)
    row_index = int(pixel_y / cell_height)
    
    return row_index, column_index

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

if __name__ == '__main__':
    main()