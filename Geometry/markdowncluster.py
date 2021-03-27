import re
import numpy as np
import matplotlib.pyplot as plt
import sys

f=open(r'tempFile.txt',"r")
ta=[float(n) for n in f]
tb=[ta[0]]
tb.extend([ta[i]-ta[i-1] for i in range(1,len(ta))])
f.close()
tc=[sum([(t==i) for t in tb]) for i in range(0,10)]
f=open(r'logFile.txt',"a")
f.write(str(sys.argv[1])+"\n")
f.write(str(sys.argv[2])+"\n")
f.write(str(sys.argv[3])+"\n")
for c in tc:
    f.write(str(c)+" ")
f.write("\n")
f.close()