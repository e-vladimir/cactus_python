# ОБРАБОТЧИКИ СПИСКОВ НА БАЗЕ НАТУРАЛЬНОЙ СОРТИРОВКИ
# 29 мар 2025

import natsort


def DistinctAndNatSortList1D(values: list, flag_distinct: bool = False, flag_sort: bool = False) -> list:
	""" Обработка списка на предмет уникальности и сортировки 1D-Списка """
	keys : list = values[:]
	if     flag_distinct: keys : list = list(set(values))

	if not flag_sort: return keys

	sorting_key = natsort.natsort_keygen(alg=natsort.ns.REAL)
	return sorted(keys, key=sorting_key)


def DistinctAndNatSortList2D(values: list, index_processing_item: int, flag_distinct: bool = False, flag_sort: bool = False) -> list:
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
