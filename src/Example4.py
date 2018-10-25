# -*- coding: utf-8 -*-

import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np
from scipy.stats import norm

win = pg.GraphicsWindow()
win.resize(550,600)
# win.setWindowTitle('pyqtgraph example: Histogram')
plt1 = win.addPlot()

# Process parameters
delta = 0.25
dt = 0.1

x = 0.0
y = 0.0
x = np.array([x])
y = np.array([y])

p1 = win.addPlot()
curve1 = p1.plot()


# Number of iterations to compute.
n = 20

# Iterate to compute the steps of the Brownian motion.
for k in range(n):
    curve1.setData(x, y)
    
    x = np.array([x + norm.rvs(scale = delta**2 * dt)])
    y = np.array([y + norm.rvs(scale = delta**2 * dt)])
    print(x)

n = 5000

# x = np.cumsum(np.random.randn(n))
# y = np.cumsum(np.random.randn(n))
# 
# 
# plt1.plot(x, y)


## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()