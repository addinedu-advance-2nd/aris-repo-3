import os
import sys
import ast
import datetime
from random import randint

from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from PyQt5.QtGui import QPixmap
import pymysql


''' 
Button, Widget, Label, Frame, dialog, Stacked Widget
팝업창 => QDialog, but QT디자이너에서 존재x
Qialog (== QMainWindow) 같다고 생각하고 진행, 코드상에서 수정
'''

#! Qt디자이너 상에서 Widget배치가 원할하지 않을 수 있음

# .ui 파일을 로드하여 MyKiosk 클래스 정의 준비
kiosk_class = uic.loadUiType("kiosk/UI/kiosk.ui")[0]
admin_class = uic.loadUiType("kiosk/UI/popup_login.ui")[0]
topping_class = uic.loadUiType("kiosk/UI/popup_topping.ui")[0]
warning_class = uic.loadUiType("kiosk/UI/popup_warning.ui")[0]
confirm_class = uic.loadUiType("kiosk/UI/popup_confirm.ui")[0]


#TODO 유정's help 
# 1. DB연결
connection = pymysql.connect(
    host='localhost',
    user='root',
    password='12345678',
    database='BARTENDROID'
)

# 메인윈도우 - 초기화면 + 메인화면 + 메뉴테이블(9)
class MyKiosk(QMainWindow, kiosk_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.stackedWidget.setCurrentWidget(self.page_initial) 



        
        self.logo_click_count = 0    

        self.ad = self.findChild(QLabel, "ad")
        pixmap = QPixmap("img/img.jpg")  
        self.ad.setPixmap(pixmap)
        self.ad.setScaledContents(True)  # QLabel 크기에 맞게 이미지 조정
        
        # 초기화면 클릭 시 이벤트 연결
        self.page_initial.mousePressEvent = self.go_to_main
        # 로고라벨 클릭시 이벤트 연결
        self.logo_label.mousePressEvent = self.go_to_admin
        # 구매버튼 클릭시 함수실행
        self.buy_btn.clicked.connect(self.go_to_confirm)

        #TODO 카테고리(5) 선택시 메뉴(9)변경
        #self.category_btn1.clicked.connect(self.show_menu)
        for i in range(1, 6):  # 1부터 5까지 반복
            button = self.findChild(QPushButton, f"category_btn{i}")
            button.clicked.connect(self.show_menu)

        # 9개 메뉴버튼 클릭시 이벤트 연결
        for i in range(1, 10):  # 1부터 9까지 반복
            button = self.findChild(QPushButton, f"menu_btn_{i}")  # menu_btn_1부터 menu_btn_9까지 버튼 찾기
            button.mousePressEvent = self.go_to_topping  # 각 버튼의 클릭 이벤트에 go_to_topping 연결

        #TODO 9개의 메뉴 [이미지,이름,가격] - 데이터베이스 활용)
        #TODO 메뉴주문시 팝업-주문확인창
        #TODO 메뉴주문시 장바구니 표시(데이터베이스 활용)



    connection.commit()
    connection.close()

    # 메인화면으로 전환
    def go_to_main(self, event):
        print("Initial page clicked") 
        self.stackedWidget.setCurrentWidget(self.page_main)

    # 로고라벨 클릭체크, 관리자창으로 전환
    def go_to_admin(self, event):
        self.logo_click_count += 1
        print(f"로고클릭 {self.logo_click_count}번")
        
        if self.logo_click_count == 5:
            self.admin_window = WindowAdmin()
            self.admin_window.show()
            print("Admin page clicked") 
            self.logo_click_count = 0        
    
    # 토핑창으로 전환
    def go_to_topping(self, event):
        self.topping_window = ToppingWindow()
        self.topping_window.show()

    # 경고팝업으로 전환
    def go_to_warning(self, event):
        self.warning_window = Warining()
        self.warning_window.show()

    # 주문확인팝업으로 전환
    def go_to_confirm(self, event):
        self.confirm_window = ConfirmWindow()
        self.confirm_window.show()       

    # 메뉴테이블(9)
    def show_menu(self):
        print("Show menu9")
        self.stackedWidget_3.setCurrentWidget(self.page_5)


        
        
       

# 팝업 - 관리자 로그인
class WindowAdmin(QMainWindow, admin_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

# 팝업 - 토핑선택
class ToppingWindow(QMainWindow, topping_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  

 # 팝업 - 주문경고
class Warining(QMainWindow, warning_class):   
    def __init__(self):
        super().__init__()
        self.setupUi(self)  

# 팝업 - 주문확인        
class ConfirmWindow(QMainWindow, confirm_class):   
    def __init__(self):
        super().__init__()
        self.setupUi(self)  
    # TODO 데이터베이스 활용

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyKiosk()
    window.show()
    app.exec_()
    connection.close()

