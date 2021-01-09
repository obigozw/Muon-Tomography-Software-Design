import keyword
import sys
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.opengl as gl
import pyqtgraph as pg
import numpy as np


import threading  # 导入线程模块
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QTimer, QThread, pyqtSignal
import time
from SendReceive import filename1

i = 99

#Matplotlib绘图
class MyFigure(FigureCanvas):#Matplotlib绘图
    def __init__(self,width=5, height=4, dpi=100):
        #第一步：创建一个创建Figure
        self.fig = Figure(figsize=(width, height), dpi=dpi)

        plt.style.use('dark_background')
        plt.xlabel("x")  # x轴上的名字
        plt.ylabel("y")  # y轴上的名字
        #plt.zlabel("z")
        self.fig = plt.figure()
        #第二步：在父类中激活Figure窗口
        super(MyFigure,self).__init__(self.fig) #此句必不可少，否则不能显示图形
        #第三步：创建一个子图，用于绘制图形用，111表示子图编号，如matlab的subplot(1,1,1)
        self.ax = Axes3D(self.fig)
    def PL(self):
        print(threading.current_thread(), time.ctime(time.time()), 'matplotlib线程和时间')
        x, y, z = [], [], []
        a, b, c,d,e,f =[],[],[],[],[],[]
        with open('test1.txt') as file_object:
            lines = file_object.readlines()
            for line in lines:
                # print(line.rstrip())
                TX = line.split(',' or '\n')
                x.append(float(TX[0]))
                y.append(float(TX[1]))
                z.append(float(TX[2]))
        plt.xlabel("X")
        plt.ylabel("Y")
        #plt.colorbar()
        #plt.grid(True)
        l = len(x)
        #print(len(x))
        i = 0
        for i in range(l):
            if (-10000 < x[i] < 10000) and (-10000 < y[i] < 10000) and (-10000 < z[i] < 10000):
                a.append(float(x[i]))
                b.append(float(y[i]))
                c.append(float(z[i]))
        self.ax.scatter(a,b,c, s=10, facecolor='r', edgecolors='r',alpha=0.3)  # s点大小,alpha透明度
        for i in range(l):
            if (-1000 < x[i] < 1000) and (-1000 < y[i] < 1000) and (-1000 < z[i] < 1000):
                d.append(float(x[i]))
                e.append(float(y[i]))
                f.append(float(z[i]))
        self.ax.scatter(d,e,f, s=30, facecolor='yellow', edgecolors='yellow', alpha=1)  # s点大小,alpha透明度


#这样写是为了使用 QThread的方法产生新的线程
class PlotThread(QThread):
    signal = pyqtSignal()
    def __init__(self):
        super(PlotThread, self).__init__()

    def run(self):
        print(threading.current_thread(), time.ctime(time.time()), 'run线程和时间')
        #getdata()
        #processdata()
        #QThread.sleep(30)
        self.signal.emit()


#用QThread类方法的多线程，可以实现
def threadplot(self):
    self.work = PlotThread()
    self.work.signal.connect(lambda: pointplot(self))
    self.work.signal.connect(processdata)
    self.work.start()
    self.work.quit()
    self.work.wait()


#直接开启threading多线程，最简单，目前采用
def threadplot2(self):
    self = self
    t1 = threading.Thread(target=pointplot(self))  # 设置为线程
    t1.setDaemon(True)
    t1.start()  # 开启线程1
    name = 'hahh'
    t2 = threading.Thread(target=getdata, args= [name,])  # 设置为线程
    t2.setDaemon(True)
    t2.start()  # 开启线程2
    '''t3 = threading.Thread(target=self.F.PL)  # 设置为线程
    t3.setDaemon(True)
    t3.start()  # 开启线程3'''
    print(threading.current_thread(),time.ctime(time.time()),'Thread线程和时间')


#数据处理函数
def getdata(name):
    print(name)
    print(threading.current_thread(),time.ctime(time.time()),'getdata线程和时间')


