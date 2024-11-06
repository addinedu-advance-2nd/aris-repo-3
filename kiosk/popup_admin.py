import sys
import pandas as pd
import pymysql

from PyQt5.QtWidgets import *
from PyQt5 import uic

PASSWD = '12345'
STYLE_ACTIVE = '''
    color: rgb(50, 50, 255);
    border: 2px solid rgb(90, 180, 255);
    border-radius: 10px; 
    font: 63 12pt "Gulim";
'''
STYLE_DEACTIVE = '''
    color: rgb(230, 230, 230);
    border: 2px solid black;
    border-radius:10px;
    font: 63 12pt "Gulim";
'''

conn = pymysql.connect(
    host='localhost', 
    port=3306, 
    user='pieces98', 
    passwd='1234',
    db='BARTENDROID'
)

form_admin = uic.loadUiType('./UI/popup_admin.ui')[0]
form_single_menu = uic.loadUiType('./UI/widget_single_menu.ui')[0]

class Popup_Admin(QDialog, form_admin):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # 시작화면 지정
        self.stack_main.setCurrentWidget(self.page_password)    # page_password

        self.btn_cancel.clicked.connect(self.close)
        self.btn_quit.clicked.connect(self.close)

        # 비밀번호 페이지
        # TODO : 우측 상단 취소 버튼 
        # 숫자 버튼
        for btn in self.keypads.findChildren(QPushButton):
            if btn.objectName()[-1].isalpha():
                continue
            btn.clicked.connect(self.enter_number)
        # 삭제 버튼
        self.btn_del.clicked.connect(self.delete_number)
        # 초기화 버튼
        self.btn_clear.clicked.connect(self.clear_number)
        # 확인 버튼
        self.btn_check_password.clicked.connect(self.check_password)
        self.entered_password = ''
        
        # 메뉴 관리 페이지의 상단 카테고리별 버튼
        self.btn_chocolate.clicked.connect(self.get_icecream_list)
        self.btn_fruit.clicked.connect(self.get_icecream_list)
        self.btn_plain.clicked.connect(self.get_icecream_list)
        self.btn_special.clicked.connect(self.get_icecream_list)
        self.btn_topping.clicked.connect(self.get_topping_list)

    def enter_number(self):
        '''버튼에 쓰여있는 숫자를 입력. 최대 20자리만 입력 가능'''
        if len(self.entered_password) == 20:
            QMessageBox.information(self, "Password Error", "패스워드는 최대 20자리 입니다.")
            return

        n = self.sender().text()[-1]
        self.entered_password += n
        self.label_password.setText('*'*len(self.entered_password))
    
    def delete_number(self):
        '''입력된 비밀번호의 마지막 숫자를 제거.'''
        self.entered_password = self.entered_password[:-1]
        self.label_password.setText('*'*len(self.entered_password))
        
    def clear_number(self):
        '''입력된 비밀번호를 초기화(비움)'''
        self.entered_password = ''
        self.label_password.setText('')

    def check_password(self):
        '''패스워드가 일치하는지를 확인. 올바르지 않은 경우 경고창 후 초기화'''
        # TODO : 현재 패스워드가 평문으로 저장되어 평문간의 비교를 사용하는 중. 
        if self.entered_password == PASSWD:
            self.stack_main.setCurrentWidget(self.page_menu_manager)
        else:
            QMessageBox.critical(self, "Password Error", "올바르지 않은 패스워드입니다.")
            self.clear_number()

    def get_icecream_list(self):
        '''쿼리를 통해 카테고리에 맞는 아이스크림 테이블을 출력'''

        target_category = self.sender().text()

        # 카테고리에 해당하는 데이터 추출
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        query_expr = f'select NAME, STATUS from ICECREAM where CATEGORY = "{target_category}"'
        cursor.execute(query_expr)
        result = cursor.fetchall()

        # 수직 정렬 레이아웃 생성 및 초기화
        if self.widget_list.layout() is None:
            self.widget_list.setLayout(QVBoxLayout(self))
        layout = self.widget_list.layout()

        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            else:
                layout.removeItem(item)

        # 추출된 데이터 위젯으로 만들어 출력
        for row in result:
            widget = MenuWidget(self, row['NAME'], row['STATUS'])
            print(row['NAME'], row['STATUS'])
            widget.setMinimumHeight(100)
            layout.addWidget(widget)
        layout.addStretch(1)
        cursor.close()


    def get_topping_list(self):
        '''쿼리를 통해 토핑 테이블을 출력'''
        # * addStretch(1)으로 해결

        cursor = conn.cursor(pymysql.cursors.DictCursor)
        query_expr = f'select NAME, STATUS from TOPPING'
        cursor.execute(query_expr)
        result = cursor.fetchall()

        # 수직 정렬 레이아웃 생성 및 초기화
        if self.widget_list.layout() is None:
            self.widget_list.setLayout(QVBoxLayout(self))
        layout = self.widget_list.layout()        

        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            else:
                layout.removeItem(item)

        # 추출된 데이터 위젯으로 만들어 출력
        for row in result:
            widget = MenuWidget(self, row['NAME'], row['STATUS'])
            widget.setMinimumHeight(100)
            layout.addWidget(widget)
        layout.addStretch(1)
        cursor.close()

