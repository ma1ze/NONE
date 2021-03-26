import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from random import randint
from PyQt5 import QtCore,QtGui,QtWidgets
from PyQt5.QtWidgets import QApplication,QLabel,QWidget,QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap,QPalette
import pyqtgraph as pg
import traceback
import psutil
from PyQt5.QtCore import QThread, pyqtSignal, QDateTime, QObject
from PyQt5.QtWidgets import QApplication, QDialog, QLineEdit, QLabel
import time
import sys

# 定义使用到的逻辑判断值
if_areaDivideInRect = False
if_rectChosen = False
if_areaDivideConfirm = False

rects_list = [[]for i in range(4)] # 4xN的数组，列自上到下分别为x,y,wight,height
num_area = 0
tag_list = [[]for i in range(2)] # 2xN的数组，列自上到下分别为ID和物理意义
num_tag = 0
label_area = ""
tag_area = ""

## 用来区分方块的颜色
test_color = []

test_color.append(QColor(100,140,30))
test_color.append(QColor(0,140,30))
test_color.append(QColor(100,0,30))
test_color.append(QColor(100,255,30))


# 待修改，测试用
class Point:
    def __init__(self,u=0,v=0):
        self.U = u
        self.V = v

point1 = Point(0,0)
point2 = Point(0,0)

class interface(QWidget):
    def __init__(self):
        super().__init__()
        # self.rects_list = []  # 存放划分完成的矩形区域
        self.init_interface()
        self.timer_start()
        self.label_area = QLabel(self)
        self.label_area.setGeometry(50, 650, 200, 40)

    def init_interface(self):

        self.setWindowTitle("显示界面")
        self.resize(840, 840) #[840,594]显示纸张区域对应的识别图，其余区域显示已经设定完成的信息
        self.setFixedSize(840, 840)
        self.init_label()
        self.move(300, 100)
        self.show()


    def init_label(self):
        self.label1 = QLabel(self)
        self.label2 = QLabel(self)
        self.label3 = QLabel(self)
        self.label4 = QLabel(self)

        self.label1.setText("已经划分好的区域:")
        self.label2.setText("已经标记好的tag:")
        self.label1.setGeometry(50, 600, 200, 40)
        self.label2.setGeometry(500, 600, 200, 40)
        self.label3.setGeometry(50, 650, 400, 200)
        self.label4.setGeometry(500, 650, 400, 200)

    # def get_Ifo_input(self,):
        # for rectangle in self.rects_list:
        #     self.areaText = self.areaText +"\n"+str(i+1)+". "+str(rectangle)
        #     i=i+1
        # self.label3.setText(self.areaText)
        # self.label4.setText(self.tagText)

    def timer_start(self):
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.get_points_info)

        self.timer.start(1000)

    def get_points_info(self):
        self.Point1 = point1
        self.Point2 = point2
        global if_rectChosen
        # 模拟随时间变化改变的位置坐标
        if(if_areaDivideInRect==True):
            self.Point1.U = randint(1, 840)
            self.Point2.U = randint(1, 840)
            self.Point1.V = randint(1, 594)
            self.Point2.V = randint(1, 594)
            # self.update()

        if(if_rectChosen == True):
            self.shape = QRect()
            self.shape.setX(min(point1.U,point2.U))
            self.shape.setY(min(point1.V,point2.V))
            self.shape.setWidth(abs(point2.U - point1.U))
            self.shape.setHeight(abs(point1.V-point2.V))
            global if_input_area,rects_list, label_area ,num_area
            rects_list[0].append(self.shape.x())
            rects_list[1].append(self.shape.y())
            rects_list[2].append(self.shape.width())
            rects_list[3].append(self.shape.height())
            num_area = num_area + 1
            label_area = label_area +"\n" + "Rect: " + "[ "+str(self.shape.x())+","+str(self.shape.y())+" ] - "+"[ "+str(self.shape.x()+self.shape.width())+","+str(self.shape.y()+self.shape.height())+" ]"
            self.label3.setText(label_area)
            if_rectChosen = False
        self.update()

    def paintEvent(self,e):
        qp = QPainter()
        qp.begin(self)
        self.drawAllArea(qp)
        self.drawLines(qp)
        # if if_areaDivideConfirm==True:

        qp.end()

    def drawAllArea(self,qp):
        global rects_list,test_color
        for i in range(num_area):
            brush = QBrush(Qt.SolidPattern)
            brush.setColor(test_color[i])
            qp.setBrush(brush)
            qp.drawRect(rects_list[0][i],rects_list[1][i],rects_list[2][i],rects_list[3][i])


    def drawLines(self,qp):
        brush = QBrush(Qt.SolidPattern)

        brush.setColor(QColor(0, 200, 100,20))
        qp.setBrush(brush)
        qp.drawRect(min(point1.U,point2.U),min(point1.V,point2.V), abs(point2.U - point1.U), abs(point1.V-point2.V))