def processdata():

    print(threading.current_thread(),time.ctime(time.time()),'processdata线程和时间')

#基础画图
def pyqtgraphplot0(self):#pyqtgraph绘图
    #W = gl.GLViewWidget()
    #W.opts['distance'] = 20
    #W.show()
    #self.ui.plot_widget = QtWidgets.QWidget()  # 实例化一个widget部件作为K线图部件
    #self.ui.plot_widget.setLayout(self.ui.gridLayout_10)  # 设置线图部件的布局层
    global d, phase,sp1, p,l,plot_plt2
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
    gx.translate(0, 500, 500)
    gy.setSize(1000,1000,1000)
    gy.setSpacing(100,100,100)
    gy.rotate(90, 1, 0, 0)
    gy.translate(500, 0, 500)
    gz.setSize(1000,1000,1000)
    gz.setSpacing(100,100,100)
    gz.translate(500,500,0)
    plot_plt1.addItem(gx)
    plot_plt2.addItem(gx)
    plot_plt3.addItem(gx)
    plot_plt1.addItem(gy)
    plot_plt2.addItem(gy)
    plot_plt3.addItem(gy)
    plot_plt1.addItem(gz)
    plot_plt2.addItem(gz)
    plot_plt3.addItem(gz)

    x, y, z = [], [], []
    filename = "".join(filename1)
    filename = 'test1.txt'
    with open(filename) as file_object:
        lines = file_object.readlines()
        for line in lines:
            # print(line.rstrip())
            TX = line.split(',' or '\n')
            x.append(float(TX[0]))
            y.append(float(TX[1]))
            z.append(float(TX[2]))
    l = len(x)
    #print(l)
    pos = np.empty((l, 3))
    po = list(zip(x, y, z))
    p = np.array(po)
    d = (p ** 2).sum(axis=1) ** 0.5
    phase = 0.
    size = np.empty((l))
    size[:] = 1
    color = np.empty((l, 4))
    color[:] = (1.0, 0.6, 0.0, 0.5)

    size[:] = self.ui.horizontalSlider.value()/10
    color[:] = (1.0, 0.6, 0.0, self.ui.horizontalScrollBar.value()/100)
    sp1 = gl.GLScatterPlotItem(pos=p, size=size, color=color, pxMode=False)

    #sp1 = gl.GLScatterPlotItem(pos=p, size=size, color=color, pxMode=False)
    #sp1.translate(-500, -500, -500)
    plot_plt1.addItem(sp1)
    plot_plt2.addItem(sp1)
    plot_plt3.addItem(sp1)
    '''t = QtCore.QTimer()
    t.timeout.connect(update)
    t.start(50)'''
    print(threading.currentThread(), time.ctime(time.time()), '1')

