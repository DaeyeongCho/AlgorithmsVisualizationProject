import os
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

from define import *

class AlgorithmsVisualizationWindow(QMainWindow):
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
        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        menu_file = menubar.addMenu("파일")
        menu_help = menubar.addMenu("도움말")

        self.close_menu = QAction("끝내기")
        self.close_menu.triggered.connect(self.closeEvent)

        menu_file.addAction(self.close_menu)

    def initToolbarUI(self):
        self.toolbar = self.addToolBar('툴바')

    def initStatebarUI(self):
        pass

    def initMainWindow(self):
        container = QHBoxLayout() # 가장 넓은 화면

        controlUIFrame = QFrame()
        controlUIFrame.setFrameShape(QFrame.Box)

        graphUIFrame = QFrame()
        graphUIFrame.setFrameShape(QFrame.Box)

        graphVisualUIFrame = QFrame()
        graphVisualUIFrame.setFrameShape(QFrame.Box)

        graphStateUIFrame = QFrame()
        graphStateUIFrame.setFrameShape(QFrame.Box)

        logUIFrame = QFrame()
        logUIFrame.setFrameShape(QFrame.Box)

        rowSpliter = QSplitter(Qt.Vertical)
        rowSpliter.addWidget(graphVisualUIFrame)
        rowSpliter.addWidget(graphStateUIFrame)


        columnSpliter = QSplitter(Qt.Horizontal)
        columnSpliter.addWidget(controlUIFrame)
        columnSpliter.addWidget(rowSpliter)
        columnSpliter.addWidget(logUIFrame)

        container.addWidget(columnSpliter)

        # 가장 큰 레이아웃인 container를 화면에 담음
        widget = QWidget()
        widget.setLayout(container)
        self.setCentralWidget(widget)


    def closeEvent(self, event):
        reply = QMessageBox.question(self, '메시지', '정말 종료하시겠습니까?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()






















if __name__ == '__main__':
    app = QApplication(sys.argv) # QApplication 객체 생성
    window = AlgorithmsVisualizationWindow() # AlgorithmsVisualizationWindow 객체 생성
    window.show() # 윈도우 창 실행
    sys.exit(app.exec_()) # 이벤트 루프 시작. 창 실행 상태 유지