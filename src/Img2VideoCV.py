'''
Make video from images using python
'''

from PIL import Image
import os
import cv2
import numpy as np

## step1 collect images
src_path = 'image/'
out_img_path = 'resize_image/'
file_list = os.listdir(src_path)

## step2 resize images -- Image
size = (800, 400)
for filenname in file_list:
    print(f'image resize: {src_path + filenname }')
    img = Image.open(src_path + filenname)
    img = img.resize(size, Image.ANTIALIAS)
    img.save(out_img_path + filenname)

## step3 make video -- cv2
img_array = []
file_list2 = os.listdir(out_img_path)
# read image
for filename2 in file_list2:
    print(f'image read: {out_img_path + filename2 }')
    imgg = cv2.imread(out_img_path + filename2)
    img_array.append(imgg)

out_video_path = 'video/project03.mp4'
# write video
out = cv2.VideoWriter(out_video_path, cv2.VideoWriter_fourcc(*'mp4v'), 1, size)
for i in range(len(img_array)):
    out.write(img_array[i])

out.release()

## step4 add music to video -- moviepy

import moviepy.editor as mpe
audio_path = './audio/sample.mp3'
video_path = 'project04_audio.mp4' ## no audio
my_clip = mpe.VideoFileClip(video_path)
audio_background = mpe.AudioFileClip(audio_path)
# final_audio = mpe.CompositeAudioClip([my_clip.audio, audio_background])
final_clip = my_clip.set_audio(audio_background)
final_clip.write_videofile('project04_audio3.mp4')

## movie effect:
# 1. librosa -- audio analysis
# 2. moviepy --
# 3. ffmpeg -- template