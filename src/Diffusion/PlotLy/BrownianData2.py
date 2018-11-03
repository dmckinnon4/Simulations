# creates data for Plotly, produces an average of entropy

import numpy as np
from scipy.stats import norm
import pickle

numFrames = 201 # 501 number of frames in animation
numParticles = 50 # 500 works OK
frameChange = 50 # 50, number of frames before making membrane 'permeable'
numAverages = 100 # 10, number of times to average entropy data
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

def entropy(numFrames, numParticles, numAverages):
    box2List =[]
    for i in range(numAverages):
        x1data, y1data = walk(numFrames, numParticles, xmin, xmax, ymin, ymax, dotSize)

        box2Particles = np.zeros(numFrames)
        for k in range(numFrames):
            x = x1data[k,:]
            inBox2 = 0
            for i in range(numParticles):
                if 0 <= x[i] : # only need to find if x is positive to test if particle in box 2
                    inBox2 = inBox2 + 1
            box2Particles[k] = inBox2
        box2List.append(box2Particles)
    box2Particles = np.mean(box2List, axis=0)
    
    y2data = box2Particles/numParticles*2   # normalize the entropy values to number of particles
    x2data = np.arange(numFrames)                
    # returns last version of x1data, y1data
    return x1data, y1data, x2data, y2data
    
x1data, y1data, x2data, y2data = entropy(numFrames, numParticles, numAverages)  

data = [params, x1data, y1data, x2data, y2data]

# write with pickle
pickle.dump(data, open( "data.pkl", "wb" ) )
