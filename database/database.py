from PyQt5 import QtWidgets, QtSql
import sys


class Data:
	def __int__(self) -> None:
		self.арр = QtWidgets.QApplication(sys.argv)




	def create_base(self) -> None:
		self.con = QtSql.QSqlDatabase.addDatabase('QSQLITE')
		self.con.setDatabaseName('data.sqlite')
		self.con.open()
		self.con.close()

	def base_struct(self) -> None:
		if self.con.open():
			print('q')
			# Работаем с базой данных
			if 'good' not in self.con.tables():
				query = QtSql.QSqlQuery()
				query.exec("create table good (id integer primary key autoincrement,goodname text, goodcount integer)")
			else:
				print('123')
		else:
			# Выводим текст описания ошибки
			print(self.con.lastError().text())

	def display(self):
		print('a')


if __name__ == '__main__':
	new = Data()
	new.create_base()
	new.base_struct()
	new.display()
