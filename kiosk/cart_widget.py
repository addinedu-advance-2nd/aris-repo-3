import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PyQt5 import uic

# UI 파일을 로드하여 클래스 형식으로 변환
form_cart = uic.loadUiType('kiosk/UI/new_widget_cart.ui')[0]

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
        self.btn_del.clicked.connect(self.remove_cart_item)
        self.btn_minus.clicked.connect(self.decrease_quantity)
        self.btn_plus.clicked.connect(self.increase_quantity)

    # 장바구니 - 제거버튼
    def remove_cart_item(self):
        cur_cart_num = int(self.cart_num.text())

        self.setParent(None)

    # 장바구니 -버튼
    def decrease_quantity(self):
        print("버튼 눌림 확인")
        quantity = int(self.cart_num.text())
        if quantity > 1:
            self.cart_num.setText(str(quantity - 1))

    # 장바구니 +버튼
    def increase_quantity(self):
        print("버튼 눌림 확인")
        quantity = int(self.cart_num.text())
        self.cart_num.setText(str(quantity + 1))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CartWidget()
    window.show()
    app.exec_()
