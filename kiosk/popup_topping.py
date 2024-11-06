import sys
import pymysql
import urllib.request

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic

form_topping = uic.loadUiType('kiosk/UI/popup_topping.ui')[0]

class Popup_Topping(QMainWindow, form_topping):
    def __init__(self, menu_name, conn):
        super().__init__()
        self.setupUi(self)  

        self.conn = conn
        self.menu_name = menu_name

        self.pixmap = QPixmap()
        self.menu_image = None
        self.load_menu_information()

    def load_menu_information(self):
        self.label_menu_name.setText(self.menu_name)

        cursor = self.conn.cursor(pymysql.cursors.DictCursor)
        # TODO : 메뉴 이름을 바탕으로 가격과 메뉴 설명(추후 추가 예정)을 가져옴. 현재는 임시로 NAME사용
        query_expr = f'select PRICE, NAME, IMG from ICECREAM where NAME="{self.menu_name}"'
        cursor.execute(query_expr)
        result, = cursor.fetchall()

        self.label_price.setText(f'{result["PRICE"]} 원')
        # TODO : 메뉴 이름을 바탕으로 가격과 메뉴 설명(추후 추가 예정)을 가져옴. 현재는 임시로 NAME사용
        self.label_menu_comment.setText(result['NAME']+'설명설명설명')

        self.menu_image = urllib.request.urlopen(result['IMG']).read()
        self.pixmap.loadFromData(self.menu_image)
        self.pixmap = self.pixmap.scaled(150, 150)
        self.img_menu.setPixmap(self.pixmap)
        

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