import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

f=open("copyitdownFORREALDay3.txt","r")
n=[g for g in f]
h1,h2=[],[]
n=n[8:]
old,new=0,0
for i in range(0,len(n)):
        if i%2==0:
                h1.append([float(n[i][1:4]),float(n[i][5:9])])
        else:
                h2.append(float(n[i][:len(n[i])-1]))
for i in range(0,len(h2)):
        if h2[i]>1000:
                print(i)
help1=h1[0:157]
help1.extend(h1[158:])
help2=h2[0:157]
help2.extend(h2[158:])
h1=help1
h2=help2
x,y,z=[h1[n][0] for n in range(0,len(h1))],[h1[n][1] for n in range(0,len(h1))],h2
#print(x)
#print(y)
#print(z)
fig=plt.figure()
ax=fig.add_subplot(111,projection='3d')
ax.scatter(x,y,z,c='k',marker='o')
ax.set_xlabel('Trigger Pad Thickness (mm)')
ax.set_ylabel('Trigger Spacing Thickness (mm)')
ax.set_zlabel('nTracks with nEv=75,nE=2')

#print(h2)
#h1,h2=[],[]
#for i in range(0,len(n)):
#    if i%2==0:
#        #print(n[i][1:5])
#        h1.append(float(n[i][1:5]))
#    else:
#        #print(n[i][1:len(n[i])-1])
#        h2.append(float(n[i][0:len(n[i])-1]))
#plt.plot(h1,h2,"k")
#plt.xlabel("Trigger Pad Thickness (mm)")
#plt.ylabel("nTracks for nEv=1000, nE=2")