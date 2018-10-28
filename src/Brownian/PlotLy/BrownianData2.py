# creates data for Plotly

import numpy as np
from scipy.stats import norm
import pickle

numFrames = 500 # 900 number of frames in animation, 1 minute = 900 frames at 15 fps
numParticles = 500 # 500 works OK
frameChange = 50 # 50, number of frames before making membrane 'permeable'
params = [numFrames, numParticles, frameChange]

boxSize = 4
xmin = -boxSize
xmax = boxSize
xmid = 0
ymin = -boxSize
ymax = boxSize
dotSize = boxSize/30 # this is a kludge to keep all dots inside box outline

def walk(numFrames, numParticles, xmin, xmax, ymin, ymax, dotSize):
    # Process parameters
    delta = 0.25
    dt = 5 # 2.5 choose value to get even mixing by 1 minute
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
                x = xmin + dotSize + abs(norm.rvs(scale = dotscale2))
            if k > frameChange: # change membrane 'permeability'
                if x > (xmax - dotSize):
                    x = xmax - dotSize - abs(norm.rvs(scale = dotscale2))
            else:
                if x > (xmid - dotSize):
                    x = xmid - dotSize - abs(norm.rvs(scale = dotscale2))
            if y < (ymin + dotSize):
                y = ymin + dotSize + abs(norm.rvs(scale = dotscale2))
            if y > (ymax - dotSize):
                y = ymax - dotSize - abs(norm.rvs(scale = dotscale2))
            # add point to array
            xdata[k,i] = x
            ydata[k,i] = y
            # get new points
            x = x + norm.rvs(scale = dotscale)
            y = y + norm.rvs(scale = dotscale)
    return [xdata, ydata]

def entropy(numFrames, numParticles, x1data):
    box2Particles = np.zeros(numFrames)
    for k in range(numFrames):
        x = x1data[k,:]
        inBox2 = 0
        for i in range(numParticles):
            if 0 <= x[i] : # only need to find if x is positive to test if particle in box 2
                inBox2 = inBox2 + 1
        box2Particles[k] = inBox2
        
    x2data = np.zeros((numFrames, numFrames))
    y2data = np.ones((numFrames, numFrames))*-10 # set negative value so not seen on graph
    for i in range(numFrames):
        for k in range(numFrames):
            # add point to array
            x2data[i,k] = k
            if k <= i:
                y2data[i,k] = box2Particles[k]
    return x2data, y2data


x1data, y1data = walk(numFrames, numParticles, xmin, xmax, ymin, ymax, dotSize)
x2data, y2data = entropy(numFrames, numParticles, x1data)
data = [params, x1data, y1data, x2data, y2data]

# write to pickle
pickle.dump(data, open( "data.pkl", "wb" ) )
