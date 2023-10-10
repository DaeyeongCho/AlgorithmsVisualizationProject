import copy
import os
import os.path
import shutil
import sys
import time
import random
import sqlite3

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
import algorithms as gb


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

        self.x = np.arange(len(gb.array)) # array를 막대그래프로 표시 초기화
        self.ypp = [x + 1 for x in gb.array]
        self.bar = pg.BarGraphItem(x=self.x, height=self.ypp, width=BAR_WIDTH, pen=None, brush=BASIC_COLOR, name="basic")
        self.graph.addItem(self.bar)

        self.y = [0] * len(gb.array) # fix는 모든 막대에서 0으로 초기화하여 안보이게 함
        self.bar_fix = pg.BarGraphItem(x=self.x, height=self.y, width=BAR_WIDTH, pen=None, brush=FIXED_COLOR, name="fixed")
        self.graph.addItem(self.bar_fix)
        
        self.y = [0] * len(gb.array) # compare는 모든 막대에서 0으로 초기화하여 안보이게 함
        self.bar_compare = pg.BarGraphItem(x=self.x, height=self.y, width=BAR_WIDTH, pen=None, brush=COMPARE_COLOR, name="compare")
        self.graph.addItem(self.bar_compare)

        self.y = [0] * len(gb.array) # compare_other 모든 막대에서 0으로 초기화하여 안보이게 함
        self.bar_compare_other = pg.BarGraphItem(x=self.x, height=self.y, width=BAR_WIDTH, pen=None, brush=COMPARE_COLOR)
        self.graph.addItem(self.bar_compare_other)

        self.y = [0] * len(gb.array) # compare_list 모든 막대에서 0으로 초기화하여 안보이게 함
        self.bar_compare_list = pg.BarGraphItem(x=self.x, height=self.y, width=BAR_WIDTH, pen=None, brush=COMPARE_COLOR)
        self.graph.addItem(self.bar_compare_list)

        self.y = [0] * len(gb.array) # pivot 모든 막대에서 0으로 초기화하여 안보이게 함
        self.bar_pivot = pg.BarGraphItem(x=self.x, height=self.y, width=BAR_WIDTH, pen=None, brush=PIVOT_COLOR, name="pivot")
        self.graph.addItem(self.bar_pivot)
        
        self.graph_timer.start() # 타이머를 시작하여 매 시간마다 그래프를 그리도록 함


    ## 그래프 리프레쉬를 멈추는 함수 ##
    def stop(self):
        self.graph_timer.stop()


    ## 매 시간마다 리프레쉬를 위해 실행되는 함수 ##
    def draw_graph(self):
        self.bar.setOpts(height=[x + 1 for x in gb.array]) # 현재 array 상태를 실시간으로 표현

        if gb.fix != []: # 현재 fix 상태를 실시간으로 표현
            self.y = [gb.array[i] + 1 if i in gb.fix else 0 for i in range(len(gb.array))]
            self.bar_fix.setOpts(height=self.y)

        if gb.compare != -1: # 현재 compare 상태를 실시간으로 표현
            self.y = [0 if i != gb.compare else gb.array[gb.compare] + 1 for i in range(len(gb.array))]
            self.bar_compare.setOpts(height=self.y)
        else:
            self.bar_compare.setOpts(height=0)

        if gb.compare_other != -1: # 현재 compare_other 상태를 실시간으로 표현
            self.y = [0 if i != gb.compare_other else gb.array[gb.compare_other] + 1 for i in range(len(gb.array))]
            self.bar_compare_other.setOpts(height=self.y)

        if gb.compare_list != []: # 현재 compare_list 상태를 실시간으로 표현
            self.y = [gb.array[i] + 1 if i in gb.compare_list else 0 for i in range(len(gb.array))]
            self.bar_compare_list.setOpts(height=self.y)

        if gb.pivot != -1: # 현재 pivot 상태를 실시간으로 표현
            self.y = [0 if i != gb.pivot else gb.array[gb.pivot] + 1 for i in range(len(gb.array))]
            self.bar_pivot.setOpts(height=self.y)
        else:
            self.bar_pivot.setOpts(height=0)



