# Source - https://stackoverflow.com/a/69097578
# Posted by mathandy, modified by community. See post 'Timeline' for change history
# Retrieved 2026-03-22, License - CC BY-SA 4.0

import cv2 as cv  # tested with version 4.5.3.56 (pip install opencv-python)
import numpy as np


def draw_grid(img, grid_shape, color=(0, 255, 0), thickness=1):
    h, w, _ = img.shape
    rows, cols = grid_shape
    dy, dx = h / rows, w / cols

    # draw vertical lines
    for x in np.linspace(start=dx, stop=w-dx, num=cols-1):
        x = int(round(x))
        cv.line(img, (x, 0), (x, h), color=color, thickness=thickness)

    # draw horizontal lines
    for y in np.linspace(start=dy, stop=h-dy, num=rows-1):
        y = int(round(y))
        cv.line(img, (0, y), (w, y), color=color, thickness=thickness)

    return img

def main():
    draw_grid()

    # TO BE COMplETED