# КАКТУС: ЛИНЕЙНЫЕ ФИЛЬТРЫ ДАННЫХ
# 2022-12-01

from G00_cactus_codes                 import SQL_SID, \
											 SQL_CVL, \
											 SQL_CUT
from G00_filter_codes                 import FILTER_EQUAL,   \
											 FILTER_MORE,    \
											 FILTER_LESS,    \
											 FILTER_INCLUDE, \
											 FILTER_IN,      \
											 FILTER_BETWEEN
from G00_result_codes                 import RESULT_ERROR_ACCESS_CONNECTION, \
											 RESULT_ERROR_CONVERT,           \
											 RESULT_ERROR_DATA_NOT_ENOUGH,   \
											 RESULT_ERROR_EXEC,              \
											 RESULT_OK,                      \
											 RESULT_OK_SKIP,                 \
											 RESULT_WARNING_NO_DATA
from G10_cactus_convertors            import AnyToString,        \
											 AnyToStrings,       \
											 StringToInteger,    \
											 StringToBoolean,    \
											 StringToDateTime,   \
											 StringsToIntegers,  \
											 StringsToFloats,    \
											 StringsToBooleans,  \
											 StringsToDatetimes, \
											 StringToFloat,      \
											 OidFromSid,         \
											 UnificationOci
from G10_list                         import DistinctAndSortList1D, \
											 DistinctAndSortList2D
from G10_math_linear                  import CheckBetween
from G20_meta_frame                   import C20_MetaFrame
from G30_cactus_controller_containers import controller_containers
from G30_cactus_struct                import T30_StructCell, \
											 T30_FilterD1,   \
											 T30_ResultCode
from G31_cactus_struct                import T31_ResultList
from G31_cactus_container_ram         import C31_ContainerRAM
from G32_cactus_container_sql         import C32_ContainerSQLite,    \
											 C32_ContainerPostgreSQL


