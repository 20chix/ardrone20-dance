#!/usr/bin/env python
import roslib
import rospy
import pygame
import std_srvs.srv
import time
from subprocess import Popen
from pygame.locals import * 
from std_msgs.msg import *
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Image
import time
import position_functions as pf
from datetime import datetime
import random
import sys
from std_srvs.srv import Trigger
import os
from drone_status import DroneStatus

class Dance():
        
    def __init__(self):

        dir_path = os.path.dirname(os.path.abspath(__file__))
        musics=[]
        while not musics:
            files = os.listdir(dir_path+'/music')
            musics = filter(lambda x: x.endswith('.mp3'), files)
        
        self.audio_path = dir_path +'/music/'+ musics[0]
        
        txts=[]
        while not txts:
            files = os.listdir(dir_path)
            print os.listdir(dir_path)
            txts = filter(lambda x: x.endswith('_beats.txt'), files)
        txt = dir_path + '/' + txts[0]    
        #readfile, parse timing
        #sys.exit()
        #f = open('/home/mm/catkin_ws/src/marker_navigator/src/music_beats.txt')
        f = open(txt)
        self.timing = []
        previuousTime = 0.0
        for line in f.readlines():
            print line
            currentTime = float(line.replace('\n', ''))
            self.timing.append(round(currentTime-previuousTime,4))
            previuousTime = currentTime
        f.close()  
        print 'timing is prepared'

        rospy.init_node('set_position', disable_signals=True)
        print 'init_node set_position'

        pygame.init()
        pygame.mixer.init()
        # Setup the main screen
        self.resolution = (340, 260) # This is the screen size of AR.Drone 2. Works also for AR.Drone 1
        self.screen     = pygame.display.set_mode( self.resolution )
        pygame.display.set_caption( 'AR.Drone Keyboard Interface' )

        # Setup the background
        self.background = pygame.Surface( self.screen.get_size() )
        self.background = self.background.convert()
        self.background.fill( (255, 255, 255) )    
        self.screen.blit( self.background, (0,0) )
        pygame.display.flip()

        self.ardrone_driver = Popen( ['rosrun', 'ardrone_autonomy', 'ardrone_driver'])
        print 'run ardrone drivers'
        
        self.copter = pf.DroneMaster()
        self.functionList=(	
                    ('move_right_left', 0.5),
                    ('move_left_right', 0.5),
                    ('move_up_down', 0.3),
                    ('move_down_up', 0.3),
                    ('move_yaw_left_right', 5),
                    ('move_yaw_right_left', 5)
        	        )
        
        #self.tick= ('yaw_right', 2)
        #self.tick_max= ('yaw_left', 10)
    
    def interruptFlying(self):
        self.copter.land()
        time.sleep(3)
        self.ardrone_driver.kill()
        print 'Interrupt Flying'
        time.sleep(2)

    def go(self):
        self.copter.takeoff(3)
        time.sleep(5)
        pygame.mixer.music.load(self.audio_path)
        pygame.mixer.music.play(-1,0.0)
        self.copter.clear()
        self.copter.goTo(1.5, 0, 0, 0.02)
        print 'x='+str(round(self.copter.x,3))+'; y='+str(round(self.copter.y,3))+'; z='+str(round(self.copter.z,3))
        print 'Go back!'        
        self.copter.goTo(0, 0, 0, 0.02)
        print 'x='+str(round(self.copter.x,3))+'; y='+str(round(self.copter.y,3))+'; z='+str(round(self.copter.z,3))
 
        #while True:
        #    self.copter.clear()
        #    time.sleep(0.5)
        #    for event in pygame.event.get():
        #        if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
        #            self.interruptFlying()
        #            sys.exit()
        #        else

                    
            #anim_num = random.randint(0, len(self.functionList)-1)
            #function = self.functionList[anim_num]
            #self.copter.stream(function[0], function[1], 0.7)
        #working loop 
        '''       
        for t in self.timing:
            print 'Beat'
            function=''
            for event in pygame.event.get():
                if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
                    self.interruptFlying()
                    sys.exit()
            #if t > self.copter.max_critical_time:
            #    print 'tick_max'
            #    function = self.tick
            #elif t < self.copter.min_critical_time:
            #    print 'tick_min'
            #    function = self.tick_max
            #else:
            anim_num = random.randint(0, len(self.functionList)-1)
            print t
            function = self.functionList[anim_num]
            self.copter.clear()
            self.copter.stream(function[0], function[1], t/2)
            '''


if __name__ == '__main__':            
    dance = Dance()
    status = -1

    while not (dance.copter.status != -1):
        status = dance.copter.getStatus()
        for event in pygame.event.get():
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
                dance.interruptFlying()
                sys.exit()
    
    dance.go()

    dance.copter.land()

    print '\n---> Shutting down driver!\n'
    print '\n---> Ended Successfully!\n'
