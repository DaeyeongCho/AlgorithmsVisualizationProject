# 프로그램 UI 적용
import os
import sys

from PyQt5 import uic
from PyQt5.QtGui import QIcon

from define import *


def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))    
    return os.path.join(base_path, relative_path)

def get_form_class():
    form = resource_path(UI_FILE_PASS)
    form_class = uic.loadUiType(form)[0]
    return form_class



icon = QIcon(ICON_PATH)      # QIcon 객체 생성