import sys
import pymysql
import urllib.request

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic

form_order_page = uic.loadUiType('kiosk/UI/popup_order.ui')[0]
form_menu_position = uic.loadUiType('kiosk/UI/widget_menu_position.ui')[0]

class Popup_order(QDialog, form_order_page):
    def __init__(self, order_information, available_positions):
        super().__init__()
        self.setupUi(self)

        self.load_order_info(order_information, available_positions)

    def load_order_info(self, order_information, available_positions):
        self.scroll_menu.setLayout(QVBoxLayout(self.scroll_menu))
        layout = self.scroll_menu.layout()

        for i, info in enumerate(order_information):
            widget = Widget_Menu_Position(info['name'], info['topping'], available_positions[i])
            widget.setStyleSheet('border: 1px solid;')
            layout.addWidget(widget)
        layout.addStretch(1)
        print(layout.count())

class Widget_Menu_Position(QWidget, form_menu_position):
    def __init__(self, menu_name, topping_name, position):
        super().__init__()
        self.setupUi(self)

        self.label_menu_name.setText(menu_name)
        self.label_topping_name.setText(topping_name)
        self.label_position.setText(position)
        print(f'Add {menu_name}, {topping_name}, {position}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    sample_order1 = [
        {'name':'나주배 소르베', 'topping': '바닐라', 'price': 5000, 'count': 1}, 
        {'name':'아몬드 봉봉', 'topping': '바닐라', 'price': 2000, 'count': 1}, 
        {'name':'피스타치오 아몬드', 'topping': '레인보우', 'price': 3000, 'count': 1}, 
        {'name':'소금우유 아이스크림', 'topping': '초콜릿', 'price': 7000, 'count': 1}, 
        {'name':'아몬드 봉봉', 'topping': '바닐라', 'price': 2000, 'count': 1}, 
        {'name':'피스타치오 아몬드', 'topping': '레인보우', 'price': 3000, 'count': 1}, 
    ]
    sample_order2 = [
        {'name':'나주배 소르베', 'topping': '바닐라', 'price': 5000, 'count': 1}, 
        {'name':'아몬드 봉봉', 'topping': '바닐라', 'price': 2000, 'count': 1}, 
    ]
    positions = ['A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'A1', 'A2', 'A3', 'B1', 'B2', 'B3', ]

    myWindow = Popup_order(sample_order1, positions)
    myWindow.show()
    app.exec_()
