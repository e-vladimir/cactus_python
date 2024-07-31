# КАКТУС: ЛИНЕЙНЫЕ ФИЛЬТРЫ ДАННЫХ
# 31 июл 2024

import datetime

from   G00_cactus_codes                 import  CACTUS_STRUCT_DATA
from   G00_filter_codes                 import  FILTERS
from   G00_status_codes                 import (CODES_COMPLETION,
                                                CODES_DATA,
                                                CODES_PROCESSING,
                                                CODES_CACTUS)

from   G10_cactus_convertors            import (UnificationIdc,
                                                IdoFromIds)
from   G10_convertor_format             import (AnyToStrings,
                                                AnyToString,
                                                StringToFloat,
                                                StringsToIntegers,
                                                StringsToFloats,
                                                StringsToBooleans,
                                                StringsToDatetimes,
                                                StringToInteger,
                                                StringToBoolean,
                                                StringToDateTime)
from   G10_list                         import (DistinctAndSortList2D,
                                                DistinctAndSortList1D)
from   G10_math_linear                  import  CheckBetween

from   G20_cactus_struct                import (T20_StructCell,
                                                T20_FilterD1)

from   G20_meta_frame                   import  C20_MetaFrame
from   G20_struct_result                import  T20_StructResult
from   G21_struct_result                import  T21_StructResult_List

from   G30_cactus_controller_containers import  controller_containers
from   G31_cactus_container_ram         import  C31_ContainerRAM
from   G32_cactus_container_sql         import (C32_ContainerSQLite,
                                                C32_ContainerPostgreSQL)


