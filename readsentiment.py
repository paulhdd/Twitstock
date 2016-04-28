import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import time
import sys

style.use("ggplot")

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1,title='Tweets sentiment for '+sys.argv[1])

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
        	x += 1
        	y += int(l)
    	xar.append(x)
    	yar.append(y)
        
    ax1.clear()
    ax1.plot(xar,yar)
    ax1.set_title('Twitter reaction to '+ sys.argv[1])
ani = animation.FuncAnimation(fig, animate, interval=1000)

plt.show()