# ライブラリのインポート
import cv2
import numpy as np

cap = cv2.VideoCapture(0)

# 色の範囲
# HSVRange["blue"]["lower"]で値を取り出せる
HSVRange = {
    "blue": {"lower": np.array([100, 50, 50]), "upper": np.array([120, 255, 255])},
    "green": {"lower": np.array([20, 50, 50]), "upper": np.array([60, 255, 255])},
    "pink": {"lower": np.array([160, 50, 50]), "upper": np.array([170, 255, 255])},
}
def mask_and_labeling(color):
    hsvLower = np.array([HSVRange[color]["lower"]])
    hsvUpper = np.array([HSVRange[color]["upper"]])
    
    # hsvからマスクを作成
    hsv_mask = cv2.inRange(hsv, hsvLower, hsvUpper)
    # cv2.imshow("hsv_mask", hsv_mask)

    # medianblurを用いてノイズ成分を除去
    blur_mask = cv2.medianBlur(hsv_mask, ksize = 3)
    # cv2.imshow("mask_with_medianblur", blur_mask)
    
    # ラベリング
    # ラベリング結果を書き出す用に二値画像をカラー変換
    src = cv2.cvtColor(blur_mask, cv2.COLOR_GRAY2BGR)

    # ラベリング処理
    nlabels, labels, stats, centroids = cv2.connectedComponentsWithStats(blur_mask)

    # 領域が3つ以上ある場合だけ処理
    if nlabels >= 2:
        top_idx = stats[:, 4].argsort()[-3 : -1]
        for i in top_idx:
            ox = int(centroids[i, 0])
            oy = int(centroids[i, 1])
            r = stats[i, 2] // 2

            cv2.circle(frame, (ox, oy), r, (255, 255, 255), 10)
            cv2.circle(frame, (ox, oy), 5, (255, 255, 255), -1)

            cv2.putText(
                frame,
                "Center X : " + str(int(centroids[i, 0])),
                (ox - 30, oy + 15),
                cv2.FONT_HERSHEY_PLAIN,
                1,
                (0, 0, 255), 
                2,
            )
            cv2.putText(
                frame, 
                "Center Y : " + str(int(centroids[i, 1])), 
                (ox - 30, oy + 30), 
                cv2.FONT_HERSHEY_PLAIN,
                1, 
                (0, 0, 255), 
                2, 
            )
            cv2.putText(
                frame, 
                "Size : " + str(int(stats[i, 4])), 
                (ox - 30, oy + 45), 
                cv2.FONT_HERSHEY_PLAIN,
                1, 
                (0, 0, 255), 
                2, 
            )


# 実行
while True:
    # circle描画はURL参照→(http://labs.eecs.tottori-u.ac.jp/sd/Member/oyamada/OpenCV/html/py_tutorials/py_gui/py_drawing_functions/py_drawing_functions.html)    
    # Webカメラのフレーム取得
    ret, frame = cap.read()
    cv2.imshow("camera", frame)
    
    # hsvに変換
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    color = "blue"
    mask_and_labeling(color)
    color = "green"
    mask_and_labeling(color)
    color = "pink"
    mask_and_labeling(color)
    cv2.imshow("output", frame)

    # 終了オプション
    k = cv2.waitKey(1)
    if k == ord("q"):
        break


# カメラリリース、windowの開放
cap.release()
cv2.destroyAllWindows()
