

# FFmpeg 基础

FFmpeg官网： https://ffmpeg.org/

## 1 什么是FFmpeg?

	A complete, cross-platform solution to record, convert and stream audio and video.
	一个完整的、跨平台的，用于生产、转换和编码音频和视频的解决方案

FFmpeg的使用和优缺点：
- 特点：命令行工具，使用cmd命令执行。
- 优点：
	- 免费、强大、海量的命令库，支持对视频、音频的各种操作
	- 简单的命令行操作容易上手，可以批量化执行。
- 缺点：
	- 复杂操作的命令行学习成本比较高，官网的说明并不直观。
	- 没有GUI，相比有GUI的视频剪辑工具，学习曲线要陡峭，而且没有拿来即用的模板。



## 2 FFmpeg命令的使用格式

``` bash
ffmpeg {1} {2} -i {3} {4} {5}
```

	1. 全局参数
	2. 输入文件参数
	3. 输入文件
	4. 输出文件参数
	5. 输出文件

命令样例：
```bash
# 将一个图片转换为一个5秒的视频


# 解析
ffmpeg
	-y # 覆盖原文件
	-framerate 25 # 帧率
	-loop 1 #循环
	-i img.jpg # 输入文件
	-c:v libx264  # 输出文件video参数
	-t 5 #5秒
	-pix_fmt yuv420p  # 输出格式
	out.mp4 # 输出文件

```


## 3 基础命令整理：
3.1 视频格式转换
```bash
# 将avi格式转换为mp4
ffmpeg -i input_filename.avi -c:v copy -c:a copy -y output_filename.mp4
```

3.2 视频和音频的分离和合并

```bash
# 从视频中提取音频
ffmpeg -i sample.avi -q:a 0 -map a sample.mp3
# 向视频中添加音频
ffmpeg -i video.mkv -i audio.mp3 -map 0:v -map 1:a -c:v copy -shortest output.mkv

```


参考链接：

1. FFmpeg 视频处理入门教程 https://mp.weixin.qq.com/s/1yCmRlaIbXUA_m60kP5gzQ
2. FFmpeg 命令行工具： https://zhuanlan.zhihu.com/p/234483408
3. Filter syntax https://chowdera.com/2021/09/20210901063350697p.html
	1.   when to use commas and semicolon:   
		- the filters of the same path are separated by commas  
		- the filters of the different paths are divided by semicolons

