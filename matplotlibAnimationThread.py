import os
import sys
import numpy as np
import time
import threading
import random

from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class BarGraphViewThread(threading.Thread):
    def __init__(self, fig, ax, array, pivot = [], compare = [], fixed = []):
        super().__init__()

        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.fig)

        self.escape = False
        self.fig = fig
        self.ax = ax
        self.array = array
        self.pivot = pivot
        self.compare = compare
        self.fixed = fixed

    def run(self):
        self.animation = FuncAnimation(self.fig, self.update, frames=self.array, init_func=self.init_bars, blit=True, interval=1)

    def init_bars(self):
        x = np.arange(len(self.array))
        self.bars = self.ax.bar(x, self.array, color='C0')
        return self.bars

    def update(self, frame):
        print(frame)
        x = np.arange(len(self.array))
        self.bars = self.ax.bar(x, self.array, color='C0')
        # self.bars = self.ax.bar(x, self.array, color='blue')
        # self.bars[1].set_facecolor('red')
        return self.bars
    

