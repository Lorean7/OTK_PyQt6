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
    QCalendarWidget,
    QCheckBox
)
from PyQt6.QtCore import Qt,QDate
from PyQt6.QtCore import Qt

from PyQt6.QtGui import QIcon


import os.path
# DB
from database.db import DB
#interface
from interface.personalWindow import personalWindow

class mainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        

        self.setWindowTitle('Начальное окно')
        self.setCentralWidget(QWidget())
        self.resize(300,150)
        self.init_gui()

    def init_gui(self):

        #кнопка  переключения режима
        self.btn_mode = QPushButton('К регистрации')
        self.btn_mode.clicked.connect(lambda: self.change_mode())
        
        #auth block
        self.auth_grid = QGridLayout()
        self.auth_group =QGroupBox('Авторизация')
        self.auth_group.setLayout(self.auth_grid)
        self.auth_group.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.auth_login = QLineEdit()
        self.auth_login.setPlaceholderText('Введите логин')
        self.auth_password = QLineEdit()
        self.auth_password.setPlaceholderText('Введите пароль')
        self.auth_password.setEchoMode(QLineEdit.EchoMode.Password)

        self.auth_btn = QPushButton('авторизация')
        self.auth_btn.clicked.connect(lambda: self.auth())

        self.auth_grid.addWidget(QLabel('Логин'),0,0)
        self.auth_grid.addWidget(self.auth_login,0,1)
        self.auth_grid.addWidget(QLabel('Пароль'),1,0)
        self.auth_grid.addWidget(self.auth_password,1,1)
        self.auth_grid.addWidget(self.auth_btn,2,1)
        

        
        #reg block
        self.reg_grid = QGridLayout()
        self.reg_group = QGroupBox('Регистрация')
        self.reg_group.setLayout(self.reg_grid)
        self.reg_group.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.reg_group.hide()

        #widgets
        self.reg_login = QLineEdit()
        self.reg_login.setPlaceholderText('Введите логин')
        self.reg_password = QLineEdit()
        self.reg_password.setPlaceholderText('Введите пароль')
        self.reg_password.setEchoMode(QLineEdit.EchoMode.Password)

        self.file_name = QLabel('Изображение не выбрано')

        self.reg_btn = QPushButton('Подтвердить регистрацию')
        self.reg_btn.clicked.connect(lambda: self.reg())
        self.add_btn = QPushButton('Выбрать аватарку')
        self.add_btn.clicked.connect(lambda: self.add_file())

        self.reg_grid.addWidget(QLabel('Логин'),0,0)
        self.reg_grid.addWidget(self.reg_login,0,1)
        self.reg_grid.addWidget(QLabel('Пароль'),1,0)
        self.reg_grid.addWidget(self.reg_password,1,1)
        self.reg_grid.addWidget(self.add_btn,2,1)
        self.reg_grid.addWidget(self.file_name,3,1)
        self.reg_grid.addWidget(self.reg_btn,4,1)
        
        #main
        self.main_grid = QGridLayout()
        self.main_grid.addWidget(self.auth_group,0,0)
        self.main_grid.addWidget(self.reg_group,0,0)
        self.main_grid.addWidget(self.btn_mode,1,0)
        #Oleja shalit
        self.calendar = QCalendarWidget()
        self.calendar.setGridVisible(True)
        self.calendar.clicked.connect(lambda: self.test())
        
        self.calendar.resize(200, 75)
        self.curent_date = QDate.currentDate()
       
        self.calendar.setMaximumDate(self.curent_date.addDays(7))
        self.calendar.setMinimumDate(self.curent_date.addDays(-7))
        self.checkBox1 = QCheckBox('Тест 1')
        self.checkBox1.clicked.connect(lambda : self.test())
        self.checkBox2 = QCheckBox('Тест 2')
        self.checkBox2.clicked.connect(lambda : self.test())


        self.curr_data = QLabel()
        self.curr_data.setText(f"Выбрана дата - {self.calendar.selectedDate().toString('yyyy-MM-dd')}")
        self.main_grid.addWidget(self.calendar,2,0)
        self.main_grid.addWidget(self.curr_data,3,0)
        self.main_grid.addWidget(self.checkBox1,4,0)
        self.main_grid.addWidget(self.checkBox2,5,0)

        self.centralWidget().setLayout(self.main_grid)

    def change_mode(self):
        if self.auth_group.isVisible():
            self.auth_group.hide()
            self.reg_group.show()
            self.btn_mode.setText('К авторизации')
        else:
            self.auth_group.show()
            self.reg_group.hide()
            self.btn_mode.setText('К регистрации')
    
    def auth(self):
        if self.auth_login.text() and self.auth_password.text():
            self.DB = DB()
            data_personal= self.DB.auth_personal(self.auth_login.text(),self.auth_password.text())
            if data_personal is False:
                QMessageBox.warning(self,'ERROR CRITICAL','Нет подключение к БД')
            elif data_personal is None:
                QMessageBox.warning(self,'error','пользователь не найден')
            else:
                self.personalWindow = personalWindow(self)
                self.personalWindow.show()
                self.close()

        else: 
            QMessageBox.warning(self,'warr','пустые поля')

    def reg(self):
        if os.path.exists(self.file_name.text()) and self.reg_login.text() and self.reg_password.text():
            self.DB = DB()
            result = self.DB.reg_personal(self.reg_login.text(),self.reg_password.text(),self.file_name.text())
            if result:
                QMessageBox.information(self,'ок','Пользователь добавлен')
            else:
                QMessageBox.warning(self,'error','Не удалость пройти регистрацию')
        else:
            QMessageBox.warning(self,'пустые поля','Заполните все данные формы')
        

    def add_file(self):
        QFileDialog()
        tmp_file_name,_ = QFileDialog.getOpenFileName(self,"Выберите файл", "","Images (*.png *.jpg)")
        self.file_name.setText(tmp_file_name)
        
    def test(self):
        self.curr_data.setText(f"Выбрана дата - {self.calendar.selectedDate().toString('yyyy-MM-dd')}")
        #логика для боксов и изменение выбора
        if self.sender() == self.checkBox1:
            if self.checkBox1.isChecked():
                self.checkBox2.setChecked(False)
        elif self.sender() == self.checkBox2:
            if self.checkBox2.isChecked():
                self.checkBox1.setChecked(False)
        print(self.checkBox1.isChecked())


    
        
            


        