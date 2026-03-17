import cv2
import numpy as np

def enhance_frame(frame, scale):
    frame = cv2.resize(frame, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)

    kernel = np.array([[0,-1,0],[-1,5,-1],[0,-1,0]])
    frame = cv2.filter2D(frame, -1, kernel)

    frame = cv2.convertScaleAbs(frame, alpha=1.15, beta=10)

    return frame