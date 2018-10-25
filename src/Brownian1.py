import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy.stats import norm

numFrames = 1000 # number of frames in animation
numParticles = 500
boxSize = 4
xmin = -boxSize
xmax = boxSize
ymin = -boxSize
ymax = boxSize
dotSize = boxSize/30 # this is a kludge to keep all dot inside box

def walk(numFrames, xmin, xmax, ymin, ymax, dotSize):
    # Process parameters
    delta = 0.25
    dt = 1.0
    dotscale = delta**2 * dt
    dotscale2 = dotscale/2
    data = []
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
        data.append([x,y])
    return data

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

# data = walk(numFrames, xmin, xmax, ymin, ymax, dotSize)
from timeit import default_timer as timer

start = timer()
data = [walk(numFrames, xmin, xmax, ymin, ymax, dotSize) for index in range(numParticles)]
end = timer()
print('walk time = ', end - start)

start = timer()
data2 = walk2(numFrames, numParticles, xmin, xmax, ymin, ymax, dotSize)
# data = [walk(numFrames, xmin, xmax, ymin, ymax, dotSize) for index in range(numParticles)]
end = timer()
print('walk2 time = ', end - start)
# print('data2 = ', data2)
data = data2

# # print(data)
# start = timer()
# data = np.array(data)
# # data = data.swapaxes(0,1)
# end = timer()
# print('swap axes = ', end - start)
# print(data.size)

# start = timer()
# newdata = []
# for i in range(numFrames):
#     temp = []
#     for dat in data:
#         temp.append(dat[i])
#     newdata.append(temp)
# data = newdata
# end = timer()
# print('swap axes 2 = ', end - start)

fig = plt.figure()
ax = plt.axes(xlim=(xmin, xmax), ylim=(ymin, ymax))
scatPlot = plt.scatter([], [], s=100)

anim = animation.FuncAnimation(fig, update, init_func=init, fargs=(scatPlot, data), 
                               interval=1, frames=numFrames, blit=True, repeat=False)
plt.show()