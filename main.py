import os
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from define import *

class AlgorithmsVisualizationWindow(QMainWindow):
    ## ======================================================= 초기 윈도우 화면 세팅 함수 ======================================================= ##
    def __init__(self): # 생성자
        super().__init__()
        self.initUI()
        self.initMenubarUI()
        self.initToolbarUI()
        self.initStatebarUI()
        self.initMainWindow()

    def initUI(self):
        self.setWindowTitle(WINDOW_TITLE)
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.icon_path = os.path.join(os.path.dirname(__file__), ICON_PATH)
        if os.path.isfile(self.icon_path):
            self.setWindowIcon(QIcon(self.icon_path))

    def initMenubarUI(self):
        pass

    def initToolbarUI(self):
        pass

    def initStatebarUI(self):
        pass

    def initMainWindow(self):
        container = QWidget()
        containerQHBoxLayout = QHBoxLayout(container) # 가장 상위 레이아웃

        horizontalSplitter = QSplitter(Qt.Horizontal) # containerQHBoxLayout 내부 레이아웃
        verticalSplitter = QSplitter(Qt.Vertical) # horizontalSplitter 내부 레이아웃

        controlUIFrame = QScrollArea() # horizontalSplitter 내부 프레임
        controlUIWidget = QWidget() # controlUIFrame 내부 위젯(스크롤 기능을 위함. 동적 생성 시 adjustSize() 함수 사용 필수)
        controlUIWindow = QVBoxLayout() # controlUIWidget 내부 레이아웃(여기에 위젯들 구현. 동적 생성 시 adjustSize() 함수 사용 필수)

        graphUIFrame = QFrame() # verticalSplitter 내부 프레임
        graphUIWindow = QVBoxLayout() # graphUIFrame 내부 레이아웃
        fig = plt.Figure()
        ax = fig.add_subplot(111)
        canvas = FigureCanvas(fig)

        graphStatusUIFrame = QScrollArea() # verticalSplitter 내부 프레임
        logUIFrame = QScrollArea() # horizontalSplitter 내부 프레임

        

        
        controlUIWidget.setLayout(controlUIWindow)
        
        controlUIFrame.setFrameShape(QFrame.StyledPanel)
        controlUIFrame.setMinimumWidth(CONTROL_UI_FRAME_MIN_WIDTH)
        controlUIFrame.setFixedWidth(CONTROL_UI_FRAME_FIX_WIDTH)
        controlUIFrame.setWidget(controlUIWidget)

        graphUIFrame.setFrameShape(QFrame.StyledPanel)
        graphUIFrame.setLayout(graphUIWindow)
        graphUIWindow.addWidget(canvas)


        graphStatusUIFrame.setFrameShape(QFrame.StyledPanel)
        graphStatusUIFrame.setMinimumHeight(GRAPH_STATUS_UI_FRAME_MIN_HEIGHT)

        logUIFrame.setFrameShape(QFrame.StyledPanel)
        logUIFrame.setMinimumWidth(LOG_UI_FRAME_MIN_WIDTH)

        verticalSplitter.addWidget(graphUIFrame)
        verticalSplitter.addWidget(graphStatusUIFrame)
        verticalSplitter.setHandleWidth(0)
        verticalSplitter.setSizes(VERTICAL_SPLITTER_SIZES)
        verticalSplitter.setStretchFactor(1, 0)

        horizontalSplitter.addWidget(controlUIFrame)
        horizontalSplitter.addWidget(verticalSplitter)
        horizontalSplitter.addWidget(logUIFrame)
        horizontalSplitter.setHandleWidth(0)
        horizontalSplitter.setSizes(HORIZONTAL_SPLITTER_SIZES)
        horizontalSplitter.setStretchFactor(0, 0)
        horizontalSplitter.setStretchFactor(2, 0)

        containerQHBoxLayout.addWidget(horizontalSplitter)

        self.setCentralWidget(container)

        


        ax.plot([1, 2, 3, 4])
        ax.grid()



    ## ============================================================================================================== ##















    # def closeEvent(self, event):
    #     reply = QMessageBox.question(self, '메시지', '정말 종료하시겠습니까?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

    #     if reply == QMessageBox.Yes:
    #         event.accept()
    #     else:
    #         event.ignore()






















if __name__ == '__main__':
    app = QApplication(sys.argv) # QApplication 객체 생성
    window = AlgorithmsVisualizationWindow() # AlgorithmsVisualizationWindow 객체 생성
    window.show() # 윈도우 창 실행
    sys.exit(app.exec_()) # 이벤트 루프 시작. 창 실행 상태 유지