## ================================================= 알고리즘 실행 스레드 클래스 ================================================= ##
class AlgorithmSimulation(QThread):
    start_signal = pyqtSignal()
    sort_finished_signal = pyqtSignal()
    search_finished_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.simulation = gb.MyAlgorithms()

        self.sort_algorithms_list = list(self.simulation.sort_algorithms.keys())
        self.search_algorithms_list = list(self.simulation.search_algorithms.keys())

    def run(self):
        global input_algorithm
        global input_size
        global input_speed
        global input_shuffle
        global input_shuffle_check
        global input_issort
        global input_search_value
        global input_isuser_value
        global input_repeat_value
        global input_isrepeat

        gb.pivot = -1
        gb.compare = -1
        gb.compare_other = -1
        gb.compare_list = []
        gb.fix = []

        if input_issort:
            if input_shuffle_check:
                self.shuffleLimitFunc()
            else:
                self.shuffleFunc()

            self.start_signal.emit()

            self.simulation.runSortFunc(input_algorithm)

            self.isSort()

            self.sort_finished_signal.emit()
        else:
            self.start_signal.emit()

            self.simulation.runSearchFunc(input_algorithm)

            if input_isrepeat:
                for _ in range(1, input_repeat_value):
                    gb.pivot = -1
                    gb.compare = -1
                    gb.compare_other = -1
                    gb.compare_list = []
                    gb.fix = []

                    if not input_isuser_value:
                        gb.search_value = random.randrange(input_size)

                    self.simulation.runSearchFunc(input_algorithm)


            self.search_finished_signal.emit()

    def shuffleFunc(self): # 지연 없이 섞기
        for _ in range(input_shuffle):
            sample = random.sample(gb.array, 2)
            gb.array[sample[0]], gb.array[sample[1]] = gb.array[sample[1]], gb.array[sample[0]]


    def shuffleLimitFunc(self): # 지연하여 섞기
        for _ in range(input_shuffle):
            sample = random.sample(gb.array, 2)
            gb.array[sample[0]], gb.array[sample[1]] = gb.array[sample[1]], gb.array[sample[0]]
            self.delay()

    def delay(self): # 딜레이 넣기
        time.sleep(input_speed/1000)

    def isSort(self): # 정렬 되었는지 결과 확인
        self.sorted = all(gb.array[i] <= gb.array[i + 1] for i in range(len(gb.array) - 1))

        if self.sorted:
            gb.fix = gb.array
            gb.pivot = -1
            gb.compare = -1
            gb.compare_other = -1
            gb.compare_list = []
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
        # 전역 변수
        global input_algorithm
        global input_size
        global input_speed
        global input_shuffle
        global input_shuffle_check
        global input_issort

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

        # 탐색 알고리즘 위젯
        self.comboBox_search_select_algorithm: QComboBox
        self.spinBox_search_data_size: QSpinBox
        self.spinBox_search_speed_limit: QSpinBox
        self.spinBox_search_search_number: QSpinBox
        self.checkBox_search_set_search_number: QCheckBox
        self.spinBox_search_repeat_number: QSpinBox
        self.checkbox_search_set_repeat_number: QCheckBox
        self.pushButton_search_start: QPushButton
        self.pushButton_search_restart: QPushButton
        self.pushButton_search_stop:QPushButton

        # 테스트 버튼 위젯
        self.testButton1: QPushButton
        self.testButton2: QPushButton
        self.testButton3: QPushButton



        self.viewGraph = ViewGraph() # 그래프 표현 클래스 객체 생성
        self.verticalLayoutGraph.addWidget(self.viewGraph.graph) # verticalLayoutGraph에 viewGraph 올림

        self.runTime = RunTimer() # 타이머 객체 생성
        self.runTime.run_time_signal.connect(self.timer_worked) # 타이머 시그널

        self.algorithmSimulation = AlgorithmSimulation() # 알고리즘 시뮬레이션 객체 생성
        self.algorithmSimulation.start_signal.connect(self.start_algorithm_thread)
        self.algorithmSimulation.sort_finished_signal.connect(self.sort_thread_finished)
        self.algorithmSimulation.search_finished_signal.connect(self.search_thread_finished)

        self.tabWidgetControl.currentChanged.connect(self.tabChangeSignal)

        self.comboBox_sort_select_Algorithm.addItems(self.algorithmSimulation.sort_algorithms_list) # 알고리즘 종류를 불러와 콤보박스에 입력
        
        self.comboBox_search_select_algorithm.addItems(self.algorithmSimulation.search_algorithms_list) # 알고리즘 종류를 불러와 콤보박스에 입력

        input_algorithm = self.comboBox_sort_select_Algorithm.currentText()
        input_size = self.spinBox_sort_data_size.value()
        input_speed = self.spinBox_sort_speed_limit.value()
        input_shuffle = self.spinBox_sort_shuffle_number.value()
        input_shuffle_check = self.checkBox_sort_shuffle_number.isChecked()
        input_issort = True

        self.stateListItem = self.listWidgetState.count() # designer에서 listWidget(State)에 입력해 놓은 기존 값 도출
        self.state_item: QListWidget.item() = None
        self.timer_item: QListWidget.item() = None

        self.listWidgetLog.clear()

        self.tabChangeSignal(0)

        ## ==================== 코드 ==================== ##





        ## ==================== 시그널 ==================== ##

        # 정렬 알고리즘 시그널
        self.pushButton_sort_start.clicked.connect(self.sortStartFunc)
        self.pushButton_sort_restart.clicked.connect(self.sortRestartFunc)
        self.pushButton_sort_stop.clicked.connect(self.sortStopFunc)


        # 탐색 알고리즘 시그널
        self.pushButton_search_start.clicked.connect(self.searchStartFunc)
        self.pushButton_search_restart.clicked.connect(self.searchRestartFunc)
        self.pushButton_search_stop.clicked.connect(self.searchStopFunc)

        # 로그 리스트 위젯 시그널
        self.listWidgetLog.itemClicked.connect(self.log_list_clicked)
        self.listWidgetLog.itemDoubleClicked.connect(self.log_list_double_clicked)


        self.testButton1.clicked.connect(self.testFunc1)
        self.testButton2.clicked.connect(self.testFunc2)
        self.testButton3.clicked.connect(self.testFunc3)

    ## ==================== 함수 ==================== ##

    
    ## 정렬 알고리즘 함수 ##
    def sortStartFunc(self): # 실행 버튼 클릭 시 동작
        global input_algorithm
        global input_size
        global input_speed
        global input_shuffle
        global input_shuffle_check
        global input_issort

        input_issort = True
        
        self.pushButton_sort_start.setEnabled(False)
        self.pushButton_sort_restart.setEnabled(True)
        self.pushButton_sort_stop.setEnabled(True)
        self.tabWidgetControl.setTabEnabled(1, False)

        self.getSortWidgetValue()
        
        self.sortFunc()





    def sortRestartFunc(self): # 다시하기 버튼 클릭 시 동작
        self.pushButton_sort_start.setEnabled(False)
        self.pushButton_sort_stop.setEnabled(True)

        self.algorithmSimulation.terminate()
        self.viewGraph.stop()
        self.runTime.stop()

        gb.array = list(range(input_size))

        self.sortFunc()





    def sortStopFunc(self): # 중지 버튼 클릭 시 동작
        self.algorithmSimulation.terminate()
        self.viewGraph.stop()
        self.runTime.stop()

        self.pushButton_sort_start.setEnabled(True)
        self.pushButton_sort_stop.setEnabled(False)
        self.tabWidgetControl.setTabEnabled(1, True)





    def getSortWidgetValue(self): # 정렬하기 위해 입력한 값들 추출
        global input_algorithm
        global input_size
        global input_speed
        global input_shuffle
        global input_shuffle_check

        input_algorithm = self.comboBox_sort_select_Algorithm.currentText()
        input_size = self.spinBox_sort_data_size.value()
        input_speed = self.spinBox_sort_speed_limit.value()
        input_shuffle = self.spinBox_sort_shuffle_number.value()
        input_shuffle_check = self.checkBox_sort_shuffle_number.isChecked()

        gb.limit = input_speed
        gb.array = list(range(input_size))

        self.statesInitFunc({
            "상태":"섞는 중",
            "진행 시간":"00:00.000",
            "알고리즘 명":input_algorithm,
            "데이터 크기":input_size,
            "속도 제한":input_speed,
            "섞는 횟수":input_shuffle
        })





    def sortFunc(self): # AlgorithmSimulation 클래스 호출하여 정렬
        self.viewGraph.start()
        self.algorithmSimulation.start()





    def sort_thread_finished(self): # AlgorithmSimulation 클래스에서 정렬 종료 시 자동 호출
        self.sortStopFunc()
        self.viewGraph.draw_graph()
        self.state_item.setText(f"상태: 정렬 완료")
        self.sortInsertDB()



    

    def sortInsertDB(self):
        global input_algorithm
        global input_size
        global input_speed
        global input_shuffle

        connection = sqlite3.connect("algorithm_log.db")
        cursor = connection.cursor()

        cursor.execute("INSERT INTO sort_algorithm (name, time, size, speed, shuffle) VALUES (?, ?, ?, ?, ?)", (input_algorithm, self.runTime.getRunTime(), input_size, input_speed, input_shuffle))
        connection.commit()

        connection.close()

        self.tabChangeSignal(0)





    ## 탐색 알고리즘 함수 ##
    def searchStartFunc(self):
        global input_algorithm
        global input_size
        global input_speed
        global input_shuffle
        global input_shuffle_check
        global input_issort

        input_issort = False
        
        self.pushButton_search_start.setEnabled(False)
        self.pushButton_search_restart.setEnabled(True)
        self.pushButton_search_stop.setEnabled(True)
        self.tabWidgetControl.setTabEnabled(0, False)

        self.getSearchWidgetValue()
        self.searchFunc()





    def searchRestartFunc(self):
        self.pushButton_search_start.setEnabled(False)
        self.pushButton_search_stop.setEnabled(True)

        self.algorithmSimulation.terminate()
        self.viewGraph.stop()
        self.runTime.stop()

        self.sortFunc()





    def searchStopFunc(self):
        self.algorithmSimulation.terminate()
        self.viewGraph.stop()
        self.runTime.stop()

        self.pushButton_search_start.setEnabled(True)
        self.pushButton_search_stop.setEnabled(False)
        self.tabWidgetControl.setTabEnabled(0, True)





    def getSearchWidgetValue(self):
        global input_algorithm
        global input_size
        global input_speed
        global input_search_value
        global input_isuser_value
        global input_repeat_value
        global input_isrepeat

        input_algorithm = self.comboBox_search_select_algorithm.currentText()
        input_size = self.spinBox_search_data_size.value()
        input_speed = self.spinBox_search_speed_limit.value()
        input_isuser_value = self.checkBox_search_set_search_number.isChecked()
        if input_isuser_value:
            input_search_value = self.spinBox_search_search_number.value()
        else:
            input_search_value = random.randrange(input_size)
        input_isrepeat = self.checkbox_search_set_repeat_number.isChecked()
        if input_isrepeat:
            input_repeat_value = self.spinBox_search_repeat_number.value()
        else:
            input_repeat_value = 1

        gb.limit = input_speed
        gb.array = list(range(input_size))
        gb.search_value = input_search_value

        self.statesInitFunc({
            "상태":"탐색 중",
            "진행 시간":"00:00.000",
            "알고리즘 명":input_algorithm,
            "데이터 크기":input_size,
            "속도 제한":input_speed,
            "탐색 값":input_search_value,
            "반복 횟수":input_repeat_value
        })




    
    def searchFunc(self): # AlgorithmSimulation 클래스 호출하여 정렬
        self.viewGraph.start()
        self.algorithmSimulation.start()





    def search_thread_finished(self):
        self.searchStopFunc()
        self.viewGraph.draw_graph()
        self.state_item.setText("상태: 탐색 완료")
        self.searchInsertDB()




    def searchInsertDB(self):
        global input_algorithm
        global input_size
        global input_speed
        global input_search_value
        global input_repeat_value

        connection = sqlite3.connect("algorithm_log.db")
        cursor = connection.cursor()

        cursor.execute("INSERT INTO search_algorithm (name, time, size, speed, value, repeat) VALUES (?, ?, ?, ?, ?, ?)", (input_algorithm, self.runTime.getRunTime(), input_size, input_speed, input_search_value, input_repeat_value))
        connection.commit()

        connection.close()

        self.tabChangeSignal(1)





    ## 공동 알고리즘 함수 ##
    def statesInitFunc(self, states_dictionary: dict):
        self.listWidgetState.clear()

        self.key_list = list(states_dictionary.keys())
        self.value_list = list(states_dictionary.values())

        for key, value in zip(self.key_list, self.value_list):
            self.listWidgetState.addItem(key + ": " + str(value))

        self.state_item = self.listWidgetState.item(0)
        self.timer_item = self.listWidgetState.item(1)

    def tabChangeSignal(self, index):
        global input_issort

        self.listWidgetLog.clear()

        connection = sqlite3.connect("algorithm_log.db")
        cursor = connection.cursor()

        if index == 0:
            input_issort = True

            cursor.execute("SELECT * FROM sort_algorithm")

            for row in cursor.fetchall():
                self.listWidgetLog.addItem(str(row[0]) + ", " + str(row[1]) + ", " + str(row[2]))

        elif index == 1:
            input_issort = False
            
            cursor.execute("SELECT * FROM search_algorithm")

            for row in cursor.fetchall():
                self.listWidgetLog.addItem(str(row[0]) + ", " + str(row[1]) + ", " + str(row[2]))

        connection.close()





    def start_algorithm_thread(self):
        self.runTime.newStart()





    ## 프로그램 종료 시 작동 함수 ##
    def closeEvent(self, event):
        event.accept()



    ## 타이머 ##
    def timer_worked(self): # 타이머 작동 중 매 타임마다 작동
        self.stateRunTimeSetFunc(self.runTime.getRunTime())

    def stateRunTimeSetFunc(self, time): # 상태 창에 진행시간 기록
        self.timer_item.setText(f"진행 시간: {time}")




    # 로그 창 관련
    def log_list_clicked(self, item):
        self.primary_num = self.listWidgetLog.row(item) + 1
        
        connection = sqlite3.connect("algorithm_log.db")
        cursor = connection.cursor()

        if input_issort:
            cursor.execute('SELECT * FROM sort_algorithm WHERE id=?', (self.primary_num,))
            self.tuple = cursor.fetchone()

            self.comboBox_sort_select_Algorithm.setCurrentText(self.tuple[1])
            self.spinBox_sort_data_size.setValue(self.tuple[3])
            self.spinBox_sort_speed_limit.setValue(self.tuple[4])
            self.spinBox_sort_shuffle_number.setValue(self.tuple[5])
        else:
            cursor.execute('SELECT * FROM search_algorithm WHERE id=?', (self.primary_num,))
            self.tuple = cursor.fetchone()

            self.comboBox_search_select_algorithm.setCurrentText(self.tuple[1])
            self.spinBox_search_data_size.setValue(self.tuple[3])
            self.spinBox_search_speed_limit.setValue(self.tuple[4])
            self.spinBox_search_search_number.setValue(self.tuple[5])
            self.checkBox_search_set_search_number.setChecked(True)
            if self.tuple[6] == 1:
                self.spinBox_search_repeat_number.setValue(1)
            else:
                self.spinBox_search_repeat_number.setValue(self.tuple[6])
                self.checkbox_search_set_repeat_number.setChecked(True)

        connection.close()

    def log_list_double_clicked(self, item):
        self.primary_num = self.listWidgetLog.row(item) + 1

        connection = sqlite3.connect("algorithm_log.db")
        cursor = connection.cursor()

        if input_issort:
            pass
        else:
            pass

        connection.close()




    ## 테스트 버튼 함수 ##
    def testFunc1(self):
        self.tabChangeSignal(0)
        print("test1")

    def testFunc2(self):
        connection = sqlite3.connect("algorithm_log.db")

        # 커서 객체 생성
        cursor = connection.cursor()

        # 모든 데이터를 조회하는 SQL 쿼리 실행
        cursor.execute("SELECT * FROM sort_algorithm")

        # fetchall()을 사용하여 모든 행을 가져오고, 반복문을 사용하여 출력
        for row in cursor.fetchall():
            print(row)

        # 커서와 연결 종료 (옵션, but recommended)
        cursor.close()
        connection.close()
        
        print("test2")

    def testFunc3(self):

        print("test3")

