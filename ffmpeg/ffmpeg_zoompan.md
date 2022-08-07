
# FFmpeg滤镜效果--镜头聚焦和移动走位

需求目标：给一个图片，使用ffmpeg实现聚焦到点A，然后从点A移动到点B，再移动到点C的效果，制作成一个视频。

## 实现思路：
因为查了下资料，没有查到怎么使用ffmpeg的一行命令实现两个不同滤镜效果按顺序实现，因此这里将 “从点A到点B” 和“从点B到点C”两个效果分别实现产出视频，然后再顺序拼接。

**因此这里的关键效果是如何实现从“从点A到点B” 镜头聚焦和移动走位。**

我并没有找到直接实现的资料，因此这里结合自己对zoompan这个filter的理解，研究出了实现命令。

最终效果：
- 原始图片： https://unsplash.com/photos/p74ndnYWRY4
- 效果：从某一个人脸移动到第二个，再移动到第三个
- 输出视频： https://www.bilibili.com/video/BV1zF411N7jn/?vd_source=94c3861f377873ab0c5abf449cde011e


## `zoompan` 滤镜说明
参考链接：

- 官方[zoompan](https://ffmpeg.org/ffmpeg-filters.html#zoompan)
- [How To Zoom In And Zoom Out Videos Using FFmpeg](https://ostechnix.com/zoom-in-and-zoom-out-videos-using-ffmpeg/)
- https://superuser.com/questions/784146/ffmpeg-how-to-create-5-second-video-zooming-out-effect-with-1-image
- https://el-tramo.be/blog/ken-burns-ffmpeg/ -- -- excellent reference
- http://underpop.online.fr/f/ffmpeg/help/zoompan.htm.gz --  ffmpeg zoompan explain


基础用例详解
1. 聚焦中心点

```bash
# 聚焦到图片center中心点，时长4秒
ffplay -i input.jpg -vf "zoompan=x='iw/2*(1-1/zoom)':y='ih/2*(1-1/zoom)':z='2':d=25*4:s=640x360"

# zoompan拆解
zoompan=
	x='iw/2*(1-1/zoom)': # iw/2 代表要聚焦的x轴，zoom = 下面放大的比例
	y='ih/2*(1-1/zoom)': # ih/2 代表要聚焦的x轴
	z='2': # 聚焦放大的比例，这里代表2倍
	d=25*4: # 输出帧数，默认25帧/秒，25*4 代表4秒
	s=640x360 # 输出视频比例，可以设置和输入图片大小一致
```

2. 聚焦其他用例
```shell
# 聚焦到top left
zoompan=
	x='0': # iw/2 代表要聚焦的x轴，zoom = 下面放大的比例
	y='0': # ih/2 代表要聚焦的x轴
	z='2': 
	d=25*4: 
	s=640x360 

# 聚焦到bottom right
zoompan=
	x='iw*(1-1/zoom)': # iw/2 代表要聚焦的x轴，zoom = 下面放大的比例
	y='ih*(1-1/zoom)': # ih/2 代表要聚焦的x轴
	z='2': 
	d=25*4: 
	s=640x360 

# 动态聚焦到center, 每帧聚焦0.002倍
zoompan=
	x='iw/2*(1-1/zoom)': # iw/2 代表要聚焦的x轴，zoom = 下面放大的比例
	y='ih/2*(1-1/zoom)': # ih/2 代表要聚焦的x轴
	z='zoom+0.002':  # 每帧聚焦0.002倍
	d=25*4: 
	s=640x360 

# 动态zoom in聚焦到center, 每帧聚焦0.002倍，最大聚焦1.2倍
zoompan=
	x='iw/2*(1-1/zoom)': # iw/2 代表要聚焦的x轴，zoom = 下面放大的比例
	y='ih/2*(1-1/zoom)': # ih/2 代表要聚焦的x轴
	z='min(zoom+0.002,1.2)':  # 每帧聚焦0.002倍，直到1.2倍
	d=25*4: 
	s=640x360 

# zoom out from center, 每帧zoom out 0.002倍，从1.2倍开始
zoompan=
	x='iw/2*(1-1/zoom)': # iw/2 代表要聚焦的x轴，zoom = 下面放大的比例
	y='ih/2*(1-1/zoom)': # ih/2 代表要聚焦的x轴
	z='if(eq(on,1),1.2,zoom-0.002)':  # zoom out 0.002倍，从1.2倍开始
	d=25*4: 
	s=640x360 
```


## 目标效果实现

### 1.聚焦到点A，再从点A移动到点B：

输入：
- 点A坐标：(100, 50)  -- 注意：坐标是指从top left点开始的x轴和y轴坐标
- 点B坐标：(400, 300)
- 输出视频比例：640x360
- 固定聚焦倍数：2
```bash

ffplay -i input.jpg -vf "zoompan=x='(100+(on/25*4)*(400-100))(1-1/zoom)':y='(50+(on/25*4)*(300-50))(1-1/zoom)':z='2':d=25*4:s=640x360"

# zoompan拆解
zoompan=
	x='(100+(on/25*4)*(400-100))(1-1/zoom)': # 从100开始，每秒*（400-100）
	y='(50+(on/25*4)*(300-50))(1-1/zoom)': # 从50开始，每秒*（300-50）
	z='2':  # zoom out 0.002倍，从1.2倍开始
	d=25*4: 
	s=640x360 

```


我们可以开发一个Python函数，将需要输入的参数提取出来，更容易理解，最终自动拼出ffmpeg命令：
- 输入：输入文件、输出文件、输出视频比例、起始点、结束点、聚焦比例、视频时间长、移动速度。
- 输出：ffmpeg 聚焦和移动命令脚本
```python
def vf_zoom_move(in_file="", out_file="", out_size=(0, 0), point_start=(0, 0), point_end=(0, 0), z_effect=1, time=0,  
                 move_speed=1):  
    scale_ratio = 10  
    upscale = f"{out_size[0] * scale_ratio}x{out_size[1] * scale_ratio}"  # 这里是先把图片的比例调大来避免产出视频抖动的问题。
    out_scale = f"{out_size[0]}x{out_size[1]}"  
    frame_rate = 25 * time  
    move_frame_rate = frame_rate / move_speed  
    vf_str = f'''  
        scale={upscale},  
        zoompan=            
	        x='({point_start[0]}+(on/{move_frame_rate})*({point_end[0] - point_start[0]}))*{scale_ratio}*(1-1/zoom):  
            y='({point_start[1]}+(on/{move_frame_rate})*({point_end[1] - point_start[1]}))*{scale_ratio}*(1-1/zoom)':  
            z='{z_effect}':  
            d={frame_rate}:  
            s={out_scale}  
    '''  
    return "ffmpeg -y -i {0} -vf \"{2}\" -pix_fmt yuv420p -c:v libx264 {1}".format(in_file, out_file,vf_str.replace("\n", "").replace(" ",""))

```


### 2. 两个视频顺序拼接

使用操作： [concat demuxer](https://ffmpeg.org/ffmpeg-formats.html#concat-1)

参考：
1. https://stackoverflow.com/questions/7333232/how-to-concatenate-two-mp4-files-using-ffmpeg

step1  先将要拼接的视频文件写入一个txt文件，例如mylist.txt
``` bash
file '/path/to/file1'
file '/path/to/file2'
file '/path/to/file3'
```

step2 执行ffmpeg命令合并
```bash
ffmpeg -f concat -safe 0 -i mylist.txt -c copy output.mp4
```


开发Python函数实现参数化：
- 输入：拼接的视频清单、输出的文件路径
- 输出：ffmpeg concat命令

```python
def vf_concat_videos(in_files=[], out_file=""):  
    list_file = 'concat_videos.txt';  
    with open(list_file, 'w') as fh:  
        for filename in in_files:  
            if isinstance(filename, str) and filename.endswith('.mp4'):  
                print(filename)  
                fh.write("file '{}'\n".format(filename))  
    return "ffmpeg -f concat -safe 0 -y -i {} -c copy {}".format(list_file, out_file)
```


## 结语

将以上1和2组合就可以产出需要的视频效果，我用Python实现的代码见：https://github.com/Hawking8su/VideoProducer/blob/master/src/FFmpegPyVideo.py