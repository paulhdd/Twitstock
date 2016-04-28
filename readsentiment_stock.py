import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import time
import sys

style.use("ggplot")

fig = plt.figure()
ax1 = fig.add_subplot(2,1,1)
ax2 = fig.add_subplot(2,1,2)

def animate(i):
    pullData = open('tweet_data_'+sys.argv[1]+'.txt','r').read()
    lines = pullData.split('\n')

    xar = []
    yar = []
    zar = []

    x = 0
    y = 0
    for l in lines:
    	if l!=lines[-1]:
    		l=l.split(' ')
    		x=x+1
    		y=y+int(l[0])
    		z=float(l[1])
    	xar.append(x)
    	yar.append(y)
    	zar.append(z)
        
    ax1.clear()
    ax1.plot(xar,yar)
    ax1.set_title('Twitter reaction to '+ sys.argv[1])
    ax2.clear()
    ax2.plot(xar,zar)
    ax2.set_title('Live price '+ sys.argv[1])

ani = animation.FuncAnimation(fig, animate, interval=1000)
plt.show()