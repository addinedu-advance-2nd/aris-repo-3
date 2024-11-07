import sys
import pymysql

from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import QPixmap

form_main_menu = uic.loadUiType('kiosk/UI/widget_main_menu.ui')[0]

'''
 QWidget : item
    QPushButton : btn_image
    QLabel : label_name, label_price
'''
class MenuWidget(QWidget, form_main_menu):
    def __init__(self, menu_name, click_callback):
        super().__init__()
        self.setupUi(self)
        self.menu_name = menu_name
        self.click_callback = click_callback

        self.btn_image.clicked.connect(self.handle_click)
    
    # 클릭 => 메뉴이름 전달
    def handle_click(self):
        self.click_callback(self.menu_name)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MenuWidget()
    window.show()
    app.exec_()

