import sys
import pymysql

from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
import mysql.connector



form_cart = uic.loadUiType('./UI/widget_cart.ui')[0]


#TODO 2. scroll 구현
#TODO 3. 팝업_토핑 메뉴담기 클릭시 => 메인메뉴_장바구니위젯_메뉴표시 (딕셔너리 or 리스트)

'''메인메뉴에서 카트에 주문목록 표시'''
class CartWidget(QWidget, form_cart):
    def __init__(self, cart_del, cart_name, cart_top, cart_num, cart_price):
        self.btn_del.setText = "삭제"
        self.cart_name.setText = "초콜릿 아이스크림"  '''from 팝업창'''
        self.cart_top.setText = "토핑1"            '''from'''
        self.cart_minus.image = "이미지"
        self.cart_num = 1
        self.cart_plus.image = "이미지"
        self.cart_plus.price = 2500

    def get_icecream():
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        query_expr = f'select NAME, STATUS from ICECREAM where CATEGORY = "{target_category}"'
        cursor.execute(query_expr)
        result = cursor.fetchall()        