class C30_FilterLinear1D(C20_MetaFrame):
	""" Линейный 1D-фильтр для структурного объекта """

	def __init__(self, idc: str):
		super().__init__()

		self._idc = UnificationIdc(idc)

	def Init_00(self):
		super().Init_00()

		self._idc             : str                           = ""
		self._data            : list[T20_StructCell]          = []
		self._filters_idp_vlp : dict[str, list[T20_FilterD1]] = dict()

	# УПРАВЛЕНИЕ ФИЛЬТРАЦИЕЙ
	def _AppendFilterIdpVlp(self, filter_type: FILTERS, idp: str, data: any, flag_invert: bool, flag_include: bool) -> T20_StructResult:
		""" Добавление фильтра IDP-VLP """
		try   :
			value  : str       = ""
			values : list[str] = []

			if type(data) is list: values = AnyToStrings(data)
			else                 : value  = AnyToString(data)

			filter_item        = T20_FilterD1(flag_invert   = flag_invert,
			                                  flag_include  = flag_include,
			                                  filter_type   = filter_type,
			                                  filter_value  = value,
			                                  filter_values = values)
			filters            = self._filters_idp_vlp.get(idp, [])
			filters.append(filter_item)
			self._filters_idp_vlp[idp] = filters

		except:
			return T20_StructResult(code     = CODES_COMPLETION.INTERRUPTED,
		                            subcodes = {CODES_DATA.ERROR_CONVERT})

		return T20_StructResult(code = CODES_COMPLETION.COMPLETED)

	def FilterIdpVlpByEqual(self, idp: str, value: any, flag_invert: bool = False) -> T20_StructResult:
		""" Фильтрация IDP-VLP: Значение равно value """
		return self._AppendFilterIdpVlp(filter_type  = FILTERS.EQUAL,
										idp          = idp,
										data         = value,
										flag_invert  = flag_invert,
										flag_include = True)

	def FilterIdpVlpByMore(self, idp: str, value: int | float, flag_invert: bool = False, flag_include: bool = False) -> T20_StructResult:
		""" Фильтрация IDP-VLP: Значение больше чем value """
		return self._AppendFilterIdpVlp(filter_type  = FILTERS.MORE,
										idp          = idp,
										data         = value,
										flag_invert  = flag_invert,
										flag_include = flag_include)

	def FilterIdpVlpByLess(self, idp: str, value: int | float, flag_invert: bool = False, flag_include: bool = False) -> T20_StructResult:
		""" Фильтрация IDP-VLP: Значение меньше чем value """
		return self._AppendFilterIdpVlp(filter_type  = FILTERS.LESS,
										idp          = idp,
										data         = value,
										flag_invert  = flag_invert,
										flag_include = flag_include)

	def FilterIdpVlpByInclude(self, idp: str, value: str | int | float, flag_invert: bool = False) -> T20_StructResult:
		""" Фильтрация IDP-VLP: Значение включает в себя value """
		return self._AppendFilterIdpVlp(filter_type  = FILTERS.INCLUDE,
										idp          = idp,
										data         = value,
										flag_invert  = flag_invert,
										flag_include = True)

	def FilterIdpVlpByIn(self, idp: str, values: list[str] | list[int] | list[float], flag_invert: bool = False) -> T20_StructResult:
		""" Фильтрация IDP-VLP: Value включает в себя значение """
		return self._AppendFilterIdpVlp(filter_type  = FILTERS.IN,
										idp          = idp,
										data         = values,
										flag_invert  = flag_invert,
										flag_include = True)

	def FilterIdpVlpByBetween(self, idp: str, value_l : int | float, value_r: int | float, flag_invert: bool = False, flag_include: bool = False) -> T20_StructResult:
		""" Фильтрация IDP-VLP: Значение в пределах value """
		return self._AppendFilterIdpVlp(filter_type  = FILTERS.BETWEEN,
										idp          = idp,
										data         = [value_l, value_r],
										flag_invert  = flag_invert,
										flag_include = flag_include)

	def ResetFiltersIdpVlp(self, idp: str = None) -> T20_StructResult:
		""" Сброс фильтрации """

		if idp is None:
			self._filters_idp_vlp.clear()

			return T20_StructResult(code = CODES_COMPLETION.COMPLETED)

		elif idp in self._filters_idp_vlp:
			del self._filters_idp_vlp[idp]

			return T20_StructResult(code = CODES_COMPLETION.COMPLETED)

		else:
			return T20_StructResult(code     = CODES_COMPLETION.COMPLETED,
			                        subcodes = {CODES_PROCESSING.SKIP})

	# ЗАХВАТ ДАННЫХ
	def _ApplyFilterIdc(self, cell: T20_StructCell) -> bool:
		""" Применение фильтрации по Idc """
		return cell.idc == self._idc

	def _ApplyFilterIdpVlp(self, vlp: str, filter_idp_vlp: T20_FilterD1) -> bool:
		""" Применение фильтра IDP-VLP """
		flag_success: bool = False

		try:
			if   filter_idp_vlp.filter_type == FILTERS.EQUAL   : flag_success = vlp == filter_idp_vlp.filter_value

			elif filter_idp_vlp.filter_type == FILTERS.MORE    :
				if filter_idp_vlp.flag_include:	                 flag_success = StringToFloat(vlp) >= StringToFloat(filter_idp_vlp.filter_value)
				else                          :                  flag_success = StringToFloat(vlp) >  StringToFloat(filter_idp_vlp.filter_value)

			elif filter_idp_vlp.filter_type == FILTERS.LESS    :
				if filter_idp_vlp.flag_include:	                 flag_success = StringToFloat(vlp) <= StringToFloat(filter_idp_vlp.filter_value)
				else                          :                  flag_success = StringToFloat(vlp) <  StringToFloat(filter_idp_vlp.filter_value)

			elif filter_idp_vlp.filter_type == FILTERS.INCLUDE : flag_success = filter_idp_vlp.filter_value in vlp

			elif filter_idp_vlp.filter_type == FILTERS.IN      : flag_success = vlp in filter_idp_vlp.filter_values

			elif filter_idp_vlp.filter_type == FILTERS.BETWEEN : flag_success = CheckBetween(StringToFloat(filter_idp_vlp.filter_values[0]), StringToFloat(vlp), StringToFloat(filter_idp_vlp.filter_values[1]), flag_include=filter_idp_vlp.flag_include)

		except: return False

		return flag_success | filter_idp_vlp.flag_invert

	def _ApplyFiltersIdpVlp(self, cell) -> bool:
		""" Применение фильтрации по IDP-VLP """
		if not self._filters_idp_vlp                                : return True

		filters_idp_vlp = self._filters_idp_vlp.get(cell.idp, [])
		if not filters_idp_vlp                                      : return False

		for filter_idp_vlp in filters_idp_vlp:
			if not self._ApplyFilterIdpVlp(cell.vlp, filter_idp_vlp): return False

		return True

	def _CaptureFromRam(self, container: C31_ContainerRAM) -> T20_StructResult:
		""" Захват данных из контейнера RAM """
		self._data.clear()

		idos : set[str] = set()

		for cell in container._s_cells.values():
			if not self._ApplyFilterIdc(cell)    : continue
			if not self._ApplyFiltersIdpVlp(cell): continue

			idos.add(cell.ido)

		if not idos: return T20_StructResult(code     = CODES_COMPLETION.COMPLETED,
		                                     subcodes = {CODES_DATA.NO_DATA})

		self._data = list(filter(lambda cell: cell.ido in idos, container._s_cells.values()))

		return T20_StructResult(code = CODES_COMPLETION.COMPLETED)

	def _TranslateFilterIdpVlpToSqlite(self, idp: str, filter_idp_vlp: T20_FilterD1) -> str:
		""" Трансляция фильтра в SQLite диалект """
		sql : str = f"({CACTUS_STRUCT_DATA.IDS.name_sql} LIKE '%.{idp}') AND "

		if   filter_idp_vlp.filter_type == FILTERS.EQUAL   : sql += f"({'NOT ' if filter_idp_vlp.flag_invert else ''}{CACTUS_STRUCT_DATA.VLP.name_sql} = '{filter_idp_vlp.filter_value}')"

		elif filter_idp_vlp.filter_type == FILTERS.MORE    :
			if filter_idp_vlp.flag_include:                  sql += f"({'NOT ' if filter_idp_vlp.flag_invert else ''}{CACTUS_STRUCT_DATA.VLP.name_sql} >= '{filter_idp_vlp.filter_value}')"
			else                          :                  sql += f"({'NOT ' if filter_idp_vlp.flag_invert else ''}{CACTUS_STRUCT_DATA.VLP.name_sql} >  '{filter_idp_vlp.filter_value}')"

		elif filter_idp_vlp.filter_type == FILTERS.LESS    :
			if filter_idp_vlp.flag_include:                  sql += f"({'NOT ' if filter_idp_vlp.flag_invert else ''}{CACTUS_STRUCT_DATA.VLP.name_sql} <= '{filter_idp_vlp.filter_value}')"
			else                          :                  sql += f"({'NOT ' if filter_idp_vlp.flag_invert else ''}{CACTUS_STRUCT_DATA.VLP.name_sql} <  '{filter_idp_vlp.filter_value}')"

		elif filter_idp_vlp.filter_type == FILTERS.INCLUDE : sql += f"({'NOT ' if filter_idp_vlp.flag_invert else ''}{CACTUS_STRUCT_DATA.VLP.name_sql} LIKE '%{filter_idp_vlp.filter_value}%')"

		elif filter_idp_vlp.filter_type == FILTERS.IN      :
			values : list[str] = list(map("'{}'".format, filter_idp_vlp.filter_values))
			sql               += f"({'NOT ' if filter_idp_vlp.flag_invert else ''}{CACTUS_STRUCT_DATA.VLP.name_sql} IN ({', '.join(values)}))"

		elif filter_idp_vlp.filter_type == FILTERS.BETWEEN :
			value_l : str = filter_idp_vlp.filter_values[0]
			value_r : str = filter_idp_vlp.filter_values[1]

			sql          += f"({'NOT ' if filter_idp_vlp.flag_invert else ''}"

			if filter_idp_vlp.flag_include: sql += f"(({CACTUS_STRUCT_DATA.VLP.name_sql} >= {value_l}) AND ({CACTUS_STRUCT_DATA.VLP.name_sql} <= {value_r}))"
			else                          : sql += f"(({CACTUS_STRUCT_DATA.VLP.name_sql} > {value_l}) AND ({CACTUS_STRUCT_DATA.VLP.name_sql} < {value_r}))"

			sql          += ")"

		else: return ""

		return f"({sql})"

	def _TranslateFilterIdpVlpToPostgreSql(self, idp: str, filter_idp_vlp: T20_FilterD1) -> str:
		""" Трансляция фильтра в SQLite диалект """
		sql : str = f"({CACTUS_STRUCT_DATA.IDS.name_sql} LIKE '%.{idp}') AND "

		if   filter_idp_vlp.filter_type == FILTERS.EQUAL   : sql += f"({'NOT ' if filter_idp_vlp.flag_invert else ''}{CACTUS_STRUCT_DATA.VLP.name_sql} = '{filter_idp_vlp.filter_value}')"

		elif filter_idp_vlp.filter_type == FILTERS.MORE    :
			if filter_idp_vlp.flag_include:                 sql += f"({'NOT ' if filter_idp_vlp.flag_invert else ''}{CACTUS_STRUCT_DATA.VLP.name_sql} >= '{filter_idp_vlp.filter_value}')"
			else                          :                 sql += f"({'NOT ' if filter_idp_vlp.flag_invert else ''}{CACTUS_STRUCT_DATA.VLP.name_sql} >  '{filter_idp_vlp.filter_value}')"

		elif filter_idp_vlp.filter_type == FILTERS.LESS    :
			if filter_idp_vlp.flag_include:                 sql += f"({'NOT ' if filter_idp_vlp.flag_invert else ''}{CACTUS_STRUCT_DATA.VLP.name_sql} <= '{filter_idp_vlp.filter_value}')"
			else                          :                 sql += f"({'NOT ' if filter_idp_vlp.flag_invert else ''}{CACTUS_STRUCT_DATA.VLP.name_sql} <  '{filter_idp_vlp.filter_value}')"

		elif filter_idp_vlp.filter_type == FILTERS.INCLUDE : sql += f"({'NOT ' if filter_idp_vlp.flag_invert else ''}{CACTUS_STRUCT_DATA.VLP.name_sql} LIKE '%{filter_idp_vlp.filter_value}%')"

		elif filter_idp_vlp.filter_type == FILTERS.IN      :
			values : list[str] = list(map("'{}'".format, filter_idp_vlp.filter_values))
			sql               += f"({'NOT ' if filter_idp_vlp.flag_invert else ''}{CACTUS_STRUCT_DATA.VLP.name_sql} IN ({', '.join(values)}))"

		elif filter_idp_vlp.filter_type == FILTERS.BETWEEN :
			value_l : str = filter_idp_vlp.filter_values[0]
			value_r : str = filter_idp_vlp.filter_values[1]

			sql          += f"({'NOT ' if filter_idp_vlp.flag_invert else ''}"

			if filter_idp_vlp.flag_include: sql += f"(({CACTUS_STRUCT_DATA.VLP.name_sql}::float >= {value_l}) AND ({CACTUS_STRUCT_DATA.VLP.name_sql}::float <= {value_r}))"
			else                          : sql += f"(({CACTUS_STRUCT_DATA.VLP.name_sql}::float > {value_l}) AND ({CACTUS_STRUCT_DATA.VLP.name_sql}::float < {value_r}))"

			sql          += ")"

		else: return ""

		return f"({sql})"

	def _CaptureFromSqlite(self, container: C32_ContainerSQLite) -> T20_StructResult:
		""" Захват данных из контейнера SQLite """
		self._data.clear()

		sql     : str       = f"SELECT DISTINCT {CACTUS_STRUCT_DATA.IDS.name_sql} FROM {self._idc} "
		result              = container.ExecSqlSelectVList(sql)
		if not result.code == CODES_COMPLETION.COMPLETED : return T20_StructResult(code     = CODES_COMPLETION.INTERRUPTED,
		                                                                           subcodes = result.subcodes)
		capture_idos        = set(map(IdoFromIds, result.data))

		filters : list[str] = []

		for idp, filters_idp_vlp in self._filters_idp_vlp.items():
			for filter_idp_vlp in filters_idp_vlp: filters.append(self._TranslateFilterIdpVlpToSqlite(idp, filter_idp_vlp))

		for filter_item in filters:
			result       = container.ExecSqlSelectVList(sql + f" WHERE {filter_item}")
			if not result.code == CODES_COMPLETION.COMPLETED  : return T20_StructResult(code     = CODES_COMPLETION.INTERRUPTED,
		                                                                                subcodes = result.subcodes)
			capture_idos = capture_idos & set(map(IdoFromIds, result.data))

		idos                = list(map("'{}'".format, capture_idos))
		sql                 = f"SELECT {CACTUS_STRUCT_DATA.IDS.name_sql}, {CACTUS_STRUCT_DATA.VLP.name_sql}, {CACTUS_STRUCT_DATA.VLT.name_sql} from {self._idc} WHERE (substr({CACTUS_STRUCT_DATA.IDS.name_sql}, 1, instr({CACTUS_STRUCT_DATA.IDS.name_sql}, '.') - 1) IN ({', '.join(idos)}))"

		result_cells        = container.ExecSqlSelectMatrix(sql)
		if not result_cells.code == CODES_COMPLETION.COMPLETED: return T20_StructResult(code     = CODES_COMPLETION.INTERRUPTED,
		                                                                                subcodes = result_cells.subcodes)

		for raw_data in result_cells.data:
			try:
				ids     = raw_data[0]
				ido_idp = ids.split('.')
				ido     = ido_idp[0]
				idp     = ido_idp[1]
				vlp     = raw_data[1]
				vlt     = int(raw_data[2])

				self._data.append(T20_StructCell(idc=self._idc, ido=ido, idp=idp, vlp=vlp, vlt=vlt))
			except: continue

		result              = T20_StructResult()
		result.code         = CODES_COMPLETION.COMPLETED

		match len(self._data):
			case 0: result.subcodes.add(CODES_DATA.NO_DATA)
			case 1: result.subcodes.add(CODES_DATA.SINGLE)

		return result

	def _CaptureFromPostgresql(self, container: C32_ContainerPostgreSQL) -> T20_StructResult:
		""" Захват данных из контейнера PostgreSQL """
		self._data.clear()

		sql     : str       = f"SELECT DISTINCT {CACTUS_STRUCT_DATA.IDS.name_sql} FROM \"{self._idc}\" "

		result              = container.ExecSqlSelectVList(sql)
		if not result.code == CODES_COMPLETION.COMPLETED      : return T20_StructResult(code     = CODES_COMPLETION.INTERRUPTED,
		                                                                                subcodes = result.subcodes)

		capture_idos        = set(map(IdoFromIds, result.data))
		filters : list[str] = []

		for idp, filters_idp_vlp in self._filters_idp_vlp.items():
			for filter_idp_vlp in filters_idp_vlp: filters.append(self._TranslateFilterIdpVlpToPostgreSql(idp, filter_idp_vlp))

		for filter_item in filters:
			result       = container.ExecSqlSelectVList(sql + f" WHERE {filter_item}")
			if not result.code == CODES_COMPLETION.COMPLETED  : return T20_StructResult(code     = CODES_COMPLETION.INTERRUPTED,
		                                                                                subcodes = result.subcodes)

			capture_idos = capture_idos & set(map(IdoFromIds, result.data))

		idos                = list(map("'{}'".format, capture_idos))
		sql                 = f"SELECT {CACTUS_STRUCT_DATA.IDS.name_sql}, {CACTUS_STRUCT_DATA.VLP.name_sql}, {CACTUS_STRUCT_DATA.VLT.name_sql} from \"{self._idc}\" WHERE (split_part({CACTUS_STRUCT_DATA.IDS.name_sql}, '.', 1) IN ({', '.join(idos)}))"

		result_cells        = container.ExecSqlSelectMatrix(sql)
		if not result_cells.code == CODES_COMPLETION.COMPLETED: return T20_StructResult(code     = CODES_COMPLETION.INTERRUPTED,
		                                                                                subcodes = result_cells.subcodes)

		for raw_data in result_cells.data:
			try:
				ids     = raw_data[0]
				ido_idp = ids.split('.')
				ido     = ido_idp[0]
				idp     = ido_idp[1]
				vlp     = raw_data[1]
				vlt     = int(raw_data[2])

				self._data.append(T20_StructCell(idc=self._idc, ido=ido, idp=idp, vlp=vlp, vlt=vlt))
			except: continue

		result              = T20_StructResult()
		result.code         = CODES_COMPLETION.COMPLETED

		match len(self._data):
			case 0: result.subcodes.add(CODES_DATA.NO_DATA)
			case 1: result.subcodes.add(CODES_DATA.SINGLE)

		return result

	def Capture(self, container_name: str) -> T20_StructResult:
		""" Захват данных """
		if not self._idc                      : return T20_StructResult(code     =  CODES_COMPLETION.INTERRUPTED,
		                                                                subcodes = {CODES_DATA.NOT_ENOUGH})

		container = controller_containers.Container(container_name)
		if container is None                  : return T20_StructResult(code     =  CODES_COMPLETION.INTERRUPTED,
		                                                                subcodes = {CODES_CACTUS.NO_CONTAINER})

		if   container.Type_RAM().data        : return self._CaptureFromRam(container)
		elif container.Type_SQLite().data     : return self._CaptureFromSqlite(container)
		elif container.Type_PostgreSQL().data : return self._CaptureFromPostgresql(container)
		else                                  : return T20_StructResult(code     =  CODES_COMPLETION.INTERRUPTED,
		                                                                subcodes = {CODES_PROCESSING.SKIP})

	# ЗАПРОС IDO
	def Idos(self, sort_by_idp: str = None) -> T21_StructResult_List:
		""" Запрос IDO """
		idos   : set[str]             = set(map(lambda cell: cell.ido, self._data))
		if not idos           : return T21_StructResult_List(code     =  CODES_COMPLETION.INTERRUPTED,
		                                                     subcodes = {CODES_DATA.NOT_ENOUGH})

		if sort_by_idp is None: return T21_StructResult_List(code = CODES_COMPLETION.COMPLETED,
		                                                     data = list(idos))

		data   : list[T20_StructCell] = list(filter(lambda cell: cell.idp == sort_by_idp, self._data))
		values : list[list[str, str]] = list(map(lambda cell: [cell.ido, cell.vlp], data))
		values                        = DistinctAndSortList2D(values                = values,
		                                                      index_processing_item = 1,
		                                                      flag_distinct         = True,
		                                                      flag_sort             = True)

		result                        = T21_StructResult_List()
		result.code                   = CODES_COMPLETION.COMPLETED
		result.data                   = list(map(lambda item: item[0], values))

		match len(result.data):
			case 0: result.subcodes.add(CODES_DATA.NO_DATA)
			case 1: result.subcodes.add(CODES_DATA.SINGLE)

		return result

	# ЗАПРОС ДАННЫХ
	def ToStrings(self, idp: str, flag_distinct: bool = False, flag_sort: bool = False) -> T21_StructResult_List:
		""" Запрос VLP для IDP списком строк """
		data   : list[T20_StructCell] = list(filter(lambda cell: cell.idp == idp, self._data))
		values : list[str]            = list(map(lambda cell: cell.vlp, data))
		values                        = DistinctAndSortList1D(values        = values,
		                                                      flag_distinct = flag_distinct,
		                                                      flag_sort     = flag_sort)

		result                        = T21_StructResult_List()
		result.code                   = CODES_COMPLETION.COMPLETED
		result.data                   = values

		match len(result.data):
			case 0: result.subcodes.add(CODES_DATA.NO_DATA)
			case 1: result.subcodes.add(CODES_DATA.SINGLE)

		return result

	def ToIntegers(self, idp: str, flag_distinct: bool = False, flag_sort: bool = False) -> T21_StructResult_List:
		""" Запрос VLP для IDP списком целых чисел """
		data   : list[T20_StructCell] = list(filter(lambda cell: cell.idp == idp, self._data))
		values : list                 = list(map(lambda cell: cell.vlp, data))

		try   : values = StringsToIntegers(values)
		except: return T21_StructResult_List(code     =  CODES_COMPLETION.INTERRUPTED,
		                                     subcodes = {CODES_DATA.ERROR_CONVERT})

		values                        = DistinctAndSortList1D(values        = values,
		                                                      flag_distinct = flag_distinct,
		                                                      flag_sort     = flag_sort)

		result                        = T21_StructResult_List()
		result.code                   = CODES_COMPLETION.COMPLETED
		result.data                   = values

		match len(result.data):
			case 0: result.subcodes.add(CODES_DATA.NO_DATA)
			case 1: result.subcodes.add(CODES_DATA.SINGLE)

		return result

	def ToFloats(self, idp: str, flag_distinct: bool = False, flag_sort: bool = False) -> T21_StructResult_List:
		""" Запрос VLP для IDP списком дробных чисел """
		data   : list[T20_StructCell] = list(filter(lambda cell: cell.idp == idp, self._data))
		values : list                 = list(map(lambda cell: cell.vlp, data))

		try   : values = StringsToFloats(values)
		except: return T21_StructResult_List(code     =  CODES_COMPLETION.INTERRUPTED,
		                                     subcodes = {CODES_DATA.ERROR_CONVERT})

		values                        = DistinctAndSortList1D(values        = values,
		                                                      flag_distinct = flag_distinct,
		                                                      flag_sort     = flag_sort)

		result                        = T21_StructResult_List()
		result.code                   = CODES_COMPLETION.COMPLETED
		result.data                   = values

		match len(result.data):
			case 0: result.subcodes.add(CODES_DATA.NO_DATA)
			case 1: result.subcodes.add(CODES_DATA.SINGLE)

		return result

	def ToBooleans(self, idp: str, flag_distinct: bool = False, flag_sort: bool = False) -> T21_StructResult_List:
		""" Запрос VLP для IDP списком логических значений """
		data   : list[T20_StructCell] = list(filter(lambda cell: cell.idp == idp, self._data))
		values : list                 = list(map(lambda cell: cell.vlp, data))

		try   : values = StringsToBooleans(values)
		except: return T21_StructResult_List(code     =  CODES_COMPLETION.INTERRUPTED,
		                                     subcodes = {CODES_DATA.ERROR_CONVERT})

		values                        = DistinctAndSortList1D(values        = values,
		                                                      flag_distinct = flag_distinct,
		                                                      flag_sort     = flag_sort)

		result                        = T21_StructResult_List()
		result.code                   = CODES_COMPLETION.COMPLETED
		result.data                   = values

		match len(result.data):
			case 0: result.subcodes.add(CODES_DATA.NO_DATA)
			case 1: result.subcodes.add(CODES_DATA.SINGLE)

		return result

	def ToDateTimes(self, idp: str, flag_distinct: bool = False, flag_sort: bool = False) -> T21_StructResult_List:
		""" Запрос VLP для IDP списком отметок даты-времени """
		data   : list[T20_StructCell] = list(filter(lambda cell: cell.idp == idp, self._data))
		values : list                 = list(map(lambda cell: cell.vlp, data))

		try   : values = StringsToDatetimes(values)
		except: return T21_StructResult_List(code     =  CODES_COMPLETION.INTERRUPTED,
		                                     subcodes = {CODES_DATA.ERROR_CONVERT})

		values                        = DistinctAndSortList1D(values        = values,
		                                                      flag_distinct = flag_distinct,
		                                                      flag_sort     = flag_sort)

		result                        = T21_StructResult_List()
		result.code                   = CODES_COMPLETION.COMPLETED
		result.data                   = values

		match len(result.data):
			case 0: result.subcodes.add(CODES_DATA.NO_DATA)
			case 1: result.subcodes.add(CODES_DATA.SINGLE)

		return result


