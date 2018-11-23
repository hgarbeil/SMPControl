# SMPControl
Motor control for SMP100 with pyEpics protocol
## Requirements
Program requires pyEpics and various hardware devices which are interfaced to the computer
via pyEpics. Also python2.7 and PyQt5. Bruker instrument communication via the BIServer. IPaddress is hardwired here.
## Motor stages
Motors can be placed into 2 positions, either in or out. In the program, the m4_instate refers to 0 for out, 1 for in, and
2 for undefined. Numerical displacements of the stage corresponding to in and out are defined is MySMPControl.py.
## Files
SMPControl.py

Main class and program which loads the ui and handles button events. This class starts the BrukerClient that interfaces to the Bruker instrument and the instantiates and addresses the MySMPEpics class which which communicates to the SMP controller via the Epics interface. The motor in and out commands also contain the logic which will allow or prevent motion from occuring.

BrukerClient.py

Program and class for the BrukerClient. In this case, we are only interested in monitoring the access door. Communication via the ui by sending a signal if the DOORLOCKED state is modified.

MySMPEpics.py

SMP controller class which relies on the Epics library to get and set the position of the M4 and M5 motors. The logic to allow motion is contained in the SMPControl.py program.

mainwin.ui

User interface file which controls content and layout of the user interface. This file is loaded upon startup by the SMPControl.py class init function.