class MenuWidget(QWidget, form_single_menu):
    '''아이스크림/토핑 리스트를 출력할 때, 각 항목을 표현하는 위젯'''
    def __init__(self, parent, menu_name, is_not_soldout):
        super().__init__()
        self.setupUi(self)

        self.parent = parent
        self.label_menu_name.setText(menu_name)
        self.label_menu_name.setStyleSheet('')

        # 현재 상태에 맞게 스타일 적용
        self.is_soldout = not is_not_soldout
        if self.is_soldout:
            self.btn_soldout.setStyleSheet(STYLE_ACTIVE)
            self.btn_not_soldout.setStyleSheet(STYLE_DEACTIVE)
        else:
            self.btn_soldout.setStyleSheet(STYLE_DEACTIVE)
            self.btn_not_soldout.setStyleSheet(STYLE_ACTIVE)

        self.btn_soldout.clicked.connect(self.change_to_soldout)
        self.btn_not_soldout.clicked.connect(self.change_to_not_soldout)

    def change_to_soldout(self):
        '''품절로 상태를 전환'''
        if self.is_soldout:
            QMessageBox.information(self, 'State Information', '이미 품절 상태입니다.')
            return
        QMessageBox.information(self, 'State Information', '품절 상태로 전환합니다.')
        
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        query_expr = f'update ICECREAM set STATUS=0 where NAME="{self.label_menu_name.text()}";'
        cursor.execute(query_expr)
        cursor.close()
        conn.commit()

        # TODO: 이걸 다시 DB에서 읽어와야하나?
        self.is_soldout = not self.is_soldout
        self.btn_soldout.setStyleSheet(STYLE_ACTIVE)
        self.btn_not_soldout.setStyleSheet(STYLE_DEACTIVE)

    def change_to_not_soldout(self):
        '''판매로 상태를 전환'''
        if not self.is_soldout:
            QMessageBox.information(self, 'State Information', '이미 판매 중인 상태입니다.')
            return
        QMessageBox.information(self, 'State Information', '판매 상태로 전환합니다.')

        cursor = conn.cursor(pymysql.cursors.DictCursor)
        query_expr = f'update ICECREAM set STATUS=1 where NAME="{self.label_menu_name.text()}";'
        cursor.execute(query_expr)
        cursor.close()
        conn.commit()

        self.is_soldout = not self.is_soldout
        self.btn_soldout.setStyleSheet(STYLE_DEACTIVE)
        self.btn_not_soldout.setStyleSheet(STYLE_ACTIVE)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = Popup_Admin()
    myWindow.show( )
    app.exec_( )
    conn.close()