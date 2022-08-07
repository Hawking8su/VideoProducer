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
   1. [librosa](https://github.com/librosa/librosa)
   2. [会跳舞的小球](https://www.bilibili.com/video/BV1qR4y1g7yD/)
   3. 学习如何制作卡点视频

2. 制作卡点动画
   1. python visualize music
   
3. 学习使用视频剪辑App：
   1. 了解视频 基本的元素
   2. 手工模仿制作一个剪辑视频



## Reference links:

1. [音视频开发-学习笔记](https://www.zhihu.com/column/c_1287080741293801472)
2. [ffmpeg音视频处理](https://coco723.github.io/blog/article/Tools/ffmpeg%E9%9F%B3%E8%A7%86%E9%A2%91%E5%A4%84%E7%90%86.html#%E5%8E%BB%E9%99%A4%E9%9F%B3%E8%A7%86%E9%A2%91%E4%B8%AD%E7%9A%84%E8%A7%86%E9%A2%91)

## Useful Tools:

### 1. you-get download video
https://you-get.org/

steps to download video from tiktok or douyin
1. locate the media link in website 
2. copy link and download using you-get
