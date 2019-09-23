from PyQt5.QtWidgets import QMainWindow, QWidget, QMessageBox
from PyQt5.QtCore import pyqtSlot, QBasicTimer, QThread, QTimer
from PyQt5 import QtCore, QtWidgets, uic
from PyQt5 import QtGui

# from PySide2.QtCore import QTimer

import pymysql
import pymysql.err as err

import re

import time

form1, base1 = uic.loadUiType('page_main.ui')
form2, base2 = uic.loadUiType('page_guest.ui')
form3, base3 = uic.loadUiType('progress_timer.ui')

def check_db_connection(user, password, ip):
    try:
        connection = pymysql.connect(host=ip, user=user, password=password, db='test')
    except err.OperationalError as e:
        if '(timed out)' in e.args[1]:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage('Timed out while connecting to {0}.'.format(ip))
            error_dialog.exec_()
        
        return (False, None)
    return (True, connection)

class MainPage(base1, form1):
    def __init__(self, user, password, ip):
        super(base1, self).__init__()
        self.setupUi(self)
        self.guestButton.clicked.connect(self.change)
        self.show()
        self.user = user
        self.password = password
        self.ip = ip

        # self.timer_thread = TimerThread(user, password, ip)
        # self.timer_thread.finished.connect(self.connect_button)
        # # self.timer_runnable.result.connect(self.handle_result)
        # self.timer_thread.start()

        status = check_db_connection(user, password, ip)
        if status[0]:
            status[1].close()
            self.connect_button()
        else:
            self.timer_progress = TimerProgress()
            self.timer_progress.show()
            self.close()

        # self.status_loop()
        # self.timer_start()        

    def connect_button(self):
        # self.timer_runnable.connection.close()
        print('connecting button')
        self.guestButton.clicked.connect(self.change)        
    
    def handle_result(self, connection):
        self.connection = connection
        print('interesting 2')
        self.guestButton.clicked.connect(self.change)

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

        # self.timer_thread = TimerThread(user, password, ip)
        # self.timer_thread.finished.connect(self.connect_button)
        # self.timer_thread.result.connect(self.handle_result)
        # self.timer_thread.start()

        status = check_db_connection(user, password, ip)
        if status[0]:
            status[1].close()
            self.connect_button()
        else:
            self.timer_progress = TimerProgress('guest')
            self.timer_progress.show()
            self.close()

    def handle_result(self, connection):
        self.connection = connection

    def connect_button(self):
        print('connecting button 2')
        self.submitButton.clicked.connect(self.change)
        # self.connection = self.timer_thread.connection
        
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
            except err.OperationalError as e:
                print(e.args)
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

class TimerThread(QtCore.QThread):
    result = QtCore.pyqtSignal(object)

    def __init__(self, user, password, ip):
        super(QtCore.QThread, self).__init__()
        self.user = user
        self.password = password
        self.ip = ip

    def run(self):
        self.status_loop()
    
    def status_loop(self):
        timerProgress = None
        status = check_db_connection(self.user, self.password, self.ip)
        if status[0]:
            print('interesting')
            self.result.emit(status[1])
            return
        status[1].close()
        loop = True
        while loop:
            if not timerProgress:
                timerProgress = TimerProgress()
            if not timerProgress.isFinished():
                continue
            else:
                timerProgress.close()
                timerProgress = TimerProgress()
                timerProgress.show()
            print('heheheheheh')
            status = check_db_connection(self.user, self.password, self.ip)
            if status[0]:
                print('woot woot')
                self.connection = status[1]
                loop = False
                self.result.emit(self.connection)
            else:
                status[1].close()
                timerProgress.start()

class TimerProgress(base3, form3):
    def __init__(self, evoked_from='main'):
        super(base3, self).__init__()
        self.setupUi(self)
        self.step = 0
        # self.timer = QBasicTimer()
        self.timer = QTimer(self)
        self.timer_start()
        self.time_left_int = 10
    
    def isFinished(self):
        return self.step >= 100 and self.time_left_int <= 0
    
    def timer_start(self):
        # self.timer = QTimer()
        # self.time_left_int = 10
        self.timer.timeout.connect(self.timer_timeout)
        self.timer.start(1000)
    
    def timer_timeout(self):
        self.step += 10
        self.time_left_int -= 1
        
    def timerEvent(self, event):
        print('hmmm')
        if self.step >= 100:
            self.timer.stop()
            return
        self.step += 10
        print('interesting')
        self.timerProgressBar.setValue(self.step)