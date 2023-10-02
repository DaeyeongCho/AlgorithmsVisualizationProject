import copy
import os
import os.path
import shutil
import sys
import time
import random

#PyQt5 임포트
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import *

# pyqtgraph 임포트
import pyqtgraph as pg

# numpy 임포트
import numpy as np

# 사용자 모듈 임포트
from define import * # 상수, 스트링 모음


# 절대 경로 추출 함수
def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))    
    return os.path.join(base_path, relative_path)

# 파일 존재 유무
def isFileFunc(file_path):
    if os.path.isfile(file_path):
        return True
    else:
        return False

# main.ui 연결 변수
form_class = uic.loadUiType(resource_path(UI_FILE_PASS))[0]



## ================================================= 진행 시간 클래스 ================================================= ##
## ================================================= 진행 시간 클래스 ================================================= ##
## ================================================= 진행 시간 클래스 ================================================= ##
## ================================================= 진행 시간 클래스 ================================================= ##
## ================================================= 진행 시간 클래스 ================================================= ##
class RunTimer(QObject):
    run_time_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.start_time = time.time()
        self.now_time = time.time()
        self.timestamp = "00:00.000"

        self.run_timer = QTimer()
        self.run_timer.setInterval(int(1))
        self.run_timer.timeout.connect(self.run)

    def newStart(self):
        self.start_time_init()
        self.start()

    def start(self):
        self.run_timer.start()

    def stop(self):
        self.run_timer.stop()

    def start_time_init(self):
        self.start_time = time.time()

    def getRunTime(self):
        return self.timestamp

    def run(self):
        self.now_time = int((time.time() - self.start_time) * 1000)
        self.timestamp = str(self.now_time // 60000).zfill(2) + ":" + str((self.now_time % 60000) // 1000).zfill(2) + "." + str(self.now_time % 1000).zfill(3)
        self.run_time_signal.emit()

## ================================================= 진행 시간 클래스 끝 ================================================= ##



## ================================================= 그래프 뷰어 클래스 ================================================= ##
## ================================================= 그래프 뷰어 클래스 ================================================= ##
## ================================================= 그래프 뷰어 클래스 ================================================= ##
## ================================================= 그래프 뷰어 클래스 ================================================= ##
## ================================================= 그래프 뷰어 클래스 ================================================= ##
## ================================================= 그래프 뷰어 클래스 ================================================= ##
class ViewGraph(QObject):
    def __init__(self):
        super().__init__()
        self.graph = pg.PlotWidget(title="graph") # pyqtgraph 객체 생성
        self.graph.setBackground('w') # pyqtgraph 색 지정
        self.graph_timer = QTimer() # graph 반복 생성을 위한 타이머
        self.graph_timer.setInterval(int(1000/fps)) # 타이머 초기화
        self.graph_timer.timeout.connect(self.draw_graph) # 타이머가 매 타임마다 실행할 함수
    

    ## 그래프를 초기화하고 fps에 맞게 그래프를 리프레쉬하는 함수 ##
    def start(self):
        self.graph.clear() # 기존 그래프 존재 시 제거

        self.graph.addLegend() # 범례 표시

        self.x = np.arange(len(array)) # array를 막대그래프로 표시 초기화
        self.ypp = [x + 1 for x in array]
        self.bar = pg.BarGraphItem(x=self.x, height=self.ypp, width=BAR_WIDTH, pen=None, brush=BASIC_COLOR, name="basic")
        self.graph.addItem(self.bar)
        
        self.y = [0] * len(array) # compare는 모든 막대에서 0으로 초기화하여 안보이게 함
        self.bar_compare = pg.BarGraphItem(x=self.x, height=self.y, width=BAR_WIDTH, pen=None, brush=COMPARE_COLOR, name="compare")
        self.graph.addItem(self.bar_compare)

        self.y = [0] * len(array) # compare_other 모든 막대에서 0으로 초기화하여 안보이게 함
        self.bar_compare_other = pg.BarGraphItem(x=self.x, height=self.y, width=BAR_WIDTH, pen=None, brush=COMPARE_COLOR)
        self.graph.addItem(self.bar_compare_other)

        self.y = [0] * len(array) # compare_list 모든 막대에서 0으로 초기화하여 안보이게 함
        self.bar_compare_list = pg.BarGraphItem(x=self.x, height=self.y, width=BAR_WIDTH, pen=None, brush=COMPARE_COLOR)
        self.graph.addItem(self.bar_compare_list)

        self.y = [0] * len(array) # pivot 모든 막대에서 0으로 초기화하여 안보이게 함
        self.bar_pivot = pg.BarGraphItem(x=self.x, height=self.y, width=BAR_WIDTH, pen=None, brush=PIVOT_COLOR, name="pivot")
        self.graph.addItem(self.bar_pivot)

        self.y = [0] * len(array) # fix는 모든 막대에서 0으로 초기화하여 안보이게 함
        self.bar_fix = pg.BarGraphItem(x=self.x, height=self.y, width=BAR_WIDTH, pen=None, brush=FIXED_COLOR, name="fixed")
        self.graph.addItem(self.bar_fix)
        
        self.graph_timer.start() # 타이머를 시작하여 매 시간마다 그래프를 그리도록 함


    ## 그래프 리프레쉬를 멈추는 함수 ##
    def stop(self):
        self.graph_timer.stop()


    ## 매 시간마다 리프레쉬를 위해 실행되는 함수 ##
    def draw_graph(self):
        self.bar.setOpts(height=[x + 1 for x in array]) # 현재 array 상태를 실시간으로 표현

        if compare != -1: # 현재 compare 상태를 실시간으로 표현
            self.y = [0 if i != compare else array[compare] + 1 for i in range(len(array))]
            self.bar_compare.setOpts(height=self.y)

        if compare_other != -1: # 현재 compare_other 상태를 실시간으로 표현
            self.y = [0 if i != compare_other else array[compare_other] + 1 for i in range(len(array))]
            self.bar_compare_other.setOpts(height=self.y)

        if compare_list != []: # 현재 compare_list 상태를 실시간으로 표현
            self.y = [array[i] + 1 if i in compare_list else 0 for i in range(len(array))]
            self.bar_compare_list.setOpts(height=self.y)

        if pivot != -1: # 현재 pivot 상태를 실시간으로 표현
            self.y = [0 if i != pivot else array[pivot] + 1 for i in range(len(array))]
            self.bar_pivot.setOpts(height=self.y)

        if fix != []: # 현재 fix 상태를 실시간으로 표현
            self.y = [array[i] + 1 if i in fix else 0 for i in range(len(array))]
            self.bar_fix.setOpts(height=self.y)

## ================================================= 그래프 뷰어 클래스 끝 ================================================= ##





## ================================================= 알고리즘 실행 스레드 클래스 ================================================= ##
## ================================================= 알고리즘 실행 스레드 클래스 ================================================= ##
## ================================================= 알고리즘 실행 스레드 클래스 ================================================= ##
## ================================================= 알고리즘 실행 스레드 클래스 ================================================= ##
## ================================================= 알고리즘 실행 스레드 클래스 ================================================= ##
class AlgorithmSimulation(QThread):
    finished_signal = pyqtSignal()

    def __init__(self, speed, shuffle, isshuffle):
        super().__init__()
        self.speed = speed
        self.shuffle = shuffle
        self.isshuffle = isshuffle

    def run(self):
        global array
        global pivot
        global compare
        global compare_other
        global compare_list
        global fix

        pivot = -1
        compare = -1
        compare_other = -1
        compare_list = []
        fix = []

        if self.isshuffle:
            self.shuffleLimitFunc()
        else:
            self.shuffleFunc()

        self.bubble_sort()

        self.isSort()

        self.finished_signal.emit()

    def shuffleFunc(self):
        global array

        for _ in range(self.shuffle):
            sample = random.sample(array, 2)
            array[sample[0]], array[sample[1]] = array[sample[1]], array[sample[0]]


    def shuffleLimitFunc(self):
        global array

        for _ in range(self.shuffle):
            sample = random.sample(array, 2)
            array[sample[0]], array[sample[1]] = array[sample[1]], array[sample[0]]
            self.delay()

    def bubble_sort(self):
        global array
        global pivot
        global compare
        global fix

        for i in range(len(array) - 1, 0, -1):
            for pivot in range(i):
                compare = pivot + 1
                self.delay()
                if array[pivot] > array[compare]:
                    array[pivot], array[compare] = array[compare], array[pivot]
                self.delay()
            self.fixbar(i)

    def delay(self):
        time.sleep(self.speed/1000)

    def fixbar(self, index):
        fix.append(index)

    def isSort(self):
        global fix

        self.sorted = all(array[i] <= array[i + 1] for i in range(len(array) - 1))

        if self.sorted:
            fix = array
            return True
        else:
            return False

## ================================================= 알고리즘 실행 스레드 클래스 끝 ================================================= ##



## ================================================= 메인 윈도우 클래스 ================================================= ##
## ================================================= 메인 윈도우 클래스 ================================================= ##
## ================================================= 메인 윈도우 클래스 ================================================= ##
## ================================================= 메인 윈도우 클래스 ================================================= ##
## ================================================= 메인 윈도우 클래스 ================================================= ##
class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()

        self.setupUi(self) # ui 임포트
        self.setWindowIcon(QIcon(resource_path(ICON_PATH))) # 아이콘 임포트

        ## ==================== 정의 ==================== ##

        # 알고리즘 분석에 사용
        global array
        global pivot
        global compare
        global fix

        # 박스 위젯 정의
        self.tabWidgetControl: QTabWidget
        self.frameGraph: QFrame
        self.verticalLayoutGraph: QVBoxLayout
        self.listWidgetState: QListWidget
        self.listWidgetLog: QListWidget
        
        # 정렬 알고리즘 위젯
        self.comboBox_sort_select_Algorithm: QComboBox 
        self.spinBox_sort_data_size: QSpinBox
        self.spinBox_sort_speed_limit: QSpinBox
        self.spinBox_sort_shuffle_number: QSpinBox
        self.checkBox_sort_shuffle_number: QCheckBox
        self.pushButton_sort_start: QPushButton
        self.pushButton_sort_restart: QPushButton
        self.pushButton_sort_stop: QPushButton
        
        # 테스트 버튼 위젯
        self.testButton1: QPushButton
        self.testButton2: QPushButton
        self.testButton3: QPushButton



        self.viewGraph = ViewGraph() # 그래프 표현 클래스 객체 생성
        self.verticalLayoutGraph.addWidget(self.viewGraph.graph) # verticalLayoutGraph에 viewGraph 올림

        self.runTime = RunTimer()
        self.runTime.run_time_signal.connect(self.timer_worked)
        

        self.algorithmSimulation: AlgorithmSimulation

        self.stateListItem = self.listWidgetState.count() # designer에서 listWidget(State)에 입력해 놓은 기존 값 도출
        self.items = [self.listWidgetState.item(i) for i in range(self.stateListItem)] # self.items[n] 0: 상태, 1: 진행 시간, 2: 알고리즘 명, 3: 데이터 크기, 4: 속도 제한, 5: 섞는 횟수, 6: 탐색 값

        ## ==================== 코드 ==================== ##





        ## ==================== 시그널 ==================== ##

        # 정렬 알고리즘 시그널
        self.pushButton_sort_start.clicked.connect(self.sortStartFunc)
        self.pushButton_sort_restart.clicked.connect(self.sortRestartFunc)
        self.pushButton_sort_stop.clicked.connect(self.sortStopFunc)

        self.testButton1.clicked.connect(self.testFunc1)
        self.testButton2.clicked.connect(self.testFunc2)
        self.testButton3.clicked.connect(self.testFunc3)

    ## ==================== 함수 ==================== ##

    
    # 정렬 알고리즘 함수
    def sortStartFunc(self):
        self.pushButton_sort_start.setEnabled(False)
        self.pushButton_sort_restart.setEnabled(True)
        self.pushButton_sort_stop.setEnabled(True)

        self.getWidgetValue()
        self.runTime.newStart()
        self.statesSetFunc(self.input_algorithm, self.runTime.getRunTime(), self.input_algorithm, self.input_size, self.input_speed, self.input_shuffle)
        self.sortFunc()





    def sortRestartFunc(self):
        global array

        self.pushButton_sort_start.setEnabled(False)
        self.pushButton_sort_stop.setEnabled(True)

        self.algorithmSimulation.terminate()
        self.viewGraph.stop()
        self.runTime.stop()

        self.runTime.newStart()
        self.statesSetFunc(self.input_algorithm, self.runTime.getRunTime(), self.input_algorithm, self.input_size, self.input_speed, self.input_shuffle)

        self.sortFunc()





    def sortStopFunc(self):
        self.algorithmSimulation.terminate()
        self.viewGraph.stop()
        self.runTime.stop()

        self.pushButton_sort_start.setEnabled(True)
        self.pushButton_sort_stop.setEnabled(False)





    def getWidgetValue(self):
        global array

        self.input_algorithm = self.comboBox_sort_select_Algorithm.currentText()
        self.input_size = self.spinBox_sort_data_size.value()
        self.input_speed = self.spinBox_sort_speed_limit.value()
        self.input_shuffle = self.spinBox_sort_shuffle_number.value()
        self.input_shuffle_check = self.checkBox_sort_shuffle_number.isChecked()

        array = list(range(self.input_size))





    def sortFunc(self):
        self.algorithmSimulation = AlgorithmSimulation(self.input_speed, self.input_shuffle, self.input_shuffle_check)
        self.algorithmSimulation.finished_signal.connect(self.sort_thread_finished)

        self.viewGraph.start()
        self.algorithmSimulation.start(self.input_speed)





    def sort_thread_finished(self):
        self.runTime.stop()
        self.sortStopFunc()
        self.viewGraph.draw_graph()

    



    # 타이머
    def timer_worked(self):
        self.stateRunTimeSetFunc(self.runTime.getRunTime())




    # State 화면 조작
    def statesSetFunc(self, algorithm_state: str = "", run_time: str = "00:00.000", algorithm_name: str = "", data_size: int = -1, speed_limite: int = -1, shuffle_number: int = -1, search_value: int = -1): # self.items[n] 0: 상태, 1: 진행 시간, 2: 알고리즘 명, 3: 데이터 크기, 4: 속도 제한, 5: 섞는 횟수, 6: 탐색 값
        print(1)
        self.items[0].setText(f"상태: {algorithm_state}")
        self.items[1].setText(f"진행 시간: {run_time}")
        self.items[2].setText(f"알고리즘 명: {algorithm_name}")
        self.items[3].setText(f"데이터 크기: {str(data_size)}")
        self.items[4].setText(f"속도 제한: {str(speed_limite)}")
        self.items[5].setText(f"섞는 횟수: {str(shuffle_number)}")
        self.items[6].setText(f"탐색 값: {str(search_value)}")

    def stateSetFunc(self, index: str, value): # self.items[n] 0: 상태, 1: 진행 시간, 2: 알고리즘 명, 3: 데이터 크기, 4: 속도 제한, 5: 섞는 횟수, 6: 탐색 값
        if index == 0:
            self.items[0].setText(f"상태: {value}")
        elif index == 1:
            self.items[1].setText(f"진행 시간: {value}")
        elif index == 2:
            self.items[2].setText(f"알고리즘 명: {value}")
        elif index == 3:
            self.items[3].setText(f"데이터 크기: {str(value)}")
        elif index == 4:
            self.items[4].setText(f"속도 제한: {str(value)}")
        elif index == 5:
            self.items[5].setText(f"섞는 횟수: {str(value)}")
        elif index == 6:
            self.items[6].setText(f"탐색 값: {str(value)}")

    def stateRunTimeSetFunc(self, time):
        self.items[1].setText(f"진행 시간: {time}")





    # 프로그램 종료 시 작동 함수
    def closeEvent(self, event):
        event.accept()







    def testFunc1(self):
        self.runTime.start()
        print("test1")

    def testFunc2(self):
        print(self.runTime.getRunTime())
        print("test2")

    def testFunc3(self):

        print("test3")

## ================================================= 메인 윈도우 클래스 끝 ================================================= ##




# 전역 변수
array: list = []
pivot: int = -1
compare: int = -1
compare_other: int = -1
compare_list: list = []
fix: list = []

fps: int


# 바인드 파일 처리
bind_path = resource_path(BIND_FILE)

if not isFileFunc(bind_path):
    bind_init_path = resource_path(BIND_INIT_FILE)
    shutil.copyfile(bind_init_path, bind_path)

bind_value = []
file = open(bind_path)
lines = file.readlines()
for line in lines:
    bind_value.append(int(line.split()[2]))
file.close()

fps = bind_value[0]




# 메인 함수
if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()
