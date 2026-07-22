import cv2
import numpy as np

def detect_accident(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    val = np.mean(gray)

    if val < 40:
        return True
    return False