#!/usr/bin/env python

import roslib; 
import rospy
import pygame
import std_srvs.srv
import time
from subprocess import Popen
from pygame.locals import * 
from std_msgs.msg import *
from geometry_msgs.msg import Twist
import os


class Warn():
    
    def __init__(self): 
        self.publisher_reset = rospy.Publisher(  '/ardrone/reset', Empty )
        self.publisher_land  = rospy.Publisher(  '/ardrone/land',      Empty )
        
    def reset(self):
        self.publisher_reset.publish( Empty())
    
    def land(self):
        self.publisher_land.publish( Empty())
    
if __name__ == '__main__':
    dir_path = os.path.dirname(os.path.abspath(__file__))
    musics=[]
    while not musics:
        files = os.listdir(dir_path+'/music')
        musics = filter(lambda x: x.endswith('.mp3'), files)
    
    audio_path = dir_path +'/music/'+ musics[0]
    
    print audio_path
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(audio_path)
    pygame.mixer.music.play(-1,0.0)
    while True:
        print 'lalalal'