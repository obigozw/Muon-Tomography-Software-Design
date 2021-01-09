import win32ui
import tkinter as tk
from tkinter import filedialog

import sys
from PyQt5 import QtCore, QtGui, uic
import locale
import re
import os
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import paramiko

filename1 = []#全局变量路径，传递给其他函数
filename2 = []#全局变量路径, 传递给其他函数

#设置文件位置
def SendChooseFile(self,lineEdit):
    root = tk.Tk()
    root.withdraw()
    file_path1 = filedialog.askopenfilename(initialdir='F:\PyCharm\projects')
    lineEdit.setText(file_path1)
    filename1.clear()
    filename1.append(file_path1)

def ReceiveChooseFile(self, lineEdit):
    root = tk.Tk()
    root.withdraw()
    file_path2 = filedialog.asksaveasfilename()
    lineEdit.setText(file_path2)
    filename2.clear()
    filename2.append(file_path2)


#测试用
'''
def testssh(self):
    ip = str(self.ip.text())
    username = str(self.name.text())
    password = str(self.password.text())
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip, 5050, username, password)
    stdin, stdout, stderr = ssh.exec_command('ls')
    print('a')
    stdout.read()
    ssh.close()
'''