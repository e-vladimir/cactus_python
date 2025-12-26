# ОБРАБОТЧИКИ СПИСКОВ
# 19 апр 2025

import re


def DistinctAndSortList1D(values: list, flag_distinct: bool = False, flag_sort: bool = False) -> list:
	""" Обработка списка на предмет уникальности и сортировки 1D-Списка """
	result : list = values[:]
	if     flag_distinct: result : list = list(set(values))

	if not flag_sort: return result

	return list(sorted(result))


def DistinctAndSortList2D(values: list, index_processing_item: int, flag_distinct: bool = False, flag_sort: bool = False) -> list:
	""" Обработка списка на предмет уникальности и сортировки 2D-Списка """
	try:
		result: list = values[:]

		if flag_distinct:
			filter_distinct : set[str] = set(map(lambda item: item[index_processing_item], values))
			result                     = list(filter(lambda item: item[index_processing_item] in filter_distinct, result))

		if flag_sort    :
			result                     = list(sorted(result, key=lambda item: item[index_processing_item]))

		return result
	except: return []


def DifferenceLists(list_1: list, list_2: list, flag_cmp_1_to_2: bool = False) -> list:
	""" Разница между списками """
	return list(set(list_1 if flag_cmp_1_to_2 else list_2).difference(list_2 if flag_cmp_1_to_2 else list_1))


def ClearList(items: list[str], clear_short: bool = True, clear_empty: bool = True, clear_spaces: bool = True, clear_numbers: bool = True, clear_simbols: bool = True, flag_sort: bool = True) -> list[str]:
	""" Очистка списка от пустых строк, пробелов, чисел, спецсимволов """
	result = items[:]

	if clear_numbers: result = [re.sub(r'[0-9]',                   '', item) for item in result]
	if clear_simbols: result = [re.sub(r'[^a-zA-Zа-яА-Я0-9ёЁ\s.]', '', item) for item in result]
	if clear_spaces : result = [item.strip().replace('  ', ' ')            for item in result]
	if clear_empty  : result = filter(lambda item: len(item) > 0, result)
	if clear_short  : result = filter(lambda item: len(item) > 2, result)

	return sorted(result) if flag_sort else result
