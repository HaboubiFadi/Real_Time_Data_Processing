import matplotlib.pyplot as plt
import matplotlib.animation as animation

from matplotlib import style
import sys
sys.path.append('/home/haboubi/Desktop/projects/pyspark/kafka_Api_finance')
from requirment import resource_path



def animate(i,key,ax1):
    ful_path=resource_path+str(key)+'.txt'
    mav=[]
    graph_data=open(ful_path,'r').read()
    lines=graph_data.split('\n')
    xs =[]
    ys= []
    l=0
    for line in lines :
        if len(line) > 1:
            l=l+1
            if l>200:
                table =line.split(',')
                xs.append(table[0][5:17])
                ys.append(float(table[4]))
                mav.append(float(table[8]))
    ax1.clear()
    ax1.plot(xs,ys)    
    ax1.plot(xs,ys)         
    ax1.plot(xs,mav)  
def animation_data(key):
    fig =plt.figure()
    ax1=fig.add_subplot(1,1,1)
    ani=animation.FuncAnimation(fig,animate,interval=100,fargs=(key,ax1))
    plt.show()