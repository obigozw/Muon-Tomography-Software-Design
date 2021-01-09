from SendReceive import filename2
import threading  # 导入线程模块
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QTimer, QThread, pyqtSignal,QObject
from PyQt5.QtWidgets import QApplication
import time

import os

import struct
import pyqtgraph.opengl as gl
import pyqtgraph as pg
import numpy as np


class ReadThread(QtCore.QThread):
    #  通过类成员对象定义信号对象
    signal = pyqtSignal(str)

    def __init__(self):
        super(ReadThread, self).__init__()

    def __del__(self):
        self.wait()

    def run(self):
        for i in range(100):
            time.sleep(0.2)
            self.signal.emit(str(i))  # 注意这里与_signal = pyqtSignal(str)中的类型相同
            print(threading.current_thread(), time.ctime(time.time()), 'run时间')


def fdaq_changename(self):
    name = filename2
    time0 = int(self.ui.lineEdit_16.text())#设置文件命的开始
    cycle = int(self.ui.lineEdit_18.text())#设置文件名的结束
    t1 = threading.Thread(target=writefile, args=[time0,cycle,])  # 写dat线程
    t1.setDaemon(True)
    t1.start()
    t2 = threading.Thread(target=dattotxt, args=[time0, cycle, ])  # dat-txt线程
    t2.setDaemon(True)
    t2.start()
    t3 = threading.Thread(target=alldatafile, args=[time0, cycle, ])  # dat-txt线程
    t3.setDaemon(True)
    t3.start()

    '''self.t4 = ReadThread()
    self.t4.signal.connect(lambda: self.plottxt0)  # 画图plottxt
    self.t4.start()
    self.t4.quit()
    self.t4.wait()'''
    plottxt(self)
    print('over')
    print(threading.current_thread(), time.ctime(time.time()), '主线程和时间')

def stop():
    print('stop')
#模仿fdaq创建dat文件
def writefile(time0 = 9,cycle = 0):
    x = 11
    y = 12
    z = 13
    a = 0.11111111111
    for i in range(cycle,time0):
        name = ''.join(filename2)
        rename = list(name)
        rename[-5] = str(i)
        name = ''.join(rename)
        with open(name,'wb') as f:
            s = struct.pack('iiid',x,y,z,a) #i是整数，d是double精度
            f.write(s)
            x += x
            y += y
            z += z
            time.sleep(10)#每十秒生成一个dat文件
            print(threading.current_thread(), time.ctime(time.time()), '线程1')
    f = open(name, 'rb')
    cont = f.read()
    cont1 = struct.unpack('iiid',cont)
    f.close()


#dat转txt文件的线程
def dattotxt(time0 = 9,cycle = 0):
    for i in range(cycle,time0):
        name = ''.join(filename2)
        rename = list(name)
        rename[-5] = str(i)
        name = ''.join(rename)
        time.sleep(11)
        with open(name, 'rb') as datfile:
            data0 = datfile.read()
            data = struct.unpack('iiid',data0)
            name = ''.join(filename2)
            rename = list(name)
            rename[-5] = str(i)
            rename[-3] = 't'
            rename[-2] = 'x'
            name = ''.join(rename)
            txtfile = open(name, 'a+')
            data1 = str(' '.join(map(str, data)))
            txtfile.write(data1)
            txtfile.close()
            print(threading.current_thread(), time.ctime(time.time()), '线程2')



def alldatafile(time0 = 9,cycle = 0):
    for i in range(cycle, time0):
        name = ''.join(filename2)
        rename = list(name)
        rename[-5] = str(i)
        rename[-3] = 't'
        rename[-2] = 'x'
        name = ''.join(rename)
        time.sleep(12)
        with open(name, 'r') as datfile:
            data = datfile.read()
            name = ''.join(filename2)
            rename = list(name)
            rename[-5] = 't'
            rename[-3] = 't'
            rename[-2] = 'x'
            name = ''.join(rename)
            txtfile = open(name, 'a+')
            txtfile.write(data + '\n')
            txtfile.close()
    print('over')

def plottxt0(self, msg):
    print('33333')
    self.ui.progressBar_2.setValue(int(msg))


