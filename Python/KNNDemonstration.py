import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from sklearn import neighbors, datasets
from matplotlib.colors import ListedColormap

iris = datasets.load_iris()
X = iris.data[:,:2]
y = iris.target

fig, ax = plt.subplots()
xdata, ydata = [], []
ln, = plt.plot([], [], 'ro', animated=True)


point = [0,0]

def onclick(event):
    print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
          ('double' if event.dblclick else 'single', event.button,
           event.x, event.y, event.xdata, event.ydata))
    point = [event.xdata, event.ydata]
    ani = FuncAnimation(fig, update, frames=np.linspace(0, 2 * np.pi, 128),
                            init_func=init2, blit=True)
    plt.show()


cid = fig.canvas.mpl_connect('button_press_event', onclick)

def init1():
    ax.set_xlim(np.min(X[:,:1])-0.5, np.max(X[:,:1])+0.5)
    ax.set_ylim(np.min(X[:,1:])-0.5, np.max(X[:,1:])+0.5)
    ax.scatter(X[:, 0], X[:, 1], c=y, cmap=ListedColormap(['#FF0000', '#00FF00', '#0000FF']))
    return ln,

def init2():
    ax.set_xlim(np.min(X[:,:1])-0.5, np.max(X[:,:1])+0.5)
    ax.set_ylim(np.min(X[:,1:])-0.5, np.max(X[:,1:])+0.5)
    ax.scatter(X[:, 0], X[:, 1], c=y, cmap=ListedColormap(['#FF0000', '#00FF00', '#0000FF']))
    ax.scatter(point[0],point[1],c="#999999" )
    return ln,

def update(frame):
    print(frame)
    xdata.append(frame)
    ydata.append(np.sin(frame))
    ln.set_data(xdata, ydata)
    return ln,

ani = FuncAnimation(fig, update, frames=np.linspace(0, 2*np.pi, 128),
                    init_func=init1, blit=True)

plt.show()
