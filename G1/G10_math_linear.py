# ЛИНЕЙНАЯ МАТЕМАТИКА
# 2023-01-28

def CheckBetween(value_min: int | float, value: int | float, value_max: int | float, flag_include: bool = True) -> bool:
	""" Проверка вхождения числа в диапазон """
	try:
		border_min = min(value_min, value_max)
		border_max = max(value_min, value_max)

		result : bool = (border_min < value) and (value < border_max)
		if flag_include:
			result = result or (value == border_min)
			result = result or (value == border_max)

		return result

	except: return False


def CalcBetween(value_min: int | float, value: int | float, value_max: int | float) -> int | float:
	""" Помещение числа в указанный предел """
	try:
		result = max(value_min, value)
		result = min(value_max, result)

		if   type(value) is int  : return int(result)
		elif type(value) is float: return float(result)
		else                     : return result
	except:
		if type(value) is int: return 0

		return 0.0
