from PyQt5.QtWidgets import QApplication, QMessageBox, QLabel
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
import sys



class DataBase:
	"""
	Класс инициализации базы данных Клиента, его автопарка и актов работ для СТО.
	Класс для внесения изменений, удалений и изменений записей в базе данных.
	API для работы с базой данных
	"""

	арр = QApplication(sys.argv)

	def __init__(self) -> None:
		self.con = QSqlDatabase.addDatabase('QSQLITE')
		self.con.setDatabaseName('./data.sqlite')

	# ===========================INITIALISE DB====================================
	def database_initialise(self) -> None:
		"""
		Инициализация таблиц в базе данных

		:return: None
		"""
		self.database_initialise_owner()
		self.database_initialise_driver()
		self.database_initialise_attachment()
		self.database_initialise_car()
		self.database_initialise_order()

	# ===========================OWNER DB====================================
	def database_initialise_owner(self) -> None:
		"""
		Инициализация компании заказчика в базе данных

		:return: None
		"""
		try:
			self.con.open()
			query = QSqlQuery()
			if 'owner_db' not in self.con.tables():
				query.exec('CREATE TABLE owner_db (owner_id INTEGER PRIMARY KEY AUTOINCREMENT,'
				           'company_name TEXT NOT NULL,'
				           'company_fullname TEXT NOT NULL,'
				           'company_unp_code TEXT NOT NULL UNIQUE,'
				           'company_address TEXT NULL,'
				           'company_phone TEXT NULL)'
				           )
			self.con.close()
		except Exception as err:
			self.exception_dialog(str(err))
		finally:
			self.con.close()

	# _____________input owner_____________
	def input_owner(self, owner_list: list) -> None:
		"""
		Ввод данных о компании заказчика

		:param owner_list: Список данных о компании
		:return: None
		"""
		try:
			self.con.open()
			query = QSqlQuery()
			query.prepare('INSERT INTO owner_db VALUES (NULL,'
			              ':company_name,'
			              ':company_fullname,'
			              ':company_unp_code,'
			              ':company_address,'
			              ':company_phone)'
			              )
			query.bindValue(':company_name', owner_list[0])
			query.bindValue(':company_fullname', owner_list[1])
			query.bindValue(':company_unp_code', int(owner_list[2]))
			query.bindValue(':company_address', owner_list[3])
			query.bindValue(':company_phone', owner_list[4])
			query.exec_()

		except Exception as err:
			self.exception_dialog(str(err))
		finally:
			self.con.close()

	# _____________display owner_____________
	def display_owner_for_name_or_id(self, company: [str, int]) -> list:
		"""
		Вывод информации об фирме-заказчике

		:param company: Сокращенное название, или номер ID в базе данных
		:return: list. Информацию об компании заказчика
		"""
		owner_list = ['owner_id',
		              'company_name',
		              'company_fullname',
		              'company_unp_code',
		              'company_address',
		              'company_phone']
		try:
			self.con.open()
			query = QSqlQuery()
			query.exec(
				'SELECT * FROM owner_db WHERE {} == {}'.format(
					'company_name' if isinstance(company, str) else 'owner_id', company))
			temp_list = []
			if query.isActive():
				query.first()
				for elem in owner_list:
					temp_list.append(query.value(elem))
			return temp_list

		except Exception as err:
			self.exception_dialog(str(err))
		finally:
			self.con.close()

	# ===========================DRIVER DB====================================
	def database_initialise_driver(self) -> None:
		"""
		Инициализация данных об представителе заказчика

		:return: None
		"""
		try:
			self.con.open()
			query = QSqlQuery()
			if 'driver_db' not in self.con.tables():
				query.exec('CREATE TABLE driver_db (driver_id INTEGER PRIMARY KEY AUTOINCREMENT,'
				           'company_id INTEGER,'
				           'name TEXT,'
				           'lastname TEXT,'
				           'position TEXT,'
				           'contact_phone TEXT,'
				           'FOREIGN KEY(company_id) REFERENCES owner_db(owner_id) ON DELETE CASCADE)')
			self.con.close()
		except Exception as err:
			self.exception_dialog(str(err))
		finally:
			self.con.close()

	# _____________input driver_____________
	def input_driver(self, driver_list: list) -> None:
		"""
		Ввод данных о представителе заказчика (Имя, Фамилия, должность, контактный номер телефона)
		:param driver_list: Список данных о представителе заказчика
		:return: None
		"""
		try:
			self.con.open()
			query = QSqlQuery()
			query.prepare('INSERT INTO driver_db VALUES (NULL,'
			              ':company_id,'
			              ':name,'
			              ':lastname,'
			              ':position,'
			              ':contact_phone')
			query.bindValue(':company_id', int(driver_list[0]))
			query.bindValue(':name', driver_list[1])
			query.bindValue(':lastname', driver_list[2])
			query.bindValue(':position', driver_list[3])
			query.bindValue(':contact_phone', driver_list[4])
			query.exec_()

		except Exception as err:
			self.exception_dialog(str(err))
		finally:
			self.con.close()

	# _____________display driver_____________
	def display_driver_for_name_or_id(self, driver: [str, int]) -> list:
		"""
		Вывод информации об водителе\представителе заказчика

		:param driver: Фамилия, или номер по базе данных - Имя, или ID водителя\заказчика
		:return: list. Сведения о водителе\заказчике
		"""
		driver_list = ['driver_id,'
		               'company_id,'
		               'name,'
		               'lastname,'
		               'position,'
		               'contact_phone']
		try:
			self.con.open()
			query = QSqlQuery()
			query.exec(
				'SELECT * FROM driver_db WHERE {} == {}'.format(
					'lastname' if isinstance(driver, str) else 'driver_id', driver))
			temp_list = []
			if query.isActive():
				query.first()
				for elem in driver_list:
					temp_list.append(query.value(elem))
			return temp_list

		except Exception as err:
			self.exception_dialog(str(err))
		finally:
			self.con.close()

	# ===========================ATTACHMENT====================================
	def database_initialise_attachment(self) -> None:
		"""
		Инициализация принадлежности объекта к автомобилю\прицепу\запчастям

		:return: None
		"""
		try:
			self.con.open()
			query = QSqlQuery()
			if 'attachment_db' not in self.con.tables():
				query.exec('CREATE TABLE driver_db (attachment_id INTEGER PRIMARY KEY AUTOINCREMENT,'
				           'spare_parts TEXT DEFAULT "Запчасти",'
				           'cargo_car TEXT DEFAULT "Автомобиль",'
				           'trailer TEXT DEFAULT "Прицеп"')
			self.con.close()
		except Exception as err:
			self.exception_dialog(str(err))
		finally:
			self.con.close()

	# ===========================CAR DB====================================
	def database_initialise_car(self) -> None:
		"""
		Инициализация базы автомобилей

		:return: None
		"""
		try:
			self.con.open()
			if self.con.isOpen():
				query = QSqlQuery()
				if 'car_db' not in self.con.tables():
					query.exec('CREATE TABLE car_db (car_id INTEGER PRIMARY KEY AUTOINCREMENT,'
					           'company_id INTEGER,'
					           'FOREIGN KEY (company_id) REFERENCES owner_db (id) ON DELETE CASCADE,'
					           'brand TEXT NOT NULL DEFAULT "Запчасти",'
					           'number TEXT NOT NULL DEFAULT car_id UNIQUE,'
					           'uzm_code TEXT NOT NULL DEFAULT "Запчасти",'
					           'year INTEGER NULL,'
					           'attachment INTEGER DEFAULT 2,'
					           'FOREIGN KEY (attachment) REFERENCES attachment_db(attachment_id))')
				self.con.close()
			else:
				print(self.con.lastError())
		except Exception as err:
			self.exception_dialog(str(err))
		finally:
			self.con.close()

	# _____________input car_____________
	def input_car(self, car_list: list) -> None:
		"""
		Ввод данных об автомобиле

		:param car_list: Список: компания, марка,номер, узм-код машины и год выпуска
		:return: None
		"""
		try:
			self.con.open()
			query = QSqlQuery()
			query.prepare('INSERT INTO driver_db VALUES (NULL,'
			              ':company_id,'
			              ':brand,'
			              ':number,'
			              ':uzm_code,'
			              ':year,'
			              ':attachment')
			query.bindValue(':company_id', int(car_list[0]))
			query.bindValue(':brand', car_list[1])
			query.bindValue(':number', car_list[2])
			query.bindValue(':uzm_code', car_list[3])
			query.bindValue(':year', int(car_list[4]))
			query.bindValue(':attachment', int(car_list[5]))
			query.exec_()

		except Exception as err:
			self.exception_dialog(str(err))
		finally:
			self.con.close()

	# _____________display car_____________
	def display_car_for_number_or_id(self, car: [str, int]) -> list:
		"""
		Вывод информации об автомобиле по номеру машины, или её id в базе данных

		:param car: Строка, или цифра - Номер машины, или ID машины
		:return: list. Сведения о машине: принадлежность к компании, бренд, номер машины,
										  узм-код машины, год и принадлежность (bool)
		"""
		car_list = ['car_id,'
		            'company_id,'
		            'brand,'
		            'number,'
		            'uzm_code,'
		            'year,'
		            'attachment'
		            ]
		try:
			self.con.open()
			query = QSqlQuery()
			query.exec(
				'SELECT * FROM car_db WHERE {} == {}'.format(
					'number' if isinstance(car, str) else 'car_id', car))
			temp_list = []
			if query.isActive():
				query.first()
				for elem in car_list:
					temp_list.append(query.value(elem))
			return temp_list

		except Exception as err:
			self.exception_dialog(str(err))
		finally:
			self.con.close()

	# ===========================ORDER DB====================================
	def database_initialise_order(self) -> None:
		"""
		Инициализация таблица о заказе в базе данных

		:return: None
		"""
		try:
			self.con.open()
			if self.con.isOpen():
				query = QSqlQuery()
				if 'order_db' not in self.con.tables():
					query.exec('CREATE TABLE order_db (order_id INTEGER PRIMARY KEY AUTOINCREMENT,'
					           'company_id INTEGER,'
					           'FOREIGN KEY (company_id) REFERENCES owner_db (id) ON DELETE CASCADE,'
					           'car_id INTEGER,'
					           'FOREIGN KEY (car_id) REFERENCES car_db (id) ON DELETE CASCADE,'
					           'car_mileage INTEGER DEFAULT 0,'
					           'order_opening_data TEXT,'
					           'order_closing_data TEXT NULL,'
					           'driver_id INTEGER NULL,'
					           'FOREIGN KEY (driver_id) REFERENCES driver_db (id) ON DELETE CASCADE,'
					           'order_status BOOL DEFAULT TRUE,'
					           'first_open BOOL DEFAULT TRUE,'
					           'prefix TEXT DEFAULT "A")'
					           )
				self.con.close()
			else:
				print(self.con.lastError())
		except Exception as err:
			self.exception_dialog(str(err))
		finally:
			self.con.close()

	# _____________input order_____________
	# _____________display order____________
	# ===========================DISPLAY ERROR DIALOG====================================
	# @staticmethod
