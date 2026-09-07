# МАТЕМАТИКА: ЛИНЕЙНАЯ
# 18 авг 2025

from statistics import mean


def AvgOrNone(in_list: list) -> float | None:
	""" Среднее из списка """
	if not in_list: return None

	return float(mean(in_list))


def AvgOrZero(data: list[int] | list[float], flag_return_int: bool = False) -> int | float:
	""" Расчёт среднего с возвратом 0 если массив пуст """
	try:
		result : float = sum(data) / len(data)
		return int(result) if flag_return_int else result
	except:
		return 0 if flag_return_int else 0.00


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
		if type(value)   is int  : return 0

		return 0.0


def MaxOrNone(in_list: list) -> int | float | None:
	""" Максимум из списка, включая None"""
	result = None

	for item in in_list:
		if (type(item) is int) or (type(item) is float):
			if result is None: result = item
			else:              result = max(result, item)

	return result


def MinOrNone(in_list: list) -> int | float | None:
	""" Максимум из списка, включая None"""
	result = None

	for item in in_list:
		if (type(item) is int) or (type(item) is float):
			if result is None: result = item
			else:              result = min(result, item)

	return result


def Sign(value: int | float) -> int:
	""" Определение знака числа """
	return -1 if value < 0 else 1
