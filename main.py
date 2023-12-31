import os
import os.path
import shutil
import sys
import types
import psutil
import time
import random
import sqlite3
import inspect

#PyQt6 임포트
from PyQt6.QtWidgets import *
from PyQt6 import uic
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import *
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtGui import QCloseEvent

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

# ui 연결 변수
form_class = uic.loadUiType(resource_path(UI_FILE_PASS))[0]
form_fps = uic.loadUiType(resource_path(FPS_UI_FILE_PASS))[0]
form_log = uic.loadUiType(resource_path(LOG_UI_FILE_PASS))[0]
form_source = uic.loadUiType(resource_path(SOURCE_UI_FILE_PASS))[0]
form_manual = uic.loadUiType(resource_path(MANUAL_UI_FILE_PASS))[0]
form_info = uic.loadUiType(resource_path(INFO_UI_FILE_PASS))[0]



## ================================================= 정보 다이얼로그 클래스 ================================================= ##
class DialogInfo(QDialog, form_info):
    def __init__(self): # 객체 초기화
            super().__init__()
            self.setupUi(self)
            self.setWindowIcon(QIcon(resource_path(ICON_PATH))) # 아이콘 임포트


## ================================================= 도움말 위젯 클래스 ================================================= ##

class WidgetHelp(QWidget, form_manual):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # UI 설정을 초기화합니다.
        self.setWindowIcon(QIcon(resource_path(ICON_PATH)))  # 아이콘을 설정합니다.

        # QWebEngineView를 설정합니다.
        self.web_engine_view = QWebEngineView(self)  # self를 부모로 QWebEngineView 인스턴스를 생성합니다.
        self.init_web_engine_view()  # HTML 파일을 로드하는 메서드를 호출합니다.

        # QVBoxLayout을 사용하여 QWebEngineView를 현재 위젯에 추가합니다.
        layout = QVBoxLayout(self)  # QVBoxLayout 인스턴스를 생성합니다.
        layout.addWidget(self.web_engine_view)  # layout에 QWebEngineView를 추가합니다.
        self.setLayout(layout)  # 위젯의 레이아웃을 설정합니다.

    def init_web_engine_view(self):
        # 로컬 HTML 파일의 경로를 설정합니다. (여기서는 실제 파일 경로를 사용하세요)
        file_path = resource_path(HELP_HTML_PASS)
        local_html_file_url = QUrl.fromLocalFile(file_path)

        # QWebEngineView를 사용하여 파일을 로드합니다.
        self.web_engine_view.load(local_html_file_url)


## ================================================= 소스코드 보기 다이얼로그 클래스 ================================================= ##

class DialogViewSource(QDialog, form_source):
    def __init__(self, algorithmsObject: gb.MyAlgorithms): # 객체 초기화
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(resource_path(ICON_PATH))) # 아이콘 임포트

        self.pushButton_end: QPushButton
        self.pushButton_end.clicked.connect(self.closeEvent)
        self.textEdit: QTextEdit
        self.listWidget: QListWidget
        self.listWidget.clicked.connect(self.listWidgetClickSignal)

        self.algorithms_names = list(algorithmsObject.sort_algorithms.keys()) + list(algorithmsObject.search_algorithms.keys())
        self.algorithms_funcs = list(algorithmsObject.sort_algorithms.values()) + list(algorithmsObject.search_algorithms.values())

        for name in self.algorithms_names:
            self.listWidget.addItem(name)

    def listWidgetClickSignal(self, index):
        current_index = self.listWidget.currentIndex()
        
        row_num = current_index.row()
        text = self.getStringInMethod(row_num)
        self.setTextEditBox(text)

    def setTextEditBox(self, text):
        self.textEdit.setText(text)

    def getStringInMethod(self, index) -> str:
        funcText = ""

        if isinstance(self.algorithms_funcs[index], types.MethodType):
            funcText = inspect.getsource(self.algorithms_funcs[index])
        elif isinstance(self.algorithms_funcs[index], list):
            for func in self.algorithms_funcs[index]:
                funcText += inspect.getsource(func)
                funcText += "\n\n"

        return funcText
    
        ## 프로그램 종료 시 작동 함수 ##
    def closeEvent(self):
        self.accept()
    

