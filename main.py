#!/usr/bin/python3

import sys
import os
import paramiko
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import pyqtSlot, QSettings
from PyQt5.QtWidgets import QMessageBox, QFileDialog
from sshConfig import Ui_MainWindow

class MyFirstGuiProgram(Ui_MainWindow):
    def __init__(self, mainWindow):
        Ui_MainWindow.__init__(self)
        self.setupUi(mainWindow)
        mainWindow.setFixedSize(mainWindow.size())
        if self.q_settings(True, "folder_value", None):
            dir_list = os.listdir(self.q_settings(True, "folder_value", None))
        else:
            dir_list = os.listdir(".")
        self.update_list(dir_list)
        self.pushButton_3.clicked.connect(self.add_text_listbox)
        self.pushButton.clicked.connect(self.select_folder)


    def update_list(self, dir_list):
        for name in dir_list :
            if name.endswith(".pub"):
                self.listWidget.addItem(str(name))


    def q_settings(self, get, value, type_variable):
        settings = QSettings("ciunas", "bennett")
        if get:
            result = settings.value(value)
            return result
        else:
            settings.setValue("folder_value", value)

    def select_folder(self):
        folder = str(QFileDialog.getExistingDirectory(None, "Select Dir"))
        if folder:
            self.q_settings(False, folder, None)
            self.listWidget.clear()
            self.update_list(os.listdir(folder))
            return folder

    def add_text_listbox(self):
        if (self.widget_info()):
            user = "root"
            key = open(os.path.expanduser("~/.ssh/" +
                 self.widget_info())).read()
            server = self.lineEdit.text()
            password = self.lineEdit_2.text()
            if server  and password:
                if r"@" in server:
                    split = server.split("@")
                    user = split[0]
                    server = split[1]
                else:
                    QMessageBox.about(self.listWidget,
                         "Message", "No User, using Root:    ")
                self.deploy_key(key, server, user, password)
            else:
                QMessageBox.about(self.listWidget,
                    "Message", "Insert host and password:    ")

    def widget_info(self):
        if self.listWidget.selectedItems():
            text = self.listWidget.currentItem().text()
            return text
        else:
            QMessageBox.about(self.listWidget,
                 "Message", "No Key Highlighted:    ")

    def deploy_key(self, key, server, username, password):
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(server, username=username, password=password)

            client.exec_command('mkdir -p ~/.ssh/')
            client.exec_command('chmod 700 ~/.ssh/')

            stdin, stdout, stderr = client.exec_command('cat'
                ' ~/.ssh/authorized_keys')
            temp = stdout.readlines()

            if key not in temp or not temp:
                client.exec_command('echo "%s" >>'
                    '~/.ssh/authorized_keys' % key)
                client.exec_command('chmod 644 ~/.ssh/authorized_keys')
                QMessageBox.about(self.listWidget,
                   "Message", "Key copied:    ")
                self.lineEdit.clear()
                self.lineEdit_2.clear()
        except paramiko.AuthenticationException:
            QMessageBox.about(self.listWidget,
               "Message", "Connection Error:    ")
        except:
            QMessageBox.about(self.listWidget,
               "Message", "Connection Error:    ")

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    prog = MyFirstGuiProgram(window)
    window.show()
    sys.exit(app.exec_())
