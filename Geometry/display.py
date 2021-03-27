import matplotlib.pyplot as plt
import numpy as np
f=open("copyitdown2.txt","r")
counter=0
coor,val=[],[]
def getCoor(n):
    return [0,0,0,0]
for n in f:
    if counter%2==0:
        coor.append(getCoor(n))
    if counter%2==1:
        val.append(float(n))
