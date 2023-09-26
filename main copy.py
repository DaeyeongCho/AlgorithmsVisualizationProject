import os
import sys
import threading
import numpy as np
import time
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

matplotlib.use('QT5Agg')

from define import *

# 프로그램 아이콘 생성
def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))    
    return os.path.join(base_path, relative_path)
form = resource_path(ICON_FILE_NAME)
form_class = uic.loadUiType(form)[0]



class MixArray(threading.Thread):
    def __init__(self, array, mixNum, ani):
        super().__init__()
        self.array = array
        self.mixNum = mixNum
        self.ani = ani

    def run(self):
        for _ in range(1000000):
            print("shuffle array")
            sampleList = random.sample(list(range(2, 70)), 2)
            self.array[sampleList[0]], self.array[sampleList[1]] = self.array[sampleList[1]], self.array[sampleList[0]]
            time.sleep(1/60)



class AlgorithmSimulation(QThread):
    def __init__(self, array, pivot, compare, fixed):
        super().__init__()
        self.array = array
        self.pivot = pivot
        self.compare = compare
        self.fixed = fixed
        self.escape = False

    def run(self):
        while not self.escape:
            pass

    def arraySort(self):
        print("arraySort")

    def arraySearch(self):
        pass
        
        



## 그래프 표현 클래스 ##
class ViewGraph(QThread):
    def __init__(self, array, pivot, compare, fixed):
        super().__init__()
        self.array = array
        self.pivot = pivot
        self.compare = compare
        self.fixed = fixed
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.fig)
        self.ax = plt.bar(np.arange(1, len(self.array) + 1), self.array, width=0.5)
        self.canvas.draw()
        self.escape = False
        self.view = True

    def run(self):
        while not self.escape:
            if self.view == True:
                self.graphAnimation()
            else:
                pass

    def graphAnimation(self):
        for height, barRectangle in zip(self.array, self.ax):
            print("draw graph")
            barRectangle.set_height(height)
            if height in self.pivot:
                barRectangle.set_color("C1")
            elif height in self.compare:
                barRectangle.set_color("C2")
            elif height in self.fixed:
                barRectangle.set_color("C3")
            else:
                barRectangle.set_color("C0")
        self.canvas.draw()
        time.sleep(1/60)
    
    def viewQuit(self):
        self.escape = True
        # self.canvas.close()

    def viewResume(self):
        self.view = True

    def viewPause(self):
        self.view = False



# 메인 윈도우
class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super( ).__init__( )
        ## ========== 정의 ========== ##

        # 박스 위젯 정의
        self.tabWidgetControl: QTabWidget
        self.frameGraph: QFrame
        self.verticalLayoutGraph: QVBoxLayout
        self.listWidgetState: QListWidget
        self.listWidgetLog: QListWidget
        
        # 정렬 알고리즘 위젯
        comboBox_sort_select_Algorithm: QComboBox
        spinBox_sort_data_size: QSpinBox
        spinBox_sort_speed_limit: QSpinBox
        spinBox_sort_shuffle_number: QSpinBox
        pushButton_sort_start: QPushButton
        pushButton_sort_restart: QPushButton
        pushButton_sort_stop: QPushButton
        
        self.testButton1: QPushButton
        self.testButton2: QPushButton
        self.testButton3: QPushButton
        self.testButton4: QPushButton
        self.testButton5: QPushButton
        self.testButton6: QPushButton
        
        ## 초기 세팅 ##

        self.setupUi(self) # ui 임포트

        self.array = list(range(1, 101))
        self.pivot = []
        self.compare = []
        self.fixed = []

        ## 그래프 출력 및 애니메이션 실행 ##
        self.canvas: FigureCanvas
        self.animationThread = ViewGraph(self.array, self.pivot, self.compare, self.fixed)
        self.verticalLayoutGraph.addWidget(self.animationThread.canvas)

        self.animationThread.start()


        # self.algorithmThread = AlgorithmSimulation(self.array, self.pivot, self.compare, self.fixed)
        # self.algorithmThread.start()

        # self.mix = MixArray(self.array, 100, self.animationThread)
        # self.mix.daemon = True
        # self.mix.start()
        

        
        ## ================================================= 시그널 들 ================================================= ##
    


    

        ## 테스트 시그널들 ##
        self.testButton1.clicked.connect(self.testFunc1)
        self.testButton2.clicked.connect(self.testFunc2)
        self.testButton3.clicked.connect(self.testFunc3)
        self.testButton4.clicked.connect(self.testFunc4)
        self.testButton5.clicked.connect(self.testFunc5)
        self.testButton6.clicked.connect(self.testFunc6)

        # 여기에 시그널, 설정 
    ## ================================================= 함수 들 ================================================= ##
    def closeEvent(self, event): ## 프로그램 종료 시 자동 작동 함수
        self.animationThread.escape = True
        event.accept()


    ## 테스트 시그널 함수 ##
    def testFunc1(self):
        print("test1 message")
        self.animationThread.viewPause()

    def testFunc2(self):
        print("test2 message")
        self.animationThread.viewResume()

    def testFunc3(self):
        self.algorithmThread.arraySort()
        print("test3 message")

    def testFunc4(self):
        self.array = list(range(1, 10))
        self.animationThread.ax = plt.bar(np.arange(1, len(self.array) + 1), self.array, width=0.5)
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
