'''
用Python将的多张图片合成视频
参考：
1. https://blog.csdn.net/qq_37080185/article/details/123895700
'''
import cv2
import os
import numpy as np

# 每张图片大小
size = (2500, 1900)

# 路径设置
src_path = './image'
sav_path = './video/cat.mp4'

# 获取图片总数
all_files = os.listdir(src_path)
index = len(all_files)

# 设置视频写入器
fourcc = cv2.VideoWriter_fourcc(*'mp4v') # MP4格式
# 参数：1.合成后视频路径，2.使用的编码器，3.帧率，4.图片大小信息
videowrite = cv2.VideoWriter(sav_path, fourcc, 2, size)
# 临时存放图片的数组
img_array = []

# 读取所有jpg格式的图片(这里图片的命名格式0.jpg, 1.jpg)
for filename in all_files:
    img = cv2.imread(os.path.join(src_path, filename))  # 读取图片
    print(f'image1:{filename}')
    # print(type(img))
    if img is None:
        print(filename + " is error!")
        continue
    img_array.append(img)

# 合成视频
for i in range(0, index):
    # resize image
    img_array[i] = cv2.resize(img_array[i], size)
    videowrite.write(img_array[i])
    print('第{}张图片合成成功'.format(i))
    print('------done!-------')

videowrite.release()