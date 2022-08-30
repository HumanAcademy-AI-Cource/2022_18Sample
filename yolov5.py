#!/usr/bin/env python3

import torch
import cv2

# 学習エンジンの準備
model = torch.hub.load("ultralytics/yolov5", "yolov5n")

# カメラの設定
cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 2)

# 繰り返し処理
while True:
    ret, frame = cap.read()
    # 学習エンジンに画像を入れて認識開始
    results = model(frame)
    # 認識結果を表示（英語）
    if results.pred[0].shape[0]:
        print("認識結果: ")
        for c in results.pred[0][:, -1].unique():
            label = results.names[int(c)]
            print("  - {}".format(label))
    else:
        print("何も認識されませんでした。")

    print("-------------------------------------------------------")
    # 認識結果が合成された画像を貰う
    img = results.render()[0]
    # 画像を表示
    cv2.imshow("Camera", img)
    cv2.waitKey(1)
