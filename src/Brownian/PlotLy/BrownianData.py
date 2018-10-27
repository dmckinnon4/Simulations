# creates data for Plotly

import numpy as np
from scipy.stats import norm
import pickle

numFrames = 1 # 900 number of frames in animation, 1 minute = 900 frames at 15 fps
numParticles = 1 # 500 is good number
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
    xdata = np.zeros((numFrames, numParticles))
    ydata = np.zeros((numFrames, numParticles))
    
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
            xdata[k,i] = x
            ydata[k,i] = y
            # get new points
            x = x + norm.rvs(scale = dotscale)
            y = y + norm.rvs(scale = dotscale)
    return [xdata, ydata]

data = walk(numFrames, numParticles, xmin, xmax, ymin, ymax, dotSize)

# write to pickle
pickle.dump(data, open( "data.pkl", "wb" ) )
