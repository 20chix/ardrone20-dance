#!/usr/bin/env python
import os
import time
import rospy
import librosa
from std_srvs.srv import Trigger

#rospy.init_node('decode_music')

dir_path = os.path.dirname(os.path.abspath(__file__))
'''
#del all with .wav
files = os.listdir(dir_path+'/music')
wavs = filter(lambda x: x.endswith('.mp3'), files)
if wavs:
	audio_path = dir_path+'/music/'+ wavs[0]
	for w in wavs:
		os.remove(dir_path+'/music/'+ w)
'''
'''
files = os.listdir(dir_path+'/music')
wavs = filter(lambda x: x.endswith('.mp3'), files)
audio_path = dir_path+'/music/'+ wavs[0]

y, sr = librosa.load(audio_path)
tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
beat_times = librosa.frames_to_time(beats)
f = open(dir_path+'/music_beats.txt', 'w')

print beat_times
for b in beat_times:
	f.write(str(round(b,4)) + '\n')
	
'''

txts=[]
while not txts:
    files = os.listdir(dir_path)
    txts = filter(lambda x: x.endswith('_beats.txt'), files)
txt = txts[0]    
#readfile, parse timing
f = open(txt)
timing = []
previuousTime = 0.0
for line in f.readlines():
    currentTime = float(line.replace('\n', ''))
    timing.append(round(currentTime-previuousTime,4))
    previuousTime = currentTime
f.close()  
print timing


