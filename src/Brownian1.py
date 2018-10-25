import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy.stats import norm

numFrames = 500 # number of frames in animation
numParticles = 50
boxSize = 4
xmin = -boxSize
xmax = boxSize
ymin = -boxSize
ymax = boxSize
dotSize = boxSize/30 # this is a kludge to keep all dots inside box outline

def walk2(numFrames, numParticles, xmin, xmax, ymin, ymax, dotSize):
    # Process parameters
    delta = 0.25
    dt = 1.0
    dotscale = delta**2 * dt
    dotscale2 = dotscale/2
    data = np.zeros((numFrames, numParticles, 2))
    
    for i in range(numParticles):
        x = np.random.uniform(xmin, 0)
        y = np.random.uniform(ymin, ymax)
        for k in range(numFrames):
            x = x + norm.rvs(scale = dotscale)
            if x < (xmin + dotSize):
                x =  xmin + dotSize + abs(norm.rvs(scale = dotscale2))
            if x > (xmax - dotSize):
                x =  xmax - dotSize - abs(norm.rvs(scale = dotscale2))
            y = y + norm.rvs(scale = dotscale)
            if y < (ymin + dotSize):
                y =  ymin + dotSize + abs(norm.rvs(scale = dotscale2))
            if y > (ymax - dotSize):
                y =  ymax - dotSize - abs(norm.rvs(scale = dotscale2))
            data[k,i] = [x,y]
    return data

def init():
    scatPlot.set_offsets([[], []])
    return [scatPlot]

def update(i, scatPlot, data):
    scatPlot.set_offsets(data[i])
    return [scatPlot]


data = walk2(numFrames, numParticles, xmin, xmax, ymin, ymax, dotSize)
C = np.zeros(shape=(numParticles, 3))
# C = C + 'Default blue'
C[0:-1][1] = 1
C[0] = [1, 0, 0]

fig = plt.figure()
ax = plt.axes(xlim=(xmin, xmax), ylim=(ymin, ymax))
scatPlot = plt.scatter([], [], s=100,  c = C)




anim = animation.FuncAnimation(fig, update, init_func=init, fargs=(scatPlot, data), 
                               interval=1, frames=numFrames, blit=True, repeat=False)
plt.show()
