#!/usr/bin/python3

import sys
import os
import paramiko
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMessageBox
from sshConfig import Ui_MainWindow
 
class MyFirstGuiProgram(Ui_MainWindow): 
    def __init__(self, mainWindow):
        Ui_MainWindow.__init__(self)
        self.setupUi(mainWindow)
        dirList = os.listdir("/home/ciunas/.ssh")
        for name in dirList :
            if name.endswith(".pub"):
                self.listWidget.addItem(str(name))
        self.pushButton_3.clicked.connect(self.addInputTextToListbox)
        self.pushButton.clicked.connect(self.widget_info)


    def addInputTextToListbox(self):
        if (self.widget_info()):
           key = open(os.path.expanduser("~/.ssh/" + 
                self.widget_info())).read()
           server = self.lineEdit.text()
           password = self.lineEdit_2.text()
           self.deploy_key(key, server, "ciunas", password)


    def widget_info(self):
        if self.listWidget.selectedItems():
            #row = self.listWidget.currentRow()
            text = self.listWidget.currentItem().text()
            #print(row )
            print(text)
            return text
        else:
            QMessageBox.about(self.listWidget,
                 "Message", "No Key Highlighted")
 
    def deploy_key(self, key, server, username, password):
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(server, username=username, password=password)
        client.exec_command('mkdir -p ~/.ssh/')
        client.exec_command('echo "%s" > ~/.ssh/authorized_keys' % key)
        client.exec_command('chmod 644 ~/.ssh/authorized_keys')
        client.exec_command('chmod 700 ~/.ssh/')


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    prog = MyFirstGuiProgram(window)
    window.show()
    sys.exit(app.exec_())
