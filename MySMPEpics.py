from epics import caput, caget, cainfo
from BrukerClient import *
#from PyQt5 import QtCore, QtGui
from time import localtime
import numpy as np
import os
import sys
import subprocess
#from ExposTimer import *


class MySMPEpics ():

    #update_position = QtCore.pyqtSignal (int, float)
    #set_status = QtCore.pyqtSignal(str, int)

    def __init__(self):
        #QtCore.QThread.__init__(self)
        # motor flags are 0 for out, 1 for in, 2 for undefined
        self.m4_in_flag = 2
        self.m5_in_flag = 2
        self.m4_invalue = -75.
        self.m4_outvalue = 75
        self.m5_invalue = 0.5
        self.m5_outvalue = 49.5




    def get_m4_value (self) :
        return caget("Dera:m4.VAL")

    def get_m5_value (self) :
        return caget ("Dera:m5.VAL")

    def get_m4_instate (self) :
        val = self.get_m4_value ()
        indiff = abs(val - self.m4_invalue)
        outdiff = abs(val - self.m4_outvalue)
        if (indiff < .1) :
            self.m4_in_flag = 1
            return (1)
        if (outdiff < .1) :
            self.m4_in_flag = 0
            return (0)
        self.m4_in_flag = 2
        return 2

    def get_m5_instate (self) :
        val = self.get_m5_value ()
        indiff = abs(val - self.m5_invalue)
        outdiff = abs(val - self.m5_outvalue)
        if (indiff < .1) :
            self.m5_in_flag = 1
            return (1)
        if (outdiff < .1) :
            self.m5_in_flag = 0
            return (0)
        self.m5_in_flag = 2
        return 2

    def set_m4_instate (self, in_state) :
        # move in if 1
        if (in_state ==1) :
            self.move_motor (4, self.m4_invalue)
        if (in_state==0) :
            self.move_motor (4, self.m4_outvalue)
        self.get_m4_instate ()

    def set_m5_instate(self, in_state):
        # move in if 1
        if (in_state == 1):
            self.move_motor(5, self.m5_invalue)
        if (in_state == 0):
            self.move_motor(5, self.m5_outvalue)
        self.get_m5_instate ()

    def set_bruker_client (self, bc) :
        self.bclient = bc


    def get_position (self, mot_num) :
        if (mot_num == 4) :
            return caget('Dera:m4.VAL')
        if (mot_num == 5) :
            return caget('Dera:m5.VAL')



    def move_motor (self, mot_num, loc) :
        if (mot_num == 4) :
            caput('Dera:m4.VAL',loc)
        if (mot_num == 5) :
            caput ('Dera:m5.VAL', loc)



