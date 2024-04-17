from typing import Union, Any, Sequence

import cv2
import numpy as np
from cv2 import Mat, UMat
from numpy import ndarray, dtype, generic

cap = cv2.VideoCapture(0)
kernel = np.ones((3, 3), np.uint8)

if cap.isOpened():
    # read
    ret, frame1 = cap.read()
    ret, frame2 = cap.read()

    while True:
        # cv2.absdiff find the differences between 2 frames
        diff = cv2.absdiff(frame1, frame2)
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2RGB)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)

        # to vien, iteration: so lan lap (co the tang, hoac giam)
        dilated = cv2.dilate(thresh, None, iterations=3)

        # ham findContours se tra ve 2 gia tri,
        #  o day khong can ket qua cua gia tri thu hai nen bo qua ( _ )
        #ct, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        #print(dilated)

        dilated = cv2.resize(dilated, (0, 0), fx=0.5, fy=0.5)
        frame1 = cv2.resize(frame1, (0, 0), fx=0.5, fy=0.5)

        # show
        cv2.imshow("Camera", frame1)
        cv2.imshow("Camera Dilated", dilated)
        frame1 = frame2
        ret, frame2 = cap.read()

        # exit
        if cv2.waitKey(10) == ord('f'):
            break

cap.release()
cv2.destroyAllWindows()