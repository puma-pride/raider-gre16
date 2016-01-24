import os
import sys
sys.path.append(os.path.abspath(__file__).replace('raider-gre16/raider.py', '') + 'pybotics/')

import time
import numpy as np
import math
import control.octosnake.octosnake as octosnake
import dynamixel

class Raider(object):

    def __init__(self, trim, name='raider'):

        # Configuration
        self._name = name
        self._trim = trim
        self.dxl = dynamixel.Dynamixel()

    def move(self, id, position):
        self.dxl.com.write(self.dxl._coder(1, id, 30, int(position+self._trim[id])))
        if id == 17 or id == 18:
            self.dxl.com.write(self.dxl._coder(1, id+100, 30, int(position)+self._trim[id]))

    def zero(self):
        for i in range(0,11):
            self.move(i, 512)
        for i in range(13,25):
            self.move(i, 512)

    def home(self, h=0, a=0):
        self.move(1, 512)
        self.move(2, 512)
        self.move(3, 512)
        self.move(4, 512)
        #self.move(5, 262)
        self.move(6, 762)
        #self.move(7, 462)
        self.move(8, 562)
        #self.move(9, 62)
        self.move(10, 952)
        self.move(13, 512)
        self.move(14, 512)
        self.move(15, 512-a)
        self.move(16, 512+a)
        self.move(17, 512-h)
        self.move(18, 512+h)
        self.move(19, 512+h)
        self.move(20, 512-h)
        self.move(21, 512+h-18)
        self.move(22, 512-h+18)
        self.move(23, 512+a)
        self.move(24, 512-a)


    def fake(self, steps, T=750.0):

        x_amp = 20
        z_amp = 15
        front_x = 8
        i = 0

        T = 500
        amplitude = 100
        offset = 612
        phase = 0

        osc = octosnake.Oscillator()

        osc.period = T
        osc.amplitude = amplitude
        osc.phase = phase
        osc.offset = offset

        init_ref = time.time()
        final = init_ref + float(T*steps/1000)
        while time.time() < final:
            osc.refresh()
            self.dxl.setPosition(6,int(osc.output))
            self.dxl.setPosition(4,int(osc.output))

trims=[0,0,0,0,0,0,0,0,0,0,0,0,0,3,-2,-5,5,0,0,-5,0,0,0,0,0]
robot = Raider(trims)
robot.home(-140, 30)
