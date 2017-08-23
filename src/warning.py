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
        rospy.init_node('reset_ardrone', disable_signals=True) 
        self.publisher_reset = rospy.Publisher(  '/ardrone/reset', Empty )
        self.publisher_land  = rospy.Publisher(  '/ardrone/land',      Empty )
        
    def reset(self):
        self.publisher_reset.publish( Empty())
    
    def land(self):
        self.publisher_land.publish( Empty())
    
if __name__ == '__main__':
    w = Warn()
    w.reset();
