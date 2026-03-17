import cv2
import numpy as np

MAX_DIMENSION = 2000

def enhance_image(img, scale):
    img = np.array(img)
    h, w, _ = img.shape

    if max(h, w) * scale > MAX_DIMENSION:
        scale = MAX_DIMENSION / max(h, w)

    img = cv2.resize(img, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)

    kernel = np.array([[0,-1,0],[-1,5,-1],[0,-1,0]])
    img = cv2.filter2D(img, -1, kernel)

    img = cv2.convertScaleAbs(img, alpha=1.2, beta=10)

    return img