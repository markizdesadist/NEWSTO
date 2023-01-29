from logger_set import wrapper_except, message_error


@wrapper_except
def switch_car_number(number: str = '1234 AA-5') -> [str, int]:
	"""
	Подгоняет текст номера машины под шаблон 1234 AA-5. Меняет руские буквы на латинские в номере машины.
	Если машина имеет номера другого государства, то возвращает его без форматирования.

	:param number: Текстовое отображение номера машины
	:return: форматированная строка номерного знака машины
	"""
	ru_alphabet = {
		'А': 'A',
		'В': 'B',
		'Е': 'E',
		'I': 'I',
		'К': 'K',
		'М': 'M',
		'Н': 'H',
		'О': 'O',
		'Р': 'P',
		'С': 'C',
		'Т': 'T',
		'Х': 'X',
		'У': 'Y'
	}
	digit = []
	alpha = ''

	if number.upper().startswith(('RU', 'EU')):
		return number.upper()[2:]

	try:
		template = '{number} {serial}-{region}'
		for elem in number:
			if elem.isdigit():
				digit.append(elem)
			elif elem.isalpha():
				if elem.upper() in ru_alphabet.keys() or elem.upper() in ru_alphabet.values():
					try:
						alpha += ru_alphabet[elem.upper()]
					except KeyError:
						alpha += elem.upper()
				else:
					raise TypeError('Символ "{}" не используется в стандарте номеров. '
					                '(Если машина принадлежит другой стране, введите код страны перед номером: '
					                'RU для российской техники, EU - для других стран. '
					                'Образец: RU "A 111 AA 22"'.
					                format(elem.upper())
					                )
		if len(digit) != 5 or len(alpha) != 2:
			raise ValueError('Длина номера "{} {}-{}" не соответствует стандарту номеров.'.
			                 format(''.join(digit[:-1]), alpha, digit[-1])
			                 )
		elif int(digit[-1]) not in range(1, 8):
			raise TypeError('Код региона "{}-{}" должен быть в формате от 1 до 7.'.format(alpha, digit[-1]))

	except TypeError as err:
		# logger.info(err)
		message_error('TypeError: Номер не действителен. {}'.format(err))
		return -1
	except ValueError as err:
		# logger.debug(err)
		message_error('ValueError: Номер не действителен. {}'.format(err))
		return -1

	return template.format(
		number=''.join(digit[:-1]),
		serial=alpha,
		region=digit[-1]
	)


if __name__ == '__main__':
	pass