## ================================================= 상태 바 관련 클래스 ================================================= ##

class ResourceMonitorThread(QThread):
    update_signal = pyqtSignal(float, float, float, int, float)

    def run(self):
        while True:
            self.msleep(1000)

            usingWholeCPU = psutil.cpu_percent(interval=None)
            memory = psutil.virtual_memory()
            usingWholeMMU = memory.percent

            pid = os.getpid()
            current_process = psutil.Process(pid)
            usingThisCPU = current_process.cpu_percent(interval=None)
            process_memory_info = current_process.memory_info()
            usingThisMMUBytes = process_memory_info.rss
            usingThisMMU = current_process.memory_percent()

            self.update_signal.emit(usingWholeCPU, usingWholeMMU, usingThisCPU, usingThisMMUBytes, usingThisMMU)


class ViewStatusBar(QObject):
    def __init__(self, statusbar):
        super().__init__()
        self.statusbar = statusbar

        self.monitor_thread = ResourceMonitorThread()
        self.monitor_thread.update_signal.connect(self.update_statusbar)
        self.monitor_thread.start()

    def update_statusbar(self, usingWholeCPU, usingWholeMMU, usingThisCPU, usingThisMMUBytes, usingThisMMU):
        self.statusbar.clearMessage()
        self.statusbar.showMessage(f"전체 CPU 사용량: {usingWholeCPU}%, 전체 메모리 사용량: {usingWholeMMU}%, 프로그램 CPU 사용량: {usingThisCPU}%, 프로그램 메모리 사용량 {usingThisMMU:.1f}%({usingThisMMUBytes}Bytes)", 2000)
        

## ================================================= FPS 설정 다이얼로그 클래스 ================================================= ##
class DialogSetFPS(QDialog, form_fps):
    change_fps_signal = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(resource_path(ICON_PATH))) # 아이콘 임포트

        self.selected_option = 60

        self.radioButton30: QRadioButton
        self.radioButton60: QRadioButton
        self.radioButton90: QRadioButton
        self.radioButton120: QRadioButton
        self.radioButton144: QRadioButton
        self.radioButton300: QRadioButton

        self.buttonBox: QDialogButtonBox


        self.radioButton30.toggled.connect(self.on_radio_button_toggled)
        self.radioButton60.toggled.connect(self.on_radio_button_toggled)
        self.radioButton90.toggled.connect(self.on_radio_button_toggled)
        self.radioButton120.toggled.connect(self.on_radio_button_toggled)
        self.radioButton144.toggled.connect(self.on_radio_button_toggled)
        self.radioButton300.toggled.connect(self.on_radio_button_toggled)

        self.buttonBox.accepted.connect(self.buttonClicked)

    def on_radio_button_toggled(self):
        if self.radioButton30.isChecked():
            self.selected_option = int(self.radioButton30.text())
        elif self.radioButton60.isChecked():
            self.selected_option = int(self.radioButton60.text())
        elif self.radioButton90.isChecked():
            self.selected_option = int(self.radioButton90.text())
        elif self.radioButton120.isChecked():
            self.selected_option = int(self.radioButton120.text())
        elif self.radioButton144.isChecked():
            self.selected_option = int(self.radioButton144.text())
        elif self.radioButton300.isChecked():
            self.selected_option = int(self.radioButton300.text())

    def buttonClicked(self):
        self.change_fps_signal.emit(self.selected_option)



