import re
import numpy as np
import matplotlib.pyplot as plt
import sys

#sys.argv[i] establishes the value of the ith gdml constant desired

#Establishes which ldmx configuration file to open
f=open(r'../ldmx-sw/Detectors/data/ldmx-det-v12/constants.gdml',"r")
#f=open(r'../ldmx-sw/Detectors/data/ldmx-det-v12/scoring_planes.gdml',"r")
ta=[n for n in f]
f.close()

#Original was 3 mm
#and .3mm
print(len(sys.argv)-1)
coor,val=[],[]
for i in range(1,len(sys.argv)):
    if i%2==1:
        coor.append(sys.argv[i])
    else:
        val.append(sys.argv[i])
for j in range(0,len(coor)):
    ta[int(coor[j])]=ta[int(coor[j])][:51]+str(val[j])+ta[int(coor[j])][len(ta[int(coor[j])])-8:]

#helper1=sys.argv[1]
#helper2=sys.argv[2]
#helper3=sys.argv[3]
#print(helper1)
#print(helper2)
#print(ta[23])

#print(ta[59])
#ta[59]=ta[59][:37]+str(helper1)+ta[59][len(ta[59])-4:]
#print(ta[35])
#print(ta[35][:51]+str(helper1)+ta[35][len(ta[35])-8:])
#ta[35]=ta[35][:51]+str(helper1)+ta[35][len(ta[35])-8:]
#ta[36]=ta[36][:51]+str(helper2)+ta[36][len(ta[36])-8:]
#ta[37]=ta[37][:51]+str(helper3)+ta[37][len(ta[37])-8:]
print(ta[35])
print(ta[36])
print(ta[37])
#ta[37]=ta[37][:51]+str(helper2)+ta[37][len(ta[37])-8:]


#f=open(r'../ldmx-sw/Detectors/data/ldmx-det-v12/constants.gdml',"w")
#for a in ta:
#    f.write(a)
