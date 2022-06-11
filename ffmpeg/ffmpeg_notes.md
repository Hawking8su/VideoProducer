# ffmpeg notes

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

## 4. Extract music from video 

Reference:
1. https://stackoverflow.com/questions/9913032/how-can-i-extract-audio-from-video-with-ffmpeg
2. https://github.com/kkroening/ffmpeg-python
```bash
ffmpeg -i sample.avi -q:a 0 -map a sample.mp3
```

