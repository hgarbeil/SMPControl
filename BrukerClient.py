import socket
import sys
import time
from PyQt5 import QtCore, QtGui


class BrukerClient (QtCore.QThread) :

    BSIZE = 1024
    serverip = '128.171.152.86'
    shutter_state = QtCore.pyqtSignal(int)
    newangles = QtCore.pyqtSignal ()
    new_door_status = QtCore.pyqtSignal(int)

    def __init__(self):
        QtCore.QThread.__init__(self)
        self.door_status = 0
        self.connect()


    def get_door_status(self):
        message = "[INSTRUMENTSTATUS /DOORLOCK ]\n"
        try:
            print "sending message to bis"
            self.command_sock.send(message)
            time.sleep(1)
            while (1):
                data = self.status_sock.recv(1024)
                print data
                if "[INSTRUMENT" in data:
                    print "found message"
                    loc = data.find("DOORLOCK=")
                    newstr = data[loc:]
                    eqloc = newstr.find('=')
                    self.door_status = int(newstr[eqloc + 1])


                    print 'Door status : %d'%self.door_status

                    # print data
        except socket.error, msg:
            print "Drive error : %s" % msg
        return (1)


    def connect (self) :
        try :
            self.shutter_status = 0
            self.chi = 0
            self.omega = 0
            self.phi = 0
            self.chi = 0
            self.bcrun = False
            self.bcstatus= True
            self.distance = 0

            self.command_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.command_sock.settimeout(10.)
            #   command_sock.setblocking(0)
            self.file_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.file_sock.settimeout(10.)
            #file_sock.setblocking(0)
            self.status_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.status_sock.settimeout(10.)
            #status_sock.setblocking(0)
            server_address = (BrukerClient.serverip, 49153)
            print >> sys.stderr, 'connecting to %s port %s'%server_address
            self.command_sock.connect (server_address)

            server_address = (BrukerClient.serverip, 49154)
            print >> sys.stderr, 'connecting to %s port %s'%server_address
            self.file_sock.connect (server_address)
            server_address = (BrukerClient.serverip, 49155)
            print >> sys.stderr, 'connecting to %s port %s'%server_address
            self.status_sock.connect (server_address)
            #self.get_status()
            #time.sleep (20)
            self.start()

            self.bcrun = False
        except socket.error, msg :
            print "Could not connect with socket : %s"%msg
            self.bcstatus = False


    def get_status (self):
        try :
            while (1):
                data = self.status_sock.recv(BrukerClient.BSIZE)
                print data
        except socket.error, msg:
            print "Shutter status error : %s" % msg

        # drive to position of 200mm, 2theta= -30 omega=0 and phi=180


    # thread method to check the status socket for any updates.
    def run (self) :
        self.bcrun = True
        while (self.bcrun) :
            try :
                data = self.status_sock.recv(1024)
            except socket.error, msg :
                #print "Thread read error: %s"%msg
                self.sleep (3)
                continue
            #get shutter status if available
            if ("[SHUTTERSTATUS" in data) :
                startloc = data.find("[SHUTTERSTATUS")
                temp = data[startloc:]
                eqloc = temp.find('=')
                self.shutter_status  = int(temp[eqloc+1])
                print "**shutter is ** ", self.shutter_status

            #get angles if available , turns this off
            ###
            # if ("[ANGLESTATUS" in data) :
            #     #print data
            #     startloc = data.find ("[ANGLESTATUS")
            #     temp = data [startloc:]
            #     eqsplit = temp.split('=')
            #     angles = eqsplit[1]
            #     subangles = angles.split(' ')
            #     print "ANGLES ARE 2theta ",subangles[0], ' omega : ',subangles[1], " phi : ", subangles[2], " chi : ", subangles[3]
            #     print "Distance is : ", eqsplit[2][0:eqsplit[2].find(']')]
            #     self.twotheta = float(subangles[0])
            #     self.phi=float(subangles[2])
            #     self.omega=float(subangles[1])
            #     self.distance=float (eqsplit[2][0:eqsplit[2].find(']')])
            #     self.newangles.emit()
            #

            if "[INSTRUMENTSTATUS" in data:
                print "found message"
                loc = data.find("DOORLOCK=")
                newstr = data[loc:]
                eqloc = newstr.find('=')
                self.door_status = int(newstr[eqloc + 1])
                #self.new_door_status.emit (self.door_status)

                print 'Door status : %d' % self.door_status


            if (len(data) == 0) :
                self.sleep (1)


    def stop (self):
        self.bcrun = False

#bc = BrukerClient()
#bc.open_shutter()
#bc.close_shutter()
#sys.exit(0)