#新数据格式
def pyqtgraphplot(self):#pyqtgraph绘图
    #W = gl.GLViewWidget()
    #W.opts['distance'] = 20
    #W.show()
    #self.ui.plot_widget = QtWidgets.QWidget()  # 实例化一个widget部件作为K线图部件
    #self.ui.plot_widget.setLayout(self.ui.gridLayout_10)  # 设置线图部件的布局层
    global d, phase, sp1, p, l, plot_plt2       #变量在其他函数中需要使用
    plot_plt1 = gl.GLViewWidget()       # 实例化一个绘图部件
    plot_plt2 = gl.GLViewWidget()
    plot_plt3 = gl.GLViewWidget()
    #self.ui.plot_plt.showGrid(x=True, y=True)  # 显示图形网格
    self.ui.gridLayout_10.addWidget(plot_plt1,0,0,1,1)      #设置plot_plt1在图层中的位置
    self.ui.gridLayout_10.addWidget(plot_plt2,0,1,2,2)
    self.ui.gridLayout_10.addWidget(plot_plt3,1,0,1,1)
    # 添加绘图部件到线图部件的网格布局层
    # 将上述部件添加到布局层中
    #W.setWindowTitle('pyqtgraph example: GLScatterPlotItem')
    plot_plt1.opts['distance'] = 150
    plot_plt2.opts['distance'] = 200
    plot_plt3.opts['distance'] = 200
    plot_plt1.opts['elevation'] = 0
    plot_plt2.opts['elevation'] = 30
    plot_plt3.opts['elevation'] = -90
    gx = gl.GLGridItem()        #创建opengl网格事项gx
    gy = gl.GLGridItem()
    gz = gl.GLGridItem()
    gx.setSize(100,100,100)     #设置gx事项
    gx.setSpacing(10,10,10)
    gx.rotate(90, 0, 1, 0)
    gx.translate(0, 50, 50)
    gy.setSize(100,100,100)
    gy.setSpacing(10,10,10)
    gy.rotate(90, 1, 0, 0)
    gy.translate(50, 0, 50)
    gz.setSize(100,100,100)
    gz.setSpacing(10,10,10)
    gz.translate(50,50,0)
    plot_plt1.addItem(gx)       #将上面创建好的事项gx添加到实例plot_plt1中
    plot_plt2.addItem(gx)
    plot_plt3.addItem(gx)
    plot_plt1.addItem(gy)
    plot_plt2.addItem(gy)
    plot_plt3.addItem(gy)
    plot_plt1.addItem(gz)
    plot_plt2.addItem(gz)
    plot_plt3.addItem(gz)

    x, y, z, r = [], [], [], []     #三维坐标和空间角r
    #filename = 'poca_file_U_3GeV_Box10x10x10cm_Sphere5cm_Free.txt'
    filename = "".join(filename1)
    with open(filename) as file_object:     #读取txt文件内容
        lines = file_object.readlines()
        for line in lines:
            # print(line.rstrip())
            TX = line.split(' ' or '\n')
            x.append(float(TX[0]))
            y.append(float(TX[1]))
            z.append(float(TX[2]))
            r.append(float(TX[3]))
    l = len(r)
    print('数据个数：',l)
    r = np.array(r)
    mask1 = -0.02 > r           #空间角阈值
    mask2 = 0.02 < r
    mask = mask1 + mask2
    x = np.array(x)
    y = np.array(y)
    z = np.array(z)
    x = x[mask]                 #筛选符合的数据
    y = y[mask]
    z = z[mask]
    x = list(x)
    y = list(y)
    z = list(z)
    l = len(x)
    print(len(x),len(y),len(z))
    position = list(zip(x, y, z))       #压缩x，y，z为（x,y,z）
    p = np.array(position)
    d = (p ** 2).sum(axis=1) ** 0.5
    phase = 0.
    size = np.empty((l))        #size点大小
    size[:] = 1
    color = np.empty((l, 4))    #color点颜色
    color[:] = (1.0, 0.6, 0.0, 0.5)
    size[:] = self.ui.horizontalSlider.value()/10       #由控件得到参数
    color[:] = (1.0, 0.6, 0.0, self.ui.horizontalScrollBar.value()/100)     #由控件得到参数
    sp1 = gl.GLScatterPlotItem(pos=p, size=size, color=color, pxMode=False) #生成gl的散点图绘图

    plot_plt1.addItem(sp1)      #添加散点图到实例
    plot_plt2.addItem(sp1)
    plot_plt3.addItem(sp1)
    print(threading.currentThread(), time.ctime(time.time()), '1')
#movetoThread,暂时不采用,并不是在真的多线程
'''def threadplot(self):
    self.work1 = PlotThread()
    self.workthread1 = QThread()
    self.work1.moveToThread(self.workthread1)
    self.work1.signal.connect(self.getdata)
    self.workthread1.started.connect(self.work1.run)
    self.workthread1.start()
    self.workthread1.quit()
    self.workthread1.wait()'''

