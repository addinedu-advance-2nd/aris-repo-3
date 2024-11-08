import sys
import pymysql
import urllib.request

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic

form_topping_page = uic.loadUiType('kiosk/UI/popup_topping.ui')[0]

class Popup_Topping(QDialog, form_topping_page):
    def __init__(self, menu_name, conn):
        super().__init__()
        self.setupUi(self)  

        # DB와의 커넥터 저장
        self.conn = conn
        # 메뉴 이름, 이미지, 가격을 위한 변수 생성
        self.menu_name = menu_name
        self.pixmap_menu = QPixmap()
        self.menu_image = None
        self.menu_price = 0

        # 3개의 토핑에 대한 이미지 자리, 라벨, 선택시 디자인을 바꿀 프레임, 버튼의 콜백함수 목록 생성
        # ! 3개의 토핑이 고정적이라 DB에서도 최소 3개의 토핑은 항상 존재해야함 
        self.topping_pixmap = [QPixmap(), QPixmap(), QPixmap()]
        self.topping_imgs = [self.img_topping_1, self.img_topping_2, self.img_topping_3]
        self.topping_name_labels = [self.label_topping_name_1, self.label_topping_name_2, self.label_topping_name_3]
        self.topping_price_labels = [self.label_topping_price_1, self.label_topping_price_2, self.label_topping_price_3]
        self.topping_prices = []
        self.topping_frames = [self.frame_topping_1, self.frame_topping_2, self.frame_topping_3]
        self.funcs = [self.select_topping_1, self.select_topping_2, self.select_topping_3]
        
        # 주문 취소/주문 하기 버튼 이벤트 지정
        self.btn_cancel.clicked.connect(self.cancel_order)
        self.btn_order.clicked.connect(self.send_order_information)
        '''
        QPushButton : btn_order
        '''

        # 상단의 메뉴 정보 출력
        self.load_menu_information()
        # 토핑 정보 출력
        self.load_topping_information()

        self.picked_topping = 0

    def load_menu_information(self):
        # 메뉴에 대한 기본정보를 시현하는 함수

        # 메뉴 이름 출력
        self.label_menu_name.setText(self.menu_name)

        # DB에서 메뉴 이름에 해당하는 정보 가져오기
        cursor = self.conn.cursor(pymysql.cursors.DictCursor)
        query_expr = f'select PRICE, NAME, IMG, CONTENT from ICECREAM where NAME="{self.menu_name}"'
        cursor.execute(query_expr)
        result, = cursor.fetchall()

        # 가격, 설명 출력
        self.menu_price = result["PRICE"]
        self.label_price.setText(f'{result["PRICE"]} 원')
        self.label_menu_comment.setText(result['CONTENT'])

        # url을 통해 이미지 가져오고 출력
        image = urllib.request.urlopen(result['IMG']).read()
        self.pixmap_menu.loadFromData(image)
        self.img_menu.setPixmap(self.pixmap_menu)
        self.img_menu.setScaledContents(True)
    
    def load_topping_information(self):
        # 토핑에 대한 기본정보를 시현하는 함수

        # DB에서 토핑정보 가져오기
        cursor = self.conn.cursor(pymysql.cursors.DictCursor)   
        query_expr = 'select NAME, PRICE, IMG, STATUS from TOPPING'
        cursor.execute(query_expr)
        topping_infos = cursor.fetchall()

        for i in range(3):
            # 각 토핑이 위치할 이미지 라벨, 라벨, 정보, 동작할 함수 지정
            img = self.topping_imgs[i]
            label_name = self.topping_name_labels[i]
            label_price = self.topping_price_labels[i]
            pixmap = self.topping_pixmap[i]
            info = topping_infos[i]
            event_func = self.funcs[i]
            
            # 토핑 이름 및 이미지 출력
            label_name.setText(info['NAME'])
            label_price.setText(f'+{info["PRICE"]}원')
            self.topping_prices.append(info["PRICE"])
            topping_image = urllib.request.urlopen(info['IMG']).read()
            pixmap.loadFromData(topping_image)
            # 품절이라면 그레이스케일로 이미지 변환
            if info['STATUS'] == 0:
                pixmap = QPixmap.fromImage(pixmap.toImage().convertToFormat(QImage.Format_Grayscale8))
            img.setPixmap(pixmap)
            img.setScaledContents(True)

            # 판매중이라면 일반 이벤트 등록, 품절이라면 품절 안내 이벤트 등록
            if info['STATUS']:
                img.mousePressEvent = event_func
            else:
                img.mousePressEvent = self.show_soldout_message

    def select_topping_1(self, event):
        # 토핑1에 대한 이벤트(프레임 강조 및 선택 토핑 정보 저장)
        self.reset_frame_style()
        self.topping_frames[0].setStyleSheet('QFrame#frame_topping_1 { border: 2px solid; }')
        self.picked_topping = 1
    
    def select_topping_2(self, event):
        # 토핑2에 대한 이벤트(프레임 강조 및 선택 토핑 정보 저장)
        self.reset_frame_style()
        self.topping_frames[1].setStyleSheet('QFrame#frame_topping_2 { border: 2px solid; }')
        self.picked_topping = 2

    def select_topping_3(self, event):
        # 토핑3에 대한 이벤트(프레임 강조 및 선택 토핑 정보 저장)
        self.reset_frame_style()
        self.topping_frames[2].setStyleSheet('QFrame#frame_topping_3 { border: 2px solid; }')
        self.picked_topping = 3

    def reset_frame_style(self):
        # 강조된 프레임 스타일을 제거
        for frame in self.topping_frames:
            frame.setStyleSheet('')
    
    def show_soldout_message(self, event):
        # 품절 안내 메세지 출력
        QMessageBox.information(self, 'Title', '이 토핑은 품절 상태입니다.')

    def cancel_order(self):
        # 주문 취소의 경우 주문정보를 비움
        self.order_info = None
        self.close()

    def send_order_information(self):
        # 선택된 토핑이 있는 경우 그에 맞춰 주문정보를 반환
        if self.picked_topping:
            self.order_info = {
                'menu': self.menu_name, 
                'topping':self.topping_name_labels[self.picked_topping-1].text(), 
                'price': self.menu_price+self.topping_prices[self.picked_topping-1]
                }
            self.close()
        else:
            QMessageBox.information(self, 'title - select topping', '토핑은 반드시 선택해야합니다.')
        

if __name__ == '__main__':
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='12345678',
        database='BARTENDROID'
    )

    app = QApplication(sys.argv)
    myWindow = Popup_Topping('초콜릿', conn)
    myWindow.show( )
    app.exec_( )
    conn.close()