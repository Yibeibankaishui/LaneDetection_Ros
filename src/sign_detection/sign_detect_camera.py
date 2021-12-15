# -*- coding: utf-8 -*-
import cv2
import numpy as np

from sign_detection import sign_detector

if __name__ == "__main__":

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    while True:
        # 逐帧捕获
        ret, frame = cap.read()
        # 如果正确读取帧，ret为True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        # 显示结果帧e

        sign_detector(frame,1)
        # cv2.imshow('frame', frame)
        if cv2.waitKey(1) == ord('q'):
            break
    # 完成所有操作后，释放捕获器
    cap.release()
    cv2.destroyAllWindows()