#刷新绘图
def pointplot(self):
    self.ui.progressBar.setValue(0)
    global d,sp1, phase, p
    #plot_plt1.items.remove(sp1)  # 移除上一次的绘图
    plot_plt2.items.remove(sp1)  # 移除上一次的绘图
    #plot_plt3.items.remove(sp1)#移除上一次的绘图
    size = np.empty(l)
    color = np.empty((l, 4))
    size[:] = self.ui.horizontalSlider.value()/10
    color[:] = (1.0, 0.6, 0.0, self.ui.horizontalScrollBar.value()/100)
    sp1 = gl.GLScatterPlotItem(pos=p, size=size, color=color, pxMode=False)
    #sp1.translate(-500, -500, -500)
    #plot_plt1.addItem(sp1)
    plot_plt2.addItem(sp1)
    #plot_plt3.addItem(sp1)
    self.ui.progressBar.setValue(100)
    #self.ui.label_40.setText(a)
    print(threading.current_thread(), time.ctime(time.time()), 'PP线程和时间')

def pyqtgraphplot1(self):
    global d, phase, sp1, p, l, plot_plt2
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

    x, y, z, r, tf = [], [], [], [], []
    # filename = 'poca_file_U_3GeV_Box10x10x10cm_Sphere5cm_Free.txt'
    filename = "".join(filename1)
    with open(filename) as file_object:
        lines = file_object.readlines()
        for line in lines:
            # print(line.rstrip())
            TX = line.split(' ' or '\n')
            x.append(float(TX[0]))
            y.append(float(TX[1]))
            z.append(float(TX[2]))
            r.append(float(TX[3]))
    l = len(r)
    print(l)
    r = np.array(r)
    tf = np.array(tf)
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
    l = len(x)
    print(len(x), len(y), len(z))
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

    # sp1 = gl.GLScatterPlotItem(pos=p, size=size, color=color, pxMode=False)
    # sp1.translate(-500, -500, -500)
    plot_plt1.addItem(sp1)
    plot_plt2.addItem(sp1)
    plot_plt3.addItem(sp1)
    '''t = QtCore.QTimer()
    t.timeout.connect(update)
    t.start(50)'''
    print(threading.currentThread(), time.ctime(time.time()), '1')

#直方图
def histogramplot_all(self):

    plt1 = pg.PlotWidget()
    x, y, z, r, tf = [], [], [], [], []
    filename = "".join(filename1)
    with open(filename) as file_object:
        lines = file_object.readlines()
        for line in lines:
            TX = line.split(' ' or '\n')
            x.append(float(TX[0]))
            y.append(float(TX[1]))
            z.append(float(TX[2]))
            r.append(float(TX[3]))          #第四列数据空间角
            tf.append(int(TX[6]))           #tf是第七列数据

    tf = np.array(tf)
    mask = 0 < tf                           #第七列非0，筛选对应的xyz
    r = np.array(r)
    r = r[mask]
    xspace = self.ui.doubleSpinBox.value()  #横坐标间隔bin
    min = self.ui.doubleSpinBox_2.value()
    max = self.ui.doubleSpinBox_3.value()
    xnumber = int((max-min)/xspace)
    y, x = np.histogram(r, bins=np.linspace(min, max, xnumber+1))#点的数量 = xnumber+1
    g = pg.PlotCurveItem(x, y, pen='y', stepMode=True, fillLevel=0, brush=(255,153,0,250))
    plt1.addItem(g)
    self.ui.gridLayout_11.addWidget(plt1,0,0,1,1)   #添加进图层



