import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PyQt5 import uic

# UI 파일을 로드하여 클래스 형식으로 변환
form_cart = uic.loadUiType('kiosk/UI/widget_cart.ui')[0]

'''
QWidget : cart_widget
    QFrame : cart_frame
        QPushButton : btn_del, btn_minus, btn_plus
        QLabel : cart_name, cart_num, cart_top, label_pirce
'''
class CartWidget(QWidget, form_cart):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CartWidget()
    window.show()
    app.exec_()
