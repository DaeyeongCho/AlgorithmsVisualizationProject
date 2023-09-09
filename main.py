import os
import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QIcon

class AlgorithmsVisualizationApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("정렬/탐색 알고리즘 시각화 프로그램")
        self.move(300, 300)
        self.resize(400, 200)
        self.path = os.path.join(os.path.dirname(__file__), 'icon.ico')
        if os.path.isfile(self.path):
            self.setWindowIcon(QIcon(self.path))
        self.show()




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = AlgorithmsVisualizationApp()
    sys.exit(app.exec_())