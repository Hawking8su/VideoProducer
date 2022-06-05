# Video Producer

Produce video from pictures using python, ffmpeg, etc

Steps:
1. get pictures from websites
2. resize picture to same size
3. compile pictures to a video
4. add music to video 

Key question:
1. what kind of video should we create? 
   1. use template for auto-production (GUI application offer template, how to use it?)
   2. use ML to create, find an example. 
    

Other thoughts:
1. 制作卡点视频：使用librosa库：music + audio analysis
    - [librosa](https://github.com/librosa/librosa)
    - [会跳舞的小球](https://www.bilibili.com/video/BV1qR4y1g7yD/)

2. 制作卡点动画

## Extract music from video using ffmpeg

https://stackoverflow.com/questions/9913032/how-can-i-extract-audio-from-video-with-ffmpeg

https://github.com/kkroening/ffmpeg-python

ffmpeg -i sample.avi -q:a 0 -map a sample.mp3

ffmpeg -i douyin_cat.mp4 -q:a 0 -map a sample.mp3

## convert avi to mp4
ffmpeg -i input_filename.avi -c:v copy -c:a copy -y output_filename.mp4

ffmpeg -i video/project03.avi -c:v copy -c:a copy -y project03.mp4

## Add music to video
https://zulko.github.io/moviepy/

https://9to5answer.com/video-editing-with-python-adding-a-background-music-to-a-video-with-sound

## you-get download video from douyin 
https://you-get.org/

