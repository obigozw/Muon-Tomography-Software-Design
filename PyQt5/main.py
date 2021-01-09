import sys
from Muon_UI import Ui_MainWindow
from Login2 import  Ui_Dialog
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QMainWindow, QGridLayout,QWidget,QApplication
from PyQt5.QtWidgets import QDialog
import struct
import os
import threading
from PyQt5.QtCore import QThread
import _thread

from PyQt5 import uic
#from PyQt5.QtGui import QIcon
from function_Demo import Tell, findhelp
from SendReceive import *
from Plot import *
from createdat import fdaq_changename
import ctypes
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid") #显示任务栏图标

#刷新界面UI，可以不用
class Runthread(QtCore.QThread):
    #  通过类成员对象定义信号对象
    _signal = pyqtSignal(str)

    def __init__(self):
        super(Runthread, self).__init__()

    def __del__(self):
        self.wait()

    def run(self):
        for i in range(100):
            time.sleep(0.1)
            self._signal.emit(str(i))  # 注意这里与_signal = pyqtSignal(str)中的类型相同
            print(threading.current_thread(), time.ctime(time.time()), 'run时间')

#登录窗口
class Log(QWidget):
    def __init__(self, parent=None):#初始化
        super(Log, self).__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

    def accept(self):#登录界面OK按钮槽设置
        username = self.ui.lineEdit_username.text()
        password = self.ui.lineEdit_password.text()
        if password == '1':#密码规定
            print('Right')
            self.close()
            my.show()#主窗口显示
        else:
               self.ui.textBrowser.setText('Wrong Password: Please try again')

    def reject(self):
        sys.exit(app.exec_())

#主窗口
class MyWindow(QMainWindow):
    def __init__(self, parent=None):
        #super(MyWindow, self).__init__(parent)
        QMainWindow.__init__(self, parent)
        self.ui = Ui_MainWindow() #uic.loadUi("Micro1.ui")
        self.ui.setupUi(self)
        #self.ui.show()
        self.ui.pushButton_3.clicked.connect(self.Tell)#不含参数Tell
        self.ui.pushButton_5.clicked.connect(lambda: self.ChooseFileSend(self.ui.lineEdit_14))#lambda表达式用于传递参数：lineEdit_14
        self.ui.pushButton_6.clicked.connect(lambda: self.ChooseFileSave(self.ui.lineEdit_15))
        self.ui.pushButton_10.clicked.connect(lambda: self.ChooseFileSend(self.ui.lineEdit_17))#lambda表达式方便一个函数调用多个部件
        #self.F = MyFigure(width=3, height=2, dpi=100)
        #self.w = gl.GLViewWidget()
        self.ui.pushButton_11.clicked.connect(self.basicplot)
        self.ui.pushButton_11.clicked.connect(self.histogram_plotall)
        self.ui.pushButton_11.clicked.connect(self.histogram_plotx)
        self.ui.pushButton_11.clicked.connect(self.histogram_ploty)
        self.ui.pushButton_11.clicked.connect(self.histogram_plotsin)
        self.ui.pushButton_14.clicked.connect(self.histogram_plotall)
        self.ui.pushButton_15.clicked.connect(self.histogram_plotx)
        self.ui.pushButton_16.clicked.connect(self.histogram_ploty)
        self.ui.pushButton_17.clicked.connect(self.histogram_plotsin)
        self.ui.pushButton_8.clicked.connect(self.start_login)
        self.ui.pushButton_8.clicked.connect(self.fdaq)
        #self.ui.pushButton_13.clicked.connect(self.PP)
        self.ui.pushButton_13.clicked.connect(self.thread_plot)


        self.ui.actioncontext_help.triggered.connect(self.findhelp)#连接网页范例
        #self.F.PL()
        #self.ui.pushButton_11.clicked.connect(self.F.PL)
        # 第六步：在GUI的groupBox中创建一个布局，用于添加MyFigure类的实例（即图形）后其他部件。
        #self.ui.gridlayout_9 = QGridLayout(self.ui.groupBox_10)  # 继承容器groupBox
        #self.ui.gridLayout_9.addWidget(self.F, 0, 0, 1, 1)
        self.t4 = None


    Tell = Tell#声明之后可以用self.Tell加载ui，：self.ui.xxxxx
    #PL = MyFigure.PL             matplotlib方法，现在已经放弃
    ChooseFileSend = SendChooseFile     #选择文档
    ChooseFileSave = ReceiveChooseFile  #保存文档
    thread_plot = threadplot            #多线程画图
    PP = pointplot                      #画完散点图之后调整图像
    histogram_plotall = histogramplot_all   #空间角直方图
    histogram_plotx = histogramplot_x       #X平面直方图
    histogram_ploty = histogramplot_y       #Y平面直方图
    histogram_plotsin = histogramplot_sin   #空间角除以sin直方图
    basicplot = pyqtgraphplot               #基础散点图画图
    fdaq = fdaq_changename                  #产生dat-txt-图像的验证流程
    findhelp = findhelp

    ##下方是次线程UI刷新的例子，注意，主线程time.sleep会影响到控件progressBar_2的显示
    def start_login(self):
        # 创建线程
        self.thread = Runthread()
        # 连接信号
        self.thread._signal.connect(self.call_backlog)  # 进程连接回传到GUI的事件
        # 开始线程
        self.thread.start()

    def call_backlog(self, msg):
        self.ui.progressBar_2.setValue(int(msg))  # 将线程的参数传入进度条
