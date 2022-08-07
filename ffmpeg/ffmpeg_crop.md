
# FFmpeg滤镜效果--剪切crop

  
## `crop=W:H:X:Y`   参数说明

- w: the width of the output video  
- h: the height of the output video  
- x: the horizontal position from where to begin cropping, starting from the left (with the absolute left margin being 0). defaults to the center `(iw-ow)/2`  
- y: the vertical position from where to begin cropping, starting from the top of the video (the absolute top being 0). defaults to the center `(ih-oh)/2`  
- other variables:  
  - t: the timestamp expressed in seconds  
  - n: the number of input frame, starting from 0;  
  - a: same as iw/ih  


## 命令用例
注意：输入必须是视频文件，不能是图片文件。

1.  静态剪切某个位置
``` bash
# crop in center   100*100 pixel
ffplay -i input.mp4 -vf "crop=100:100"  
# crop 2/3 of input size 
ffplay -i input.mp4 -vf "crop=2/3*in_w:2/3*in_h"  
# Crop 10 pixels from the left and right borders, and 20 pixels from the top and bottom borders  
ffplay -i input.mp4 -vf "crop=in_w-2*10:in_h-2*20"
```


2. 剪切并动态移动
```bash
# crop half of width, and move from left to right -- OK
ffplay -i input.mp4 -vf "crop=iw/2:ih:iw/2*t/5:0"  

# note: input should be a video  
crop=  
  w=iw/2: # output width  
  h=ih:  
  x=iw/2*t/5: # horizontal, move from left, t/5 -- or t/4 for 4 second video  
  y=0 # vertical, move from top
  
# move from right to left 
crop=iw/2:ih:iw/2*(5-t)/5:0  

# move from top to bottom 
crop=iw:ih/2:0:ih/2*t/5 
# move from bottom to top
crop=iw:ih/2:0:ih/2*(5-t)/5
```


参考资料：
1. https://www.linuxuprising.com/2020/01/ffmpeg-how-to-crop-videos-with-examples.html
2. https://video.stackexchange.com/questions/4563/how-can-i-crop-a-video-with-ffmpeg


