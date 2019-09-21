# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\madou\Documents\Courses\IUS\2019 Fall\CSCI-P445\Projects\CS-Event-App\event_app\guest_login.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(530, 383)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(40, 65, 61, 21))
        self.label.setObjectName("label")
        self.nameInput = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.nameInput.setGeometry(QtCore.QRect(120, 60, 361, 31))
        self.nameInput.setReadOnly(True)
        self.nameInput.setObjectName("nameInput")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(40, 170, 55, 16))
        self.label_2.setObjectName("label_2")
        self.emailInput = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.emailInput.setGeometry(QtCore.QRect(120, 160, 361, 31))
        self.emailInput.setInputMethodHints(QtCore.Qt.ImhEmailCharactersOnly|QtCore.Qt.ImhMultiLine)
        self.emailInput.setReadOnly(True)
        self.emailInput.setObjectName("emailInput")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(230, 240, 93, 28))
        self.pushButton.setObjectName("pushButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 530, 26))
        self.menubar.setObjectName("menubar")
        self.menuguest_login = QtWidgets.QMenu(self.menubar)
        self.menuguest_login.setObjectName("menuguest_login")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuguest_login.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Full Name:"))
        self.label_2.setText(_translate("MainWindow", "Email:"))
        self.pushButton.setText(_translate("MainWindow", "Submit"))
        self.menuguest_login.setTitle(_translate("MainWindow", "guest login"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
