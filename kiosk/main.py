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
from popup_order import Popup_order

from menu_widget import MenuWidget
from cart_widget import CartWidget

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)


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
        self.total_cart_num = 0  

        self.cart_widget = CartWidget()

        # cursor = self.conn.cursor(pymysql.cursors.DictCursor)

     

        # 화면보호기 이미지 설정
        self.set_ad_img()

        # test
        self.check_order()
        
        # 초기화면 클릭 시 이벤트 연결
        self.page_initial.mousePressEvent = self.go_to_main
        # 로고라벨 클릭시 이벤트 연결
        self.logo_label.mousePressEvent = self.go_to_admin
        # TODO: qt designer 내 객체 이름이 규칙에 맞지 않아서 수정이 필요
        # TODO: 버튼의 클릭 이벤트에 대해서 mousePressEvent를 할지, clicked.connect를 할지, 통일시킬지 말지 결정이 필요함. 
        # 구매버튼 클릭시 함수실행
        self.buy_btn.clicked.connect(self.go_to_confirm_order)

        # TODO 메뉴테이블 
        '''
        [Menu Widget]
        QFrame : menu_frame
            QScrollArea : menu_area
        '''

        '''
        [Cart Widget]
        QFrame : cart_frame
            QScrollArea : cart_area
        '''
        # 객체 찾기
        self.target_frame = self.findChild(QFrame, "menu_frame")  
        self.scroll_area = self.findChild(QScrollArea, "menu_area") 

        self.cart_frame = self.findChild(QFrame, "cart_frame")  
        self.cart_area = self.findChild(QScrollArea, "cart_area") 

        # 레이아웃 설정 + 간격제거
        self.menu_layout = QVBoxLayout(self.target_frame)
        self.menu_layout.setContentsMargins(0, 0, 0, 0) 
        self.menu_layout.setSpacing(0)

        cart_frame_layout = QVBoxLayout(self.cart_frame)
        cart_frame_layout.setContentsMargins(0, 0, 0, 0)  # 여백 제거
        cart_frame_layout.addWidget(self.cart_area)  # QScrollArea 추가

        # ScrollArea 설정, menu_frame의 cart_area크기에 맞춤
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setMinimumSize(self.target_frame.size()) 

        self.cart_area.setWidgetResizable(True)
        self.cart_area.setMinimumSize(self.cart_frame.size())

        # ScrollArea의 콘텐츠 위젯 설정, QVBoxLayout을 ScrollArea의 콘텐츠 위젯에 설정
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)  
        self.scroll_area.setWidget(self.scroll_content)

        # QScrollArea 내부에 들어갈 콘텐츠 위젯과 레이아웃 설정
        self.cart_content = QWidget()
        self.cart_layout = QVBoxLayout(self.cart_content)
        self.cart_area.setWidget(self.cart_content)



        # ScrollArea를 menu_layout에 추가
        self.menu_layout.addWidget(self.scroll_area)


        # 카테고리 버튼 4개
        '''
        QPushButton : category_btn(1~4)
        '''
        for i in range(1, 5): 
            button = self.findChild(QPushButton, f"category_btn{i}")            
            button.clicked.connect(self.show_menu)

        #TODO 장바구니


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
        
        order_info = self.topping_window.order_info
        if order_info:
            print('go_to_topping 함수 실행 order_info = ', order_info)
            # self.update_cart_widget(order_info)
            self.show_cart(order_info)

        else:
            print('주문 정보가 없습니다.')

    def go_to_confirm_order(self):
        # 메인화면 내 장바구니의 주문정보를 받아와 
        #TODO : 샘플 주문을 장바구니에서 가져온 정보로 바꿔야함. 
        sample_order1 = [
            {'name':'나주배 소르베', 'topping': '바닐라', 'price': 5000, 'count': 1}, 
            {'name':'아몬드 봉봉', 'topping': '바닐라', 'price': 2000, 'count': 1}, 
            {'name':'피스타치오 아몬드', 'topping': '레인보우', 'price': 3000, 'count': 1}, 
            {'name':'소금우유 아이스크림', 'topping': '초콜릿', 'price': 7000, 'count': 1}, 
            {'name':'아몬드 봉봉', 'topping': '바닐라', 'price': 2000, 'count': 1}, 
            {'name':'피스타치오 아몬드', 'topping': '레인보우', 'price': 3000, 'count': 1}, 
        ]
        self.order_info = sample_order1
        self.available_positions = ['A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'A1', 'A2', 'A3', 'B1', 'B2', 'B3', ]
        self.order_window = Popup_order(self.order_info, self.available_positions)
        self.order_window.show()

        # TODO : 메인화면(장바구니)을 초기화하는 함수가 필요함.

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
                menu_widget.setMinimumSize(10, 10)  # 메뉴위젯 크기 조정
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

    # 카트 위젯에 새로운 주문 추가
    def show_cart(self, order_info):
        print("show_cart 함수를 실행합니다, order_info :", order_info)

        # 1. CartWidget 인스턴스를 생성
        cart_item_widget = CartWidget()
        cart_item_widget.setFixedSize(QSize(160, 140))  # 장바구니 너비 186

        # CartWidget이 스크롤 영역의 가로 크기에 맞춰지도록 설정
        cart_item_widget.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        # 주문 정보를 CartWidget의 라벨에 설정
        cart_item_widget.cart_name.setText(order_info['menu'])
        cart_item_widget.cart_num.setText(str(1))
        cart_item_widget.cart_top.setText(order_info['topping'])
        cart_item_widget.label_price.setText(f"{order_info['price']} 원")

        # 2. 기존 레이아웃의 addStretch 제거
        if self.cart_layout.count() > 0 and isinstance(self.cart_layout.itemAt(self.cart_layout.count() - 1), QSpacerItem):
            self.cart_layout.takeAt(self.cart_layout.count() - 1)

        # 3. 새로운 CartWidget을 장바구니 레이아웃에 추가
        self.cart_layout.addWidget(cart_item_widget)

        # 4. 장바구니 레이아웃에 빈 공간 추가
        self.cart_layout.addStretch()  # addStretch로 남은 공간을 공백으로 채움
        print(f'current cart : {self.cart_layout.count()}')
        # 5. 장바구니 UI 업데이트
        self.cart_content.update()
        self.cart_content.adjustSize()

        print(f"장바구니에 항목 추가됨: 메뉴 - {order_info['menu']}, 토핑 - {order_info['topping']}, 가격 - {order_info['price']}")

    # 장바구니에 3개 이상 담길 경우 경고
    def check_order(self):
        print(self.total_cart_num)
        if self.total_cart_num >= 3:
            QMessageBox.warning(self, "Order Error", "아직 초보 바텐드로이드에게\n3개 이상의 주문은 무리에요😭")
            return



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyKiosk()
    window.show()
    app.exec_()
    connection.close()