class C30_FilterLinear1D(C20_MetaFrame):
	""" Линейный 1D-фильтр для структурного объекта """

	def __init__(self, oci: str):
		super().__init__()

		self._oci = oci

	def Init_00(self):
		super().Init_00()

		self._oci             : str                           = ""
		self._data            : list[T30_StructCell]          = []
		self._filters_pid_cvl : dict[str, list[T30_FilterD1]] = dict()

	# УПРАВЛЕНИЕ ФИЛЬТРАЦИЕЙ
	def _AppendFilterPidCvl(self, filter_type: int, pid: str, data: any, flag_invert: bool, flag_include: bool) -> T30_ResultCode:
		""" Добавление фильтра PID-CVL """
		try   :
			value  : str       = ""
			values : list[str] = []

			if type(data) is list: values = AnyToStrings(data)
			else                 : value  = AnyToString(data)

			filter_item        = T30_FilterD1(flag_invert, flag_include, filter_type, value, values)
			filters            = self._filters_pid_cvl.get(pid, [])
			filters.append(filter_item)
			self._filters_pid_cvl[pid] = filters

		except: return T30_ResultCode(RESULT_ERROR_CONVERT)

		return T30_ResultCode(RESULT_OK)

	def FilterPidCvlByEqual(self, pid: str, value: any, flag_invert: bool = False) -> T30_ResultCode:
		""" Фильтрация PID-CVL: Значение равно value """
		return self._AppendFilterPidCvl(filter_type  = FILTER_EQUAL,
										pid          = pid,
										data         = value,
										flag_invert  = flag_invert,
										flag_include = True)

	def FilterPidCvlByMore(self, pid: str, value: int | float, flag_invert: bool = False, flag_include: bool = False) -> T30_ResultCode:
		""" Фильтрация PID-CVL: Значение больше чем value """
		return self._AppendFilterPidCvl(filter_type  = FILTER_MORE,
										pid          = pid,
										data         = value,
										flag_invert  = flag_invert,
										flag_include = flag_include)

	def FilterPidCvlByLess(self, pid: str, value: int | float, flag_invert: bool = False, flag_include: bool = False) -> T30_ResultCode:
		""" Фильтрация PID-CVL: Значение меньше чем value """
		return self._AppendFilterPidCvl(filter_type  = FILTER_LESS,
										pid          = pid,
										data         = value,
										flag_invert  = flag_invert,
										flag_include = flag_include)

	def FilterPidCvlByInclude(self, pid: str, value: str | int | float, flag_invert: bool = False) -> T30_ResultCode:
		""" Фильтрация PID-CVL: Значение включает в себя value """
		return self._AppendFilterPidCvl(filter_type  = FILTER_INCLUDE,
										pid          = pid,
										data         = value,
										flag_invert  = flag_invert,
										flag_include = True)

	def FilterPidCvlByIn(self, pid: str, values: list[str] | list[int] | list[float], flag_invert: bool = False) -> T30_ResultCode:
		""" Фильтрация PID-CVL: Value включает в себя значение """
		return self._AppendFilterPidCvl(filter_type  = FILTER_IN,
										pid          = pid,
										data         = values,
										flag_invert  = flag_invert,
										flag_include = True)

	def FilterPidCvlByBetween(self, pid: str, value_l : int | float, value_r: int | float, flag_invert: bool = False, flag_include: bool = False) -> T30_ResultCode:
		""" Фильтрация PID-CVL: Значение в пределах value """
		return self._AppendFilterPidCvl(filter_type  = FILTER_BETWEEN,
										pid          = pid,
										data         = [value_l, value_r],
										flag_invert  = flag_invert,
										flag_include = flag_include)

	def ResetFiltersPidCvl(self, pid: str = None) -> T30_ResultCode:
		""" Сброс фильтрации """

		if pid is None:
			self._filters_pid_cvl.clear()
			return T30_ResultCode(RESULT_OK)

		elif pid in self._filters_pid_cvl:
			del self._filters_pid_cvl[pid]
			return T30_ResultCode(RESULT_OK)

		return T30_ResultCode(RESULT_OK_SKIP)

	# ЗАХВАТ ДАННЫХ
	def _ApplyOci(self, cell: T30_StructCell) -> bool:
		""" Применение фильтрации по Oci """
		return cell.oci == self._oci

	def _ApplyFilterPidCvl(self, cvl: str, filter_pid_cvl: T30_FilterD1) -> bool:
		""" Применение фильтра PID-CVL """
		flag_success: bool = False

		try:
			if   filter_pid_cvl.filter_type == FILTER_EQUAL   : flag_success = cvl == filter_pid_cvl.filter_value

			elif filter_pid_cvl.filter_type == FILTER_MORE    :
				if filter_pid_cvl.flag_include:	                flag_success = StringToFloat(cvl) >= StringToFloat(filter_pid_cvl.filter_value)
				else                          :                 flag_success = StringToFloat(cvl) >  StringToFloat(filter_pid_cvl.filter_value)

			elif filter_pid_cvl.filter_type == FILTER_LESS    :
				if filter_pid_cvl.flag_include:	                flag_success = StringToFloat(cvl) <= StringToFloat(filter_pid_cvl.filter_value)
				else                          :                 flag_success = StringToFloat(cvl) <  StringToFloat(filter_pid_cvl.filter_value)

			elif filter_pid_cvl.filter_type == FILTER_INCLUDE : flag_success = filter_pid_cvl.filter_value in cvl

			elif filter_pid_cvl.filter_type == FILTER_IN      : flag_success = cvl in filter_pid_cvl.filter_values

			elif filter_pid_cvl.filter_type == FILTER_BETWEEN : flag_success = CheckBetween(StringToFloat(filter_pid_cvl.filter_values[0]), StringToFloat(cvl), StringToFloat(filter_pid_cvl.filter_values[1]), flag_include=filter_pid_cvl.flag_include)

		except: return False

		return flag_success ^ filter_pid_cvl.flag_invert

	def _ApplyFiltersPidCvl(self, cell) -> bool:
		""" Применение фильтрации по PID-CVL """
		if not self._filters_pid_cvl                                : return True

		filters_pid_cvl = self._filters_pid_cvl.get(cell.pid, [])
		if not filters_pid_cvl                                      : return False

		for filter_pid_cvl in filters_pid_cvl:
			if not self._ApplyFilterPidCvl(cell.cvl, filter_pid_cvl): return False

		return True

	def _CaptureFromRam(self, container: C31_ContainerRAM) -> T30_ResultCode:
		""" Захват данных из контейнера RAM """
		self._data.clear()

		oids : set[str] = set()

		for cell in container._s_cells.values():
			if not self._ApplyOci(cell)          : continue
			if not self._ApplyFiltersPidCvl(cell): continue

			oids.add(cell.oid)

		if not oids: return T30_ResultCode(RESULT_WARNING_NO_DATA)

		self._data = list(filter(lambda cell: cell.oid in oids, container._s_cells.values()))

		return T30_ResultCode(RESULT_OK)

	def _TranslateFilterPidCvlToSqlite(self, pid: str, filter_pid_cvl: T30_FilterD1) -> str:
		""" Трансляция фильтра в SQLite диалект """
		sql : str = f"({SQL_SID} LIKE '%.{pid}') AND "

		if   filter_pid_cvl.filter_type == FILTER_EQUAL   : sql += f"({'NOT ' if filter_pid_cvl.flag_invert else ''}{SQL_CVL} = '{filter_pid_cvl.filter_value}')"

		elif filter_pid_cvl.filter_type == FILTER_MORE    :
			if filter_pid_cvl.flag_include:                 sql += f"({'NOT ' if filter_pid_cvl.flag_invert else ''}{SQL_CVL} >= '{filter_pid_cvl.filter_value}')"
			else                          :                 sql += f"({'NOT ' if filter_pid_cvl.flag_invert else ''}{SQL_CVL} >  '{filter_pid_cvl.filter_value}')"

		elif filter_pid_cvl.filter_type == FILTER_LESS    :
			if filter_pid_cvl.flag_include:                 sql += f"({'NOT ' if filter_pid_cvl.flag_invert else ''}{SQL_CVL} <= '{filter_pid_cvl.filter_value}')"
			else                          :                 sql += f"({'NOT ' if filter_pid_cvl.flag_invert else ''}{SQL_CVL} <  '{filter_pid_cvl.filter_value}')"

		elif filter_pid_cvl.filter_type == FILTER_INCLUDE : sql += f"({'NOT ' if filter_pid_cvl.flag_invert else ''}{SQL_CVL} LIKE '%{filter_pid_cvl.filter_value}%')"

		elif filter_pid_cvl.filter_type == FILTER_IN      :
			values : list[str] = list(map("'{}'".format, filter_pid_cvl.filter_values))
			sql               += f"({'NOT ' if filter_pid_cvl.flag_invert else ''}{SQL_CVL} IN ({', '.join(values)}))"

		elif filter_pid_cvl.filter_type == FILTER_BETWEEN :
			value_l : str = filter_pid_cvl.filter_values[0]
			value_r : str = filter_pid_cvl.filter_values[1]

			sql          += f"({'NOT ' if filter_pid_cvl.flag_invert else ''}"

			if filter_pid_cvl.flag_include: sql += f"(({SQL_CVL} >= {value_l}) AND ({SQL_CVL} <= {value_r}))"
			else                          : sql += f"(({SQL_CVL} > {value_l}) AND ({SQL_CVL} < {value_r}))"

			sql          += ")"

		else: return ""

		return f"({sql})"

	def _TranslateFilterPidCvlToPostgreSql(self, pid: str, filter_pid_cvl: T30_FilterD1) -> str:
		""" Трансляция фильтра в SQLite диалект """
		sql : str = f"({SQL_SID} LIKE '%.{pid}') AND "

		if   filter_pid_cvl.filter_type == FILTER_EQUAL   : sql += f"({'NOT ' if filter_pid_cvl.flag_invert else ''}{SQL_CVL} = '{filter_pid_cvl.filter_value}')"

		elif filter_pid_cvl.filter_type == FILTER_MORE    :
			if filter_pid_cvl.flag_include:                 sql += f"({'NOT ' if filter_pid_cvl.flag_invert else ''}{SQL_CVL} >= '{filter_pid_cvl.filter_value}')"
			else                          :                 sql += f"({'NOT ' if filter_pid_cvl.flag_invert else ''}{SQL_CVL} >  '{filter_pid_cvl.filter_value}')"

		elif filter_pid_cvl.filter_type == FILTER_LESS    :
			if filter_pid_cvl.flag_include:                 sql += f"({'NOT ' if filter_pid_cvl.flag_invert else ''}{SQL_CVL} <= '{filter_pid_cvl.filter_value}')"
			else                          :                 sql += f"({'NOT ' if filter_pid_cvl.flag_invert else ''}{SQL_CVL} <  '{filter_pid_cvl.filter_value}')"

		elif filter_pid_cvl.filter_type == FILTER_INCLUDE : sql += f"({'NOT ' if filter_pid_cvl.flag_invert else ''}{SQL_CVL} LIKE '%{filter_pid_cvl.filter_value}%')"

		elif filter_pid_cvl.filter_type == FILTER_IN      :
			values : list[str] = list(map("'{}'".format, filter_pid_cvl.filter_values))
			sql               += f"({'NOT ' if filter_pid_cvl.flag_invert else ''}{SQL_CVL} IN ({', '.join(values)}))"

		elif filter_pid_cvl.filter_type == FILTER_BETWEEN :
			value_l : str = filter_pid_cvl.filter_values[0]
			value_r : str = filter_pid_cvl.filter_values[1]

			sql          += f"({'NOT ' if filter_pid_cvl.flag_invert else ''}"

			if filter_pid_cvl.flag_include: sql += f"(({SQL_CVL}::float >= {value_l}) AND ({SQL_CVL}::float <= {value_r}))"
			else                          : sql += f"(({SQL_CVL}::float > {value_l}) AND ({SQL_CVL}::float < {value_r}))"

			sql          += ")"

		else: return ""

		return f"({sql})"

	def _CaptureFromSqlite(self, container: C32_ContainerSQLite) -> T30_ResultCode:
		""" Захват данных из контейнера SQLite """
		self._data.clear()

		sql     : str       = f"SELECT DISTINCT {SQL_SID} FROM {UnificationOci(self._oci)} "
		result              = container.ExecSqlSelectVList(sql)
		if not result.code == RESULT_OK      : return T30_ResultCode(result.code)
		capture_oids = set(map(OidFromSid, result.items))

		filters : list[str] = []

		for pid, filters_pid_cvl in self._filters_pid_cvl.items():
			for filter_pid_cvl in filters_pid_cvl: filters.append(self._TranslateFilterPidCvlToSqlite(pid, filter_pid_cvl))

		for filter_item in filters:
			result       = container.ExecSqlSelectVList(sql + f" WHERE {filter_item}")
			if not result.code == RESULT_OK  : return T30_ResultCode(result.code)
			capture_oids = capture_oids & set(map(OidFromSid, result.items))

		oids                = list(map("'{}'".format, capture_oids))
		sql                 = f"SELECT {SQL_SID}, {SQL_CVL}, {SQL_CUT} from {UnificationOci(self._oci)} WHERE (substr({SQL_SID}, 1, instr({SQL_SID}, '.') - 1) IN ({', '.join(oids)}))"

		result_cells        = container.ExecSqlSelectMatrix(sql)
		if not result_cells.code == RESULT_OK: return T30_ResultCode(result_cells.code)

		for raw_data in result_cells.items:
			try:
				sid     = raw_data[0]
				oid_pid = sid.split('.')
				oid     = oid_pid[0]
				pid     = oid_pid[1]
				cvl     = raw_data[1]
				cut     = int(raw_data[2])

				self._data.append(T30_StructCell(oci=self._oci, oid=oid, pid=pid, cvl=cvl, cut=cut))
			except: continue

		if not self._data                   : return T30_ResultCode(RESULT_WARNING_NO_DATA)

		return T30_ResultCode(RESULT_OK)

	def _CaptureFromPostgresql(self, container: C32_ContainerPostgreSQL) -> T30_ResultCode:
		""" Захват данных из контейнера PostgreSQL """
		self._data.clear()

		sql     : str       = f"SELECT DISTINCT {SQL_SID} FROM \"{UnificationOci(self._oci)}\" "

		result              = container.ExecSqlSelectVList(sql)
		if not result.code == RESULT_OK      : return T30_ResultCode(result.code)

		capture_oids        = set(map(OidFromSid, result.items))
		filters : list[str] = []

		for pid, filters_pid_cvl in self._filters_pid_cvl.items():
			for filter_pid_cvl in filters_pid_cvl: filters.append(self._TranslateFilterPidCvlToPostgreSql(pid, filter_pid_cvl))

		for filter_item in filters:
			result       = container.ExecSqlSelectVList(sql + f" WHERE {filter_item}")
			if not result.code == RESULT_OK  : return T30_ResultCode(result.code)

			capture_oids = capture_oids & set(map(OidFromSid, result.items))

		oids                = list(map("'{}'".format, capture_oids))
		sql                 = f"SELECT {SQL_SID}, {SQL_CVL}, {SQL_CUT} from \"{UnificationOci(self._oci)}\" WHERE (split_part({SQL_SID}, '.', 1) IN ({', '.join(oids)}))"

		result_cells        = container.ExecSqlSelectMatrix(sql)
		if not result_cells.code == RESULT_OK: return T30_ResultCode(result_cells.code)

		for raw_data in result_cells.items:
			try:
				sid     = raw_data[0]
				oid_pid = sid.split('.')
				oid     = oid_pid[0]
				pid     = oid_pid[1]
				cvl     = raw_data[1]
				cut     = int(raw_data[2])

				self._data.append(T30_StructCell(oci=self._oci, oid=oid, pid=pid, cvl=cvl, cut=cut))
			except: continue

		if not self._data                    : return T30_ResultCode(RESULT_WARNING_NO_DATA)

		return T30_ResultCode(RESULT_OK)

	def Capture(self, container_name: str) -> T30_ResultCode:
		""" Захват данных """
		if not self._oci                      : return T31_ResultList(RESULT_ERROR_DATA_NOT_ENOUGH)

		container = controller_containers.GetContainer(container_name)
		if container is None                  : return T31_ResultList(RESULT_ERROR_ACCESS_CONNECTION)

		if   container.TypeIsRAM().flag       : return self._CaptureFromRam(container)
		elif container.TypeIsSQLite().flag    : return self._CaptureFromSqlite(container)
		elif container.TypeIsPostgreSQL().flag: return self._CaptureFromPostgresql(container)

		return T30_ResultCode(RESULT_ERROR_EXEC)

	# ЗАПРОС OID
	def Oids(self, sort_by_pid: str = None) -> T31_ResultList:
		""" Запрос OID """
		oids   : set[str]             = set(map(lambda cell: cell.oid, self._data))
		if not oids: return T31_ResultList(RESULT_WARNING_NO_DATA)

		if sort_by_pid is None: return T31_ResultList(RESULT_OK, list(oids))

		data   : list[T30_StructCell] = list(filter(lambda cell: cell.pid == sort_by_pid, self._data))
		values : list[list[str, str]] = list(map(lambda cell: [cell.oid, cell.cvl], data))
		values                        = DistinctAndSortList2D(values, 1, True, True)
		if not values: return T31_ResultList(RESULT_WARNING_NO_DATA)

		return T31_ResultList(RESULT_OK, list(map(lambda item: item[0], values)))

	# ЗАПРОС ДАННЫХ
	def ToStrings(self, pid: str, flag_distinct: bool = False, flag_sort: bool = False) -> T31_ResultList:
		""" Запрос CVL для PID списком строк """
		data   : list[T30_StructCell] = list(filter(lambda cell: cell.pid == pid, self._data))
		values : list[str]            = list(map(lambda cell: cell.cvl, data))
		values                        = DistinctAndSortList1D(values, flag_distinct=flag_distinct, flag_sort=flag_sort)
		if not values: return T31_ResultList(RESULT_WARNING_NO_DATA)

		return T31_ResultList(RESULT_OK, values)

	def ToIntegers(self, pid: str, flag_distinct: bool = False, flag_sort: bool = False) -> T31_ResultList:
		""" Запрос CVL для PID списком целых чисел """
		data   : list[T30_StructCell] = list(filter(lambda cell: cell.pid == pid, self._data))
		values : list                 = list(map(lambda cell: cell.cvl, data))

		try   : values = StringsToIntegers(values)
		except: return T31_ResultList(RESULT_ERROR_CONVERT)

		values                        = DistinctAndSortList1D(values, flag_distinct=flag_distinct, flag_sort=flag_sort)
		if not values: return T31_ResultList(RESULT_WARNING_NO_DATA)

		return T31_ResultList(RESULT_OK, values)

	def ToFloats(self, pid: str, flag_distinct: bool = False, flag_sort: bool = False) -> T31_ResultList:
		""" Запрос CVL для PID списком дробных чисел """
		data   : list[T30_StructCell] = list(filter(lambda cell: cell.pid == pid, self._data))
		values : list                 = list(map(lambda cell: cell.cvl, data))

		try   : values = StringsToFloats(values)
		except: return T31_ResultList(RESULT_ERROR_CONVERT)

		values                        = DistinctAndSortList1D(values, flag_distinct=flag_distinct, flag_sort=flag_sort)
		if not values: return T31_ResultList(RESULT_WARNING_NO_DATA)

		return T31_ResultList(RESULT_OK, values)

	def ToBooleans(self, pid: str, flag_distinct: bool = False, flag_sort: bool = False) -> T31_ResultList:
		""" Запрос CVL для PID списком логических значений """
		data   : list[T30_StructCell] = list(filter(lambda cell: cell.pid == pid, self._data))
		values : list                 = list(map(lambda cell: cell.cvl, data))

		try   : values = StringsToBooleans(values)
		except: return T31_ResultList(RESULT_ERROR_CONVERT)

		values                        = DistinctAndSortList1D(values, flag_distinct=flag_distinct, flag_sort=flag_sort)
		if not values: return T31_ResultList(RESULT_WARNING_NO_DATA)

		return T31_ResultList(RESULT_OK, values)

	def ToDateTimes(self, pid: str, flag_distinct: bool = False, flag_sort: bool = False) -> T31_ResultList:
		""" Запрос CVL для PID списком отметок даты-времени """
		data   : list[T30_StructCell] = list(filter(lambda cell: cell.pid == pid, self._data))
		values : list                 = list(map(lambda cell: cell.cvl, data))

		try   : values = StringsToDatetimes(values)
		except: return T31_ResultList(RESULT_ERROR_CONVERT)

		values                        = DistinctAndSortList1D(values, flag_distinct=flag_distinct, flag_sort=flag_sort)
		if not values: return T31_ResultList(RESULT_WARNING_NO_DATA)

		return T31_ResultList(RESULT_OK, values)


