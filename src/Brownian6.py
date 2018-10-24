from pyqtgraph.Qt import QtGui, QtCore, QtWidgets
import numpy as np
import pyqtgraph as pg
from pyqtgraph.ptime import time

app = QtWidgets.QApplication([])

p = pg.plot()
p.setWindowTitle('live plot from serial')
curve = p.plot()

data.append(float(line[4]))
xdata = np.array(data, dtype='float64')
curve.setData(xdata)