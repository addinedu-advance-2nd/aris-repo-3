import sys
import pymysql

from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import QPixmap

form_main_menu = uic.loadUiType('./UI/widget_main_menu.ui')[0]

#TODO 1. scroll 구현
#TODO 2. 메뉴이미지 클릭시 => 팝업_토핑으로 창전환
#TODO 3. 메인메뉴(데이터베이스) => 위젯_메뉴로 데이터 전달
'''메인메뉴에서 DB메뉴를 표시'''
'''parent는 메인페이지에서 사용'''

class MenuWidget(QWidget, form_main_menu):
    def __init__(self, parent, widget_count, menu_url, menu_name, menu_pirce):
        super().__init__()
        self.setupUi(self)
        self.parent = parent

        self.counter = 0

        # 수직레이아웃
        self.col_layout = QVBoxLayout(self)
        # 수평레이아웃
        self.row_layout = QHBoxLayout()
        # 수직레이아웃에 수평레이아웃 넣기
        self.col_layout.addLayout(self.row_layout)
        # 위젯 개수(가변)
        self.add_widgets(widget_count)

    def add_widgets(self, widget_count):
        for i in range(widget_count):
            # QLabel을 예제 위젯으로 사용
            widget = QLabel(f"menu_{i+1}")

            # 현재 행(row_layout)에 위젯 추가
            self.row_layout.addWidget(widget)
            self.counter += 1

            # 4개의 위젯이 채워지면 새 행 추가
            if self.counter == 4:
                self.row_layout.addStretch(1)  # 현재 행의 남은 공간 채우기
                self.row_layout = QHBoxLayout()  # 새로운 행 생성
                self.col_layout.addLayout(self.row_layout)  # 수직 레이아웃에 새로운 행 추가
                self.counter = 0  # 카운터 초기화
        
        self.row_layout.addStretch(1)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget_count = 15  # 가변적인 위젯 수로 설정 가능 #TODO 
    window = MenuWidget(widget_count)
    window.show()
    app.exec_()

