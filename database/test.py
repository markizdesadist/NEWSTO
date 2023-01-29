


def test_owner(dat):
	temp = dat.get_owner(name=111222333)
	lst = [temp.id, temp.company_name]
	print(lst)
	print('{id}, {name}'.format(id=temp.id, name=temp.company_name))
	for elem in dat.get_owner():
		print(elem.company_name)

def test_car(dat):
	# temp = dat.get_car(name=2)
	# for elem in temp:
	# 	print(elem.id)
	# temp = dat.get_car(name='1226BB7')
	# lst = [temp.number, temp.company_id]
	# print(lst)
	# temp = dat.get_car(name=2)
	# lst = [temp.number, temp.company_id]
	# print(lst)
	temp = [elem.id for elem in dat.get_car(name=2)]
	print(temp)
	for elem in dat.get_car(name=2):
		print(elem.number, elem.company_id)

def test_driver(dat):
	for temp in dat.get_driver(name=2):
		print(temp.name, temp.lastname, temp.company_id)

def test_order(dat):
	for temp in dat.get_orders(name=None, old='False'):
		print('company - {}, act: {}-{}'.format(temp.company_id, temp.id, temp.prefix))




owner_list = [
	['SGP', 'SGP', 111222333, 'Minsk', '666'],
	['BAMS', 'BAMS', 222333444, 'Minsk', '555'],
	['NEVA', 'NEVA', 333444555, 'Minsk', '777'],
	['Arena', 'Arena', 444555666, 'Minsk', '888'],
	['Bordy', 'Bordy', 555666777, 'Minsk', '888']
]
car_list = [
	[1, 'MAZ', '5440', '1226BB7', 'UZM5440F8', '2007', 1],
	[2, 'MAZ', '4370', '1338AA5', 'UZM4370F8', '2011', 1],
	[2, 'MAZ', '5551', '5454EE7', 'UZM5551F8', '2020', 1],
	[3, 'MTM', '93866', 'EE88885', 'UZM93866', '2020', 2],
	[4, 'MTM', '9387', 'EE12224', 'UZM9387', '2019', 2]
]
driver_list = [
	[2,'Oleg', 'Rustam', 'meckanic', '888855'],
	[2,'Vasil', 'Werty', 'meckanic', '888855'],
	[1,'Vadim', 'Lukas', 'meckanic', '888855'],
	[3,'Gena', 'Ferdy', 'meckanic', '888855']
]
order_list = [
	# [1, 2, 1, '888855'],
	# [2, 2, 1, '888855'],
	# [1, 3, 2, '888855'],
	[3, 3, 3, '888855']
]

def add_note(dat):
	for elem in owner_list:
		dat.set_owner(*elem)
	for elem in car_list:
		dat.set_car(*elem)
	for elem in driver_list:
		dat.set_driver(*elem)

if __name__ == '__main__':
	pass