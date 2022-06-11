# Video Producer

Produce video from pictures using python, ffmpeg, etc

Steps:
1. get pictures from websites -- use `requests`
2. resize picture to same size -- use `PIL.Image`
3. compile pictures to a video -- use `ffmpeg`
4. add music to video -- use `ffmpeg`


Key questions:
1. what kind of video should we create? 
   1. use template for auto-production (GUI application offer template, how to use it?)
   2. use ML to create, find an example. 
    

Ideas on making videos:
1. 制作卡点视频：使用librosa库：music + audio analysis
    - [librosa](https://github.com/librosa/librosa)
    - [会跳舞的小球](https://www.bilibili.com/video/BV1qR4y1g7yD/)

2. 制作卡点动画

## Useful Tools:

### 1. you-get download video
https://you-get.org/

steps to download video from tiktok or douyin
1. locate the media link in website 
2. copy link and download using you-get