def plottxt(self):
    plot_plt1 = gl.GLViewWidget()  # 实例化一个绘图部件
    plot_plt2 = gl.GLViewWidget()
    plot_plt3 = gl.GLViewWidget()
    # self.ui.plot_plt.showGrid(x=True, y=True)  # 显示图形网格
    self.ui.gridLayout_10.addWidget(plot_plt1, 0, 0, 1, 1)
    self.ui.gridLayout_10.addWidget(plot_plt2, 0, 1, 2, 2)
    self.ui.gridLayout_10.addWidget(plot_plt3, 1, 0, 1, 1)
    # 添加绘图部件到线图部件的网格布局层
    # 将上述部件添加到布局层中
    # W.setWindowTitle('pyqtgraph example: GLScatterPlotItem')
    plot_plt1.opts['distance'] = 150
    plot_plt2.opts['distance'] = 200
    plot_plt3.opts['distance'] = 200
    plot_plt1.opts['elevation'] = 0
    plot_plt2.opts['elevation'] = 30
    plot_plt3.opts['elevation'] = -90
    gx = gl.GLGridItem()
    gy = gl.GLGridItem()
    gz = gl.GLGridItem()
    gx.setSize(100, 100, 100)
    gx.setSpacing(10, 10, 10)
    gx.rotate(90, 0, 1, 0)
    gx.translate(0, 50, 50)
    gy.setSize(100, 100, 100)
    gy.setSpacing(10, 10, 10)
    gy.rotate(90, 1, 0, 0)
    gy.translate(50, 0, 50)
    gz.setSize(100, 100, 100)
    gz.setSpacing(10, 10, 10)
    gz.translate(50, 50, 0)
    plot_plt1.addItem(gx)
    plot_plt2.addItem(gx)
    plot_plt3.addItem(gx)
    plot_plt1.addItem(gy)
    plot_plt2.addItem(gy)
    plot_plt3.addItem(gy)
    plot_plt1.addItem(gz)
    plot_plt2.addItem(gz)
    plot_plt3.addItem(gz)
    name = ''.join(filename2)
    rename = list(name)
    rename[-5] = 't'
    rename[-3] = 't'
    rename[-2] = 'x'
    name = ''.join(rename)
    print(name)
    timebar = 0
    while not os.access(name, os.R_OK):
        print('no file')
        QApplication.processEvents()
        time.sleep(1)
    if os.access(name, os.F_OK):
        x, y, z, r = [], [], [], []
        with open(name) as file_object:
            lines = file_object.readlines()
            for line in lines:
                # print(line.rstrip())
                TX = line.split(' ' or '\n')
                x.append(float(TX[0]))
                y.append(float(TX[1]))
                z.append(float(TX[2]))
                r.append(float(TX[3]))
        l = len(r)
        print('总数据个数: ',len(r))
        r = np.array(r)
        mask1 = -0.02 > r
        mask2 = 0.02 < r
        mask = mask1 + mask2
        x = np.array(x)
        y = np.array(y)
        z = np.array(z)
        x = x[mask]
        y = y[mask]
        z = z[mask]
        x = list(x)
        y = list(y)
        z = list(z)
        #l = len(x)
        print('有效数据个数： ',len(x), len(y), len(z))
        pos = np.empty((l, 3))
        po = list(zip(x, y, z))
        p = np.array(po)
        size = np.empty((l))
        size[:] = 1
        color = np.empty((l, 4))
        color[:] = (1.0, 0.6, 0.0, 0.5)
        size[:] = self.ui.horizontalSlider.value() / 10
        color[:] = (1.0, 0.6, 0.0, self.ui.horizontalScrollBar.value() / 100)
        sp1 = gl.GLScatterPlotItem(pos=p, size=size, color=color, pxMode=False)
        plot_plt1.addItem(sp1)
        plot_plt2.addItem(sp1)
        plot_plt3.addItem(sp1)
        print(threading.currentThread(), time.ctime(time.time()), '3')
        QApplication.processEvents()

    while os.access(name, os.F_OK):
        X, Y, Z, R = [], [], [], []
        with open(name) as file_object:
            lines = file_object.readlines()
            for line in lines:
                # print(line.rstrip())
                TX = line.split(' ' or '\n')
                X.append(float(TX[0]))
                Y.append(float(TX[1]))
                Z.append(float(TX[2]))
                R.append(float(TX[3]))
        print(len(R),'R长度')
        print(len(r),'r长度')
        if len(r) == len(R):
            print('进入=')
            for i in range(0,1500):
                QApplication.processEvents()
                time.sleep(0.01)
            timebar +=1

        elif len(R) > len(r):
            print('进入>')
            plot_plt2.items.remove(sp1)
            timebar =0
            L = len(R)
            r = np.array(R)
            mask1 = -0.02 > r
            mask2 = 0.02 < r
            mask = mask1 + mask2
            X = np.array(X)
            Y = np.array(Y)
            Z = np.array(Z)
            X = X[mask]
            Y = Y[mask]
            Z = Z[mask]
            X = list(X)
            Y = list(Y)
            Z = list(Z)
            L = len(X)
            print('有效数据的个数： ', len(X), len(Y), len(Z))
            pos = np.empty((l, 3))
            po = list(zip(X, Y, Z))
            p = np.array(po)
            print(p)
            #d = (p ** 2).sum(axis=1) ** 0.5
            size = np.empty((L))
            size[:] = 1
            color = np.empty((L, 4))
            color[:] = (1.0, 0.6, 0.0, 0.5)
            size[:] = self.ui.horizontalSlider.value() / 10
            color[:] = (1.0, 0.6, 0.0, self.ui.horizontalScrollBar.value() / 100)
            sp1 = gl.GLScatterPlotItem(pos=p, size=size, color=color, pxMode=False)
            plot_plt1.addItem(sp1)
            plot_plt2.addItem(sp1)
            plot_plt3.addItem(sp1)
            print(threading.currentThread(), time.ctime(time.time()), '3')
            QApplication.processEvents()

        else:
            print('wrong')

        if timebar == 2:
            print('没了')
            break



'''直接使用师兄给的文件
filename2 = 'C:\\Users\\obigo\\Desktop\\fec_mpgd_ws_334w_al_20191211_0-0DD.dat'
filename1 = 'C:/Users/obigo/Desktop/222222.dat'
strb = '中国'
def writedat():
    i = 0
    with open(filename2,'rb') as fileobject:
        contents = fileobject.read()
        print(type(contents))
    with open(filename1, mode='wb', buffering=-1, encoding=None, errors=None, newline=None, closefd=True, opener=None) as fileobject:
        fileobject.write(contents)
    #f = open(filename2,'r')
    #f.close()

writedat()
'''