class C31_FilterLinear2D(C30_FilterLinear1D):
	""" Линейный 2D-Фильтр для структурного объекта """

	# Запрос данных
	def ToStringsWithIdos(self, idp: str, flag_distinct: bool = False, flag_sort: bool = False) -> T21_StructResult_List:
		""" Запрос IDO-CLV для IDP со списком строк """
		data   : list[T20_StructCell] = list(filter(lambda cell: cell.idp == idp, self._data))
		values : list[list[str, str]] = list(map(lambda cell: [cell.ido, cell.vlp], data))
		values                        = DistinctAndSortList2D(values                = values,
		                                                      index_processing_item = 1,
		                                                      flag_distinct         = flag_distinct,
		                                                      flag_sort             = flag_sort)

		result                        = T21_StructResult_List()
		result.code                   = CODES_COMPLETION.COMPLETED
		result.data                   = values

		match len(result.data):
			case 0: result.subcodes.add(CODES_DATA.NO_DATA)
			case 1: result.subcodes.add(CODES_DATA.SINGLE)

		return result

	def ToIntegersWithIdos(self, idp: str, flag_distinct: bool = False, flag_sort: bool = False) -> T21_StructResult_List:
		""" Запрос IDO-CLV для IDP со списком целых чисел """
		data   : list[T20_StructCell] = list(filter(lambda cell: cell.idp == idp, self._data))
		values : list[list[str, int]] = list(map(lambda cell: [cell.ido, StringToInteger(cell.vlp)], data))
		values                        = DistinctAndSortList2D(values                = values,
		                                                      index_processing_item = 1,
		                                                      flag_distinct         = flag_distinct,
		                                                      flag_sort             = flag_sort)

		result                        = T21_StructResult_List()
		result.code                   = CODES_COMPLETION.COMPLETED
		result.data                   = values

		match len(result.data):
			case 0: result.subcodes.add(CODES_DATA.NO_DATA)
			case 1: result.subcodes.add(CODES_DATA.SINGLE)

		return result

	def ToFloatsWithIdos(self, idp: str, flag_distinct: bool = False, flag_sort: bool = False) -> T21_StructResult_List:
		""" Запрос IDO-CLV для IDP со списком дробных чисел """
		data   : list[T20_StructCell]   = list(filter(lambda cell: cell.idp == idp, self._data))
		values : list[list[str, float]] = list(map(lambda cell: [cell.ido, StringToFloat(cell.vlp)], data))
		values                          = DistinctAndSortList2D(values                = values,
		                                                      index_processing_item = 1,
		                                                      flag_distinct         = flag_distinct,
		                                                      flag_sort             = flag_sort)

		result                          = T21_StructResult_List()
		result.code                     = CODES_COMPLETION.COMPLETED
		result.data                     = values

		match len(result.data):
			case 0: result.subcodes.add(CODES_DATA.NO_DATA)
			case 1: result.subcodes.add(CODES_DATA.SINGLE)

		return result

	def ToBooleansWithIdos(self, idp: str, flag_distinct: bool = False, flag_sort: bool = False) -> T21_StructResult_List:
		""" Запрос IDO-CLV для IDP со списком логических значений """
		data   : list[T20_StructCell]  = list(filter(lambda cell: cell.idp == idp, self._data))
		values : list[list[str, bool]] = list(map(lambda cell: [cell.ido, StringToBoolean(cell.vlp)], data))
		values                         = DistinctAndSortList2D(values                = values,
		                                                      index_processing_item = 1,
		                                                      flag_distinct         = flag_distinct,
		                                                      flag_sort             = flag_sort)

		result                         = T21_StructResult_List()
		result.code                    = CODES_COMPLETION.COMPLETED
		result.data                    = values

		match len(result.data):
			case 0: result.subcodes.add(CODES_DATA.NO_DATA)
			case 1: result.subcodes.add(CODES_DATA.SINGLE)

		return result

	def ToDateTimesWithIdos(self, idp: str, flag_distinct: bool = False, flag_sort: bool = False) -> T21_StructResult_List:
		""" Запрос IDO-CLV для IDP со списком DateTime """
		data   : list[T20_StructCell]      = list(filter(lambda cell: cell.idp == idp, self._data))
		values : list[list[str, datetime.datetime | None]] = list(map(lambda cell: [cell.ido, StringToDateTime(cell.vlp)], data))
		values                             = DistinctAndSortList2D(values                = values,
		                                                      index_processing_item = 1,
		                                                      flag_distinct         = flag_distinct,
		                                                      flag_sort             = flag_sort)

		result                             = T21_StructResult_List()
		result.code                        = CODES_COMPLETION.COMPLETED
		result.data                        = values

		match len(result.data):
			case 0: result.subcodes.add(CODES_DATA.NO_DATA)
			case 1: result.subcodes.add(CODES_DATA.SINGLE)

		return result