'''
    def writefile(self, time0, cycle):
        x = 11
        y = 12
        z = 13
        a = 0.11111111111
        for i in range(cycle, time0):
            name = ''.join(filename2)
            rename = list(name)
            rename[-5] = str(i)
            name = ''.join(rename)
            with open(name, 'wb') as f:
                s = struct.pack('iiid', x, y, z, a)  # i是整数，d是double精度
                f.write(s)
                x += x
                y += y
                z += z
                time.sleep(10)  # 每十秒生成一个dat文件
                print(threading.current_thread(), time.ctime(time.time()), '线程1')
        f = open(name, 'rb')
        cont = f.read()
        cont1 = struct.unpack('iiid', cont)
        f.close()

    # dat转txt文件的线程
    def dattotxt(self, time0=3, cycle=0):
        for i in range(cycle, time0):
            name = ''.join(filename2)
            rename = list(name)
            rename[-5] = str(i)
            name = ''.join(rename)
            time.sleep(11)
            with open(name, 'rb') as datfile:
                data0 = datfile.read()
                data = struct.unpack('iiid', data0)
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

    def alldatafile(self, time0=3, cycle=0):
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
            print('总数据个数: ', len(r))
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
            # l = len(x)
            print('有效数据个数： ', len(x), len(y), len(z))
            pos = np.empty((l, 3))
            po = list(zip(x, y, z))
            p = np.array(po)
            d = (p ** 2).sum(axis=1) ** 0.5
            phase = 0.
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
            print(len(R), 'R长度')
            print(len(r), 'r长度')
            if len(r) == len(R):
                print('进入=')
                for i in range(0, 150):
                    QApplication.processEvents()
                    time.sleep(0.1)
                timebar += 1

            elif len(R) > len(r):
                print('进入>')
                plot_plt2.items.remove(sp1)
                timebar = 0
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
                # d = (p ** 2).sum(axis=1) ** 0.5
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

    def plottxt0(self,msg):
        self.ui.progressBar_2.setValue(int(msg))

    def fdaq_changename(self):
        name = filename2
        time0 = int(self.ui.lineEdit_16.text())
        cycle = int(self.ui.lineEdit_18.text())
        t1 = threading.Thread(target=self.writefile, args=[time0, cycle, ])  # 写dat线程
        t1.setDaemon(True)
        t1.start()
        t2 = threading.Thread(target=self.dattotxt, args=[time0, cycle, ])  # dat-txt线程
        t2.setDaemon(True)
        t2.start()
        t3 = threading.Thread(target=self.alldatafile, args=[time0, cycle, ])  # dat-txt线程
        t3.setDaemon(True)
        t3.start()

        print('over')
        print(threading.current_thread(), time.ctime(time.time()), '主线程和时间')

    def stop():
        print('stop')



    def PPP(self):#绘图
        #W = gl.GLViewWidget()
        #W.opts['distance'] = 20
        #W.show()
        #self.ui.plot_widget = QtWidgets.QWidget()  # 实例化一个widget部件作为K线图部件
        #self.ui.plot_widget.setLayout(self.ui.gridLayout_10)  # 设置线图部件的布局层
        plot_plt1 = gl.GLViewWidget()  # 实例化一个绘图部件
        plot_plt2 = gl.GLViewWidget()
        plot_plt3 = gl.GLViewWidget()
        #self.ui.plot_plt.showGrid(x=True, y=True)  # 显示图形网格
        self.ui.gridLayout_10.addWidget(plot_plt1,0,0,1,1)
        self.ui.gridLayout_10.addWidget(plot_plt2,0,1,2,2)
        self.ui.gridLayout_10.addWidget(plot_plt3,1,0,1,1)
        # 添加绘图部件到线图部件的网格布局层
        # 将上述部件添加到布局层中
        #W.setWindowTitle('pyqtgraph example: GLScatterPlotItem')
        plot_plt1.opts['distance'] = 1500
        plot_plt2.opts['distance'] = 2000
        plot_plt3.opts['distance'] = 2000
        plot_plt1.opts['elevation'] = 0
        plot_plt2.opts['elevation'] = 30
        plot_plt3.opts['elevation'] = -90
        gx = gl.GLGridItem()
        gy = gl.GLGridItem()
        gz = gl.GLGridItem()

        gx.setSize(1000,1000,1000)
        gx.setSpacing(100,100,100)
        gx.rotate(90, 0, 1, 0)
        gx.translate(-500, 0, 0)
        gy.setSize(1000,1000,1000)
        gy.setSpacing(100,100,100)
        gy.rotate(90, 1, 0, 0)
        gy.translate(0, -500, 0)
        gz.setSize(1000,1000,1000)
        gz.setSpacing(100,100,100)
        gz.translate(0,0,-500)

        plot_plt1.addItem(gx)
        plot_plt2.addItem(gx)
        plot_plt3.addItem(gx)
        plot_plt1.addItem(gy)
        plot_plt2.addItem(gy)
        plot_plt3.addItem(gy)
        plot_plt1.addItem(gz)
        plot_plt2.addItem(gz)
        plot_plt3.addItem(gz)

        ##
        ##  First example is a set of points with pxMode=False
        ##  These demonstrate the ability to have points with real size down to a very small scale
        ##

        x, y, z = [], [], []
        with open('test1.txt') as file_object:
            lines = file_object.readlines()
            for line in lines:
                # print(line.rstrip())
                TX = line.split(',' or '\n')
                x.append(float(TX[0]))
                y.append(float(TX[1]))
                z.append(float(TX[2]))
        l = len(x)
        print(l)
        pos = np.empty((l, 3))
        po = list(zip(x, y, z))
        p = np.array(po)
        size = np.empty((l))
        size[:] = 1
        color = np.empty((l, 4))
        color[:] = (1.0, 0.6, 0.0, 0.5)
        sp1 = gl.GLScatterPlotItem(pos=p, size=size, color=color, pxMode=False)
        sp1.translate(-500, -500, -500)
        plot_plt1.addItem(sp1)
        plot_plt2.addItem(sp1)
        plot_plt3.addItem(sp1)


    def Pl(self):
        print(keyword.kwlist)
        print(plt.style.available)
        x, y, z = [], [], []
        with open('test1.txt') as file_object:
            lines = file_object.readlines()
            for line in lines:
                # print(line.rstrip())
                TX = line.split(',' or '\n')
                x.append(float(TX[0]))
                y.append(float(TX[1]))
                z.append(float(TX[2]))
        plt.xlabel("x")  # x轴上的名字
        plt.ylabel("y")  # y轴上的名字
        self.F.ax.scatter(x, y, z, facecolor = '#ffa02f', edgecolors = '#0f0f0f')




    def Tell(self):     #一个槽，在Micro1.py加也可以
            a = 'ss'
            self.lineEdit_13.setText(a)
'''

if __name__ == '__main__': #可以使用，最简单的图标设置方式
    app = QtWidgets.QApplication(sys.argv)
    my = MyWindow()
    log = Log()
    app.setWindowIcon(QtGui.QIcon('25.ico'))    #设置图标
    name = '中国科学技术大学'
    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap("25.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)    #图标默认需在项目目录下
    my.setWindowIcon(icon)
    #mywindow.setWindowIcon('F:\Pycharm\projects\myICON.ico')
    my.setWindowTitle(name)
    #my.show()              #主界面显示
    log.show()              #登陆界面显示，如果不需要登陆界面请注释掉这一行，并将上一行解除注释
    sys.exit(app.exec_())

'''
if __name__ == '__main__': #图标和标题设,但是功能无法实现
    # import sys
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = QtWidgets.QMainWindow()
    my = Ui_MainWindow()
    my.setupUi(mainWindow)

    #app.setWindowIcon(QtGui.QIcon('28.ico'))  # 设置图标

    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap("28.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
    mainWindow.setWindowIcon(icon)
    # mywindow.setWindowIcon('F:\Pycharm\projects\myICON.ico')
    mainWindow.setWindowTitle("USTC_fel==514")
    mainWindow.show()

    sys.exit(app.exec_())
'''