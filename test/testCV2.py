'''
Creating Video from Images using OpenCV-Python
Reference：
1. https://theailearner.com/2018/10/15/creating-video-from-images-using-opencv-python/
'''
import cv2
import numpy as np
import glob

img_array = []
for filename in glob.glob('./image/0.jpg'):
    print(filename)
    img = cv2.imread(filename)
    height, width, layers = img.shape
    size = (width, height)
    img_array.append(img)


out_path = './video/project.avi'
out = cv2.VideoWriter(out_path, cv2.VideoWriter_fourcc(*'DIVX'), 1, size)

for i in range(len(img_array)):
    out.write(img_array[i])
out.release()