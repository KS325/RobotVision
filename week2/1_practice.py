
import numpy as np
import cv2

cap = cv2.VideoCapture(0)
grayscale = False
flip = False
stop = False

# 実行
while (True):
    if stop == False:
        ret, frame = cap.read()
    if grayscale:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    if flip:
        frame = cv2.flip(frame, 1)

    cv2.imshow('camera', frame)
    # 終了オプション
    k = cv2.waitKey(1)
    if k == ord('q'):
        break
    if k == ord('g'):
        grayscale = not grayscale
    if k == ord('f'):
        flip = not flip
    if k == ord('s'):
        stop = not stop

cap.release()
cv2.destroyAllWindows()