## ================================================= 메인 윈도우 클래스 끝 ================================================= ##


# 전역 변수
input_algorithm: str
input_size: int
input_speed: int
input_shuffle: int
input_shuffle_check: bool
input_issort: bool
input_search_value: int
input_isuser_value: bool
input_repeat_value: int
input_isrepeat: bool

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

# DB 처리
connection = sqlite3.connect("algorithm_log.db")
cursor = connection.cursor()

table_name = "sort_algorithm"
cursor.execute(f"SELECT count(name) FROM sqlite_master WHERE type='table' AND name='{table_name}'")

if not (cursor.fetchone()[0] == 1):
    cursor.execute('''
    CREATE TABLE sort_algorithm (
        id INTEGER PRIMARY KEY,
        name CHAR,
        time CHAR,
        size INTEGER,
        speed INTEGER,
        shuffle INTEGER
    )
    ''')

table_name = "search_algorithm"
cursor.execute(f"SELECT count(name) FROM sqlite_master WHERE type='table' AND name='{table_name}'")

if not (cursor.fetchone()[0] == 1):
    cursor.execute('''
    CREATE TABLE search_algorithm (
        id INTEGER PRIMARY KEY,
        name CHAR,
        time CHAR,
        size INTEGER,
        speed INTEGER,
        value INTEGER,
        repeat INTEGER
    )
    ''')

connection.close()


# 메인 함수
if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()
