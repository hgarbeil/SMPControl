# SMPControl
Motor control for SMP100 with pyEpics protocol
## Requirements
Program requires pyEpics and various hardware devices which are interfaced to the computer
via pyEpics. Also python2.7 and PyQt5. Bruker instrument communication via the BIServer. IPaddress is hardwired here.
## Motor stages
Motors can be placed into 2 positions, either in or out. In the program, the m4_instate refers to 0 for out, 1 for in, and
2 for undefined. Numerical displacements of the stage corresponding to in and out are defined is MySMPControl.py.
