# ffmpeg notes

Official Website: https://ffmpeg.org/

## 1. Make video from images

Reference:
1. [slideshow](https://trac.ffmpeg.org/wiki/Slideshow)

make video from jpgs, at framerate = 10 -- 10 picture per second
```bash
ffmpeg -framerate 10 -pattern_type glob -i '*.jpg' -c:v libx264 -pix_fmt yuv420p out.mp4
```

Example with each image will have a duration of 5 seconds (the inverse of 1/5 frames per second). The video stream will have a frame rate of 30 fps by duplicating the frames accordingly:
```bash
ffmpeg -framerate 1/5 -pattern_type glob -i '*.jpg' -c:v libx264 -r 30 -pix_fmt yuv420p out.mp4
```

Example with output video duration set to 30 seconds with `-t 30` from single image
```bash
ffmpeg -loop 1 -i img.jpg -c:v libx264 -t 30 -pix_fmt yuv420p out.mp4
```


## 2. Zoom in and out 
    
Reference:
1. [zoompan](https://ffmpeg.org/ffmpeg-filters.html#zoompan)
2. [How To Zoom In And Zoom Out Videos Using FFmpeg](https://ostechnix.com/zoom-in-and-zoom-out-videos-using-ffmpeg/)

Zoom in toward the center of the video to 2x zoom for the first 3 seconds of every 5 second block of time
```bash
ffmpeg -i out.mp4 -vf "zoompan=z='if(lte(mod(time,5),3),2,1)':d=1:x=iw/2-(iw/zoom/2):y=ih/2-(ih/zoom/2):fps=30" out_zoom.mp4
```

Zoom in up to 1.5x and pan always at center of picture: -- not working 
```bash
ffmpeg -i out.mp4 -vf "zoompan=z='min(zoom+0.0015,1.5)':d=700:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'" out_zoom2.mp4
```

## 3. Add overlay

Reference:
1. https://superuser.com/questions/727379/how-to-make-left-right-transition-of-overlay-image-ffmpeg

overlay a small picture from left to right 
```bash
ffmpeg -i Test.mp4 -i transparent.png -filter_complex "overlay=x='if(gte(t,0), -w+(t)*100, 3)':y=450" out.mp4

ffmpeg -i out.mp4 -i dog_small.jpg -filter_complex "overlay=x='if(gte(t,0), -w+(t)*50, 3)':y=350" out_overlay.mp4
```

## 4. Extract music from video & add audio to video

Reference:
1. https://stackoverflow.com/questions/9913032/how-can-i-extract-audio-from-video-with-ffmpeg
2. https://github.com/kkroening/ffmpeg-python
3. https://stackoverflow.com/questions/11779490/how-to-add-a-new-audio-not-mixing-into-a-video-using-ffmpeg?answertab=trending#tab-top
```bash
# extract audio to video
ffmpeg -i sample.avi -q:a 0 -map a sample.mp3


# add audio to video 

ffmpeg -i video.mkv -i audio.mp3 -map 0 -map 1:a -c:v copy -shortest output.mkv


```



## 5. convert avi to mp4

```bash
ffmpeg -i input_filename.avi -c:v copy -c:a copy -y output_filename.mp4

ffmpeg -i video/project03.avi -c:v copy -c:a copy -y project03.mp4

```


----
20220625
## 6. zoom in/out slowly for 5 seconds

Reference: 

1. https://superuser.com/questions/784146/ffmpeg-how-to-create-5-second-video-zooming-out-effect-with-1-image
```bash
# zoom in 
ffmpeg -loop 1 -i image1.jpg -vf "zoompan=z='min(zoom+0.0015,1.5)':d=125" -c:v libx264 -t 5 -s "800x450" zoomin.mp4

ffmpeg -loop 1 -i 0.jpg -vf "zoompan=z='min(zoom+0.0015,1.5)':d=125" -c:v libx264 -t 5 -s "800x450" zoomin.mp4

# zoom out 
ffmpeg -loop 1 -i 0.jpg -vf "zoompan=z='if(lte(zoom,1.0),1.5,max(1.001,zoom-0.0015))':d=125" -c:v libx264 -t 5 -s "800x450" zoomout.mp4

```

Trials:
1. https://el-tramo.be/blog/ken-burns-ffmpeg/ -- excellent reference
2. https://zhuanlan.zhihu.com/p/234483408 -- list of filter commands
2. https://www.youtube.com/watch?v=7c85ChNOuTg&t=105s -- move video from left to right
3. http://underpop.online.fr/f/ffmpeg/help/zoompan.htm.gz  -- ffmpeg zoompan explain


```bash
# make 5 second video with 1 pic
ffmpeg -loop 1 -i 0.jpg  -c:v libx264 -t 5 -s "800x450" onepic.mp4

ffmpeg -i input.mp4 -vf
"crop=in_w*0.90:in_h*0.90:(in_w*0.10)/10*t:108,scale=1920:1080" output.mp4

ffmpeg -i onepic.mp4 -vf "crop=in_w*0.90:in_h*0.90:(in_w*0.10)/10*t:108,scale=1920:1080" moveright.mp4

# Zoom-in up to 1.5 and pan at same time to some spot near center of picture
ffmpeg -loop 1 -i 0.jpg -vf "zoompan=z='min(zoom+0.0015,1.5)':d=700:x='if(gte(zoom,1.5),x,x+1/a)':y='if(gte(zoom,1.5),y,y+1)'" -c:v libx264 -t 5 -s "640x360" zoominandpan.mp4


```

```text
// zoom in 
ffmpeg -i in.jpg
    -filter_complex
        "zoompan=z='zoom+0.002':d=25*4:s=1280x800" // zoom in linearly 20% by adding 0.002 to the previous zoom vlaue
    -pix_fmt yuv420p -c:v libx264 out.mp4

zoompan=
    z='zoom+0.002'// zoom in linearly 20% by adding 0.002 for each frame
    :d=25*4  // duration of effect 
    :s=1280x800


// zoom out from the bottom right 
zoompan=
    x='iw-iw/zoom':
    y='ih-ih/zoom':
    z='if(eq(on,1),1.2,zoom-0.002)':
    d=25*4:s=1280x800
    
// cropping
zoompan=
    z='zoom+0.002':d=25*4:s=1280x2048,
crop=
    w=1280:h=800:x='(iw-ow)/2':y='(ih-oh)/2'
    
// padding
pad=
    w=9600:h=6000:x='(ow-iw)/2':y='(oh-ih)/2',
zoompan=
    z='zoom+0.002':d=25*4:s=1280x800
    
// panning
pad=
    w=9600:h=6000:x='(ow-iw)/2':y='(oh-ih)/2',
zoompan=
    x='(iw-0.625*ih)/2':
    y='(1-on/(25*4))*(ih-ih/zoom)':
    z='if(eq(on,1),2.56,zoom+0.002)':
    d=d=25*4:s=1280x800
```

```bash
# zoom in top left
ffmpeg -i 3.jpg -vf "zoompan=z='zoom+0.002':d=25*4:s=1280x800"  -pix_fmt yuv420p -c:v libx264 zoomintopleft.mp4
# zoom out bottom right
ffmpeg -i 3.jpg -vf "zoompan=x='iw-iw/zoom':y='ih-ih/zoom':z='if(eq(on,1),1.2,zoom-0.002)':d=25*4:s=1280x800"  -pix_fmt yuv420p -c:v libx264 zoomoutbottomright.mp4

# zoom in center: key param: x, y 
ffmpeg -i 3.jpg -vf "zoompan=x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':z='zoom+0.002':d=25*4:s=1280x800"  -pix_fmt yuv420p -c:v libx264 zoomincenter.mp4
ffmpeg -i 3.jpg -vf "zoompan=x=0:y=200:z='zoom+0.002':d=25*4:s=1280x800"  -pix_fmt yuv420p -c:v libx264 zoominsomewhere2.mp4

# padding 
ffmpeg -i 3.jpg -vf "pad=w=9600:h=6000:x='(ow-iw)/2':y='(oh-ih)/2',zoompan=z='zoom+0.002':d=25*4:s=1280x800"  -pix_fmt yuv420p -c:v libx264 padding.mp4
## this one is not quite working
ffmpeg -i 3.jpg -vf "pad=w=1350:h=844:x='(ow-iw)/2':y='(oh-ih)/2',zoompan=x='(iw-1.501*ih)/2':y='(1-on/(25*4))*(ih-ih/zoom)':z='if(eq(on,1),1.066,zoom+0.002)':d=25*4:s=1280x800"  -pix_fmt yuv420p -c:v libx264 padding2.mp4

ffmpeg -i 3.jpg -vf "pad=w=9600:h=6000:x='(ow-iw)/2':y='(oh-ih)/2',zoompan=x='(iw-0.625*ih)/2':y='(1-on/(25*4))*(ih-ih/zoom)':z='if(eq(on,1),2.56,zoom+0.002)':d=25*4:s=1280x800"  -pix_fmt yuv420p -c:v libx264 padding3.mp4

```



```bash
ffmpeg -i liuyifei_wide.jpg -vf "zoompan=x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':z='zoom+0.002':d=25*4:s=1280x800"  -pix_fmt yuv420p -c:v libx264 zoomincenter-liuyifei.mp4
# add audio 
ffmpeg -i zoomincenter-liuyifei.mp4 -i dance.mp3 -map 0 -map 1:a -c:v copy -shortest zoomincenter-liuyifei-audio.mkv

```

## 20220703

### zoom

reference: https://ffmpeg.org/ffmpeg-filters.html#zoompan

```bash
ffmpeg -i liuyifei_wide.jpg -vf "zoompan=x='iw-iw/zoom':y='ih-ih/zoom':z='zoom+0.002':d=25*4:s=1280x800"  -pix_fmt yuv420p -c:v libx264 zoomtest-liuyifei.mp4

ffmpeg -i liuyifei_wide.jpg -vf "zoompan=z='min(zoom+0.002,1.2)':x='iw/2-iw*(1/2+500/100)*on/100-iw/zoom/2':y='ih/2-ih/zoom/2':d=100:s=1280x800"  -pix_fmt yuv420p -c:v libx264 zoomtest-liuyifei.mp4

ffmpeg -i liuyifei_wide.jpg -vf "pad=w=9600:h=6000:x='(ow-iw)/2':y='(oh-ih)/2',zoompan=x='(iw-(ow/oh)*ih)/2':y='(1-on/100)*(ih-ih/zoom)':z='if(eq(on,1),((iw/ih)/(ow/oh)),zoom+0.002)':d=100:s=1280x800"  -pix_fmt yuv420p -c:v libx264 zoomtest-liuyifei.mp4

ffmpeg -i 3.jpg -vf "zoompan=z='1.5':x='(1-on/100)*(iw/2-iw/zoom/2)':d=100:s=1280x800"  -pix_fmt yuv420p -c:v libx264 zoomtest02-liuyifei.mp4

# zoom in center
ffplay -i zoomtest03-liuyifei.mp4 -vf "zoompan=z='1.5':x='(iw-iw/zoom)/2':y='(ih-ih/zoom)/2'"
# zoom in left center
ffplay -i zoomtest03-liuyifei.mp4 -vf "zoompan=z='1.5':x=0:y='(ih-ih/zoom)/2'"
# zoom from left to : note on output frame count = 25*4 = 100 -- works! 
ffplay -i zoomtest03-liuyifei.mp4 -vf "zoompan=z='1.5':x='(iw-iw/zoom)*(on/100)':y='(ih-ih/zoom)/2'"




```

### crop 

- `crop=W:H:X:Y` 
    - w: the width of the output video
    - h: the height of the output video
    - x: the horizontal position from where to begin cropping, starting from the left (with the absolute left margin being 0). defaults to the center `(iw-ow)/2`
    - y: the vertical position from where to begin cropping, starting from the top of the video (the absolute top being 0). defaults to the center `(ih-oh)/2`

- other variables:
    - t: the timestamp expressed in seconds
    - n: the number of input frame, starting from 0;
    - a: same as iw/ih
  
- note:
  - start from top left
```bash
# ffplay for preview 
ffplay -i zoomtest03-liuyifei.mp4 -vf "crop=iw/2:ih:iw/2*t/5:0"

# crop in center
ffplay -i zoomtest03-liuyifei.mp4 -vf "crop=100:100"

# crop 2/3 of input size 
ffplay -i zoomtest03-liuyifei.mp4 -vf "crop=2/3*in_w:2/3*in_h"

# Crop 10 pixels from the left and right borders, and 20 pixels from the top and bottom borders
ffplay -i zoomtest03-liuyifei.mp4 -vf "crop=in_w-2*10:in_h-2*20"

# Apply trembling effect
ffplay -i zoomtest03-liuyifei.mp4 -vf "crop=in_w/2:in_h/2:(in_w-out_w)/2+((in_w-out_w)/2)*sin(n/10):(in_h-out_h)/2 +((in_h-out_h)/2)*sin(n/7)"

# Apply erratic camera effect depending on timestamp
ffplay -i zoomtest03-liuyifei.mp4 -vf "crop=in_w/2:in_h/2:(in_w-out_w)/2+((in_w-out_w)/2)*sin(t*10):(in_h-out_h)/2 +((in_h-out_h)/2)*sin(t*13)"

```

move from left to right
```bash
# move from left to right -- OK
ffmpeg -i zoomtest03-liuyifei.mp4 -vf "crop=iw/2:ih:iw/2*t/5:0"  -c:v libx264 zoomtest04-liuyifei.mp4

# note: input should be a video
crop=
  w=iw/2: # output width
  h=ih:
  x=iw/2*t/5: # horizontal, move from left, t/5 -- or t/4 for 4 second video
  y=0 # vertical, move from top 

# move from right to left -- OK
crop=iw/2:ih:iw/2*(5-t)/5:0
# move from left to right 
crop=iw/2:ih:iw/2*t/5:0
ffplay -i zoomtest03-liuyifei.mp4 -vf "crop=iw/2:ih:iw/2*t/5:0,pad=w=1280:h=800:x='(ow-iw)/2':y='(oh-ih)/2" 

# move from top to bottom -- OK
crop=iw:ih/2:0:ih/2*t/5 
# move from bottom to top -- OK
crop=iw:ih/2:0:ih/2*(5-t)/5
ffplay -i zoomtest03-liuyifei.mp4 -vf "crop=iw:ih/2:0:ih/2*(5-t)/5"

# multiple filters at the same time 
ffplay -i zoomtest03-liuyifei.mp4 -vf "crop=iw:ih/2:0:ih/2*t/5, transpose=1"

# one filter then another
# use of in_time  

ffplay -i zoomtest03-liuyifei.mp4 -vf "zoompan=z='if(between(in_time,0,2),zoom+0.002,zoom-0.002)':d=100:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"

# reference: https://superuser.com/questions/959905/ffmpeg-sequentially-apply-filters
ffmpeg -i input.wmv -loop 1 -t 5 -framerate 30 -i image.jpg -t 5 -f lavfi -i anullsrc -filter_complex \
"[1:v]scale=640:-1,pad=iw:ih*(4/3):0:(oh-ih)/2,setsar=1/1[title]; [title][2:a][0:v][0:a]concat=n=2:v=1:a=1[v][a]" \
 -map "[v]" -map "[a]" output.wmv


```
time: 0 => iw/2*0/5
time: 1 => iw/2*1/5


time: 0 => iw/2* 5/5
time: 1 => iw/2* 4/5


Reference:
1. https://ottverse.com/crossfade-between-videos-ffmpeg-xfade-filter/

2. https://chowdera.com/2021/09/20210901063350697p.html

when to use commas and semicolon: 
- the filters of the same path are separated by commas
- the filters of the different paths are divided by semicolons

```bash
ffplay -i zoomtest03-liuyifei.mp4 -vf "split [main][tmp]; [tmp] crop=iw:ih/2:0:0, vflip [flip]; [main][flip] overlay=0:H/2"

split [main][tmp]; # input: split to 2 streams
[tmp] crop=iw:ih/2:0:0, vflip [flip];  # filter effect on [tmp], output is [flip]
[main][flip] overlay=0:H/2   # output: [main][flip]

ffplay -i zoomtest03-liuyifei.mp4 -vf "split [main][tmp]; [tmp] crop=iw/4:ih/4:0:0 [crop]; [main][crop] overlay=y='if(lte(t,2),0,H-h)'"
```

## 20220730

goal: 
1. wrap into functions

function 

```bash
ffplay -i liuyifei_3.jpg -vf "scale=6400x3600,zoompan=x='100*10/zoom+(on/(25*4))*((400-100)*10*(1-1/zoom)):y='50*10/zoom+(on/(25*4))*((300-50)*10*(1-1/zoom))':z='2':d=25*4:s=640x360"


# Goal: move from point a to point b 
# zoom in point A 
    point_a = (1489, 278)
    point_b = (467, 371)

# zoom in 
zoompan=
x='iw*(1-1/zoom)*(1489/1920)':
y='(ih-ih/zoom)*(278/1280)':
z='zoom+0.010':
d=25*4:
s=1920x1280


# zoom out from the bottom right 
zoompan=
    x='iw(1-1/zoom)':
    y='ih-ih/zoom':
    z='if(eq(on,1),1.2,zoom-0.002)':
    d=25*4:s=1280x800


ffplay -i windows_people_resize.jpg -vf "zoompan=x='(iw-iw/zoom)*(1489/1920)':y='(ih-ih/zoom)*(278/1280)':z='zoom+0.010':d=25*8:s=1920x1280"

# move from point A to point B 
zoompan=
x='(1489+(on/(25*4))*(467-1489))*(1-1/zoom)':
y='(278+(on/(25*4))*(371-278))*(1-1/zoom)':
z='2':
d=25*4:
s=1920x1280



ffplay -i windows_people_resize.jpg -vf "zoompan=x='1489/zoom+(on/(25*4))*((467-1489)*(1-1/zoom))':y='278/zoom+(on/(25*4))*((371-278)*(1-1/zoom))':z='2.8':d=25*4:s=1920x1280"

ffplay -i windows_people_resize.jpg -vf "zoompan=x='(1489+(on/(25*4))*(467-1489))*(1-1/zoom)':y='(278+(on/(25*4))*(371-278))*(1-1/zoom)':z='2':d=25*4:s=1920x1280"

```