def histogramplot_x(self):

    pltx = pg.PlotWidget()
    x, y, z, r, tf = [], [], [], [], []
    filename = "".join(filename1)
    with open(filename) as file_object:
        lines = file_object.readlines()
        for line in lines:
            # print(line.rstrip())
            TX = line.split(' ' or '\n')
            x.append(float(TX[0]))
            y.append(float(TX[1]))
            z.append(float(TX[2]))
            r.append(float(TX[4]))          #第5列数据X平面映射
            tf.append(int(TX[6]))
    tf = np.array(tf)
    mask = 0 < tf  # 第七列非0，筛选对应的xyz
    r = np.array(r)
    r = r[mask]
    xspace = self.ui.doubleSpinBox_6.value()
    min = self.ui.doubleSpinBox_4.value()
    max = self.ui.doubleSpinBox_5.value()
    xnumber = int((max-min)/xspace)
    y, x = np.histogram(r, bins=np.linspace(min, max, xnumber+1))#点的数量 = xnumber+1
    g = pg.PlotCurveItem(x, y, pen='y', stepMode=True, fillLevel=0, brush=(255,153,0,250))
    pltx.addItem(g)
    self.ui.gridLayout_13.addWidget(pltx,0,0,1,1)   #添加进图层

def histogramplot_y(self):

    plty = pg.PlotWidget()
    x, y, z, r, tf = [], [], [], [], []
    filename = "".join(filename1)
    with open(filename) as file_object:
        lines = file_object.readlines()
        for line in lines:
            # print(line.rstrip())
            TX = line.split(' ' or '\n')
            x.append(float(TX[0]))
            y.append(float(TX[1]))
            z.append(float(TX[2]))
            r.append(float(TX[5]))          #第六列数据Y平面映射
            tf.append(int(TX[6]))
    tf = np.array(tf)
    mask = 0 < tf  # 第七列非0，筛选对应的xyz
    r = np.array(r)
    r = r[mask]
    xspace = self.ui.doubleSpinBox_9.value()
    min = self.ui.doubleSpinBox_7.value()
    max = self.ui.doubleSpinBox_8.value()
    xnumber = int((max-min)/xspace)
    y, x = np.histogram(r, bins=np.linspace(min, max, xnumber+1))#点的数量 = xnumber+1
    g = pg.PlotCurveItem(x, y, pen='y', stepMode=True, fillLevel=0, brush=(255,153,0,250))
    plty.addItem(g)
    self.ui.gridLayout_16.addWidget(plty,0,0,1,1)   #添加进图层


def histogramplot_sin(self):

    pltsin = pg.PlotWidget()
    x, y, z, r, tf = [], [], [], [], []
    filename = "".join(filename1)
    with open(filename) as file_object:
        lines = file_object.readlines()
        for line in lines:
            TX = line.split(' ' or '\n')
            x.append(float(TX[0]))
            y.append(float(TX[1]))
            z.append(float(TX[2]))
            r.append(float(TX[3]))
            tf.append(int(TX[6]))
    tf = np.array(tf)
    mask = 0 < tf  # 第七列非0，筛选对应的xyz
    r = np.array(r)
    r = r[mask]

    xspace = self.ui.doubleSpinBox_11.value()
    min = self.ui.doubleSpinBox_12.value()
    max = self.ui.doubleSpinBox_10.value()
    xnumber = int((max-min)/xspace)

    i =0
    bin_value, bin_edge = np.histogram(r, bins=np.linspace(min, max, xnumber+1))
    bin_center = np.zeros(len(bin_value)+1)
    bin_center[-1] = max
    for i in range(0,len(bin_value)):
        bin_center[i] = (bin_edge[i] + bin_edge[i+1]) / 2
        bin_value[i] = bin_value[i] / abs(np.sin(bin_center[i]))
    #y, x = np.histogram(r, bins=np.linspace(min, max, xnumber+1))#点的数量 = xnumber+1
    print(len(r))
    g = pg.PlotCurveItem(bin_center, bin_value, pen='y', stepMode=True, fillLevel=0, brush=(255,153,0,250))
    pltsin.addItem(g)
    ##下方注释掉的是拟合最优一元高斯曲线
    '''mu = np.mean(r)
    sigma = np.std(r)
    y = norm.pdf(bin_center, mu, sigma)  # 拟合一条最佳正态分布曲线y
    print(len(r))
    print(sigma)
    print(mu)
    print(y)
    print(len(y))


    bin_ccenter = np.zeros(len(bin_value))
    for i in range(0,len(bin_value)):
        bin_ccenter[i] = (bin_edge[i] + bin_edge[i+1]) / 2
    mu = np.mean(r)
    sigma = np.std(r)
    q = pg.PlotDataItem(bin_edge,y)
    pltsin.addItem(q)'''
    #plt1.plot(x, y, stepMode=True, fillLevel=1, brush=(0,0,255,150))
    self.ui.gridLayout_20.addWidget(pltsin,0,0,1,1)


