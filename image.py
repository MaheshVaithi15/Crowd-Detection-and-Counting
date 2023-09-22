import cv2

from skimage.feature import hog

import tkinter as tk

from tkinter import filedialog

import matplotlib.pyplot as plt

from odapi import DetectorAPI

root = tk.Tk()
root.withdraw()




img = cv2.imread(filedialog.askopenfilename())

#resized_img = cv2.resize(img,(128*4,64*4))

resized_img1 = cv2.resize(img,(img.shape[1],img.shape[0]))

#fd , hogimg = hog(resized_img,orientations=9,pixels_per_cell=(8,8),cells_per_block=(2,2),visualize=True,multichannel=True,channel_axis=False)

odapi = DetectorAPI()
            
threshold = 0.7

boxes, scores, classes, num = odapi.processFrame(resized_img1)

for i in range(len(boxes)):

    if classes[i] == 1 and scores[i] > threshold:
        box = boxes[i]

        cv2.rectangle(resized_img1, (box[1], box[0]), (box[3], box[2]), (255,0,0), 2)








cv2.imshow('Detected Image',resized_img1)

#plt.imshow(hogimg,cmap='gray')
#plt.show()

cv2.waitKey(0)
cv2.destroyAllWindows()
