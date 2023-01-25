import site

data = site.getsitepackages()

print(data)

from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5 import QtWidgets
import sys


class DataBase:
    app = QtWidgets.QApplication(sys.argv)


    def __init__(self):
        self.con = QSqlDatabase.addDatabase('QSQLITE')
        self.con.setDatabaseName('.\\db.sqlite')

    def start(self):

        self.con.open()

    def database_initialization(self):
        self.start()
        if self.con.open():
            query = QSqlQuery()
            if 'owner_db' not in self.con.tables():
                query.exec('CREATE TABLE owner_db (id INTEGER PRIMARY KEY AUTOINCREMENT,'
                           'company_name TEXT NOT NULL,'
                           'company_fullname TEXT NOT NULL,'
                           'company_unp_code INTEGER NOT NULL,'
                           'company_address TEXT NULL,'
                           'company_phone TEXT NULL'
                           )
            if 'driver_db' not in self.con.tables():
                query.exec('CREATE TABLE driver_db (id INTEGER PRIMARY KEY AUTOINCREMENT,'
                           'company_id INTEGER,'
                           'FOREIGN KEY (company_id) REFERENCES owner_db (id),'
                           'name TEXT,'
                           'lastname TEXT,'
                           'position TEXT,'
                           'contact_phone TEXT'
                           )
            if 'car_db' not in self.con.tables():
                query.exec('CREATE TABLE car_db (id INTEGER PRIMARY KEY AUTOINCREMENT,'
                           'company_id INTEGER,'
                           'FOREIGN KEY (company_id) REFERENCES owner_db (id),'
                           'brand TEXT NOT NULL DEFAULT "Запчасти",'
                           'number TEXT NOT NULL DEFAULT "Запчасти",'
                           'uzm_code TEXT NOT NULL DEFAULT "Запчасти",'
                           'year INTEGER NULL,'
                           'attachment TEXT DEFAULT "Запчасти"'
                           )
            if 'order_db' not in self.con.tables():
                query.exec('CREATE TABLE order_db (id INTEGER PRIMARY KEY AUTOINCREMENT,'
                           'company_id INTEGER,'
                           'FOREIGN KEY (company_id) REFERENCES owner_db (id),'
                           'car_id INTEGER,'
                           'FOREIGN KEY (car_id) REFERENCES car_db (id),'
                           'car_mileage INTEGER DEFAULT 0,'
                           'order_opening_data TEXT,'
                           'order_closing_data TEXT NULL,'
                           'driver_id INTEGER NULL,'
                           'FOREIGN KEY (driver_id) REFERENCES driver_db (id),'
                           'order_status BOOL DEFAULT TRUE,'
                           'first_open BOOL DEFAULT TRUE,'
                           'prefix TEXT DEFAULT "A"'
                           )
            self.con.close()
        else:
            print(self.con.lastError().text())

    def insert_owner_value(self, elem: list) -> None:
        try:
            self.start()
            query = QSqlQuery()
            # print(','.join(elem))
            query.prepare('INSERT INTO owner_db VALUES (null,'
                          ':company_name,'
                          ':company_fullname,'
                          ':company_unp_code,'
                          ':company_adress,'
                          ':company_phone)'
                          )
            query.bindValue(':company_name', elem[0])
            query.bindValue(':company_fullname', elem[1])
            query.bindValue(':company_unp_code', elem[2])
            query.bindValue(':company_adress', elem[3])
            query.bindValue(':company_phone', elem[4])
            query.exec_()
        except Exception:
            print('Error: ')
        finally:
            self.con.close()

    def display(self):
        self.start()
        # try:
        #     self.start()
        #     query = QSqlQuery()
        #     query.exec('SELECT * FROM owner_db')
        #     print(query.size())
        # except Exception:
        #     pass
        # finally:
        #     self.con.close()


# if __name__ == "__main__":
#     elem_xml = ['БАМС', 'Белавтомазсервис', '195678333', 'Минск', '256']
#     db = DataBase()
#     db.database_initialization()
#     db.insert_owner_value(elem_xml)
#     db.display()
