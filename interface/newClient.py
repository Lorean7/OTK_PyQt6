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
    QVBoxLayout,
    
)
from PyQt6.QtCore import Qt,QRegularExpression
from PyQt6.QtGui import QRegularExpressionValidator
import os.path
# DB
from database.db import DB
#interface


class newClient(QMainWindow):
    def __init__(self,parent):
        super().__init__()
        self.add_order = parent
        

        self.setWindowTitle('Добавить клиента')
        self.setCentralWidget(QWidget())
        self.resize(300,150)
        self.init_gui()

    def init_gui(self):
        #validaor
        validator = QRegularExpressionValidator(QRegularExpression("[0-9]*"))
        

        self.main_grid = QVBoxLayout()

        self.name_client =QLineEdit()

        self.phone_client = QLineEdit()
        self.phone_client.setValidator(validator)
        self.phone_client.setMaxLength(12)

        self.email_client = QLineEdit()
        self.email_client.setMaxLength(30)

        self.btn_add_client = QPushButton('Добавить')
        self.btn_add_client.clicked.connect(lambda: self.add_client())

        self.main_grid.addWidget(QLabel('Введите имя'))
        self.main_grid.addWidget(self.name_client)

        self.main_grid.addWidget(QLabel('Введите номер'))
        self.main_grid.addWidget(self.phone_client)

        self.main_grid.addWidget(QLabel('Введите почту'))
        self.main_grid.addWidget(self.email_client)

        self.main_grid.addWidget(self.btn_add_client)


        self.centralWidget().setLayout(self.main_grid)
    def add_client(self):
        name = self.name_client.text()
        phone = self.phone_client.text()
        email = self.email_client.text()
        if name and phone and email:
            self.DB = DB()
            response = self.DB.add_client(name,phone,email)
            if response:
                QMessageBox.information(self,'ok','клиент добавлен в систему')
            else:
                QMessageBox.warning(self,'err','Имя пользователя занято')

        else:
            QMessageBox.warning(self,'err','Заполните все поля')




        