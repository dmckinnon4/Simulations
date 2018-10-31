import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['animation.ffmpeg_path'] = '/anaconda3/bin/ffmpeg' # this has to come before animation import
import matplotlib.animation as animation
from scipy.stats import norm

numFrames = 1 # 900 number of frames in animation, 1 minute = 900 frames at 15 fps
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
            # check particles are within limits and adjust if necessary
            if x < (xmin + dotSize):
                x =  xmin + dotSize + abs(norm.rvs(scale = dotscale2))
            if x > (xmax - dotSize):
                x =  xmax - dotSize - abs(norm.rvs(scale = dotscale2))
            if y < (ymin + dotSize):
                y =  ymin + dotSize + abs(norm.rvs(scale = dotscale2))
            if y > (ymax - dotSize):
                y =  ymax - dotSize - abs(norm.rvs(scale = dotscale2))
            # add point to array
            data[k,i] = [x,y]
            # get new points
            x = x + norm.rvs(scale = dotscale)
            y = y + norm.rvs(scale = dotscale)
    return data

data = walk(numFrames, numParticles, xmin, xmax, ymin, ymax, dotSize)
# print("all")
# print(data, "\n")
data = data[0].T
# print("transform")
# print(data, "\n")

print(data[1:], "\n")
import plotly
import plotly.graph_objs as go
 
# Create a trace
trace = go.Scatter(
    x = data[0],
    y = data[1],
    mode = 'markers'
)

data = [trace]
 
plotly.offline.plot(data, filename='basic-line.html')
