import subprocess
from Muon_UI import Ui_MainWindow
from SendReceive import filename2, filename1

import threading  # 导入线程模块
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QTimer, QThread, pyqtSignal
import time



fuploadfile_path = []
fdaqfile_path = []
config = []
time0 = 0


def getinformation(self):
    global fuploadfile_path,fdaqfile_path,config,time
    fuploadfile_path = filename1
    fdaqfile_path = filename2
    time = int(self.ui.lineEdit_16.text())

#设置fupload
def setfupload():
    global fuploadfile_path1
    port = '0x0001'
    cmd = 'fupload -e'+ port + fuploadfile_path
    subprocess.Popen(cmd, shell=True)

#设置fdaq
def setfdaq():
    global fdaqfile_path,time0
    t =  str(time0)
    cmd = 'fupload -X -T -t' + t + fdaqfile_path
    subprocess.Popen(cmd, shell=True)


class FDAQThread(QThread):
    signal = pyqtSignal()
    def __init__(self):
        super(FDAQThread, self).__init__()

    def run(self):
        setfdaq()
        #global fdaqfile_path, time0#time0 是设置的时间
        #print(threading.current_thread(), time.ctime(time.time()), 'run线程和时间')
        #t = str(time0)
        #cmd = 'fupload -X -T -t' + t + fdaqfile_path
        #subprocess.Popen(cmd, shell=True)
        self.signal.emit()

#检测felix采集数据的时间
def wait(self):
    self.ui.statusbar.showMessage('please wait',5000)
    time_start = time.time()
    while time_start+60 <= time.time():
        time_end = time.time()
    print('time cost', time_end - time_start, 's')

def threadfdaq(self):
    getinformation(self)
    setfupload()
    self.work = FDAQThread()
    self.work.signal.connect(wait)
    self.work.start()
    self.work.quit()
    self.work.wait()