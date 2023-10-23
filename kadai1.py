
# ライブラリのインポート
import copy

import cv2
import numpy as np

# アプリ用のスタジアム、ボール画像を読みこみ
ball_img = cv2.imread("./image_data/ball.png")
stadium_img = cv2.imread("./image_data/stadium.png")

# スタジアムの大きさを適当に変更 (二つ目の引数は(w,h))
w  = 1200
h = 700
stadium_img = cv2.resize(stadium_img, (w, h))

# / ではなく // で切り捨て
# ボールの高さ、幅の[半分](半分だから注意！！)
# (注意!)今回ボールの大きさが H:198、W:200と両方偶数のためこれで良いが、奇数の場合は工夫が必要
ball_h, ball_w = ball_img.shape[0] // 2, ball_img.shape[1] // 2

# ボールの中心位置（中心座標)を初期ではスタジアムの中心に設定
idx_h = stadium_img.shape[0] // 2
idx_w = stadium_img.shape[1] // 2

print(idx_h)

def plan1(speed):
    while True:
        global idx_h
        global idx_w
        # スタジアムのコピーを作成
        stadium_copy = copy.deepcopy(stadium_img)

        # ボールの再配置
        stadium_copy[
            (idx_h - ball_h) : (idx_h + ball_h), (idx_w - ball_w) : (idx_w + ball_w)
        ] = ball_img

        # 結果画像の表示
        cv2.imshow("output", stadium_copy)

        # 終了オプション
        k = cv2.waitKey(1)
        if k == ord("q"):
            break
        elif k == ord("w"):
            if idx_h >= ball_h + speed:
                idx_h -= speed
            else:
                idx_h = ball_h
        elif k == ord("s"):
            if idx_h <= h - ball_h - speed:
                idx_h += speed
            else:
                idx_h = h - ball_h
        elif k == ord("a"):
            if idx_w >= ball_w + speed:
                idx_w -= speed
            else:
                idx_w = ball_w
        elif k == ord("d"):
            if idx_w <= w - ball_w - speed:
                idx_w += speed
            else:
                idx_w = w - ball_w


def plan2():
    while True:
        global idx_h
        global idx_w
        # スタジアムのコピーを作成
        stadium_copy = copy.deepcopy(stadium_img)
        
        new_ball_h = ball_img.shape[0]
        new_ball_w = ball_img.shape[1]
        TB = False
        LR = False

        if idx_h - ball_h < 0:
            TB = "top"
            new_ball_h = ball_h - idx_h
        elif idx_h + ball_h > h:
            TB = "bottom"
            new_ball_h = idx_h + ball_h - h
        
        if idx_w - ball_w < 0:
            LR = "left"
            new_ball_w = ball_w - idx_w
        elif idx_w + ball_w > w:
            LR = "right"
            new_ball_w = ball_w + idx_w - w
        
        """
        if TB == "top" and LR == "left":
            new_ball_img = ball_img[:new_ball_h, :new_ball_w]
            ball_img = ball_img[new_ball_h:, new_ball_w:]
        elif TB == "top" and LR == "right":
            new_ball_img = ball_img[:new_ball_h, ball_img.shape[1] - new_ball_w:]
            ball_img = ball_img[new_ball_h:, :ball_img.shape[1] - new_ball_w]
        elif TB == "bottom" and LR == "left":
            new_ball_img = ball_img[ball_img.shape[0] - new_ball_h:, :new_ball_w]
            ball_img = ball_img[:ball_img.shape[0] - new_ball_h, new_ball_w:]
        elif TB == "bottom" and LR == "right":
            new_ball_img = ball_img[ball_img.shape[0] - new_ball_h:, ball_img.shape[1] - new_ball_w:]
            ball_img = ball_img[:ball_img.shape[0] - new_ball_h, :ball_img.shape[1] - new_ball_w]
        """
        if TB == "top":
            new_ball_crop_h_img = ball_img[:new_ball_h, :]
            new_ball_h_img = ball_img[new_ball_h:, :]
        elif TB == "bottom":
            new_ball_crop_h_img = ball_img[ball_img.shape[0] - new_ball_h:, :]
            new_ball_h_img = ball_img[:ball_img.shape[0] - new_ball_h, :]
        
        if LR == "left":
            new_ball_crop_w_img = ball_img[:, :new_ball_w]
            new_ball_w_img = ball_img[:, new_ball_w:]
        elif LR == "right":
            new_ball_crop_w_img = ball_img[:, ball_img.shape[1] - new_ball_w:]
            new_ball_w_img = ball_img[:, :ball_img.shape[1] - new_ball_w]

        # ボールの再配置
        """
        stadium_copy[
            (idx_h - ball_h) : (idx_h + ball_h), (idx_w - ball_w) : (idx_w + ball_w)
        ] = ball_img
        """
        if TB == False:
            stadium_copy[(idx_h - ball_h) : (idx_h + ball_h),] = ball_img[0]
        elif TB == "top":
            stadium_copy[:(idx_h + new_ball_h)]

        # 結果画像の表示
        cv2.imshow("output", stadium_copy)

        # 終了オプション
        k = cv2.waitKey(1)
        if k == ord("q"):
            break
        elif k == ord("w"):
            idx_h -= speed
        elif k == ord("s"):
            idx_h += speed
        elif k == ord("a"):
            idx_w -= speed
        elif k == ord("d"):
            idx_w += speed

speed = 10

cv2.destroyAllWindows()