## ================================================= LOG 비교 다이얼로그 클래스 ================================================= ##
class DialogSetLog(QDialog, form_log):
    def __init__(self, input_issort, primary_num): # 객체 초기화
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(resource_path(ICON_PATH))) # 아이콘 임포트

        self.issort = input_issort
        self.primary_key = primary_num
        self.islist: bool

        self.listWidget_select: QListWidget
        self.listWidget_compare: QListWidget
        self.pushButton_back: QPushButton
        self.pushButton_end: QPushButton

        self.pushButton_back.clicked.connect(self.logListView)
        self.listWidget_compare.itemDoubleClicked.connect(self.logDataView)
        self.pushButton_end.clicked.connect(self.close)

        # 초기화 코드
        connection = sqlite3.connect("algorithm_log.db")
        cursor = connection.cursor()

        if self.issort:
            cursor.execute("SELECT * FROM sort_algorithm WHERE id = ?", (self.primary_key,))
            self.row = cursor.fetchone()
            self.row_dict = {
            "상태":"로그에 기록 됨",
            "진행 시간": self.row[2],
            "알고리즘 명": self.row[1],
            "데이터 크기": self.row[3],
            "속도 제한": self.row[4],
            "섞는 횟수": self.row[5]
        }
        else:
            cursor.execute("SELECT * FROM search_algorithm WHERE id = ?", (self.primary_key,))
            self.row = cursor.fetchone()
            self.row_dict = {
                "상태":"로그에 기록 됨",
                "진행 시간": self.row[2],
                "알고리즘 명":self.row[1],
                "데이터 크기":self.row[3],
                "속도 제한":self.row[4],
                "탐색 값":self.row[5],
                "반복 횟수":self.row[6]
            }

        connection.close()
        # 초기화 코드 끝


        self.key_list = list(self.row_dict.keys())
        self.value_list = list(self.row_dict.values())

        for key, value in zip(self.key_list, self.value_list):
            self.listWidget_select.addItem(key + ": " + str(value))

        self.state_item = self.listWidget_select.item(0)
        self.timer_item = self.listWidget_select.item(1)

        self.logListView()






    def logDataView(self, table_id): # 리스트 위젯에 특정 튜플의 데이터 추가
        if self.islist == False:
            return

        self.primary_id = self.listWidget_compare.row(table_id) + 1
        
        self.listWidget_compare.clear()

        connection = sqlite3.connect("algorithm_log.db")
        cursor = connection.cursor()

        if self.issort:
            cursor.execute("SELECT * FROM sort_algorithm WHERE id = ?", (self.primary_id,))
            self.row = cursor.fetchone()
            self.row_dict = {
            "상태":"로그에 기록 됨",
            "진행 시간": self.row[2],
            "알고리즘 명": self.row[1],
            "데이터 크기": self.row[3],
            "속도 제한": self.row[4],
            "섞는 횟수": self.row[5]
        }
        else:
            cursor.execute("SELECT * FROM search_algorithm WHERE id = ?", (self.primary_id,))
            self.row = cursor.fetchone()
            self.row_dict = {
                "상태":"로그에 기록 됨",
                "진행 시간": self.row[2],
                "알고리즘 명":self.row[1],
                "데이터 크기":self.row[3],
                "속도 제한":self.row[4],
                "탐색 값":self.row[5],
                "반복 횟수":self.row[6]
            }

        connection.close()

        self.key_list = list(self.row_dict.keys())
        self.value_list = list(self.row_dict.values())

        for key, value in zip(self.key_list, self.value_list):
            self.listWidget_compare.addItem(key + ": " + str(value))

        self.state_item = self.listWidget_compare.item(0)
        self.timer_item = self.listWidget_compare.item(1)
        self.pushButton_back.setEnabled(True)
        self.islist = False



    def logListView(self): # 비교 리스트 위젯에 테이블의 모든 튜플 추가
        self.listWidget_compare.clear()

        connection = sqlite3.connect("algorithm_log.db")
        cursor = connection.cursor()

        if self.issort:
            cursor.execute("SELECT * FROM sort_algorithm")

            for row in cursor.fetchall():
                self.listWidget_compare.addItem(str(row[0]) + ", " + str(row[1]) + ", " + str(row[2]) + ", " + str(row[3]) + ", " + str(row[4]))

        else:
            cursor.execute("SELECT * FROM search_algorithm")

            for row in cursor.fetchall():
                self.listWidget_compare.addItem(str(row[0]) + ", " + str(row[1]) + ", " + str(row[2]) + ", " + str(row[3]) + ", " + str(row[4]) + ", " + str(row[5]))

        connection.close()
        self.pushButton_back.setEnabled(False)
        self.islist = True



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
        else:
            self.bar_compare_other.setOpts(height=0)

        if gb.compare_list != []: # 현재 compare_list 상태를 실시간으로 표현
            self.y = [gb.array[i] + 1 if i in gb.compare_list else 0 for i in range(len(gb.array))]
            self.bar_compare_list.setOpts(height=self.y)
        else:
            self.y = [0] * len(gb.array)
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
            sample = np.random.choice(gb.array, size=2, replace=False)
            gb.array[sample[0]], gb.array[sample[1]] = gb.array[sample[1]], gb.array[sample[0]]


    def shuffleLimitFunc(self): # 지연하여 섞기
        for _ in range(input_shuffle):
            sample = np.random.choice(gb.array, size=2, replace=False)
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

        # 메뉴 바 위젯
        self.menu_exit: QMenu
        self.menu_sort_init: QMenu
        self.menu_search_init: QMenu
        self.menu_set_fps: QMenu
        self.menu_set_fullscreen: QMenu
        self.menu_view_code: QMenu
        self.menu_manual: QMenu
        self.menu_info: QMenu

        # 상태 바 위젯
        self.statusbar: QStatusBar


        if fullscreen != 0:
            self.showMaximized()
            self.menu_set_fullscreen.setChecked(True)



        self.viewGraph = ViewGraph() # 그래프 표현 클래스 객체 생성
        self.verticalLayoutGraph.addWidget(self.viewGraph.graph) # verticalLayoutGraph에 viewGraph 올림

        self.runTime = RunTimer() # 타이머 객체 생성
        self.runTime.run_time_signal.connect(self.timer_worked) # 타이머 시그널

        self.statusbarTimer = ViewStatusBar(self.statusbar) # 상태바 타이머 생성

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

        # 메뉴바 시그널
        self.menu_exit.triggered.connect(self.close)
        self.menu_sort_init.triggered.connect(self.initSortLog)
        self.menu_search_init.triggered.connect(self.initSearchLog)
        self.menu_set_fps.triggered.connect(self.setFPS)
        self.menu_set_fullscreen.triggered.connect(self.fullScreenFunc)
        self.menu_view_code.triggered.connect(self.view_source)
        self.menu_manual.triggered.connect(self.view_manual)
        self.menu_info.triggered.connect(self.view_info)

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
        self.listWidgetLog.setEnabled(False)

        self.getSortWidgetValue()
        
        self.sortFunc()





    def sortRestartFunc(self): # 다시하기 버튼 클릭 시 동작
        self.pushButton_sort_start.setEnabled(False)
        self.pushButton_sort_stop.setEnabled(True)
        self.listWidgetLog.setEnabled(False)

        self.algorithmSimulation.terminate()
        self.viewGraph.stop()
        self.runTime.stop()

        gb.array = np.array(list(range(input_size)))

        self.sortFunc()





    def sortStopFunc(self): # 중지 버튼 클릭 시 동작
        self.algorithmSimulation.terminate()
        self.viewGraph.stop()
        self.runTime.stop()
        self.listWidgetLog.setEnabled(True)

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
        gb.array = np.array(list(range(input_size)))

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
        self.listWidgetLog.setEnabled(False)

        self.getSearchWidgetValue()
        self.searchFunc()





    def searchRestartFunc(self):
        self.pushButton_search_start.setEnabled(False)
        self.pushButton_search_stop.setEnabled(True)
        self.listWidgetLog.setEnabled(False)

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
        self.listWidgetLog.setEnabled(True)





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
        gb.array = np.array(list(range(input_size)))
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
                self.listWidgetLog.addItem(str(row[0]) + ", " + str(row[1]) + ", " + str(row[2]) + ", " + str(row[3]) + ", " + str(row[4]))

        elif index == 1:
            input_issort = False
            
            cursor.execute("SELECT * FROM search_algorithm")

            for row in cursor.fetchall():
                self.listWidgetLog.addItem(str(row[0]) + ", " + str(row[1]) + ", " + str(row[2]) + ", " + str(row[3]) + ", " + str(row[4]) + ", " + str(row[5]))

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

            self.getSortWidgetValue()

            self.statesInitFunc({
            "상태":"로그에 기록 됨",
            "진행 시간":self.tuple[2],
            "알고리즘 명":input_algorithm,
            "데이터 크기":input_size,
            "속도 제한":input_speed,
            "섞는 횟수":input_shuffle
        })

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

            self.getSearchWidgetValue()

            self.statesInitFunc({
                "상태":"로그에 기록 됨",
                "진행 시간": self.tuple[2],
                "알고리즘 명":input_algorithm,
                "데이터 크기":input_size,
                "속도 제한":input_speed,
                "탐색 값":input_search_value,
                "반복 횟수":input_repeat_value
            })

        connection.close()

    def log_list_double_clicked(self, item):
        self.primary_num = self.listWidgetLog.row(item) + 1

        self.log_window = DialogSetLog(input_issort, self.primary_num)
        self.log_window.show()

        connection.close()




    ## 메뉴바 관련 함수 ##
    def initSortLog(self): #정렬 테이블 초기화
        if self.show_dialog_init_table():
            connection = sqlite3.connect('algorithm_log.db')
            cursor = connection.cursor()

            cursor.execute('DELETE FROM sort_algorithm')

            connection.commit()
            connection.close()

            self.tabChangeSignal(self.tabWidgetControl.currentIndex())
            self.show_dialog_init_complete()

    def initSearchLog(self): #탐색 테이블 초기화
        if self.show_dialog_init_table():
            connection = sqlite3.connect('algorithm_log.db')
            cursor = connection.cursor()

            cursor.execute('DELETE FROM search_algorithm')

            connection.commit()
            connection.close()

            self.tabChangeSignal(self.tabWidgetControl.currentIndex())
            self.show_dialog_init_complete()


    def show_dialog_init_table(self): # 초기화 경고
        response = QMessageBox.question(self, "경고", "정말 초기화 하시겠습니까?")
        if response == QMessageBox.StandardButton.Yes:
            return True
        else:
            return False
        
    def show_dialog_init_complete(self): # 초기화 완료 메시지
        QMessageBox.information(self, "정보", "초기화 되었습니다.")


    def setFPS(self):
        self.fps_window = DialogSetFPS()
        self.fps_window.show()

        self.fps_window.change_fps_signal.connect(self.changeFPS)

    def changeFPS(self, getFPS):
        global fps

        bind_path = resource_path(BIND_FILE)

        with open(bind_path, 'r') as file:
            lines = file.readlines()

        lines[0] = f'fps = {getFPS}' + "\n"

        with open(bind_path, 'w') as file:
            file.writelines(lines)

        fps = getFPS

        self.viewGraph.graph_timer.setInterval(int(1000/fps))

    def fullScreenFunc(self, checked):
        global fullscreen

        bind_path = resource_path(BIND_FILE)

        with open(bind_path, 'r') as file:
            lines = file.readlines()

        if checked:
            lines[1] = f'fullscreen = 1' + "\n"
            fullscreen = 1
            self.showMaximized()
        else:
            lines[1] = f'fullscreen = 0' + "\n"
            fullscreen = 0
            self.showNormal()

        with open(bind_path, 'w') as file:
            file.writelines(lines)

    def view_source(self):
        self.source_window = DialogViewSource(self.algorithmSimulation.simulation)
        self.source_window.show()

    
    def view_manual(self):
        self.help_window = WidgetHelp()
        self.help_window.show()


    def view_info(self):
        self.info_window = DialogInfo()
        self.info_window.show()


    def closeEvent(self, event: QCloseEvent) -> None:
        reply = QMessageBox.question(self, '종료 확인', '정말 종료하시겠습니까?', 
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, 
                                     QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            QApplication.closeAllWindows()
        else:
            event.ignore()




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
file = open(bind_path, 'r')
lines = file.readlines()
for line in lines:
    bind_value.append(int(line.split()[2]))
file.close()

fps = bind_value[0]
fullscreen = bind_value[1]

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
    app.exec()
