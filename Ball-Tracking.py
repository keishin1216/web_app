# -*- coding: utf-8 -*-
"""
Created on Sat Jul  2 16:04:33 2022

@author: 81809
"""

import cv2
import numpy as np

xmin, xmax = 100, 700
ymin, ymax = 100, 400

path = r"C:\\Users\81809\Downloads\677577884.395129.mp4"
cap = cv2.VideoCapture(path)
fgbg = cv2.createBackgroundSubtractorMOG2()

while(cap.isOpened()):

     ret, frame = cap.read()
     
     detframe = frame[ymin:ymax, xmin:xmax]
     cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 0, 255), 1)
     fgmask = fgbg.apply(detframe)
    # moment = cv2.countNonZero(fgmask)  # 動体検知した画素数を取得
     #text = 'Motion:' + str(moment)
     #font = cv2.FONT_HERSHEY_SIMPLEX
     #cv2.putText(frame, text, (20, 400), font, 1, (0, 255, 0), 2, cv2.LINE_AA)
     hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
     # 赤のHSV範囲
     lower_red1 = np.array([0,64,0])
     upper_red1 = np.array([30,255,255])
     
     lower_red2 = np.array([150,64,0])
     upper_red2 = np.array([179,255,255])
     
     # 白のHSV範囲
     lower_white = np.array([0, 0, 100])
     upper_white = np.array([180, 45, 255])
      
     # 黄のHSV範囲
     #lower_yellow = np.array([20,80,10])
     #upper_yellow = np.array([50,255,255])
     # 青のHSV範囲
     lower_blue = np.array([90, 64, 0])
     upper_blue = np.array([150, 255, 255])
     
     mask_red1 = cv2.inRange(hsv, lower_red1, upper_red1)
     mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)
     mask_red = mask_red1 + mask_red2
     res_red = cv2.bitwise_and(frame,frame, mask= mask_red)
     # 白以外にマスク
     mask_white = cv2.inRange(hsv, lower_white, upper_white)
     res_white = cv2.bitwise_and(frame, frame, mask=mask_white)
     #mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)
     #res_yellow = cv2.bitwise_and(frame,frame, mask= mask_yellow)
     mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
     res_blue = cv2.bitwise_and(frame,frame, mask= mask_blue)
     
    
           # グレースケール
     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
     gray = cv2.medianBlur(gray, 9)
     ret2,th = cv2.threshold(gray,200,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
               
     cimg = th
     contours, hierarchy = cv2.findContours(cimg,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
     print(len(contours))
     for i, cnt in enumerate(contours):
    # 輪郭の面積を計算する。
      area = cv2.contourArea(cnt)
    #　抽出する範囲を指定
      if area > 5 and area < 30:
        # 最小外接円を計算する
        (x, y), radius = cv2.minEnclosingCircle(cnt)
        if y > ymin and y < ymax and x > xmin and x < xmax:
            cv2.circle(frame, (int(x), int(y)),
                       int(radius), (0, 0, 255), 3)
     
    
     
     
      cv2.imshow("frame", frame)
      cv2.imshow("a", gray)
     if cv2.waitKey(10) & 0xFF == ord ('q'):
       break
cap.release()
cv2.destroyAllWindows() 