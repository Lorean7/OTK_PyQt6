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
    QComboBox
)
from PyQt6.QtCore import Qt

# DB
from database.db import DB

#interface
from interface.newClient import newClient


class addOrderWindow(QMainWindow):
    def __init__(self,name_personal,parent):
        super().__init__()
        self.personal_window = parent
        self.name_personal = name_personal
        self.setWindowTitle('Добавить заказ')
        self.setCentralWidget(QWidget())
        self.resize(300,150)
        self.init_gui()

    def init_gui(self):
        self.DB = DB()
        self.services = self.DB.get_services()
        self.main_grid = QVBoxLayout()
        self.main_grid.addWidget(QLabel('Введите Имя текущего оператора'))
        self.name_personal_input = QLineEdit()
        self.name_personal_input.setText(self.name_personal)
        self.name_personal_input.setReadOnly(True)

        self.main_grid.addWidget(self.name_personal_input)

        self.main_grid.addWidget(QLabel('Имя клиента'))
        self.client_name_input = QLineEdit()
        self.main_grid.addWidget(self.client_name_input)
        
        self.main_grid.addWidget(QLabel('Выберите услугу'))
        self.combo_box_services = QComboBox()
        for service in self.services:
            self.combo_box_services.addItem(service['name_service'])

        self.main_grid.addWidget(self.combo_box_services)
        
        self.btn_add = QPushButton('Добавить')
        self.btn_add.clicked.connect(lambda: self.add())
        self.main_grid.addWidget(self.btn_add)

        self.btn_back = QPushButton('Назад')
        self.btn_back.clicked.connect(lambda: self.back())
        self.main_grid.addWidget(self.btn_back)
        self.centralWidget().setLayout(self.main_grid)

    def back(self):
        self.close()
        self.personal_window.show()

    def add(self):
        if self.client_name_input.text():
            self.DB = DB()
            response = self.DB.add(self.client_name_input.text(),self.name_personal_input.text(),self.combo_box_services.currentText())

            if response is False:
                result_quest = QMessageBox.question(self,'Пользователя нет','Добавить?')
                if result_quest == QMessageBox.StandardButton.Yes:
                    print('добавляем пользователя')
                    newClientWindow = newClient(self)
                    newClientWindow.setWindowModality(Qt.WindowModality.ApplicationModal)
                    newClientWindow.name_client.setText(self.client_name_input.text())
                    newClientWindow.show()
                else:
                    QMessageBox.information(self,'Отмена операции', 'Укажите имя пользователя, который уже существует')
            
            elif response is True:
                QMessageBox.information(self,'Успешно', 'Данные добавлены')
            self.client_name_input.clear()
        




        