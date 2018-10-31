import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['animation.ffmpeg_path'] = '/anaconda3/bin/ffmpeg' # this has to come before animation import
import matplotlib.animation as animation
from scipy.stats import norm

numFrames = 900 # 900 number of frames in animation, 1 minute = 900 frames at 15 fps
numParticles = 500 # 500 is good number
boxSize = 4
xmin = -boxSize
xmax = boxSize
ymin = -boxSize
ymax = boxSize
dotSize = boxSize/30 # this is a kludge to keep all dots inside box outline

def walk(numFrames, numParticles, xmin, xmax, ymin, ymax, dotSize):
    # Process parameters
    delta = 0.25
    dt = 2.5 # choose value to get even mixing by 1 minute
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

data = walk(numFrames, numParticles, xmin, xmax, ymin, ymax, dotSize)

fig = plt.figure()
ax = plt.axes(xlim=(xmin, xmax), ylim=(ymin, ymax))
ax.tick_params(bottom=False, left=False, labelbottom=False, labelleft=False ) 
scatPlot = plt.scatter([], [], s=100)

anim = animation.FuncAnimation(fig, update, init_func=init, fargs=(scatPlot, data), 
                               interval=1, frames=numFrames, blit=True, repeat=False)

# parameters have big effect on video quality and file size, dpi can be reduced for these small videos
# dpi <100 crashes program
# bitrate=-1 gives best quality, but have to worry about file size, do not need a very high bit rate
anim.save('Brownian1.mp4', fps=15, writer='ffmpeg', bitrate=2000, dpi=100)

plt.show()
