import glob
import os
import sys
import subprocess
from PyQt6.QtGui import QImage, QPixmap,qRgb,QColor,QPainter,QBitmap,QPen
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QTextEdit, QPushButton,QMessageBox,QFileDialog,QListWidget
from ctypes import *
import numpy as np


lib:CDLL

pixel_white = 255
pixel_black = 0

py_data  = np.zeros((200,200),dtype=np.int )

py_l_data = np.zeros((200))
py_r_data = np.zeros((200))
py_s_data = np.zeros((200))

bmp_files:list

image_w =0
image_h = 0

image:QImage

imag_pixmap:QPixmap

dir_path:str
root_path:str
class MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("智能车图像上位机-ycc")
        
        self.dispos_label = QLabel(self)
        self.dispos_label.setGeometry(340,100,300,30)
        
        self.tips = QLabel(self)
        self.tips.setGeometry(350,80,800,30)
        self.tips.setText("图像数据uint8 Pixle[H][W]  左右边界uint8_t l_b[H] r_b[H]  回馈变量uint8_t reback_value[H]  函数void process_image()")
        
        
        self.vartips = QLabel(self)
        self.vartips.setGeometry(200,90,300,30)
        self.vartips.setText("返回的变量")
        
        self.file_lab = QLabel(self)
        self.file_lab.setGeometry(50,90,300,30)
        self.file_lab.setText("文件目录")
        
        self.image_label = QLabel(self)
        
        self.load_image("1.BMP")
        self.image_label.setGeometry(380, 150, image_w*4, image_h*4)
        self.image_label.mouseMoveEvent = self.on_mouse_move
        self.image_label.setMouseTracking(True)
        
       
        self.bianyi_edit = QTextEdit(self)
        self.bianyi_edit.setGeometry(620, 5, 300, 70)
        self.bianyi_edit.setText("待编译")
        
   
        self.filelist_list = QListWidget(self)
        self.filelist_list.setGeometry(20, 125, 150, 520)
        self.filelist_list.itemDoubleClicked.connect(self.choce_file)
        
        
        self.var_list = QListWidget(self)
        self.var_list.setGeometry(190, 125, 150, 520)
        
        
        # 创建输入框和按钮用于输入C语言代码
        self.code_edit = QTextEdit(self)
        self.code_edit.setGeometry(10, 10, 300, 90)
        self.code_edit.setText("代码编辑处")
        
        self.bianyi_button = QPushButton("编译", self)
        self.bianyi_button.setGeometry(340, 10, 60, 30)
        self.bianyi_button.clicked.connect(self.process_image)
        
        
        self.switch_button = QPushButton("黑白交换", self)
        self.switch_button.setGeometry(430, 40, 80, 30)
        self.switch_button.clicked.connect(self.swichcolor)
        
        self.choceDir_button = QPushButton("选择目录", self)
        self.choceDir_button.setGeometry(340, 40, 70, 30)
        self.choceDir_button.clicked.connect(self.open_folder_dialog)
        
        self.last_button = QPushButton("上一张", self)
        self.last_button.setGeometry(540, 10, 60, 30)
        self.last_button.clicked.connect(self.image_last)
        
        self.next_button = QPushButton("下一张", self)
        self.next_button.setGeometry(540, 40, 60, 30)
        self.next_button.clicked.connect(self.image_next)
        
        
        self.zixing_button = QPushButton("函数执行", self)
        self.zixing_button.setGeometry(430,10, 80, 30)
        self.zixing_button.clicked.connect(self.zixing)
        self.zixing_button.setEnabled(False)
        
    def swichcolor(self):
        global pixel_black,pixel_white
        if(pixel_black==255):
            pixel_black=0
            pixel_white=255
            self.tips.setText("当前黑0白255")
        else:
            pixel_black=255
            pixel_white=0
            self.tips.setText("当前黑255白0")
        self.choce_file()
        self.zixing()
        
    def choce_file(self):
        self.load_image(root_path+"\\"+self.filelist_list.currentItem().text())
        self.tips.setText("宽:"+str(image_w)+"高:"+str(image_h))
        
    def image_next(self):
        self.filelist_list.setCurrentRow(self.filelist_list.currentRow()+1)
        self.choce_file()
        self.zixing()
    
    def image_last(self):
        self.filelist_list.setCurrentRow(self.filelist_list.currentRow()-1)
        self.choce_file()
        

    def open_folder_dialog(self):
        # 创建文件夹选择对话框
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.FileMode.Directory)
        dialog.setOption(QFileDialog.Option.ShowDirsOnly)

        # 显示文件夹选择对话框
        if dialog.exec() == QFileDialog.DialogCode.Accepted:
            # 获取选择的文件夹路径
            global dir_path
            dir_path = dialog.selectedFiles()[0]
            self.tips.setText(dir_path)
            global bmp_files
            # 获取指定目录下的 BMP 文件列表
            bmp_files = glob.glob(os.path.join(dir_path, '*.bmp'))

            
            # # 遍历 BMP 文件列表，显示图像
            for bmp_file in bmp_files:
                # 读取 BMP 文件到 QImage 对象
                self.filelist_list.addItem(bmp_file.split('\\')[1])
                global root_path
                root_path = bmp_file.split('\\')[0]
            
            self.file_lab.setText("文件数量:"+str(len(bmp_files)))
        
        
    def on_mouse_move(self,event):
        # 获取当前鼠标所指的像素坐标
        pos = event.pos() - self.image_label.pos()
        x, y = int((pos.x()+380)/4), int((pos.y()+150)/4)
        value:int=0

        if(image.pixelIndex(x,y)==0):
            value=pixel_white
        else:
            value= pixel_black
            
        # 显示像素坐标
        self.dispos_label.setText("坐标: ({}, {}),值:{}".format(x, y,value))
        
        

        


    #显示数据
    def displaydata(self):




        myimage = imag_pixmap.toImage()
        
        painter = QPainter(myimage)
        color = QColor(255, 0, 0, 255)
        pen = QPen(QColor(color))
        
        painter.setPen(pen)
        
        self.var_list.clear()
        for i in range(image_h):
            x = py_l_data[i]
            y = i
            
            
            painter.drawImage(x,y,QImage(1,1,QImage.Format.Format_RGB32))
            
            x2 = py_r_data[i]
            y = i
            
            painter.drawImage(x2,y,QImage(1,1,QImage.Format.Format_RGB32))
            
            painter.drawImage(int((x2+x)/2),y,QImage(1,1,QImage.Format.Format_RGB32))
            
            self.var_list.addItem(str(py_s_data[i]))
            


        painter.end()
        pixmap = QPixmap.fromImage(myimage)
        self.image_label.setPixmap(pixmap.scaled( pixmap.width()*4,pixmap.height()*4))
        
        self.vartips.setText("变量总数:"+str(image_h))


    #图片数据给动态库
    def cuanzi(self):
        b_btr = cast(lib.Pixle,POINTER(c_uint8  *image_w  * image_h))
        for i in range(image_h):
            for j in range(image_w):
                # print(i,j)
                b_btr.contents[i][j]=py_data[i][j]
                 
                 
        print("传值成功,把数组传递给动态库图片数组")


    #执行动态库函数
    def zixing(self):
        self.cuanzi()
        
        process_image = lib.process_image
        process_image.restype = None
        process_image()
        print("执行动态库函数")

        global py_l_data,py_r_data,py_s_data
        data_ptr = cast(lib.l_b,POINTER(c_uint8 * image_h))
        data_ptr_r = cast(lib.r_b,POINTER(c_uint8 * image_h))
        data_ptr_data = cast(lib.reback_value,POINTER(c_uint8 * image_h))
        
        c_array =  np.ctypeslib.as_array(data_ptr.contents)
        c_array_r =  np.ctypeslib.as_array(data_ptr_r.contents)
        c_array_data =  np.ctypeslib.as_array(data_ptr_data.contents)
        
        # 将 c_array 中的值赋值给 py_array

        
        py_l_data = [int(c_array[i]) for i in range(image_h)]
        py_r_data = [int(c_array_r[i]) for i in range(image_h)]
        py_s_data = [int(c_array_data[i]) for i in range(image_h)]
        
        print("从动态库中读取边界信息值成功")
        
        self.displaydata()
        

    #加载图片
    def load_image(self, filename):
        # 从文件中加载图像
        global image
        print(239)
        image = QImage(filename)
        print(241)
        image = image.convertToFormat(QImage.Format.Format_Mono)
        
        global imag_pixmap,scaled_pixmap
        # 将图像显示在标签中
        imag_pixmap = QPixmap.fromImage(image)
        print(246)
        # 放大图像
        scaled_pixmap = imag_pixmap.scaled(imag_pixmap.width() * 4, imag_pixmap.height() * 4)
        
        global image_w,image_h
        image_w = image.width()
        image_h = image.height()
        print(25)
        self.image_label.setGeometry(380, 150, image_w*4, image_h*4)
        self.image_label.setPixmap(scaled_pixmap)
        print(256)
        
     
        global py_data,py_l_data,py_r_data,py_s_data
        py_data  = np.zeros((image_h,image_w),dtype=np.int )

        py_l_data = np.zeros((image_h))
        py_r_data = np.zeros((image_h))
        py_s_data = np.zeros((image_h))
        
        for y in range(image_h):
            for x in range(image_w):
                pixel_value = image.pixelIndex(x,y)
                if(pixel_value==0):
                    pixel_value=pixel_white
                else:
                    pixel_value = pixel_black
                py_data[y][x]=pixel_value
               # print(pixel_value)

            
    
    #编译
    def process_image(self):
        
        # 读取输入框中的代码
        code = self.code_edit.toPlainText()

        if(code == ""):
            self.bianyi_edit.setText("代码空")
            return
        # 编译代码
        with open("image.c", "w") as f:
            f.write(code)
            
        result = subprocess.run(["gcc", "-shared", "-fPIC", "-o", "image.so", "image.c"],capture_output=True,text=True)


        if result.returncode == 0:
            self.bianyi_edit.setText("编译成功")
            self.zixing_button.setEnabled(True)
            self.bianyi_button.setEnabled(False)
            

        else:
            print("编译失败，错误信息如下：")
            print(result.stderr)
            self.bianyi_edit.setText("编译失败，错误信息如下："+result.stderr)
        
        global lib
        try:
            # 加载C语言库并调用函数处理图像
            lib = CDLL("./image.so")
            
        except OSError:
        # 如果加载失败，打印错误信息并退出程序
            print("加载库失败")
            self.bianyi_edit.setText("加载库失败")
        return
    

if __name__ == '__main__':
    
    
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setGeometry(0,0,1000,600)
    window.show()
    
    sys.exit(app.exec())
