# -*- coding: utf-8 -*-
from peewee import Model, SqliteDatabase
from peewee import PrimaryKeyField, ForeignKeyField
from peewee import CharField, TextField, IntegerField, DateField, BooleanField
from peewee import IntegrityError
from datetime import datetime
from logger_set import logger, message_error, message_done, wrapper_except
from macros import switch_car_number
from typing import Any
from re import compile

db = SqliteDatabase('database.db')


# =============TABLE MODULE==================
class BaseModel(Model):
	"""
	Базовая модель для записи таблиц. Предоставляет подключение 'children' к базе данных.
	"""

	class Meta:
		database = db


class OwnerDB(BaseModel):
	"""
	Модель таблицы Организация (Owner)
	Имеет поля: id - идентификатор записи в базе данных,
				company_name - краткое название Организации,
				company_full_name - полное название Организации,
				company_unp_code - УНП Организации (уникальное),
				company_address - юридический адрес,
				company_phone - контактные телефоны.
	"""
	id = PrimaryKeyField(null=False)
	company_name = CharField(max_length=100, null=False)
	company_full_name = TextField(null=False)
	company_unp_code = IntegerField(unique=True)
	company_address = TextField(null=True)
	company_phone = TextField(null=True)

	class Meta:
		db_table = "owners"
		order_by = ('company_name',)


class DriverDB(BaseModel):
	"""
	Модель таблицы Представитель (Drivers)
	Имеет поля: id - идентификатор записи в базе данных,
				name - Имя представителя,
				lastname - Фамилия представителя,
				position - должность представителя,
				mobile_phone - контактный номер представителя,
				company_id - принадлежность к Организации. Связанное поля с полем id клиента.
	"""
	id = PrimaryKeyField(null=False)
	name = CharField(max_length=100, null=True)
	lastname = CharField(max_length=100, null=True)
	position = CharField(max_length=100, null=True)
	mobile_phone = TextField(null=True)
	company_id = ForeignKeyField(
		OwnerDB,
		related_name='company_id',
		to_field='id',
		on_delete='cascade',
		on_update='cascade',
		null=True
	)

	class Meta:
		db_table = "drivers"
		order_by = ('name',)


class AttachmentDB(BaseModel):
	"""
	Принадлежность автомобиля к группе (машина - 1 / прицеп - 2 / запчасти - 3)
	"""
	car = IntegerField(default=1)
	trailer = IntegerField(default=2)
	parts = IntegerField(default=3)

	class Meta:
		db_table = "attachment"
		order_by = ('id',)


class CarDB(BaseModel):
	"""
	Модель таблицы Автомобилей (Cars)
	Имеет поля: id - поле идентификатора автомобиля в базе данных,
				company_id - принадлежность к Организации заказчика, связанный ключ с id компании,
				brand - сведения о модели автомобиля(по умолчанию - Запчасти),
				brand - сведения о марке автомобиля(по умолчанию - Запчасти),
				model - сведения о модели автомобиля(по умолчанию - Запчасти),
				number - номер машины (уникальный),
				uzm_code - УЗМ-код шасси машины,
				year - год выпуска,
				attachment - принадлежность записи к группе (машина/прицеп/запчасти)
	"""
	id = PrimaryKeyField(null=False)
	company_id = ForeignKeyField(
		OwnerDB,
		related_name='company_id',
		to_field='id',
		on_delete='cascade',
		on_update='cascade',
		null=False
	)
	brand = CharField(max_length=100, null=False, default='Запчасти')
	model = CharField(max_length=100, null=False, default='Запчасти')
	number = CharField(unique=True, null=False, default='Запчасти')
	uzm_code = TextField(null=True, default='Запчасти')
	year = IntegerField(null=True)
	attachment = IntegerField(default=3)

	class Meta:
		db_table = "cars"
		order_by = ('number',)


