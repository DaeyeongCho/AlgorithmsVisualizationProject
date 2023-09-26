import os
import sys

from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import QIcon

from define import * # 상수, 스트링 모음
from ui_connection import get_form_class # ui 적용

form_class = get_form_class()

## ================================================= 메인 윈도우 클래스 ================================================= ##
class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super( ).__init__( )
        ## ========== 정의 ========== ##

        self.setupUi(self) # ui 임포트
        



        # 시그널 작성

    # 함수 작성

    








if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()
