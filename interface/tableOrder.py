from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QGroupBox,
    QGridLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QMessageBox,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QComboBox,
    QAbstractItemView
)
from PyQt6.QtCore import Qt,QRegularExpression
from PyQt6.QtGui import QPixmap,QRegularExpressionValidator,QIcon




import os.path
# DB
from database.db import DB



class tableOrder(QMainWindow):
    def __init__(self,parent):
        super().__init__()
        self.personal_window = parent
        self.setWindowTitle('Список заказов')
        self.setCentralWidget(QWidget())
        self.resize(600,300)
        self.table = QTableWidget()
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        
        self.init_gui()

    def init_gui(self):
        
        self.update_table()
        self.DB = DB()
        self.services = self.DB.get_services()
        self.personals = self.DB.get_personals()
        self.clients = self.DB.get_clients()
        # блок удаления
        self.deleteOrder_group = QGroupBox('Удаление заказа')
        self.deleteOrder_loyout = QVBoxLayout()
        self.deleteOrder_group.setLayout(self.deleteOrder_loyout)
        self.deleteOrder_loyout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.deleteOrder_loyout.addWidget(QLabel('id заказа'))
        self.id_delete_order = QLineEdit()
        validator = QRegularExpressionValidator(QRegularExpression('[0-9]*'))
        self.id_delete_order.setValidator(validator)
        self.deleteOrder_loyout.addWidget(self.id_delete_order)
        self.btn_delete_order = QPushButton('Удалить')
        self.btn_delete_order.clicked.connect(lambda: self.delete())
        self.deleteOrder_loyout.addWidget(self.btn_delete_order)
        # блок обновления
        self.updateOrder_group = QGroupBox('Обновление заказа')
        self.updateOrder_loyout = QVBoxLayout()
        self.updateOrder_group.setLayout(self.updateOrder_loyout)

        self.updateOrder_loyout.addWidget(QLabel('id заказа для обновления'))
        self.update_id_order = QLineEdit()
        self.update_id_order.setValidator(validator)
        self.updateOrder_loyout.addWidget(self.update_id_order)

        self.updateOrder_loyout.addWidget(QLabel('Выберите услугу'))
        self.combo_box_services = QComboBox()
        for service in self.services:
            self.combo_box_services.addItem(service['name_service'])
        self.updateOrder_loyout.addWidget(self.combo_box_services)

        self.updateOrder_loyout.addWidget(QLabel('Выберите имя оператора'))
        self.combo_box_personal = QComboBox()
        headers_personal = list(dict(self.personals[0]).keys())
        for personal in self.personals:
                self.combo_box_personal.addItem(personal['login'],'login')
            
        self.updateOrder_loyout.addWidget(self.combo_box_personal)

        self.updateOrder_loyout.addWidget(QLabel('Выберите имя клиента'))
        self.combo_box_clients = QComboBox()
        for client in self.clients:
            self.combo_box_clients.addItem(client['FIO'])
        self.updateOrder_loyout.addWidget(self.combo_box_clients)

        self.btn_update_order = QPushButton('Обновить данные')
        self.btn_update_order.clicked.connect(lambda: self.update_order())
        self.updateOrder_loyout.addWidget(self.btn_update_order)

    
        self.btn_back_personal = QPushButton('Вернуть в личный кабинет')
        self.btn_back_personal.clicked.connect(lambda: self.back())
        layout = QGridLayout()
        layout.addWidget(self.deleteOrder_group,0,0)
        layout.addWidget(self.updateOrder_group,0,1)
        
        layout.addWidget(self.table,2,0,1,2)
        
        layout.addWidget(self.btn_back_personal,3,0,1,2)
        self.centralWidget().setLayout(layout)
        self.resize(600,400)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)

    def back(self):
        self.hide()
        self.personal_window.show()
    
    def delete(self):
        self.DB = DB()
        if self.id_delete_order.text():
            response = self.DB.delete(int(self.id_delete_order.text()))
            if response:
                QMessageBox.information(self,'ok','Заказ найден и удален')
                self.update_table()
            else:
                QMessageBox.warning(self,'error','Заказ не найден')

        else: 
            QMessageBox.warning(self,'error','Укажите id заказа')

    def update_table(self):
        # Очистка таблицы если она существует
        if self.table is not None:
            self.table.clear()
        
        self.DB = DB()
        data_orders = self.DB.get_orders()
        if data_orders:
            # Получение списка имен ключей из первого элемента массива данных
            headers = list(dict(data_orders[0]).keys())

            # настройки таблицы
            self.table.setColumnCount(len(headers)) # Установка количества столбцов
            self.table.setRowCount(len(data_orders)) # Установка количества строк
            # Установка названий столбцов
            self.table.setHorizontalHeaderLabels(headers)
    
            # Заполнение таблицы данными из массива
            #print(list(enumerate(data_orders)))
            for i, element in enumerate(data_orders):
                for j, header in enumerate(headers):

                        self.table.setItem(i, j, QTableWidgetItem(str(element[header])))
                        self.table.setColumnWidth(j,200)
        else:
            QMessageBox.warning(self,'Ошибка','В базе данных нет информации')


                
    def update_order(self):
       id_order = self.update_id_order.text()
       service_name =  self.combo_box_services.currentText()
       personal_name = self.combo_box_personal.currentText()
       client_name = self.combo_box_clients.currentText()
       if id_order and service_name and personal_name and client_name:
            self.DB = DB()
            response = self.DB.update(id_order,service_name,personal_name,client_name)
            if response:
                self.update_table()
            else:
                QMessageBox.warning(self,'err','Заказ не найден')

       else:
           QMessageBox.warning(self,'err','Заполните все данные')




 



        