import cv2

from skimage.feature import hog

import tkinter as tk

from tkinter import filedialog

from odapi import DetectorAPI

root = tk.Tk()
root.withdraw()

cv2.startWindowThread()

cap = cv2.VideoCapture(filedialog.askopenfilename())

#fgbg = cv2.createBackgroundSubtractorMOG2()

while True:

    ret , frame = cap.read()

    resized_frame = cv2.resize(frame,(800,500))

    
    #fd , hogimg = hog(resized_frame,orientations=9,pixels_per_cell=(8,8),cells_per_block=(2,2),visualize=True,multichannel=True)

    #fg = fgbg.apply(hogimg)


    #cv2.imshow('HOG VIDEO',hogimg)

    
    odapi = DetectorAPI()
            
    threshold = 0.7

    boxes, scores, classes, num = odapi.processFrame(resized_frame)

    for i in range(len(boxes)):

        if classes[i] == 1 and scores[i] > threshold:
            box = boxes[i]

            cv2.rectangle(resized_frame, (box[1], box[0]), (box[3], box[2]), (255,0,0), 2)

        

    cv2.imshow('Detected VIDEO',resized_frame)

    
    #cv2.imshow('HOG',fg)

    #cv2.imshow('Original Video',frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):

        break
cap.release()
cv2.destroyAllWindows()


