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

        self.conn = conn
        self.menu_name = menu_name

        self.pixmap_menu = QPixmap()
        self.menu_image = None

        self.topping_pixmap = [QPixmap(), QPixmap(), QPixmap()]
        self.topping_imgs = [self.img_topping_1, self.img_topping_2, self.img_topping_3]
        self.topping_labels = [self.label_topping_name_1, self.label_topping_name_2, self.label_topping_name_3]
        self.topping_frames = [self.frame_topping_1, self.frame_topping_2, self.frame_topping_3]
        self.funcs = [self.select_topping_1, self.select_topping_2, self.select_topping_3]
        
        self.btn_cancel.clicked.connect(self.cancel_order)

        self.load_menu_information()
        self.load_topping_information()

        self.picked_topping = 0

    def load_menu_information(self):
        # 메뉴에 대한 기본정보를 시현하는 함수
        self.label_menu_name.setText(self.menu_name)

        cursor = self.conn.cursor(pymysql.cursors.DictCursor)
        # TODO : 메뉴 이름을 바탕으로 가격과 메뉴 설명(추후 추가 예정)을 가져옴. 현재는 임시로 NAME사용
        query_expr = f'select PRICE, NAME, IMG from ICECREAM where NAME="{self.menu_name}"'
        cursor.execute(query_expr)
        result, = cursor.fetchall()

        self.label_price.setText(f'{result["PRICE"]} 원')
        # TODO : 메뉴 이름을 바탕으로 가격과 메뉴 설명(추후 추가 예정)을 가져옴. 현재는 임시로 NAME사용
        self.label_menu_comment.setText(result['NAME']+'설명설명설명')

        image = urllib.request.urlopen(result['IMG']).read()
        self.pixmap_menu.loadFromData(image)
        self.img_menu.setPixmap(self.pixmap_menu)
        self.img_menu.setScaledContents(True)
    
    def load_topping_information(self):
        # 토핑에 대한 기본정보를 시현하는 함수

        cursor = self.conn.cursor(pymysql.cursors.DictCursor)
        query_expr = 'select NAME, IMG, STATUS from TOPPING'
        cursor.execute(query_expr)
        topping_infos = cursor.fetchall()

        for i in range(3):
            img = self.topping_imgs[i]
            label = self.topping_labels[i]
            pixmap = self.topping_pixmap[i]
            info = topping_infos[i]
            event_func = self.funcs[i]
            
            label.setText(info['NAME'])
            topping_image = urllib.request.urlopen(info['IMG']).read()
            pixmap.loadFromData(topping_image)
            img.setPixmap(pixmap)
            img.setScaledContents(True)

            img.mousePressEvent = event_func

    def select_topping_1(self, event):
        self.reset_frame_style()
        self.topping_frames[0].setStyleSheet('QFrame#frame_topping_1 { border: 2px solid; }')
        self.picked_topping = 1
    
    def select_topping_2(self, event):
        self.reset_frame_style()
        self.topping_frames[1].setStyleSheet('QFrame#frame_topping_2 { border: 2px solid; }')
        self.picked_topping = 2

    def select_topping_3(self, event):
        self.reset_frame_style()
        self.topping_frames[2].setStyleSheet('QFrame#frame_topping_3 { border: 2px solid; }')
        self.picked_topping = 3

    def reset_frame_style(self):
        for frame in self.topping_frames:
            frame.setStyleSheet('')

    def cancel_order(self):
        self.picked_topping = 0
        self.send_order_information()
        self.close()

    def send_order_information(self):
        pass

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