class C31_FilterLinear2D(C30_FilterLinear1D):
	""" Линейный 2D-Фильтр для структурного объекта """

	# Запрос данных
	def ToStringsWithOids(self, pid: str, flag_distinct: bool = False, flag_sort: bool = False) -> T31_ResultList:
		""" Запрос OID-CLV для PID со списком строк """
		data   : list[T30_StructCell] = list(filter(lambda cell: cell.pid == pid, self._data))
		values : list[list[str, str]] = list(map(lambda cell: [cell.oid, cell.cvl], data))
		values                        = DistinctAndSortList2D(values, 1, flag_distinct=flag_distinct, flag_sort=flag_sort)
		if not values: return T31_ResultList(RESULT_WARNING_NO_DATA)

		return T31_ResultList(RESULT_OK, values)

	def ToIntegersWithOids(self, pid: str, flag_distinct: bool = False, flag_sort: bool = False) -> T31_ResultList:
		""" Запрос OID-CLV для PID со списком целых чисел """
		data   : list[T30_StructCell] = list(filter(lambda cell: cell.pid == pid, self._data))
		values : list[list[str, str]] = list(map(lambda cell: [cell.oid, StringToInteger(cell.cvl)], data))
		values                        = DistinctAndSortList2D(values, 1, flag_distinct=flag_distinct, flag_sort=flag_sort)
		if not values: return T31_ResultList(RESULT_WARNING_NO_DATA)

		return T31_ResultList(RESULT_OK, values)

	def ToFloatsWithOids(self, pid: str, flag_distinct: bool = False, flag_sort: bool = False) -> T31_ResultList:
		""" Запрос OID-CLV для PID со списком дробных чисел """
		data   : list[T30_StructCell] = list(filter(lambda cell: cell.pid == pid, self._data))
		values : list[list[str, str]] = list(map(lambda cell: [cell.oid, StringToFloat(cell.cvl)], data))
		values                        = DistinctAndSortList2D(values, 1, flag_distinct=flag_distinct, flag_sort=flag_sort)
		if not values: return T31_ResultList(RESULT_WARNING_NO_DATA)

		return T31_ResultList(RESULT_OK, values)

	def ToBooleansWithOids(self, pid: str, flag_distinct: bool = False, flag_sort: bool = False) -> T31_ResultList:
		""" Запрос OID-CLV для PID со списком логических значений """
		data   : list[T30_StructCell] = list(filter(lambda cell: cell.pid == pid, self._data))
		values : list[list[str, str]] = list(map(lambda cell: [cell.oid, StringToBoolean(cell.cvl)], data))
		values                        = DistinctAndSortList2D(values, 1, flag_distinct=flag_distinct, flag_sort=flag_sort)
		if not values: return T31_ResultList(RESULT_WARNING_NO_DATA)

		return T31_ResultList(RESULT_OK, values)

	def ToDateTimesWithOids(self, pid: str, flag_distinct: bool = False, flag_sort: bool = False) -> T31_ResultList:
		""" Запрос OID-CLV для PID со списком DateTime """
		data   : list[T30_StructCell] = list(filter(lambda cell: cell.pid == pid, self._data))
		values : list[list[str, str]] = list(map(lambda cell: [cell.oid, StringToDateTime(cell.cvl)], data))
		values                        = DistinctAndSortList2D(values, 1, flag_distinct=flag_distinct, flag_sort=flag_sort)
		if not values: return T31_ResultList(RESULT_WARNING_NO_DATA)

		return T31_ResultList(RESULT_OK, values)
