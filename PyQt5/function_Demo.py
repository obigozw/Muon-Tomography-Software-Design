
##此文件展示简单的函数实现方法

import webbrowser
import os

def Tell(self):  # 一个槽，在main.py中加也可以
    a = 'ustc'
    self.ui.label_39.setText(a)
    b = (self.ui.lineEdit_16.text())
    port = '0x1'
    print(b+' ' + port)
    self.ui.statusbar.showMessage('ustc', msecs = 5000)

#默认浏览器链接网页：点击菜单中的
def findhelp(self):
    webbrowser.open('https://www.riverbankcomputing.com/software/pyqt/')
    os.system(r"MuonTomographySoftwareGuide.docx")