class OrderDB(BaseModel):
	"""
	Модель таблицы Актов (Orders)
	Имеет поля: id - поле идентификатора акта, он же номер акта,
				prefix - буква-префикс акта, добавляется к номеру акта,
				company_id - поле зависимости от id клиента,
				car_id - поле зависимости от id клиента,
				driver_id - поле зависимости от id клиента,
				start_date - дата создания акта (по умолчанию - текущая дата),
				finish_date - дата закрытия акта,
				car_mileage - пробег машины на момент открытия акта,
				first_open - идентификатор (bool, по умолчанию - True) первой записи об акте,
				opening_order - идентификатор (bool, по умолчанию - True), что акт открыт и находится в работе.
	"""
	id = PrimaryKeyField(null=False)
	prefix = CharField(default='A')
	company_id = ForeignKeyField(
		OwnerDB,
		related_name='company_id',
		to_field='id',
		on_delete='cascade',
		on_update='cascade',
		null=False
	)
	car_id = ForeignKeyField(
		CarDB,
		related_name='car_id',
		to_field='id',
		on_delete='cascade',
		on_update='cascade',
		null=False
	)
	driver_id = ForeignKeyField(
		DriverDB,
		related_name='driver_id',
		to_field='id',
		on_delete='cascade',
		on_update='cascade',
		null=True
	)
	start_date = DateField(default=datetime.now())
	finish_date = DateField(null=True)
	car_mileage = IntegerField(default=0)
	first_open = BooleanField(null=False, default=True)
	opening_order = BooleanField(null=False, default=True)

	class Meta:
		db_table = "orders"
		order_by = ('id',)


# ====================CRATE TABLE=================

