'''
Add background music to a video use Moviepy
Reference:
1. https://9to5answer.com/video-editing-with-python-adding-a-background-music-to-a-video-with-sound
2. https://stackoverflow.com/questions/48728145/video-editing-with-python-adding-a-background-music-to-a-video-with-sound
'''

import moviepy.editor as mpe
audio_path = './audio/sample.mp3'
video_path = 'project04_audio.mp4' ## no audio
my_clip = mpe.VideoFileClip(video_path)
audio_background = mpe.AudioFileClip(audio_path)
# final_audio = mpe.CompositeAudioClip([my_clip.audio, audio_background])
final_clip = my_clip.set_audio(audio_background)
final_clip.write_videofile('project04_audio3.mp4')