def exception_dialog(error_text: str) -> None:
	"""
	Выводит на экран всплывающий диалог с ошибкой, или предупреждением

	:param error_text: Текст ошибки или предупреждения
	:return: None
	"""
	QMessageBox.critical(
		None,
		"App Name - Error!",
		"Database Error: {}".format(error_text)
	)
	sys.exit(1)

	# Create the application's dialog window
	win = QLabel("Connection Successfully Opened!")
	win.setWindowTitle("App Name")
	win.resize(200, 100)
	win.show()
	sys.exit(app.exec_())


if __name__ == '__main__':
	# xml_list_owner = (
	# 	['BAMS', 'BelAuto', '12365222224789', 'Minsk', '2564444'],
	# 	['UBS', 'Ultr', '111111', 'Minsk', '2564444'],
	# 	['TAIM', 'TAIM', '777777777', 'Minsk', '2564444']
	# )
	# xml_list_car = (
	# 	[2, 'MAZ', '1234AA', '111111111111', '2007', '1'],
	# 	[1, 'KAMAZ', '1526BB', '222222222222', '2021', '2'],
	# 	[2, 'VOLVO', '1244AA', '333333333333', '2020', '2']
	# )
	# xml_list_order = (
	# 	['BAMS', 'BelAuto', '12365222224789', 'Minsk', '2564444'],
	# 	['UBS', 'Ultr', '111111', 'Minsk', '2564444'],
	# 	['TAIM', 'TAIM', '777777777', 'Minsk', '2564444']
	# )
	# db = DataBase()
	# db.database_initialise()
	# for elem in xml_list_owner:
	# 	db.input_owner(elem)
	# db.display_owner_for_name_or_id(0)
	# for elem in xml_list_car:
	# 	db.input_car(elem)
	# db.display_car_for_number_or_id(0)
	exception_dialog('qweqwe')