class DBAPI:
	"""
	Класс создания скелета базы данных.
	Предоставляет методы взаимодействия с базой данных.
	"""

	# ------------------------Create DB
	@wrapper_except
	def database_initialization(self) -> None:
		"""
		Создает скелет базы данных.
		TODO: Инициализирует поле AttachmentDB

		:return: None
		"""
		db.connect()
		OwnerDB.create_table()
		DriverDB.create_table()
		AttachmentDB.create_table()
		CarDB.create_table()
		OrderDB.create_table()

	# ------------------------CLIENT
	@wrapper_except
	def set_owner(self,
	              company_name: str,
	              company_full_name: str,
	              company_unp_code: int,
	              company_address: str = None,
	              company_phone: str = None,
	              company_id: int = None) -> None:
		"""
		Добавляет сведения о клиенте в базу данных.
		При наличии company_id (по умолчанию - Null), производит замену данных в существующей записи о клиенте.

		:param company_name: Краткое название клиента
		:param company_full_name: Полное название клиента TODO: убрать из записи названия символ '"', заменить
		:param company_unp_code: УНП компании. (уникальный) Уникальный номер предприятия.
		:param company_address: Юридический адрес организации.
		:param company_phone: Телефоны компании.
		:param company_id: Id компании (по умолчанию - None)
		:return: None
		"""
		try:
			if company_id and self.check_presence(element=company_id):
				if company_name and company_full_name and company_unp_code:
					owner = OrderDB.get(OwnerDB.id == company_id)
					owner.company_name = company_name.strip()
					owner.company_full_name = self.switch_quotes(company_full_name)
					owner.company_unp_code = int(company_unp_code)
					if company_address:
						owner.company_address = company_address.strip()
					if company_phone:
						owner.company_phone = company_phone.strip()
					owner.save()
			else:
				OwnerDB.create(
					company_name=company_name.strip(),
					company_full_name=self.switch_quotes(company_full_name),
					company_unp_code=int(company_unp_code),
					company_address=company_address.strip(),
					company_phone=company_phone.strip()
				)
		except TypeError as err:
			message_error('TypeError: ' + str(err))

	@wrapper_except
	def get_owner(self, identification: int = None) -> Any:
		"""
		При отсутствии identification (по умолчанию - None), возвращает список всех клиентов из базы данных.
		При наличии identification, проверяет наличие в базе данных идентификатора, а затем возвращает данный о клиенте.

		:param identification: Id клиента из базы данных.
		:return: Модель, или список Моделей OwnerDB.
		"""
		try:
			if identification:
				if self.check_presence(element=identification):
					return OwnerDB.get(OwnerDB.id == identification)
				else:
					raise ValueError('Отсутствует запись о клиенте.')
			else:
				return OwnerDB.select()
		except ValueError as err:
			message_error('ValueError: {}'.format(str(err)))

	# ------------------------CAR
	@wrapper_except
	def set_car(self,
	            company_id: int,
	            brand: str,
	            model: str,
	            number: str,
	            uzm_code: str,
	            year: [str, int],
	            attachment: str,
	            car_id: int = None) -> None:
		"""
		Устанавливает запись о машине клиента.
		При наличии car_id, производит изменения в записи о машине клиента.

		:param company_id: Id клиента
		:param brand: Марка машины
		:param model: Модель машины
		:param number: Номер машины (уникален)
		:param uzm_code: УЗМ код шасси
		:param year: Год выпуска
		:param attachment: Принадлежность: 1 - Машина, 2 - Прицеп, 3 - Запчасти (по умолчанию)
		:param car_id: Id машины из базы данных
		:return: None
		"""
		try:
			if car_id and company_id and self.check_presence(company_id) and self.check_presence(element=car_id,
			                                                                                     attr_id=company_id,
			                                                                                     attr='car'):
				car = CarDB.get(CarDB.id == car_id)
				if brand:
					car.brand = brand.strip()
				if model:
					car.model = model.strip()
				if number:
					car.number = switch_car_number(number)
				if uzm_code:
					car.uzm_code = uzm_code.strip()
				if year:
					car.year = str(year).strip()
				if attachment:
					car.attachment = attachment
				car.save()
			if self.check_presence(company_id):
				CarDB.create(
					company_id=company_id,
					brand=brand.strip(),
					model=model.strip(),
					number=switch_car_number(number),
					uzm_code=uzm_code.strip(),
					year=str(year).strip(),
					attachment=attachment
				)
		except TypeError as err:
			message_error('TypeError: ' + str(err))
		except ValueError as err:
			message_error('ValueError: ' + str(err))
		except IntegrityError as err:
			message_error('IntegrityError: ' + str(err))

	@wrapper_except
	def get_car(self, identification: [str, int] = None) -> Any:
		"""
		При отсутствии identification (по умолчанию = None), возвращает список всех автомобилей в базе данных.
		При identification = str (номер машины), возвращает автомобиль по номеру машины.
		При identification = int (id клиента), возвращает список всех автомобилей принадлежащих клиенту.

		:param identification: Int - id клиента, Str - номер машины
		:return: Модель, или список Моделей CarDB. Список машин, машин клиента, или сведения о машине по номеру
		"""
		try:
			if identification:
				if isinstance(identification, str):
					number = switch_car_number(identification)
					return CarDB.get(CarDB.number == number)
				else:
					if self.check_presence(identification):
						return CarDB.select().where(CarDB.company_id == identification)
			else:
				return CarDB.select()
		except ValueError as err:
			message_error('ValueError: ' + str(err))
		except IntegrityError as err:
			message_error('IntegrityError: ' + str(err))

	# ------------------------DRIVER
	@wrapper_except
	def set_driver(self,
	               company_id: int,
	               name: str = '',
	               lastname: str = '',
	               position: str = '',
	               mobile_phone: str = '',
	               driver_id: int = None) -> None:
		"""
		Добавляет запись о представителе Организации заказчика.
		Если представитель есть в базе данных, то по аргументу driver_id, производит изменения параметров представителя.

		:param company_id: Id заказчика
		:param name: Имя представителя. По умолчанию - None
		:param lastname: Фамилия представителя. По умолчанию - None
		:param position: Должность представителя. По умолчанию - None
		:param mobile_phone: контактный номер телефона. По умолчанию - None
		:param driver_id: По умолчанию - None, иначе: Int - id представителя, для изменения полей базы данных.
		:return: None
		"""
		try:
			if driver_id and company_id and self.check_presence(company_id) and self.check_presence(element=driver_id,
			                                                                                        attr_id=company_id,
			                                                                                        attr='driver'):
				driver = CarDB.get(CarDB.id == driver_id)
				if name:
					driver.name = name.strip().capitalize()
				if lastname:
					driver.lastname = lastname.strip().capitalize()
				if position:
					driver.position = position.strip().capitalize()
				if mobile_phone:
					driver.mobile_phone = mobile_phone.strip()
				driver.save()
			if self.check_presence(company_id):
				DriverDB.create(
					company_id=company_id,
					name=name.strip().capitalize(),
					lastname=lastname.strip().capitalize(),
					position=position.strip().capitalize(),
					mobile_phone=mobile_phone.strip()
				)
		except TypeError as err:
			message_error('TypeError: ' + str(err))
		except ValueError as err:
			message_error('ValueError: ' + str(err))

	@wrapper_except
	def get_driver(self, identification: int) -> Any:
		"""
		Возвращает список представителей зарегистрированных за Организацией заказчика.
		Проверяет наличие представителя на принадлежность к Организации заказчика.

		:param identification: Id клиента
		:return: Модель DriverDB. Список представителей.
		"""
		try:
			if self.check_presence(element=identification):
				return DriverDB.select().where(DriverDB.company_id == identification)
		except Exception as err:
			message_error('ValueError: ' + str(err))

	# ------------------------ORDER
	@wrapper_except
	def set_order(self, company_id: int, car_id: int, driver_id: int = None, car_mileage: int = None) -> None:
		"""
		Создаёт новый акт. Проверяет наличие машины у клиента,
		или принадлежность представителя заказчика к Организации заказчика

		:param company_id: Int. Id клиента из базы данных
		:param car_id: Int. Id машины из базы данных
		:param driver_id: Int. Id представителя из базы данных
		:param car_mileage: Int. Пробег машины
		:return: None
		"""
		try:
			if self.check_presence(element=company_id) \
					and self.check_presence(element=car_id, attr_id=company_id, attr='car') \
					and self.check_presence(element=driver_id, attr_id=company_id, attr='driver'):
				OrderDB.create(
					company_id=company_id,
					car_id=car_id,
					driver_id=driver_id,
					car_mileage=car_mileage
				)
		except TypeError as err:
			message_error('TypeError: ' + str(err))
		except ValueError as err:
			message_error('ValueError: ' + str(err))

	@wrapper_except
	def get_orders(self, identification: int = None, attribute: str = 'owner', old: str = 'True') -> Any:
		"""
		При отсутствии identification, возвращает список всех открытых актов
		(закрытых при значении параметра old: str = 'False')
		При наличии identification и attribute: str = 'car', возвращает список всех открытых актов с id машины в акте
		(закрытых при значении параметра old: str = 'False')
		При наличии identification и attribute: str = 'owner' (по умолчанию),
		возвращает список всех открытых актов с id клиента в акте
		(закрытых при значении параметра old: str = 'False')

		:param identification: Id клиента, или машины
		:param attribute: Параметр: 'owner' - для поиска по id клиента, 'car' - для поиска по id машины.
		:param old: Параметр: str.
					'True' - для возврата списка открытых актов.
					'False' - для возврата списка закрытых актов
		:return: Модель, или список Моделей Актов (OrderDB)
		"""
		if identification:
			if attribute.strip().lower() == 'owner':
				return OrderDB.select().where(OrderDB.company_id == identification
				                              and (OrderDB.opening_order == True
				                                   if old.strip().capitalize() == 'True' else
				                                   OrderDB.opening_order == False))
			if attribute.strip().lower() == 'car':
				return OrderDB.select().where(OrderDB.car_id == identification
				                              and (OrderDB.opening_order == True
				                                   if old.strip().capitalize() == 'True' else
				                                   OrderDB.opening_order == False))
		else:
			return OrderDB.select().where(OrderDB.opening_order == True
			                              if old.strip().capitalize() == 'True' else
			                              OrderDB.opening_order == False)

	@logger.catch
	def update_order(self,
	                 order_id: int = None,
	                 prefix: bool = False,
	                 company_id: int = None,
	                 car_id: int = None,
	                 driver_id: int = None,
	                 start_date: int = None,
	                 finish_date: int = None,
	                 car_mileage: int = None,
	                 opening_order: bool = True) -> None:
		"""
		При наличии id акта, производит замену значений.
		Иначе создаёт новый акт.

		:param order_id: Int
		:param prefix: Bool (по умолчанию str('A'), при наличии id акта и значении True, увеличивает значение на 1)
		:param company_id: Int
		:param car_id: Int
		:param driver_id: Int
		:param start_date: Data, в формате str. Дата создания акта
		:param finish_date: Data, в формате str. Дата закрытия акта
		:param car_mileage: Int. Пробег машины
		:param opening_order: Bool. Отметка о закрытии акта (True - открыт, False - закрыт)
		:return: None
		"""
		try:
			if not order_id:
				self.set_order(company_id=company_id, car_id=car_id, driver_id=driver_id, car_mileage=car_mileage)
			else:
				order = OrderDB.get(OrderDB.id == order_id)
				if prefix:
					order.prefix = chr(ord(order.prefix) + 1)
					order.first_open = False
				if company_id and self.check_presence(element=company_id) \
						and self.check_presence(element=(car_id if car_id else order.car_id),
						                        attr_id=(company_id if company_id else order.company_id),
						                        attr='car') \
						and self.check_presence(element=(driver_id if driver_id else order.driver_id),
						                        attr_id=(company_id if company_id else order.company_id),
						                        attr='driver'):
					order.company_id = company_id
				if car_id and self.check_presence(element=car_id,
				                                  attr_id=(company_id if company_id else order.company_id),
				                                  attr='car'):
					order.car_id = car_id
				if driver_id and self.check_presence(element=driver_id,
				                                     attr_id=(company_id if company_id else order.company_id),
				                                     attr='driver'):
					order.driver_id = driver_id
				if start_date:
					order.start_date = start_date
				if finish_date:
					order.finish_date = finish_date
				if car_mileage:
					order.car_mileage = car_mileage
				if not opening_order and order.opening_order:
					order.opening_order = opening_order
					order.finish_date = datetime.now()
				if opening_order and not order.opening_order:
					order.opening_order = opening_order
					order.finish_date = None
				order.save()

		except ValueError as err:
			message_error('ValueError: ' + str(err))
		except IntegrityError as err:
			message_error('IntegrityError: ' + str(err))

	@classmethod
	@wrapper_except
	def delete_order(cls, order_id: int) -> None:
		"""
		TODO: Выводит окно подтверждения для удаления акта.
		Удаляет выбранный акт. Выводит сообщение об успешности удаление,
		или ошибку, при отсутствии записи в базе данных.

		:param order_id: Id акта для удаления
		:return: None
		"""
		try:
			if order_id:
				order = OrderDB.get(OrderDB.id == order_id)
				text = [order.id, order.prefix, order.start_date, OwnerDB.get(OwnerDB.id == order.company_id)]
				order.delete_instance()
				message_done(
					'Удален акт №{}-{} от {}. Клиент: {}.'.format(text[0], text[1], text[2], text[3].company_name))

		except Exception:
			message_error('DeleteError: Акт отсутствует в Базе данных')

	@wrapper_except
	def check_presence(self, element: int, attr_id: int = None, attr: str = 'owner') -> bool:
		"""
		Проверяет наличие клиента в базе данных, а также принадлежность представителя к Организации,
		или наличие машины в автопарке клиента.

		:param element: Параметр: id машины, или представителя заказчика для сравнения с базой данных.
		:param attr_id: Параметр: id клиента, для формирования списка автопарка, или представителей организации.
		:param attr: Аттрибуты:
					 'owner' - для проверки клиента в базе данных (по умолчанию),
					 'car' - для проверки машины у клиента,
					 'driver' - для проверки принадлежности представителя к организации заказчика.
		:return: Bool
		"""

		temp_dict = {
			'owner': [[elem.id for elem in self.get_owner()],
			          ValueError('Нету такого клиента.')],
			'car': [[elem.id for elem in self.get_car(name=attr_id)],
			        ValueError('У клиента {name} нету данной машины.'.
			                   format(name=[elem.name for elem in OrderDB.get(OwnerDB.id == attr_id)][0]))],
			'driver': [[elem.id for elem in self.get_driver(name=attr_id)],
			           ValueError('У клиента {name} нету такого работника.'.
			                      format(name=[elem.name for elem in OrderDB.get(OwnerDB.id == attr_id)][0]))]
		}
		try:
			if element in temp_dict[attr][0]:
				return True
			else:
				raise temp_dict[attr][1]
		except ValueError as err:
			message_error(str(err))

	@logger.catch
	def switch_quotes(self, text: str) -> str:
		"""
		Изменяет символы '"' на '<<' и '>>' для дальнейшего использования при печати,
		и обхода невозможности использования символа в python.

		:param text: Строка для замены символа '"' на '`' TODO: в перспективе '<<' и '>>'
		:return: str
		"""
		quotes = '"'
		if quotes in text:
			pattern = compile(quotes)
			text = pattern.sub('`', text)
		return text.strip()


if __name__ == "__main__":
	dat = DBAPI()
	# dat.database_initialization()
	pass
