# ОБРАБОТЧИКИ СПИСКОВ
# 16 июн 2024

import natsort


def DistinctAndSortList1D(values: list, flag_distinct: bool = False, flag_sort: bool = False) -> list:
	""" Обработка списка на предмет уникальности и сортировки 1D-Списка """
	keys : list = values[:]
	if     flag_distinct: keys : list = list(set(values))

	if not flag_sort: return keys

	sorting_key = natsort.natsort_keygen(alg=natsort.ns.REAL)
	return sorted(keys, key=sorting_key)


def DistinctAndSortList2D(values: list, index_processing_item: int, flag_distinct: bool = False, flag_sort: bool = False) -> list:
	""" Обработка списка на предмет уникальности и сортировки 2D-Списка """
	try:
		result: list = values[:]

		if flag_distinct:
			filter_distinct : set[str] = set(map(lambda item: item[index_processing_item], values))
			result                     = list(filter(lambda item: item[index_processing_item] in filter_distinct, result))

		if flag_sort    :
			key_values      : list     = list(map(lambda item: item[index_processing_item], result))
			index_values               = natsort.index_natsorted(key_values, alg=natsort.ns.REAL)
			result                     = list(natsort.order_by_index(result, index_values))

		return result
	except: return []


def DifferenceLists(list_1: list, list_2: list) -> list:
	""" Разница между списками """
	result = []

	for item in (list_1 + list_2):
		check_exist : bool = item in list_1
		check_exist       &= item in list_2

		if check_exist    : continue
		if item in result : continue

		result.append(item)

	return result
