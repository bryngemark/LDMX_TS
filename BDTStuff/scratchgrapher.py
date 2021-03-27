import matplotlib.pyplot as plt
def getArray(word):
    f=open(word,"r")
    a=[float(lines) for lines in f]
    f.close()
    ax,ay=[],[]
    print(len(a))
    for i in range(0,100):
        ax.append(a[2*i])
        ay.append(a[2*i+1])
    return ax,ay
ax,ay=getArray("scratch1.txt")
bx,by=getArray("scratch2.txt")
cx,cy=getArray("scratch3.txt")
dx,dy=getArray("scratch4.txt")
plt.xlabel("Fraction of Remaining True Rate Events")
plt.ylabel("Fraction of Remaining False Rate Events")
plt.title("True/False Rate ROC Curves for Residual Selection")
plt.plot(ax,ay,"r",label="1 e Events")
plt.plot(bx,by,"b",label="2 e Events")
plt.plot(cx,cy,"g",label="3 e Events")
plt.plot(dx,dy,"k",label="4 e Events")
plt.legend(loc="upper left")
plt.show()