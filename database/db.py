import mysql.connector
import os
from dotenv import load_dotenv
from PyQt6.QtCore import QDate
from model.user import user


class DB():
    def __init__(self):
       self.db = None
       self.cursor = None
       load_dotenv()

    def open(self):
        try:
            self.db = mysql.connector.connect(
                host=os.getenv('host'),
                user=os.getenv('user'),
                password=os.getenv('password'),
                database=os.getenv('database'),
            )
            self.cursor = self.db.cursor(dictionary=True)
        except mysql.connector.Error as e:
            print(e)
        finally:
            if self.db is not None:
                return True
            else:
                return False
            
        
        

    def close(self):
        if self.db is not None:
            self.cursor.close()
            self.db.close()

    #шаблон функции с обработчиком исключений
    def template(self):
        try:
            print('подключение  к бд ')
            self.open()
            #логика ниже

        except mysql.connector.Error as e:
            print('ERROR' , e)

        finally:
            if self.db is not None:    
                    self.close()

    def get_orders(self):
        try:
            print('подключение  к бд ')
            self.open()

            #logic code
            sql = """
                  SELECT id_order, p.login as name_operator, s.name_service as service, s.price_service as price, c.FIO as name_client, data_create_order
                  FROM orders
                  JOIN personals p ON p.id_personal = personals_id_personal  
                  JOIN services s ON s.id_service = services_id_service  
                  JOIN clients c ON c.id_client = clients_id_client
                  ORDER BY id_order;
                  """
            self.cursor.execute(sql)
            response = self.cursor.fetchall()
            return response
        except mysql.connector.Error as e:
            print('ERROR' , e)

        finally:
            if self.db is not None:
                self.close()
    
        

    def auth_personal(self,login,password):
        try:
            print('подключение  к бд ')
            response_open = self.open()
            print(response_open)
            if response_open:
                #logic
                self.cursor.execute("SELECT * from personals WHERE login=%s AND password=%s",(login,password))
                response_sql = self.cursor.fetchone()

                if response_sql is not None:
                    user['login'] = response_sql['login']
                    user['id'] = response_sql['id_personal']
                    user['avatar'] = response_sql['avatar']
                    return(response_sql)
                else:
                    return response_sql
            else:
                return False

            


        except mysql.connector.Error as e:
            print(e)
        finally:
            if self.db is not None:
                print('отключение от бд')
                self.close()

    def reg_personal(self,login,password,file_path):
        try:
            print('подключение  к бд ')
            self.open()

            sql = "SELECT id_personal from personals WHERE login=%s"
            self.cursor.execute(sql,(login,))
            response = self.cursor.fetchone()

            if response is None:
                data_img = None
                with open(file_path,'rb') as f:
                    data_img = f.read()

                sql = """
                    INSERT INTO personals (login, password,avatar) VALUES (%s, %s,%s) 
                    """
                self.cursor.execute(sql,(login,password,data_img))
                self.db.commit()
                return True
            else:
                return False
        except mysql.connector.Error as e:
            print(e)
        finally:
            if self.db is not None:
                print('отключение от бд')
                self.close()

    def delete(self,id):
        try:
            print('подключение  к бд ')
            self.open()
            self.cursor.execute("SELECT * FROM orders WHERE id_order=%s",(id,))
            response = self.cursor.fetchone()
            print(response)
            if response:
                self.cursor.execute("DELETE FROM orders WHERE id_order=%s",(id,))
                self.db.commit()
                return True
            else: 
                return False
            
        except mysql.connector.Error as e:
            print(e)
        finally: 
            if self.db is not None:
                print('отключение от бд')
                self.close()
    def update(self,id_order,service_name,personal_name,client_name):
        try:
            print('подключение  к бд ')
            self.open()
            self.cursor.execute('SELECT * FROM orders WHERE id_order=%s',(id_order,))
            response = self.cursor.fetchone()
            if response:
                self.cursor.execute('SELECT id_service FROM services WHERE name_service=%s',(service_name,))
                service = self.cursor.fetchone()
                id_service = int(service['id_service'])

                self.cursor.execute('SELECT id_personal FROM personals WHERE login=%s',(personal_name,))
                personal = self.cursor.fetchone()
                id_personal = int(personal['id_personal'])

                self.cursor.execute('SELECT id_client FROM clients WHERE FIO=%s',(client_name,))
                client = self.cursor.fetchone()
                id_client = int(client['id_client'])


                print(id_client,id_personal,id_service)
                self.cursor.execute("""UPDATE orders 
                                    SET personals_id_personal=%s, services_id_service=%s, clients_id_client=%s
                                     WHERE id_order=%s;""",(id_personal,id_service,id_client,id_order))
                self.db.commit()
                return True
            else:
                return False
            
        except mysql.connector.Error as e:
            print(e)
        finally: 
            if self.db is not None:
                print('отключение от бд')
                self.close()

    def get_services(self):
        try:
            print('start')
            self.open()
            self.cursor.execute("SELECT * FROM services")
            response = self.cursor.fetchall()
            if response:
                return response
            else: 
                return None
        except mysql.connector.Error as e:
            print(e)
        finally:
            if self.db is not None:
                print("END")
                self.close

    def get_personals(self):
        try:
            print('start')
            self.open()
            self.cursor.execute("SELECT * FROM personals")
            response = self.cursor.fetchall()
            if response:
                return response
            else: 
                return None
        except mysql.connector.Error as e:
            print(e)
        finally:
            if self.db is not None:
                print("END")
                self.close

    def get_clients(self):
        try:
            print('start')
            self.open()
            self.cursor.execute("SELECT * FROM clients")
            response = self.cursor.fetchall()
            if response:
                return response
            else: 
                return None
        except mysql.connector.Error as e:
            print(e)
        finally:
            if self.db is not None:
                print("END")
                self.close

    def add(self,name_client,name_personal,name_service):
        try: 
            self.open()
            self.cursor.execute("SELECT * FROM clients WHERE FIO=%s",(name_client,))
            response_client = self.cursor.fetchone()

            self.cursor.execute("SELECT * FROM personals WHERE login=%s",(name_personal,))
            response_personal = self.cursor.fetchone()

            self.cursor.execute("SELECT * FROM services WHERE name_service=%s",(name_service,))
            response_service = self.cursor.fetchone()
            if response_client and response_personal and response_service:
                # Получаем текущую дату
                #date = datetime.datetime.now()
                date = QDate.currentDate()
                # Преобразуем дату в строку в формате 'YYYY-MM-DD'
                #date_str = date.strftime('%Y-%m-%d')
                date_str = date.toString('yyyy-MM-dd')

                # Преобразуем строку в дату
                #date = datetime.datetime.strptime(date_str, '%Y-%m-%d')
                self.cursor.execute("""INSERT INTO orders 
                                    (personals_id_personal, services_id_service, clients_id_client, data_create_order)
                                    VALUES(%s,%s,%s,%s);""",
                                    (response_personal['id_personal'],response_service['id_service'],response_client['id_client'],date_str))

                self.db.commit()
                return True
            else:
                return False
            
        except mysql.connector.Error as e:
            print(e)

        finally:
            self.close()
    
        #шаблон функции с обработчиком исключений
    def add_client(self,name,phone,email):
        try:
            print('подключение  к бд ')
            self.open()
            #logic code
            self.cursor.execute("SELECT * FROM clients WHERE FIO=%s",(name,))
            response_clients = self.cursor.fetchone()
            if response_clients is None:
                self.cursor.execute("INSERT INTO clients (FIO ,telephone, email) VALUES(%s,%s,%s)",(name,phone,email))
                self.db.commit()
                return True
            else:
                return False
        
        except mysql.connector.Error as e:
            print('ERROR' , e)

        finally:
            if self.db is not None:
                self.close()



