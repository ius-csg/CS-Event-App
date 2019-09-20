from PyQt5.QtWidgets import QMainWindow, QWidget
from PyQt5.QtCore import pyqtSlot
from PyQt5 import QtCore, QtWidgets, uic
from PyQt5 import QtGui

# from pymysql import cursors
import pymysql

import re



# class MainPage(QMainWindow):
#     def __init__(self):
#         super(MainPage, self).__init__()
        
#         self.guest_ui = 'page_guest.ui'
#         self.main_ui = 'page_main.ui'

#         self.emailregex = r'(?:[a-z0-9!#$%&\'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&\'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])'
        
#         # self.dlg_main = uic.loadUi(self.main_ui)
#         # self.dlg_guest = uic.loadUi(self.guest_ui)
        
#         self.show_main_ui()
        
#         print(self.widget)
#         # self.guestButton = self.dlg_main.findChild(QtWidgets.QPushButton, 'guestButton')
#         # print(self.dlg_main.findChild(QtWidgets.QPushButton, 'guestButton'))
#         # self.guestButton.clicked.connect(self.guestPressed)

#     def show_main_ui(self):
#         # self.main_window.show()
#         self.dlg_main.show()
#         self.widget = self.dlg_main.findChild(QtWidgets.QWidget, 'mainWidget')
#         self.guestButton = self.dlg_main.findChild(QtWidgets.QPushButton, 'guestButton')
#         # print(self.dlg_main.findChild(QtWidgets.QPushButton, 'guestButton'))
#         self.guestButton.clicked.connect(self.guestPressed)

#     def show_guest_ui(self):
#         # self.guest_window.show()
#         self.dlg_main = uic.loadUi(self.guest_ui)
#         self.dlg_main.show()
#         self.widget = self.dlg_main.findChild(QtWidgets.QWidget, 'guestWidget')
    
#     def guestPressed(self):
#         # self.dlg_guest = uic.loadUi(self.guest_ui)
#         # self.submit = self.main_window.findChild(QtWidgets.QPushButton, 'submitButton')
#         # self.submit.connect(self.submitPressed)
#         self.show_guest_ui()
#         self.submitButton = self.widget.findChild(QtWidgets.QPushButton, 'submitButton')
#         self.submitButton.clicked.connect(self.submitPressed)

#     def submitPressed(self):
#         self.guest_name_textEdit = self.widget.findChild(QtWidgets.QTextEdit, 'nameTextEdit')
#         self.guest_email_textEdit = self.widget.findChild(QtWidgets.QTextEdit, 'emailTextEdit')
        
#         self.name = self.guest_name_textEdit.text()
#         self.email = self.guest_email_textEdit.text()

#         if re.match(self.emailregex, self.email):
#             print('email matches')

form1, base1 = uic.loadUiType('page_main.ui')
form2, base2 = uic.loadUiType('page_guest.ui')        


class MainPage(base1, form1):
    def __init__(self, user, password, ip):
        super(base1, self).__init__()
        self.setupUi(self)
        self.guestButton.clicked.connect(self.change)
        self.show()
        self.user = user
        self.password = password
        self.ip = ip

    def change(self):
        self.guest = GuestPage(self.user, self.password, self.ip)
        self.guest.show()
        self.close()

class GuestPage(base2, form2):
    def __init__(self, user, password, ip):
        super(base2, self).__init__()
        self.emailregex = r'(?:[a-z0-9!#$%&\'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&\'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])'
        self.setupUi(self)
        self.user = user
        self.password = password
        self.ip = ip
        self.connection = pymysql.connect(host=ip, user=user, password=password, db='test')
        self.submitButton.clicked.connect(self.change)
    
    def change(self):
        self.name = self.nameTextEdit.toPlainText()
        self.email = self.emailTextEdit.toPlainText()
        print(self.email)
        if re.match(self.emailregex, self.email):
            print('email matches')
            try:
                with self.connection.cursor() as cursor:
                    sql = 'INSERT INTO `event_registrar` (name, email) VALUES ("{0}", "{1}")'.format(self.name, self.name)
                    cursor.execute(sql)
                self.connection.commit()
            finally:
                self.connection.close()
            self.main = MainPage(self.user, self.password, self.ip)
            self.main.show()
            self.close()
        else:
            print('invalid email')
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage('Email must be a valid email')
            error_dialog.exec_()