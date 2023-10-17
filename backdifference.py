
import numpy as np
import cv2
from matplotlib import pyplot as plt

img_path1 = "./matigai_2.jpg"
img_path2 = "./matigai_3.jpg"

# 画像の読み込み
img1 = cv2.imread(img_path1)
img2 = cv2.imread(img_path2)

fgbg = cv2.bgsegm.createBackgroundSubtractorMOG()
background = fgbg.apply(img1)
fgmask = fgbg.apply(img2)

cv2.imshow("flow", fgmask)

k = cv2.waitKey(0)
cv2.destroyAllWindows


