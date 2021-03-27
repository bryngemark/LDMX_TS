import sys
import numpy as np
nElectron=2
nEvent=500
f= open("copyitdownFORREALDay3.txt","a")
if int(sys.argv[1])==0:
    f.write(str(sys.argv[2])+"\n")
else:
    f.write(str(np.sqrt((float(sys.argv[2])/nEvent-nElectron)**2))+"\n")
####TO BE GENERATED TO EVALUATE CONFIGURATION FITNESS
f.close()