class menu(QWidget):
    def __init__(self):
        super().__init__()
        self.init_Menu()

    def init_Menu(self):
        self.setWindowTitle("控制窗口")
        self.resize(400, 400)
        self.setFixedSize(400, 400)
        self.move(1140, 100)
        self.init_StartPage()
        self.init_AreaDividePage()
        self.init_TagSetPage()
        self.init_squareSetPage()
        self.init_taskChoosePage()
        self.start_buttonPush.clicked.connect(self.on_startButton_clicked)
        self.nextStepToTag_buttonPush.clicked.connect(self.on_nextStepToTagButton_clicked)
        self.square_buttonPush.clicked.connect(self.on_squareButton_clicked)
        self.squareSetConfirm_buttonPush.clicked.connect(self.on_squareSetConfirmButton_clicked)
        self.nextStepToTask_buttonPush.clicked.connect(self.on_nextStepToTaskChoose_clicked)
        self.show()

    # 按下界面中的开始按钮后，识别四个点的标记属性设定地图类型
    def on_startButton_clicked(self):
        self.startFrame.setVisible(False)
        self.areaDivideFrame.setVisible(True)
        self.setWindowTitle("选择区域划分的图形")

    def on_squareButton_clicked(self):
        self.squareSetFrame.setVisible(True)
        self.areaDivideFrame.setVisible(False)
        self.setWindowTitle("选择长方形区域")
        global if_areaDivideInRect
        if_areaDivideInRect = True

    # 确认选择长方形的区域，需要两点的坐标分别记作(u1,v1)和(u2,v2)
    def on_squareSetConfirmButton_clicked(self):
        self.squareSetFrame.setVisible(False)
        self.areaDivideFrame.setVisible(True)
        self.setWindowTitle("选择区域划分的图形")
        global if_areaDivideInRect,if_rectChosen, if_input_area
        if_areaDivideInRect = False
        if_rectChosen = True
        if_input_area = True

    def on_nextStepToTagButton_clicked(self):
        self.areaDivideFrame.setVisible(False)
        self.tagSetFrame.setVisible(True)
        self.setWindowTitle("Tag标记")
        global if_areaDivideConfirm
        if_areaDivideConfirm = True

    def on_nextStepToTaskChoose_clicked(self):
        self.taskChooseFrame.setVisible(True)
        self.tagSetFrame.setVisible(False)
        self.setWindowTitle("任务选择")

    def init_StartPage(self):
        self.startFrame = QFrame(self)
        self.startVerticalLayout = QVBoxLayout(self.startFrame)
        self.start_buttonPush = QPushButton("开始")
        self.startVerticalLayout.addWidget(self.start_buttonPush)

    def init_AreaDividePage(self):
        self.areaDivideFrame = QFrame(self)
        self.areaDivideVerticalLayout = QVBoxLayout(self.areaDivideFrame)
        self.square_buttonPush = QPushButton("长方形")
        self.circle_buttonPush = QPushButton("圆形")
        self.triangle_buttonPush = QPushButton("三角形")
        self.nextStepToTag_buttonPush = QPushButton("结束区域划分")
        self.areaDivideVerticalLayout.addWidget(self.square_buttonPush)
        self.areaDivideVerticalLayout.addWidget(self.circle_buttonPush)
        self.areaDivideVerticalLayout.addWidget(self.triangle_buttonPush)
        self.areaDivideVerticalLayout.addWidget(self.nextStepToTag_buttonPush)
        self.areaDivideFrame.setVisible(False)

    def init_TagSetPage(self):
        self.tagSetFrame = QFrame(self)
        self.tagSetVerticalLayout = QVBoxLayout(self.tagSetFrame)
        self.nextStepToTask_buttonPush = QPushButton("结束tag标记")
        self.tagSetVerticalLayout.addWidget(self.nextStepToTask_buttonPush)
        self.tagSetFrame.setVisible(False)

    def init_squareSetPage(self):
        self.squareSetFrame = QFrame(self)
        self.squareSetVerticalLayout = QVBoxLayout(self.squareSetFrame)
        self.squareSetConfirm_buttonPush = QPushButton("确认长方形区域划分")
        self.squareSetVerticalLayout.addWidget(self.squareSetConfirm_buttonPush)
        self.squareSetFrame.setVisible(False)

    def init_taskChoosePage(self):
        self.taskChooseFrame = QFrame(self)
        self.taskChooseVerticalLayout = QVBoxLayout(self.taskChooseFrame)
        self.task1Choose_buttonPush = QPushButton("task1")
        self.task2Choose_buttonPush = QPushButton("task2")
        self.task3Choose_buttonPush = QPushButton("task3")
        self.taskChooseVerticalLayout.addWidget(self.task1Choose_buttonPush)
        self.taskChooseVerticalLayout.addWidget(self.task2Choose_buttonPush)
        self.taskChooseVerticalLayout.addWidget(self.task3Choose_buttonPush)
        self.taskChooseFrame.setVisible(False)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    interfaceWindow = interface()
    menuWindow = menu()
    sys.exit(app.exec_())
