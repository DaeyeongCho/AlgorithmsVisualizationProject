import os
import sys
import numpy as np
import time

from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

matplotlib.use('QT5Agg')

from define import *

def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))    
    return os.path.join(base_path, relative_path)

form = resource_path('main.ui')
form_class = uic.loadUiType(form)[0]

class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super( ).__init__( )
        ## ========== 정의 ========== ##

        # 박스 위젯 정의
        self.tabWidgetControl = QTabWidget()
        self.frameGraph = QFrame()
        self.verticalLayoutGraph = QVBoxLayout()
        self.listWidgetState = QListWidget()
        self.listWidgetLog = QListWidget()
        
        self.testButton1 = QPushButton()
        self.testButton2 = QPushButton()
        self.testButton3 = QPushButton()
        self.testButton4 = QPushButton()
        self.testButton5 = QPushButton()
        self.testButton6 = QPushButton()

        ## 초기 세팅 ##
        
        self.array = [5, 2, 4, 3, 1]
        
        self.setupUi(self) # ui 임포트
        
        self.add_graph_to_layout() # 그래프 삽입
        
        ## ================================================= 시그널 들 ================================================= ##
    







        ## 테스트 시그널들 ##
        self.testButton1.clicked.connect(self.testFunc1)
        self.testButton2.clicked.connect(self.testFunc2)
        self.testButton3.clicked.connect(self.testFunc3)
        self.testButton4.clicked.connect(self.testFunc4)
        self.testButton5.clicked.connect(self.testFunc5)
        self.testButton6.clicked.connect(self.testFunc6)
        # x = np.arange(0, 5)
        # self.ax.bar(x, [1, 5, 3, 4, 2])

        # 여기에 시그널, 설정 
    ## ================================================= 함수 들 ================================================= ##

    # 그래프 생성 함수
    def add_graph_to_layout(self):
        # Figure, FigureCanvas 생성
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.fig)

        # FigureCanvas를 QVBoxLayout에 추가
        self.verticalLayoutGraph.addWidget(self.canvas)
        self.animation = FuncAnimation(self.fig, self.update, frames=self.array, init_func=self.init_bars, blit=True, interval=1)
        self.canvas.draw()


    def init_bars(self):
        x = np.arange(len(self.array))
        self.bars = self.ax.bar(x, self.array, color='blue')
        return self.bars

    def update(self, frame):
        x = np.arange(len(self.array))
        self.bars = self.ax.bar(x, self.array)
        # self.bars = self.ax.bar(x, self.array, color='blue')
        # self.bars[1].set_facecolor('red')
        return self.bars
    




    ## 테스트 시그널 함수 ##
    def testFunc1(self):
        self.animation.pause()
        print("test1 message")

    def testFunc2(self):
        self.animation.resume()
        print("test2 message")

    def testFunc3(self):
        self.array = [1, 2, 3, 4, 5]
        print("test3 message")

    def testFunc4(self):

        print("test4 message")

    def testFunc5(self):

        print("test5 message")

    def testFunc6(self):

        print("test6 message")




if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = WindowClass( )
    myWindow.show( )
    app.exec_( )