'''def PP(self):#pyqtgraph绘图
    global d,sp1, phase, p
    plot_plt2.items.remove(sp1)
    size = np.empty((l))
    color = np.empty((l, 4))
    size[:] = self.ui.horizontalSlider.value()/10
    color[:] = (1.0, 0.6, 0.0, self.ui.horizontalScrollBar.value()/100)
    sp1 = gl.GLScatterPlotItem(pos=p, size=size, color=color, pxMode=False)
    #sp1.translate(-500, -500, -500)
    plot_plt2.addItem(sp1)'''

'''def update():
    global phase, d, sp1
    print(d)
    s = -np.cos(d * 2 + phase)
    color = np.empty((len(d), 4), dtype=np.float32)
    color[:, 3] = np.clip(s * 0.1, 0, 1)
    color[:, 0] = np.clip(s * 3.0, 0, 1)
    color[:, 1] = np.clip(s * 1.0, 0, 1)
    color[:, 2] = np.clip(s ** 3, 0, 1)
    sp1.setData(color=color)
    phase -= 0.1
'''





#matplotlib画图
def PL(self):
    print(keyword.kwlist)
    x, y, z = [], [], []
    with open('test1.txt') as file_object:
        lines = file_object.readlines()
        for line in lines:
            # print(line.rstrip())
            TX = line.split(',' or '\n')
            x.append(float(TX[0]))
            y.append(float(TX[1]))
            z.append(float(TX[2]))

    fig = plt.figure()
    ax = Axes3D(fig)
    # ax = fig.add_subplot(111, projection='3d')
    ax.scatter(x, y, z)
    self.ax.scatter(x[i], y[i], z[i], s=30, facecolor='#ffa02f', edgecolors='#0f0f0f', alpha=0.5)  # s点大小,alpha透明度
    plt.show()



'''
data = np.random.randint(100,500,(3,4,4))
print(x[0])
x,y,z = data[0],data[1],data[2]
print(data)
fig = plt.figure()
ax1 = fig.add_subplot(121,projection='3d')
ax1.plot_surface(x,y,z,cmap=plt.cm.winter,rstride=1,cstride=1) /# rstride和cstride是隔几行几列取一个数字，代表曲面的稀疏度
ax2 = fig.add_subplot(122,projection='3d')
ax2.plot_surface(x,y,z,cmap=plt.cm.winter,rstride=100,cstride=100)
plt.show()
'''

'''
def f(x, y):
    return np.sin(np.sqrt(x ** 2 + y ** 2))
#x = np.linspace(-6,6,30)
#y = np.linspace(-6,6,30)
X, Y = np.meshgrid(x, y)

Z,Z = np.meshgrid(z,z)


fig = plt.figure()
ax = plt.axes(projection='3d')
ax.contour3D(X, Y, Z, 50)
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')
plt.show()
'''

'''
length = len(y)
plt.figure(2)
plt.plot(x, y, 'rx')
plt.xlabel('USTC,000s')
plt.ylabel('USTC,000s')
plt.show()#让绘制的图像在屏幕上显示出来
'''

'''
X,Y = [],[]
with open('test1.txt', 'r') as f:#1
    lines = f.readlines()#2
    for line in lines:#3
        value = [float(s) for s in line.split()]#4
        X.append(value[0])#5
        Y.append(value[1])

print(X)
print(Y)

plt.plot(X, Y)
plt.show()
'''