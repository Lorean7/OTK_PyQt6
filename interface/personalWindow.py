from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QGroupBox,
    QGridLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QFileDialog,
    QMessageBox,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from model.user import user

import os.path
# DB
from database.db import DB

#interface 
from interface.tableOrder import tableOrder
from interface.addOrderWindow import addOrderWindow



class personalWindow(QMainWindow):
    def __init__(self,parent):
        super().__init__()
        self.main_window = parent
        self.setWindowTitle('Личный кабинет')
        self.setCentralWidget(QWidget())
        self.resize(270,225)
        self.init_gui()

    def init_gui(self):
        self.main_grid = QGridLayout()
        #подгрузка картинок
        #pixmap = QPixmap("D:/python/app/img/3dwall13.JPG") 
        pixmap = QPixmap() 
        pixmap.loadFromData(user['avatar'])
        #создание автара
        self.avatar_picture = QLabel()
        self.avatar_picture.setPixmap(pixmap)
        self.avatar_picture.setScaledContents(True)
        self.avatar_picture.setMaximumSize(70,70)
        #кнопки
        self.btn_back = QPushButton('Выйти')
        self.btn_back.clicked.connect(lambda: self.back())
        self.btn_display_table = QPushButton('Просмотреть все заказы')
        self.btn_display_table.clicked.connect(lambda: self.display_table())
        self.btn_add_order = QPushButton('Добавить заказ')
        self.btn_add_order.clicked.connect(lambda: self.add_order())
        #основная сетка
        self.main_grid.addWidget(self.avatar_picture,0,0)
        self.main_grid.addWidget(QLabel(F"Логин: {user['login']}"),1,0)
        self.main_grid.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.main_grid.addWidget(self.btn_display_table,0,1)
        self.main_grid.addWidget(self.btn_add_order,0,2)

        self.main_grid.addWidget(self.btn_back, 2, 0, 1,self.main_grid.columnCount(), alignment=Qt.AlignmentFlag.AlignBottom)
        

        


        self.centralWidget().setLayout(self.main_grid)

    def back(self):
        self.hide()
        self.main_window.show()

    def display_table(self):
        self.tableOrder = tableOrder(self)
        self.tableOrder.showMaximized()

    def add_order(self):
        self.addOrderWindow = addOrderWindow(user['login'],self)
        self.addOrderWindow.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.addOrderWindow.show()
 



        