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

from popup_admin import Popup_Admin
from popup_topping import Popup_Topping

from menu_widget import MenuWidget
from cart_widget import CartWidget

''' 
Button, Widget, Label, Frame, dialog, Stacked Widget
팝업창 => QDialog, but QT디자이너에서 존재x
Qialog (== QMainWindow) 같다고 생각하고 진행, 코드상에서 수정
'''


# .ui 파일을 로드하여 MyKiosk 클래스 정의 준비
kiosk_class = uic.loadUiType("kiosk/UI/new_kiosk.ui")[0]
admin_class = uic.loadUiType("kiosk/UI/popup_login.ui")[0]
topping_class = uic.loadUiType("kiosk/UI/popup_topping.ui")[0]
warning_class = uic.loadUiType("kiosk/UI/popup_warning.ui")[0]
confirm_class = uic.loadUiType("kiosk/UI/popup_confirm.ui")[0]


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

        # 화면보호기 이미지 설정
        self.set_ad_img()
        
        # 초기화면 클릭 시 이벤트 연결
        self.page_initial.mousePressEvent = self.go_to_main
        # 로고라벨 클릭시 이벤트 연결
        self.logo_label.mousePressEvent = self.go_to_admin
        # 구매버튼 클릭시 함수실행
        # self.buy_btn.clicked.connect(self.go_to_confirm)

        # TODO 메뉴테이블 
        '''
        QFrame : menu_frame
            QScrollArea : menu_area
        '''
        # 객체 찾기
        target_frame = self.findChild(QFrame, "menu_frame")  
        self.scroll_area = self.findChild(QScrollArea, "menu_area") 

        # 수직 레이아웃 설정 + 간격제거
        self.menu_layout = QVBoxLayout(target_frame)
        self.menu_layout.setContentsMargins(0, 0, 0, 0) 
        self.menu_layout.setSpacing(0)

        # 카테고리 버튼 4개
        '''
        QPushButton : category_btn(1~4)
        '''
        for i in range(1, 5): 
            button = self.findChild(QPushButton, f"category_btn{i}")            
            button.clicked.connect(self.show_menu)

        # ScrollArea 설정, menu_frame의 크기에 맞춤
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setMinimumSize(target_frame.size()) 

        # ScrollArea의 콘텐츠 위젯 설정, QVBoxLayout을 ScrollArea의 콘텐츠 위젯에 설정
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)  
        self.scroll_area.setWidget(self.scroll_content)

        # ScrollArea를 menu_layout에 추가
        self.menu_layout.addWidget(self.scroll_area)
        

        #TODO 장바구니
        '''
        QFrame : cart_frame
            QScrollArea : cart_area
        '''
        # 객체 찾기
        cart_frame = self.findChild(QFrame, "cart_frame")  
        self.cart_area = self.findChild(QScrollArea, "cart_area") 

        # ScrollArea 설정, cart_frame의 크기에 맞춤
        self.cart_area.setWidgetResizable(True)
        self.cart_area.setMinimumSize(cart_frame.size()) 

        # ScrollArea의 콘텐츠 위젯 설정, 장바구니 항목을 담을 수직 레이아웃 추가
        self.cart_content = QWidget()
        self.cart_layout = QVBoxLayout(self.cart_content)  
        self.cart_area.setWidget(self.cart_content)
        self.cart_layout.setContentsMargins(0, 0, 0, 0)
        self.cart_layout.setSpacing(5)

        
        self.cart_widget = CartWidget()
        # CartWidget 내부 요소에 접근하여 버튼 이벤트 설정
        self.cart_widget.btn_del.clicked.connect(self.remove_cart_item)
        self.cart_widget.btn_minus.clicked.connect(self.decrease_quantity)
        self.cart_widget.btn_plus.clicked.connect(self.increase_quantity)
    connection.commit()
    
    # 화면보호기 이미지 설정
    def set_ad_img(self):
        self.ad_img_num = 1 

        self.ad = self.findChild(QLabel, "ad")
        pixmap = QPixmap(f"img/ad{self.ad_img_num}.png")  
        self.ad.setPixmap(pixmap)
        self.ad.setScaledContents(True)

        self.ad_timer = QTimer(self)
        
        self.ad_timer.timeout.connect(self.change_ad_img)
        self.ad_timer.start(3000)

    # 3초마다 화면보호기 이미지 변경
    def change_ad_img(self):
        print(self.ad_img_num)
        self.ad_img_num += 1
        if self.ad_img_num > 2:
            self.ad_img_num = 1
        
        pixmap = QPixmap(f"img/ad{self.ad_img_num}.png")  
        self.ad.setPixmap(pixmap)
        self.ad.setScaledContents(True)

    # 메인화면으로 전환
    def go_to_main(self, event):
        print("Initial page clicked") 
        self.stackedWidget.setCurrentWidget(self.page_main)

        # 화면보호기 타이머 중지
        self.ad_timer.stop()

    # 로고라벨 클릭체크, 관리자창으로 전환
    def go_to_admin(self, event):
        self.logo_click_count += 1
        print(f"로고클릭 {self.logo_click_count}번")
        
        if self.logo_click_count == 5:
            self.admin_window = Popup_Admin(connection)
            self.admin_window.show()
            print("Admin page clicked") 
            self.logo_click_count = 0        
    
    # 토핑창으로 전환
    def go_to_topping(self, menu_name):
        # TODO : 메뉴이름을 전달받는 과정이 추가되어야
        self.topping_window = Popup_Topping(menu_name, connection)
        self.topping_window.exec()

        # order = self.topping_window.order_info  # 메인에서 주문 정보 전달 => cart_widget에서 받는다
        # print('order: ', order)
            # Popup_Topping 창이 닫힌 후 order_info 확인
        order_info = self.topping_window.order_info
        if order_info:
            print('주문 정보 확인:', order_info)  # 디버깅용 출력
            self.open_order(self, self.menu_name, 1000)
        else:
            print('주문 정보가 없습니다.')
    

    # 메뉴위젯으로 전환 (4xn)
    def show_menu(self):
        # 클릭된 버튼 확인
        button = self.sender()
        button_name = button.objectName()

        # 각 버튼에 따라 보여줄 메뉴 위젯 수 설정
        widget_counts = {
            "category_btn1": 8,
            "category_btn2": 10,
            "category_btn3": 6,
            "category_btn4": 12
        }

        # 버튼 이름을 사용하여 생성할 메뉴 위젯 수를 가져오기
        num_widgets = widget_counts.get(button_name, 8)  # 기본값 8

        # 기존 '메뉴위젯'과 레이아웃 완전 초기화
        while self.scroll_layout.count():
            item = self.scroll_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()  # 위젯 삭제
            elif item.layout():
                while item.layout().count():
                    inner_item = item.layout().takeAt(0)
                    if inner_item.widget():
                        inner_item.widget().deleteLater()  # 레이아웃 안의 위젯 삭제
                item.layout().deleteLater()  # 하위 레이아웃 삭제

        # 필요한 개수만큼 4개씩 배치하고, 마지막 행에만 남은 위젯 수 추가
        full_rows = num_widgets // 4
        remaining_widgets = num_widgets % 4
        menu_names = ["초콜릿", "바닐라", "딸기", "민트초코", "블루베리"] * (num_widgets // 5 + 1)

        # 4개씩 채우는 행 생성
        for row in range(full_rows):
            row_layout = QHBoxLayout()
            row_layout.setSpacing(10)  # 위젯 간격을 균일하게 설정
            for j in range(4):
                menu_widget = MenuWidget(menu_names[row * 4 + j], self.go_to_topping)
                menu_widget.setMinimumSize(200, 200)  # 메뉴위젯 크기 조정
                menu_widget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
                row_layout.addWidget(menu_widget)
            self.scroll_layout.addLayout(row_layout)

        # 마지막 행에 남은 위젯 배치 (가운데 정렬)
        if remaining_widgets > 0:
            last_row_layout = QHBoxLayout()
            last_row_layout.setSpacing(10)

            for _ in range((4 - remaining_widgets) // 2):
                last_row_layout.addStretch()

            for k in range(remaining_widgets):
                menu_widget = MenuWidget(menu_names[full_rows * 4 + k], self.go_to_topping)
                menu_widget.setMinimumSize(200, 200)
                menu_widget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
                last_row_layout.addWidget(menu_widget)

            for _ in range(4 - remaining_widgets - (4 - remaining_widgets) // 2):
                last_row_layout.addStretch()

            self.scroll_layout.addLayout(last_row_layout)

        # 레이아웃 강제 업데이트
        self.scroll_content.update()
        self.scroll_content.adjustSize()

        print(f"{num_widgets}개의 메뉴 위젯이 레이아웃에 추가되었습니다.")


    #TODO
    def open_order(self, menu_name, price):
        # Popup_Topping 창을 열어 주문 정보 가져오기
        topping_window = Popup_Topping(menu_name, price, self)
        topping_window.exec()
        print(order_info)
        order_info = topping_window.order_info  # Popup_Topping 창에서 받은 주문 정보
        self.update_cart_widget(order_info)
    def update_cart_widget(self, order_info):
        # CartWidget의 각 요소에 주문 정보 표시
        print(order_info)
        self.cart_widget.cart_name.setText(order_info['name'])
        self.cart_widget.cart_num.setText("1")  # 초기 수량은 1
        self.cart_widget.cart_top.setText(order_info['topping'])
        self.cart_widget.label_price.setText(f"{order_info['price']} 원")

    # 장바구니 - 제거버튼
    def remove_cart_item(self):
        self.cart_widget.setParent(None)
    # 장바구니 - -버튼
    def decrease_quantity(self):
        quantity = int(self.cart_widget.cart_num.text())
        if quantity > 1:
            self.cart_widget.cart_num.setText(str(quantity - 1))
    # 장바구니 +버튼
    def increase_quantity(self):
        quantity = int(self.cart_widget.cart_num.text())
        self.cart_widget.cart_num.setText(str(quantity + 1))
    




if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyKiosk()
    window.show()
    app.exec_()
    connection.close()

