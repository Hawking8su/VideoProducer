'''
Librosa -- music and audio analysis
Reference:
1. https://librosa.org/doc/latest/tutorial.html

TODO:
1. learn basic knowledge of how to make music
What is Mel-frequency cepstral coefficients?
'''

import librosa

# Get the file path to an included audio example
filename = librosa.example('nutcracker')

# Load the audio as a waveform y,
# Store the sampling rate as sr
y, sr = librosa.load(filename)

# Run the default beat tracker
tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)

# Convert the frame indices of beat events into timestamps
beat_times = librosa.frames_to_time(beat_frames, sr=sr)

