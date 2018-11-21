###
# SMPControl.py
# Top level python module to load the gridscan mainwindow and handle events
# generated by user interactions.nt
from PyQt5 import QtCore, QtWidgets, QtGui, uic
from epics import caget, cainfo, caput
from MySMPEpics import *
from BrukerClient import *
import sys

class SMPControl (QtWidgets.QMainWindow):

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.ui = uic.loadUi("mainwin.ui", self)
        self.smp = MySMPEpics()
        self.bc = BrukerClient()

        # get start positions of the m4 and m5 motors
        self.m4_instate = self.smp.get_m4_instate()
        self.m5_instate = self.smp.get_m5_instate()
        print "SMP M4 : %d"%self.m4_instate
        print "SMP M5 : %d"%self.m5_instate
        self.set_motor_labels()
        # get door status, 1 if locked, otherwise zero
        self.door_status = bc.get_door_status()
        curval = caget ("Dera:m4.VAL")
        if curval == None :
            mbox = QtGui.QMessageBox ()
            mbox.setWindowTitle ("GridScan Problem : EPICS")
            mbox.setIcon (QtGui.QMessageBox.Critical)
            mbox.setText ("Problem with EPICS communication")
            mbox.setInformativeText("Start EPICS IOC")
            mbox.exec_()
            sys.exit (app.exit(-1))

        self.ui.exitButton.clicked.connect(self.closeup)
        self.ui.m4_inbutton.clicked.connect (self.m4_in_event)
        self.bc.new_door_status.connect (self.update_door_status)
        self.bc.start()


    def update_door_status (self, doorlockFlag) :
        if (doorlockFlag == 1):
            self.ui.door_label.setText ("Door is closed")
        else :
            self.ui.door_label.setText("Door is open!")

    def set_motor_labels(self):
        self.m4_instate = self.smp.get_m4_instate()
        if self.m4_instate == 0:
            self.ui.m4_pos_label.setText("Out")

        if self.m4_instate == 1:
            self.ui.m4_pos_label.setText("In")
        if self.m4_instate == 2:
            self.ui.m4_pos_label.setText("Not Set")
        self.m5_instate = self.smp.get_m5_instate()
        if self.m5_instate == 0:
            self.ui.m5_pos_label.setText("Out")
            return
        if self.m5_instate == 1:
            self.ui.m5_pos_label.setText("In")
            return
        self.ui.m5_pos_label.setText("Not Set")

    ###
    # m4 in button pushed
    # conditions to move motor are that the door must be closed
    # otherwise ok to move in, doesn't care about m5
    ###
    def m4_in_event(self):
        if self.door_status == 0 :
            print "Door must be closed, no action will be taken...."
            return
        self.smp.set_m4_instate (1)
        self.set_motor_labels()

    ###
    # m4_out_event
    # m4 can only be moved out if m5 is out
    ###
    def m4_out_event (self) :
        if self.door_status == 0 :
            print "Door must be closed, no action will be taken...."
            return
        self.m5_instate = self.smp.get_m5_instate()
        #if m5 is in do nothing
        if self.m5_instate == 1 :
            print "Motor 5 must be out, no action will be taken...."
            return
        # move m4 out
        self.smp.set_m4_instate (0)
        # update labels
        self.set_motor_labels()

    def m5_in_event (self) :
        if self.door_status == 0 :
            print "Door must be closed, no action will be taken...."
            return
        self.m4_instate = self.smp.get_m4_instate()
        #if m4 is out do nothing
        if self.m4_instate == 0:
            print "Motor 4 must be in, no action will be taken...."
            return
        self.smp.set_m5_instate (1)
        self.set_motor_labels()

    def m5_out_event (self) :
        if self.door_status == 0 :
            print "Door must be closed, no action will be taken...."
            return
        self.smp.set_m5_instate (0)
        self.set_motor_labels()


	def closeup(self) :
        self.bc.stop()
        sys.exit(app.exit (0))





if __name__=='__main__':
    app = QtWidgets.QApplication(sys.argv)
    SMP = SMPControl()
    SMP.show()
    sys.exit(app.exec_())