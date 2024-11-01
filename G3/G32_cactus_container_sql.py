# КАКТУС: КОНТЕЙНЕР-SQL
# 01 ноя 2024

import psycopg2
import sqlite3
import s3m

from   copy                     import  copy

from   G00_cactus_codes         import (CONTAINERS,
                                        CACTUS_STRUCT_DATA)
from   G00_status_codes         import (CODES_COMPLETION,
                                        CODES_PROCESSING,
                                        CODES_DB,
                                        CODES_DATA)

from   G10_cactus_check         import (CheckIdc,
                                        CheckIdo,
                                        CheckIdp)
from   G10_cactus_convertors    import (IdoFromIds,
                                        IdpFromIds)
from   G10_list                 import  DifferenceLists

from   G20_cactus_struct        import  T20_StructCell
from   G21_cactus_struct        import (T21_StructResult_CursorS3m,
                                        T21_StructResult_StructCell,
                                        T21_StructResult_StructCells,
                                        T21_StructResult_VltRange,
                                        T21_VltRange,
                                        T21_StructResult_CursorPostgresql)
from   G21_struct_result        import (T21_StructResult_String,
                                        T21_StructResult_Bool,
                                        T21_StructResult_Int,
                                        T21_StructResult_List)

from   G31_cactus_container_sql import  C31_ContainerSQL


# КАКТУС: КОНТЕЙНЕР-SQLite
class C32_ContainerSQLite(C31_ContainerSQL):
	""" Кактус: Контейнер SQLite """

	# Модель данных
	def Init_00(self):
		super().Init_00()

		self._options_filename : str = ""

	def Init_01(self):
		super().Init_01()

		self._container_type = CONTAINERS.SQLITE

	def Init_10(self):
		super().Init_10()

		self.connection : s3m.Connection | None = None

	# Механика данных: Параметры подключения
	def OptionsFilename(self, filename: str = None) -> T21_StructResult_String:
		""" Запрос/Установка параметра подключения: Имя файла """
		if filename is None: return T21_StructResult_String(code = CODES_COMPLETION.COMPLETED,
															data = self._options_filename)

		else               :                                       self._options_filename = filename

	# Механика данных: Состояния
	def StateConnected(self) -> T21_StructResult_Bool:
		""" Запрос состояния подключения """
		result      = T21_StructResult_Bool()
		result.code = CODES_COMPLETION.COMPLETED
		result.data = False

		if self.connection is None: return result

		try    : self.connection.cursor()
		except : return result

		result.data = True

		return result

	# Механика управления: Управление подключением
	def Connect(self) -> T21_StructResult_Bool:
		""" Подключение к СУБД """
		if self.StateConnected().data:
			return T21_StructResult_Bool(code     = CODES_COMPLETION.COMPLETED,
										 subcodes = {CODES_PROCESSING.SKIP})

		self.connection = None
		
		try   :
			self.connection = s3m.Connection(path              = f"{self.OptionsFilename().data}.sqlite",
											 isolation_level   = None,
											 check_same_thread = False)
		except:
			return T21_StructResult_Bool(code     = CODES_COMPLETION.INTERRUPTED,
										 subcodes = {CODES_DB.ERROR_CONNECTION})

		try   :
			cursor = self.connection.cursor()
			cursor.execute('PRAGMA journal_mode=MEMORY;')
		except:
			pass

		self.PrepareDisconnect()

		return T21_StructResult_Bool(code = CODES_COMPLETION.COMPLETED,
									 data = True)

	def Disconnect(self) -> T21_StructResult_Bool:
		""" Отключение от СУБД """
		if self.connection is None:
			return T21_StructResult_Bool(code     = CODES_COMPLETION.COMPLETED,
										 subcodes = {CODES_PROCESSING.SKIP},
										 data     = True)

		try   : self.connection.close()
		except: pass

		self.connection = None

		return T21_StructResult_Bool(code = CODES_COMPLETION.COMPLETED,
									 data = True)

	# Механика управления: Выполнение SQL
	def ExecSql(self, sql: str | list[str]) -> T21_StructResult_CursorS3m:
		""" Выполнение запроса с кодом """
		self.PrepareConnect()

		if self.connection is None:
			return T21_StructResult_CursorS3m(code     = CODES_COMPLETION.INTERRUPTED,
			                                  subcodes = {CODES_DB.ERROR_CONNECTION})

		try:
			sql_cursor      = self.connection.cursor()

			if   type(sql) is str  : sql_cursor.execute(sql + ';' if ';' not in sql else '')
			elif type(sql) is list : sql_cursor.executescript('\n'.join(sql))

			self.connection.commit()

			return T21_StructResult_CursorS3m(code   = CODES_COMPLETION.COMPLETED,
			                                  cursor = sql_cursor)

		except sqlite3.IntegrityError:
			self.PrepareDisconnect()
			return T21_StructResult_CursorS3m(code     = CODES_COMPLETION.INTERRUPTED,
			                                  subcodes = {CODES_DB.ERROR_DB})

		except sqlite3.ProgrammingError:
			self.PrepareDisconnect()
			return T21_StructResult_CursorS3m(code     = CODES_COMPLETION.INTERRUPTED,
			                                  subcodes = {CODES_DB.ERROR_SQL})

		except sqlite3.OperationalError:  # Сюда попадают и ошибки SQL-синтаксиса
			self.PrepareDisconnect()
			return T21_StructResult_CursorS3m(code     = CODES_COMPLETION.INTERRUPTED,
			                                  subcodes = {CODES_DB.ERROR_SQL})

		except:
			self.PrepareDisconnect()
			return T21_StructResult_CursorS3m(code     = CODES_COMPLETION.INTERRUPTED,
			                                  subcodes = {CODES_DB.ERROR_DB})

	def ExecSqlSelectRowCount(self, sql: str | list[str]) -> T21_StructResult_Int:
		"""Выполнение запроса с числом строк"""
		result_cursor = self.ExecSql(sql)
		if not result_cursor.code == CODES_COMPLETION.COMPLETED:
			self.PrepareDisconnect()

			return T21_StructResult_Int(code     = CODES_COMPLETION.INTERRUPTED,
										subcodes = result_cursor.subcodes)

		try   :
			cursor      = result_cursor.cursor
			count : int = cursor.rowcount
			cursor.close()
		except:
			return T21_StructResult_Int(code     = CODES_COMPLETION.INTERRUPTED,
										subcodes = {CODES_DB.ERROR_DB})

		self.PrepareDisconnect()

		return T21_StructResult_Int(code = CODES_COMPLETION.COMPLETED,
									data = count)

	def ExecSqlSelectSingle(self, sql: str | list[str]) -> T21_StructResult_String:
		"""Выполнение запроса с получением значения"""
		result_cursor = self.ExecSql(sql)
		if not result_cursor.code == CODES_COMPLETION.COMPLETED:
			self.PrepareDisconnect()

			return T21_StructResult_String(code     = result_cursor.code,
										   subcodes = result_cursor.subcodes)

		try:
			cursor           = result_cursor.cursor
			data : list[str] = cursor.fetchone()
			cursor.close()
		except:
			return T21_StructResult_String(code     = CODES_COMPLETION.INTERRUPTED,
										   subcodes = {CODES_DB.ERROR_DB})

		self.PrepareDisconnect()

		if (not data) or (data is None):
			return T21_StructResult_String(code     = CODES_COMPLETION.COMPLETED,
										   subcodes = {CODES_DATA.NO_DATA})

		return T21_StructResult_String(code = CODES_COMPLETION.COMPLETED,
									   data = data[0])

	def ExecSqlSelectHList(self, sql: str | list[str]) -> T21_StructResult_List:
		"""Выполнение запроса с получением горизонтального списка значений"""
		result_cursor = self.ExecSql(sql)
		if not result_cursor.code == CODES_COMPLETION.COMPLETED:
			self.PrepareDisconnect()
			return T21_StructResult_List(code     = result_cursor.code,
										 subcodes = result_cursor.subcodes)

		try:
			cursor           = result_cursor.cursor
			data : list[str] = cursor.fetchone()
			cursor.close()
		except:
			return T21_StructResult_List(code     = CODES_COMPLETION.INTERRUPTED,
										 subcodes = {CODES_DB.ERROR_DB})

		self.PrepareDisconnect()

		result      = T21_StructResult_List()
		result.code = CODES_COMPLETION.COMPLETED
		result.data = data[:] if data is not None else []

		match len(result.data):
			case 0: result.subcodes.add(CODES_DATA.NO_DATA)
			case 1: result.subcodes.add(CODES_DATA.SINGLE)
			case _: pass

		return result

	def ExecSqlSelectVList(self, sql: str | list[str]) -> T21_StructResult_List:
		"""Выполнение запроса с получением вертикального списка значений"""
		result_cursor  = self.ExecSql(sql)
		if not result_cursor.code == CODES_COMPLETION.COMPLETED:
			self.PrepareDisconnect()
			return T21_StructResult_List(code     = result_cursor.code,
										 subcodes = result_cursor.subcodes)

		try:
			cursor           = result_cursor.cursor
			data : list[str] = list(map(lambda raw: raw[0], cursor.fetchall()))
			cursor.close()
		except:
			return T21_StructResult_List(code     = CODES_COMPLETION.INTERRUPTED,
										 subcodes = {CODES_DB.ERROR_DB})

		self.PrepareDisconnect()

		result      = T21_StructResult_List()
		result.code = CODES_COMPLETION.COMPLETED
		result.data = data[:] if data is not None else []

		match len(result.data):
			case 0: result.subcodes.add(CODES_DATA.NO_DATA)
			case 1: result.subcodes.add(CODES_DATA.SINGLE)
			case _: pass

		return result

	def ExecSqlSelectMatrix(self, sql: str | list[str]) -> T21_StructResult_List:
		"""Выполнение запроса с получением матрицы"""
		result_cursor  = self.ExecSql(sql)
		if not result_cursor.code == CODES_COMPLETION.COMPLETED:
			self.PrepareDisconnect()
			return T21_StructResult_List(code     = result_cursor.code,
										 subcodes = result_cursor.subcodes)

		try:
			cursor           = result_cursor.cursor
			data : list[str] = cursor.fetchall()
			cursor.close()
		except:
			return T21_StructResult_List(code     = CODES_COMPLETION.INTERRUPTED,
										 subcodes = {CODES_DB.ERROR_DB})

		self.PrepareDisconnect()

		result      = T21_StructResult_List()
		result.code = CODES_COMPLETION.COMPLETED
		result.data = data[:] if data is not None else []

		match len(result.data):
			case 0: result.subcodes.add(CODES_DATA.NO_DATA)
			case 1: result.subcodes.add(CODES_DATA.SINGLE)
			case _: pass

		return result

	# Логика данных: Регистрация класса
	def RegisterClass(self, idc: str) -> T21_StructResult_Bool:
		""" Регистрация класса структурного объекта """
		if not CheckIdc(idc): return T21_StructResult_Bool(code     = CODES_COMPLETION.INTERRUPTED,
														   subcodes = {CODES_DATA.ERROR_CHECK},
														   data     = False)

		result         = T21_StructResult_Bool()
		result.code    = CODES_COMPLETION.COMPLETED
		result.data    = True

		sql      : str = f"CREATE TABLE IF NOT EXISTS {idc} ({CACTUS_STRUCT_DATA.IDS.name_sql} TEXT PRIMARY KEY, {CACTUS_STRUCT_DATA.VLP.name_sql} TEXT NOT NULL, {CACTUS_STRUCT_DATA.VLT.name_sql} INT NOT NULL)"

		result_s_table = self.ExecSql(sql)
		if not result_s_table.code == CODES_COMPLETION.COMPLETED:
			result.code = CODES_COMPLETION.INTERRUPTED
			result.subcodes.add(CODES_PROCESSING.PARTIAL)
			result.subcodes.add(CODES_DB.ERROR_SQL)

		sql      : str = f"CREATE TABLE IF NOT EXISTS {idc}_ ({CACTUS_STRUCT_DATA.IDS.name_sql} TEXT, {CACTUS_STRUCT_DATA.VLP.name_sql} TEXT NOT NULL, {CACTUS_STRUCT_DATA.VLT.name_sql} INT NOT NULL)"
		result_s_table = self.ExecSql(sql)
		if not result_s_table.code == CODES_COMPLETION.COMPLETED:
			result.code = CODES_COMPLETION.INTERRUPTED
			result.subcodes.add(CODES_PROCESSING.PARTIAL)
			result.subcodes.add(CODES_DB.ERROR_SQL)

		sql      : str = f"CREATE INDEX IF NOT EXISTS index_{idc}_ids_ ON {idc}_ ({CACTUS_STRUCT_DATA.IDS.name_sql})"
		result_s_index = self.ExecSql(sql)
		if not result_s_index.code == CODES_COMPLETION.COMPLETED:
			result.code = CODES_COMPLETION.INTERRUPTED
			result.subcodes.add(CODES_PROCESSING.PARTIAL)
			result.subcodes.add(CODES_DB.ERROR_SQL)

		sql      : str = f"CREATE INDEX IF NOT EXISTS index_{idc}_vlt_ ON {idc}_ ({CACTUS_STRUCT_DATA.VLT.name_sql})"
		result_s_index = self.ExecSql(sql)
		if not result_s_index.code == CODES_COMPLETION.COMPLETED:
			result.code = CODES_COMPLETION.INTERRUPTED
			result.subcodes.add(CODES_PROCESSING.PARTIAL)
			result.subcodes.add(CODES_DB.ERROR_SQL)

		return result

	# Логика данных: S-Ячейка
	def DeleteSCell(self, cell: T20_StructCell, flag_capture_delta: bool = False) -> T21_StructResult_StructCell:
		""" Удаление S-Ячейки """
		result_check : bool      = CheckIdc(cell.idc)
		result_check            &= CheckIdo(cell.ido)
		result_check            &= CheckIdp(cell.idp)

		if not result_check:
			return T21_StructResult_StructCell(code     = CODES_COMPLETION.INTERRUPTED,
											   subcodes = {CODES_DATA.ERROR_CHECK})

		cell_start  : T20_StructCell | None = None

		if flag_capture_delta:
			result_cell = self.ReadSCell(cell)
			cell_start  = result_cell.data

		sql         : str                   = f"DELETE FROM {cell.idc} WHERE {CACTUS_STRUCT_DATA.IDS.name_sql} = '{cell.ids}'"
		result_sql                          = self.ExecSqlSelectRowCount(sql)

		if not result_sql.code == CODES_COMPLETION.COMPLETED :
			return T21_StructResult_StructCell(code     = CODES_COMPLETION.INTERRUPTED,
											   subcodes = result_sql.subcodes)

		elif   result_sql.data == 0                          :
			return T21_StructResult_StructCell(code     = CODES_COMPLETION.COMPLETED,
											   subcodes = {CODES_DATA.NO_DATA})

		result                              = T21_StructResult_StructCell()
		result.code                         = CODES_COMPLETION.COMPLETED

		if flag_capture_delta:
			result_cell = self.ReadSCell(cell)
			cell_end    = result_cell.data
			cells       = [cell_start, cell_end]
			cells.remove(None)

			result.data = cells[0]

		return result

	def ReadSCell(self, cell: T20_StructCell) -> T21_StructResult_StructCell:
		""" Запрос S-Ячейки """
		result_check : bool      = CheckIdc(cell.idc)
		result_check            &= CheckIdo(cell.ido)
		result_check            &= CheckIdp(cell.idp)

		if not result_check:
			return T21_StructResult_StructCell(code     = CODES_COMPLETION.INTERRUPTED,
											   subcodes = {CODES_DATA.ERROR_CHECK})

		sql          : str       = f"SELECT {CACTUS_STRUCT_DATA.VLP.name_sql}, {CACTUS_STRUCT_DATA.VLT.name_sql} FROM {cell.idc} WHERE {CACTUS_STRUCT_DATA.IDS.name_sql} = '{cell.ids}'"
		result_sql               = self.ExecSqlSelectHList(sql)

		if not result_sql.code == CODES_COMPLETION.COMPLETED:
			return T21_StructResult_StructCell(code     = CODES_COMPLETION.INTERRUPTED,
											   subcodes = result_sql.subcodes)

		data         : list[str] = result_sql.data
		if len(data) < 2 :
			return T21_StructResult_StructCell(code     = CODES_COMPLETION.COMPLETED,
											   subcodes = {CODES_DATA.NO_DATA})

		result                   = T21_StructResult_StructCell()
		result.data              = CODES_COMPLETION.COMPLETED

		try                                 :
			result_cell     = T20_StructCell()
			result_cell.idc = cell.idc
			result_cell.ido = cell.ido
			result_cell.idp = cell.idp
			result_cell.vlp = data[0]
			result_cell.vlt = int(data[1])
		except                              :
			return T21_StructResult_StructCell(code     = CODES_COMPLETION.INTERRUPTED,
											   subcodes = {CODES_DATA.ERROR_CONVERT})

		result.data = result_cell
		return result

	def SyncSCell(self, cell: T20_StructCell, flag_capture_delta: bool = False) -> T21_StructResult_StructCell:
		""" Синхронизация S-Ячейки """
		result_check : bool      = CheckIdc(cell.idc)
		result_check            &= CheckIdo(cell.ido)
		result_check            &= CheckIdp(cell.idp)

		if not result_check:
			return T21_StructResult_StructCell(code     = CODES_COMPLETION.INTERRUPTED,
											   subcodes = {CODES_DATA.ERROR_CHECK})

		result_cell         = self.ReadSCell(cell)
		check_error  : bool = not result_cell.code == CODES_COMPLETION.COMPLETED
		check_error        &= CODES_DATA.NO_DATA in result_cell.subcodes
		if check_error:
			return T21_StructResult_StructCell(code     = CODES_COMPLETION.INTERRUPTED,
											   subcodes = result_cell.subcodes)

		cell_in_container   = result_cell.data

		result_write : bool = True
		if cell_in_container is not None: result_write = (cell_in_container.vlt < cell.vlt)

		result = T21_StructResult_StructCell()
		result.code = CODES_COMPLETION.COMPLETED

		if not result_write:
			result.subcodes.add(CODES_PROCESSING.SKIP)

			if flag_capture_delta: result.data = cell_in_container

			return result

		result_cell         = self.WriteSCell(cell, False, flag_capture_delta)
		if not result_cell.code == CODES_COMPLETION.COMPLETED:
			return T21_StructResult_StructCell(code     = CODES_COMPLETION.INTERRUPTED,
											   subcodes = result_cell.subcodes)

		result.subcodes = result_cell.subcodes

		if flag_capture_delta: result.data = result_cell.data

		return result

	def WriteSCell(self, cell: T20_StructCell, flag_skip: bool = False, flag_capture_delta: bool = False) -> T21_StructResult_StructCell:
		""" Запись S-Ячейки """
		result_check : bool      = CheckIdc(cell.idc)
		result_check            &= CheckIdo(cell.ido)
		result_check            &= CheckIdp(cell.idp)

		if not result_check:
			return T21_StructResult_StructCell(code     = CODES_COMPLETION.INTERRUPTED,
											   subcodes = {CODES_DATA.ERROR_CHECK})

		cell_start   : T20_StructCell | None = None

		if flag_capture_delta: cell_start = self.ReadSCell(cell).data

		sql          : str  = f"INSERT INTO {cell.idc} ({CACTUS_STRUCT_DATA.IDS.name_sql}, {CACTUS_STRUCT_DATA.VLP.name_sql}, {CACTUS_STRUCT_DATA.VLT.name_sql}) VALUES ('{cell.ids}', '{cell.vlp}', {cell.vlt}) "
		if flag_skip : sql += f"ON CONFLICT ({CACTUS_STRUCT_DATA.IDS.name_sql}) DO NOTHING"
		else         : sql += f"ON CONFLICT ({CACTUS_STRUCT_DATA.IDS.name_sql}) DO UPDATE SET {CACTUS_STRUCT_DATA.VLP.name_sql}='{cell.vlp}', {CACTUS_STRUCT_DATA.VLT.name_sql}={cell.vlt}"

		result_sql                           = self.ExecSqlSelectRowCount(sql)

		if not result_sql.code == CODES_COMPLETION.COMPLETED:
			return T21_StructResult_StructCell(code     = CODES_COMPLETION.INTERRUPTED,
											   subcodes = result_sql.subcodes)

		result                               = T21_StructResult_StructCell()
		result.code                          = CODES_COMPLETION.COMPLETED

		if flag_capture_delta:
			cell_end    = self.ReadSCell(cell).data
			result.data = None if cell_end == cell_start else cell_end

			if result.data is None: result.subcodes.add(CODES_PROCESSING.SKIP)
		elif not result_sql.data:
			result.subcodes.add(CODES_PROCESSING.SKIP)

		return result

	# Логика данных: Пакет S-Ячеек
	def DeleteSCells(self, cell_cells: T20_StructCell | list[T20_StructCell], flag_capture_delta: bool = False) -> T21_StructResult_StructCells:
		""" Удаление пакета S-Ячеек """
		result_check : bool = False
		result_check       |= type(cell_cells) is T20_StructCell
		result_check       |= type(cell_cells) is list

		if not result_check:
			return T21_StructResult_StructCells(code     = CODES_COMPLETION.INTERRUPTED,
												subcodes = {CODES_DATA.ERROR_TYPE})

		cells_before : list[T20_StructCell] = []
		cells_after  : list[T20_StructCell] = []

		if flag_capture_delta: cells_before = self.ReadSCells(cell_cells).data

		result            = T21_StructResult_StructCells()

		if   type(cell_cells) is T20_StructCell:
			result_check : bool = CheckIdc(cell_cells.idc)

			if not result_check                                 : return T21_StructResult_StructCells(code     = CODES_COMPLETION.INTERRUPTED,
																	                                  subcodes = {CODES_DATA.ERROR_CHECK})

			sql     : str       = f"DELETE FROM {cell_cells.idc}"

			filters : list[str] = []
			if bool(cell_cells.ido): filters.append(f"({CACTUS_STRUCT_DATA.IDS.name_sql} LIKE '{cell_cells.ido}%')")
			if bool(cell_cells.idp): filters.append(f"({CACTUS_STRUCT_DATA.IDS.name_sql} LIKE '%{cell_cells.idp}')")
			if bool(cell_cells.vlp): filters.append(f"({CACTUS_STRUCT_DATA.VLP.name_sql} LIKE '{cell_cells.vlp}' = '{cell_cells.vlp}')")
			if bool(cell_cells.vlt): filters.append(f"({CACTUS_STRUCT_DATA.VLT.name_sql} LIKE '{cell_cells.vlt}' = '{cell_cells.vlt}')")

			if filters: sql += " WHERE " + ' AND '.join(filters)

			result_sql          = self.ExecSqlSelectMatrix(sql)

			if not result_sql.code == CODES_COMPLETION.COMPLETED: return T21_StructResult_StructCells(code     = CODES_COMPLETION.INTERRUPTED,
																	                                  subcodes = result_sql.subcodes)

			for raw_line in result_sql.data:
				try:
					ids = raw_line[0]
					vlp = raw_line[1]
					vlt = raw_line[2]

					result_cell = T20_StructCell()
					result_cell.idc = cell_cells.idc
					result_cell.ido = IdoFromIds(ids)
					result_cell.idp = IdpFromIds(ids)
					result_cell.vlp = vlp
					result_cell.vlt = int(vlt)
				except:
					result.subcodes.add(CODES_DATA.ERROR_CONVERT)
					result.subcodes.add(CODES_PROCESSING.PARTIAL)

		elif type(cell_cells) is list          :
			filters : dict[str, list[str]] = dict()

			for cell in cell_cells:
				result_check: bool      = CheckIdc(cell.idc)
				result_check           &= CheckIdo(cell.ido)
				result_check           &= CheckIdp(cell.idp)

				if not result_check:
					result.subcodes.add(CODES_DATA.ERROR_CHECK)
					result.subcodes.add(CODES_PROCESSING.PARTIAL)
					continue

				filters_idc : list[str] = filters.get(cell.idc, [])
				filters_idc.append(cell.ids)

				filters[cell.idc]       = filters_idc

			sql    : list[str]            = []
			sql.append("BEGIN TRANSACTION;")

			for idc, idss in filters.items():
				select_sql  = f"DELETE FROM {idc} WHERE {CACTUS_STRUCT_DATA.IDS.name_sql} IN ("
				select_sql += ', '.join(f"'{ids}'" for ids in idss)
				select_sql += ");"

				sql.append(select_sql)

			sql.append("COMMIT;")

			result_sql          = self.ExecSqlSelectMatrix(sql)

			if not result_sql.code == CODES_COMPLETION.COMPLETED:
				self.ExecSql("ROLLBACK;")

				return T21_StructResult_StructCells(code     = CODES_COMPLETION.INTERRUPTED,
				                                    subcodes = result_sql.subcodes)

			for raw_line in result_sql.data:
				try:
					ids = raw_line[0]
					vlp = raw_line[1]
					vlt = raw_line[2]

					result_cell = T20_StructCell()
					result_cell.idc = cell_cells.idc
					result_cell.ido = IdoFromIds(ids)
					result_cell.idp = IdpFromIds(ids)
					result_cell.vlp = vlp
					result_cell.vlt = int(vlt)
				except:
					result.subcodes.add(CODES_DATA.ERROR_CONVERT)
					result.subcodes.add(CODES_PROCESSING.PARTIAL)

		if flag_capture_delta:
			cells_after = self.ReadSCells(cell_cells).data

			result.data = DifferenceLists(cells_before, cells_after, True)

			match len(result.data):
				case 0: result.subcodes.add(CODES_DATA.NO_DATA)
				case 1: result.subcodes.add(CODES_DATA.SINGLE)

		return result

	def ReadSCells(self, cell_cells: T20_StructCell | list[T20_StructCell]) -> T21_StructResult_StructCells:
		""" Запрос пакета S-Ячеек """
		result_check : bool = False
		result_check       |= type(cell_cells) is T20_StructCell
		result_check       |= type(cell_cells) is list

		if not result_check:
			return T21_StructResult_StructCells(code     = CODES_COMPLETION.INTERRUPTED,
												subcodes = {CODES_DATA.ERROR_TYPE})

		result            = T21_StructResult_StructCells()

		if   type(cell_cells) is T20_StructCell:
			result_check : bool = CheckIdc(cell_cells.idc)

			if not result_check                                 : return T21_StructResult_StructCells(code     = CODES_COMPLETION.INTERRUPTED,
																	                                  subcodes = {CODES_DATA.ERROR_CHECK})

			sql     : str       = f"SELECT {CACTUS_STRUCT_DATA.IDS.name_sql}, {CACTUS_STRUCT_DATA.VLP.name_sql}, {CACTUS_STRUCT_DATA.VLT.name_sql} FROM {cell_cells.idc}"

			filters : list[str] = []
			if bool(cell_cells.ido): filters.append(f"({CACTUS_STRUCT_DATA.IDS.name_sql} LIKE '{cell_cells.ido}%')")
			if bool(cell_cells.idp): filters.append(f"({CACTUS_STRUCT_DATA.IDS.name_sql} LIKE '%{cell_cells.idp}')")
			if bool(cell_cells.vlp): filters.append(f"({CACTUS_STRUCT_DATA.VLP.name_sql} LIKE '{cell_cells.vlp}' = '{cell_cells.vlp}')")
			if bool(cell_cells.vlt): filters.append(f"({CACTUS_STRUCT_DATA.VLT.name_sql} LIKE '{cell_cells.vlt}' = '{cell_cells.vlt}')")

			if filters: sql += " WHERE " + ' AND '.join(filters)

			result_sql          = self.ExecSqlSelectMatrix(sql)

			if not result_sql.code == CODES_COMPLETION.COMPLETED: return T21_StructResult_StructCells(code     = CODES_COMPLETION.INTERRUPTED,
																	                                  subcodes = result_sql.subcodes)

			for raw_line in result_sql.data:
				try:
					ids = raw_line[0]
					vlp = raw_line[1]
					vlt = raw_line[2]

					result_cell = T20_StructCell()
					result_cell.idc = cell_cells.idc
					result_cell.ido = IdoFromIds(ids)
					result_cell.idp = IdpFromIds(ids)
					result_cell.vlp = vlp
					result_cell.vlt = int(vlt)

					result.data.append(result_cell)
				except:
					result.subcodes.add(CODES_DATA.ERROR_CONVERT)
					result.subcodes.add(CODES_PROCESSING.PARTIAL)

		elif type(cell_cells) is list          :
			filters : dict[str, list[str]] = dict()

			for cell in cell_cells:
				result_check: bool      = CheckIdc(cell.idc)
				result_check           &= CheckIdo(cell.ido)
				result_check           &= CheckIdp(cell.idp)

				if not result_check:
					result.subcodes.add(CODES_DATA.ERROR_CHECK)
					result.subcodes.add(CODES_PROCESSING.PARTIAL)
					continue

				filters_idc : list[str] = filters.get(cell.idc, [])
				filters_idc.append(cell.ids)

				filters[cell.idc]       = filters_idc

			sql    : list[str]            = []

			for idc, idss in filters.items():
				select_sql  = f"SELECT '{idc}' as '{CACTUS_STRUCT_DATA.IDC.name_sql}', {CACTUS_STRUCT_DATA.IDS.name_sql}, {CACTUS_STRUCT_DATA.VLP.name_sql}, {CACTUS_STRUCT_DATA.VLT.name_sql} FROM {idc} WHERE {CACTUS_STRUCT_DATA.IDS.name_sql} IN ("
				select_sql += ', '.join(f"'{ids}'" for ids in idss)
				select_sql += ")"

				sql.append(select_sql)

			sql    : str                  = " UNION ALL ".join(sql)

			result_sql          = self.ExecSqlSelectMatrix(sql)

			if not result_sql.code == CODES_COMPLETION.COMPLETED: return T21_StructResult_StructCells(code     = CODES_COMPLETION.INTERRUPTED,
																	                                  subcodes = result_sql.subcodes)

			for raw_line in result_sql.data:
				try:
					idc = raw_line[0]
					ids = raw_line[1]
					vlp = raw_line[2]
					vlt = raw_line[3]

					result_cell = T20_StructCell()
					result_cell.idc = idc
					result_cell.ido = IdoFromIds(ids)
					result_cell.idp = IdpFromIds(ids)
					result_cell.vlp = vlp
					result_cell.vlt = int(vlt)

					result.data.append(result_cell)
				except:
					result.subcodes.add(CODES_DATA.ERROR_CONVERT)
					result.subcodes.add(CODES_PROCESSING.PARTIAL)

		match len(result.data):
			case 0: result.subcodes.add(CODES_DATA.NO_DATA)
			case 1: result.subcodes.add(CODES_DATA.SINGLE)

		return result

	def SyncSCells(self, cells: list[T20_StructCell], flag_capture_delta: bool = False) -> T21_StructResult_StructCells:
		""" Запись пакета S-Ячеек """
		result                              = T21_StructResult_StructCells()

		cells_before : list[T20_StructCell] = []
		cells_after  : list[T20_StructCell] = []

		if flag_capture_delta: cells_before = self.ReadSCells(cells).data

		filters      : dict[str, list[str]] = dict()

		sqls: list[str] = []

		for cell in cells:
			result_check : bool = CheckIdc(cell.idc)
			result_check       &= CheckIdo(cell.ido)
			result_check       &= CheckIdp(cell.idp)

			if not result_check:
				result.subcodes.add(CODES_DATA.ERROR_CHECK)
				result.subcodes.add(CODES_PROCESSING.PARTIAL)
				continue

			sql : str = f"INSERT INTO {cell.idc} ({CACTUS_STRUCT_DATA.IDS.name_sql}, {CACTUS_STRUCT_DATA.VLP.name_sql}, {CACTUS_STRUCT_DATA.VLT.name_sql}) VALUES ('{cell.ids}', '{cell.vlp}', {cell.vlt}) "
			sql      += f"ON CONFLICT ({CACTUS_STRUCT_DATA.IDS.name_sql}) DO UPDATE SET {CACTUS_STRUCT_DATA.VLP.name_sql}='{cell.vlp}', {CACTUS_STRUCT_DATA.VLT.name_sql}={cell.vlt} WHERE {CACTUS_STRUCT_DATA.VLT.name_sql} <= {cell.vlt}"
			sql      += f";"

			sqls.append(sql)

		if not sqls: return T21_StructResult_StructCells(code     = CODES_COMPLETION.INTERRUPTED,
			                                             subcodes = {CODES_DATA.ERROR_CHECK})

		sqls.insert(0, "BEGIN TRANSACTION;")
		sqls.append("COMMIT;")

		result_sql = self.ExecSql(sqls)

		if not result_sql.code == CODES_COMPLETION.COMPLETED:
			self.ExecSql("ROLLBACK;")

			return T21_StructResult_StructCells(code     = CODES_COMPLETION.INTERRUPTED,
			                                    subcodes = result_sql.subcodes)

		if flag_capture_delta:
			cells_after = self.ReadSCells(cells).data

			result.data = DifferenceLists(cells_before, cells_after)

			match len(result.data):
				case 0: result.subcodes.add(CODES_DATA.NO_DATA)
				case 1: result.subcodes.add(CODES_DATA.SINGLE)

		return result

	def WriteSCells(self, cells: list[T20_StructCell], flag_skip: bool = False,  flag_capture_delta: bool = False) -> T21_StructResult_StructCells:
		""" Запись пакета S-Ячеек """
		result                              = T21_StructResult_StructCells()
		result.data              = CODES_COMPLETION.COMPLETED

		cells_before : list[T20_StructCell] = []
		cells_after  : list[T20_StructCell] = []

		if flag_capture_delta: cells_before = self.ReadSCells(cells).data

		filters      : dict[str, list[str]] = dict()

		sqls: list[str] = []

		for cell in cells:
			result_check: bool = CheckIdc(cell.idc)
			result_check &= CheckIdo(cell.ido)
			result_check &= CheckIdp(cell.idp)

			if not result_check:
				result.subcodes.add(CODES_DATA.ERROR_CHECK)
				result.subcodes.add(CODES_PROCESSING.PARTIAL)
				continue

			sql         : str  = f"INSERT INTO {cell.idc} VALUES ('{cell.ids}', '{cell.vlp}', {cell.vlt}) "
			if flag_skip: sql += f"ON CONFLICT ({CACTUS_STRUCT_DATA.IDS.name_sql}) DO NOTHING"
			else        : sql += f"ON CONFLICT ({CACTUS_STRUCT_DATA.IDS.name_sql}) DO UPDATE SET {CACTUS_STRUCT_DATA.VLP.name_sql}='{cell.vlp}', {CACTUS_STRUCT_DATA.VLT.name_sql}={cell.vlt}"
			sql               += ';'

			sqls.append(sql)

		if not sqls: return T21_StructResult_StructCells(code     = CODES_COMPLETION.INTERRUPTED,
			                                             subcodes = {CODES_DATA.ERROR_CHECK})

		sqls.insert(0, "BEGIN TRANSACTION;")
		sqls.append("COMMIT;")

		result_sql = self.ExecSql(sqls)

		if not result_sql.code == CODES_COMPLETION.COMPLETED:
			self.ExecSql("ROLLBACK;")

			return T21_StructResult_StructCells(code     = CODES_COMPLETION.INTERRUPTED,
			                                    subcodes = result_sql.subcodes)

		if flag_capture_delta:
			cells_after = self.ReadSCells(cells).data

			result.data = DifferenceLists(cells_before, cells_after, True)

			match len(result.data):
				case 0: result.subcodes.add(CODES_DATA.NO_DATA)
				case 1: result.subcodes.add(CODES_DATA.SINGLE)

		return result

	# Логика данных: D-Ячейка
	def DeleteDCell(self, cell: T20_StructCell, flag_capture_delta: bool = False) -> T21_StructResult_StructCell:
		""" Удаление D-Ячейки """
		result_check : bool      = CheckIdc(cell.idc)
		result_check            &= CheckIdo(cell.ido)
		result_check            &= CheckIdp(cell.idp)
		result_check            &= bool(cell.vlt)

		if not result_check:
			return T21_StructResult_StructCell(code     = CODES_COMPLETION.INTERRUPTED,
											   subcodes = {CODES_DATA.ERROR_CHECK})

		cell_start  : T20_StructCell | None = None

		if flag_capture_delta:
			result_cell = self.ReadDCell(cell)
			cell_start  = result_cell.data

		sql         : str                   = f"DELETE FROM {cell.idc}_ WHERE ({CACTUS_STRUCT_DATA.IDS.name_sql} = '{cell.ids}') AND ({CACTUS_STRUCT_DATA.VLT.name_sql} = {cell.vlt})"
		result_sql                          = self.ExecSqlSelectRowCount(sql)

		if not result_sql.code == CODES_COMPLETION.COMPLETED :
			return T21_StructResult_StructCell(code     = CODES_COMPLETION.INTERRUPTED,
											   subcodes = result_sql.subcodes)

		elif   result_sql.data == 0                          :
			return T21_StructResult_StructCell(code     = CODES_COMPLETION.COMPLETED,
											   subcodes = {CODES_DATA.NO_DATA})

		result                              = T21_StructResult_StructCell()
		result.code                         = CODES_COMPLETION.COMPLETED

		if flag_capture_delta:
			result_cell = self.ReadDCell(cell)
			cell_end    = result_cell.data
			cells       = [cell_start, cell_end]
			cells.remove(None)

			result.data = cells[0]

		return result

	def ReadDCell(self, cell: T20_StructCell) -> T21_StructResult_StructCell:
		""" Запрос D-Ячейки """
		result_check : bool      = CheckIdc(cell.idc)
		result_check            &= CheckIdo(cell.ido)
		result_check            &= CheckIdp(cell.idp)
		result_check            &= bool(cell.vlt)

		if not result_check:
			return T21_StructResult_StructCell(code     = CODES_COMPLETION.INTERRUPTED,
											   subcodes = {CODES_DATA.ERROR_CHECK})

		sql          : str       = f"SELECT {CACTUS_STRUCT_DATA.VLP.name_sql}, {CACTUS_STRUCT_DATA.VLT.name_sql} FROM {cell.idc}_ WHERE ({CACTUS_STRUCT_DATA.IDS.name_sql} = '{cell.ids}') AND ({CACTUS_STRUCT_DATA.VLT.name_sql} = {cell.vlt})"
		result_sql               = self.ExecSqlSelectHList(sql)

		if not result_sql.code == CODES_COMPLETION.COMPLETED:
			return T21_StructResult_StructCell(code     = CODES_COMPLETION.INTERRUPTED,
											   subcodes = result_sql.subcodes)

		data         : list[str] = result_sql.data
		if len(data) < 2 :
			return T21_StructResult_StructCell(code     = CODES_COMPLETION.COMPLETED,
											   subcodes = {CODES_DATA.NO_DATA})

		result                   = T21_StructResult_StructCell()
		result.data              = CODES_COMPLETION.COMPLETED

		try                                 :
			result_cell     = T20_StructCell()
			result_cell.idc = cell.idc
			result_cell.ido = cell.ido
			result_cell.idp = cell.idp
			result_cell.vlp = data[0]
			result_cell.vlt = int(data[1])
		except                              :
			return T21_StructResult_StructCell(code     = CODES_COMPLETION.INTERRUPTED,
											   subcodes = {CODES_DATA.ERROR_CONVERT})

		result.data = result_cell
		return result

	def WriteDCell(self, cell: T20_StructCell, flag_capture_delta: bool = False) -> T21_StructResult_StructCell:
		""" Запись D-Ячейки """
		result_check : bool                  = CheckIdc(cell.idc)
		result_check                        &= CheckIdo(cell.ido)
		result_check                        &= CheckIdp(cell.idp)
		result_check                        &= bool(cell.vlt)

		if not result_check:
			return T21_StructResult_StructCell(code     = CODES_COMPLETION.INTERRUPTED,
											   subcodes = {CODES_DATA.ERROR_CHECK})

		cell_start   : T20_StructCell | None = None

		if flag_capture_delta: cell_start = self.ReadDCell(cell).data

		sql          : str                   = f"INSERT INTO {cell.idc}_ ({CACTUS_STRUCT_DATA.IDS.name_sql}, {CACTUS_STRUCT_DATA.VLP.name_sql}, {CACTUS_STRUCT_DATA.VLT.name_sql}) SELECT '{cell.ids}', '{cell.vlp}', '{cell.vlt}' WHERE NOT EXISTS (SELECT 1 FROM {cell.idc}_ WHERE {CACTUS_STRUCT_DATA.IDS.name_sql} = '{cell.ids}' AND _vlt = {cell.vlt})"

		result_sql                           = self.ExecSqlSelectRowCount(sql)

		if not result_sql.code == CODES_COMPLETION.COMPLETED:
			return T21_StructResult_StructCell(code     = CODES_COMPLETION.INTERRUPTED,
											   subcodes = result_sql.subcodes)

		result                               = T21_StructResult_StructCell()
		result.code                          = CODES_COMPLETION.COMPLETED

		if flag_capture_delta:
			cell_end    = self.ReadDCell(cell).data
			result.data = None if cell_end == cell_start else cell_end

			if result.data is None: result.subcodes.add(CODES_PROCESSING.SKIP)
		elif not result_sql.data:
			result.subcodes.add(CODES_PROCESSING.SKIP)

		return result

	# Логика данных: Пакет D-Ячеек
	def DeleteDCells(self, cell: T21_VltRange, flag_capture_delta: bool = False) -> T21_StructResult_StructCells:
		""" Удаление пакета D-Ячеек """
		result_check : bool                 = CheckIdc(cell.idc)
		result_check                       &= CheckIdo(cell.ido)
		result_check                       &= CheckIdp(cell.idp)

		if not result_check                                 : return T21_StructResult_StructCells(code     = CODES_COMPLETION.INTERRUPTED,
		                                                                                          subcodes = {CODES_DATA.ERROR_CHECK})

		cells_before : list[T20_StructCell] = []
		cells_after  : list[T20_StructCell] = []

		if flag_capture_delta: cells_before = self.ReadDCells(cell).data

		result                              = T21_StructResult_StructCells()

		sql          : str                  = f"DELETE FROM {cell.idc}_"

		filters : list[str] = []
		filters.append(f"({CACTUS_STRUCT_DATA.IDS.name_sql} = '{cell.ids}')")
		if cell.vlt_l: filters.append(f"({CACTUS_STRUCT_DATA.VLT.name_sql} >= '{cell.vlt_l}')")
		if cell.vlt_r: filters.append(f"({CACTUS_STRUCT_DATA.VLT.name_sql} <= '{cell.vlt_r}')")

		if filters: sql += " WHERE " + ' AND '.join(filters)

		result_sql                          = self.ExecSqlSelectMatrix(sql)

		if not result_sql.code == CODES_COMPLETION.COMPLETED: return T21_StructResult_StructCells(code     = CODES_COMPLETION.INTERRUPTED,
																                                  subcodes = result_sql.subcodes)

		if flag_capture_delta:
			cells_after = self.ReadSCells(cell).data

			result.data = DifferenceLists(cells_before, cells_after, True)

			match len(result.data):
				case 0: result.subcodes.add(CODES_DATA.NO_DATA)
				case 1: result.subcodes.add(CODES_DATA.SINGLE)

		return result

	def ReadDCells(self, cell: T21_VltRange) -> T21_StructResult_StructCells:
		""" Запрос пакета D-Ячеек """
		result_check : bool      = CheckIdc(cell.idc)
		result_check            &= CheckIdo(cell.ido)
		result_check            &= CheckIdp(cell.idp)

		if not result_check                                 : return T21_StructResult_StructCells(code     = CODES_COMPLETION.INTERRUPTED,
											                                                      subcodes = {CODES_DATA.ERROR_CHECK})

		filters      : list[str] = []
		filters.append(f"({CACTUS_STRUCT_DATA.IDS.name_sql} = '{cell.ids}')")
		if cell.vlt_l: filters.append(f"({CACTUS_STRUCT_DATA.VLT.name_sql} >= '{cell.vlt_l}')")
		if cell.vlt_r: filters.append(f"({CACTUS_STRUCT_DATA.VLT.name_sql} <= '{cell.vlt_r}')")

		sql          : str       = f"SELECT {CACTUS_STRUCT_DATA.VLP.name_sql}, {CACTUS_STRUCT_DATA.VLT.name_sql} FROM {cell.idc}_ WHERE "
		sql                     += ' AND '.join(filters)

		result_sql = self.ExecSqlSelectMatrix(sql)

		if not result_sql.code == CODES_COMPLETION.COMPLETED: return T21_StructResult_StructCells(code     = CODES_COMPLETION.INTERRUPTED,
		                                                                                          subcodes = result_sql.subcodes)

		result                   = T21_StructResult_StructCells()
		result.code              = CODES_COMPLETION.COMPLETED

		for raw_line in result_sql.data:
			try:
				vlp = raw_line[0]
				vlt = raw_line[1]

				result_cell = T20_StructCell()
				result_cell.idc = cell.idc
				result_cell.ido = cell.ido
				result_cell.idp = cell.idp
				result_cell.vlp = vlp
				result_cell.vlt = int(vlt)

				result.data.append(result_cell)
			except:
				result.subcodes.add(CODES_DATA.ERROR_CONVERT)
				result.subcodes.add(CODES_PROCESSING.PARTIAL)

		match len(result.data):
			case 0: result.subcodes.add(CODES_DATA.NO_DATA)
			case 1: result.subcodes.add(CODES_DATA.SINGLE)

		return result

	# Логика данных: Диапазон VLT
	def ReadVltRange(self, cell: T21_VltRange) -> T21_StructResult_VltRange:
		""" Запрос границ cUT D-Ячейки """
		result_check : bool      = CheckIdc(cell.idc)
		result_check            &= CheckIdo(cell.ido)
		result_check            &= CheckIdp(cell.idp)

		if not result_check                                 : return T21_StructResult_VltRange(code     = CODES_COMPLETION.INTERRUPTED,
			                                                                                   subcodes = {CODES_DATA.ERROR_CHECK})

		result                   = T21_StructResult_VltRange()

		filters      : list[str] = []
		filters.append(f"({CACTUS_STRUCT_DATA.IDS.name_sql} = '{cell.ids}')")
		if cell.vlt_l: filters.append(f"({CACTUS_STRUCT_DATA.VLT.name_sql} >= '{cell.vlt_l}')")
		if cell.vlt_r: filters.append(f"({CACTUS_STRUCT_DATA.VLT.name_sql} <= '{cell.vlt_r}')")

		sql          : str       = f"SELECT MIN({CACTUS_STRUCT_DATA.VLT.name_sql}), MAX({CACTUS_STRUCT_DATA.VLT.name_sql}) FROM {cell.idc}_ WHERE"
		sql                     += ' AND '.join(filters)

		result_sql = self.ExecSqlSelectHList(sql)

		if not result_sql.code == CODES_COMPLETION.COMPLETED: return T21_StructResult_VltRange(code     = CODES_COMPLETION.INTERRUPTED,
		                                                                                       subcodes = result_sql.subcodes)
		try   :
			result.data       = copy(cell)
			result.data.vlt_l = result_sql.data[0]
			result.data.vlt_r = result_sql.data[1]
		except:			                                      return T21_StructResult_VltRange(code     =  CODES_COMPLETION.INTERRUPTED,
			                                                                                   subcodes = {CODES_DATA.ERROR_CONVERT})

		return result

	def ReadVlts(self, cell: T21_VltRange) -> T21_StructResult_List:
		""" Запрос списка VLT """
		result_check : bool      = CheckIdc(cell.idc)
		result_check            &= CheckIdo(cell.ido)
		result_check            &= CheckIdp(cell.idp)

		if not result_check                                 : return T21_StructResult_List(code     = CODES_COMPLETION.INTERRUPTED,
			                                                                               subcodes = {CODES_DATA.ERROR_CHECK})

		result                   = T21_StructResult_List()

		filters      : list[str] = []
		filters.append(f"({CACTUS_STRUCT_DATA.IDS.name_sql} = '{cell.ids}')")
		if cell.vlt_l: filters.append(f"({CACTUS_STRUCT_DATA.VLT.name_sql} >= '{cell.vlt_l}')")
		if cell.vlt_r: filters.append(f"({CACTUS_STRUCT_DATA.VLT.name_sql} <= '{cell.vlt_r}')")

		sql          : str       = f"SELECT DISTINCT {CACTUS_STRUCT_DATA.VLT.name_sql} FROM {cell.idc}_ WHERE"
		sql                     += ' AND '.join(filters)

		result_sql = self.ExecSqlSelectVList(sql)

		if not result_sql.code == CODES_COMPLETION.COMPLETED: return T21_StructResult_List(code     = CODES_COMPLETION.INTERRUPTED,
		                                                                                   subcodes = result_sql.subcodes)

		result.data = result_sql.data

		return result


# КАКТУС: КОНТЕЙНЕР-PostgreSQL
class C32_ContainerPostgreSQL(C31_ContainerSQL):
	""" Кактус: Контейнер PostgreSQL """

	# Модель данных
	def Init_00(self):
		super().Init_00()

		self._options_server_ip       : str = ""
		self._options_server_tcp_port : int = 5432
		self._options_server_dbase    : str = ""
		self._options_server_login    : str = ""
		self._options_server_password : str = ""

	def Init_01(self):
		super().Init_01()

		self._container_type = CONTAINERS.POSTGRESQL

	def Init_10(self):
		super().Init_10()

		self.connection : psycopg2.extensions.connection | None = None

	# Механика данных: Параметры подключения
	def OptionsServerIp(self, ip: str = None) -> T21_StructResult_String:
		""" Запрос/Установка параметра подключения: IP сервера """
		if ip is None: return T21_StructResult_String(code = CODES_COMPLETION.COMPLETED, data = self._options_server_ip)
		else         :        self._options_server_ip = ip

	def OptionsServerTcpPort(self, tcp_port: int = None) -> T21_StructResult_Int:
		""" Запрос/Установка параметра подключения: TCP-порт """
		if tcp_port is None: return T21_StructResult_Int(code = CODES_COMPLETION.COMPLETED, data = self._options_server_tcp_port)
		else               :        self._options_server_tcp_port = tcp_port

	def OptionsServerDBase(self, basename: str = None) -> T21_StructResult_String:
		""" Запрос/Установка параметра подключения: Имя схемы """
		if basename is None: return T21_StructResult_String(code = CODES_COMPLETION.COMPLETED, data = self._options_server_dbase)
		else               :        self._options_server_dbase = basename

	def OptionsServerLogin(self, login: str = None) -> T21_StructResult_String:
		""" Запрос/Установка параметра подключения: Логин """
		if login is None: return T21_StructResult_String(code = CODES_COMPLETION.COMPLETED, data = self._options_server_login)
		else            :        self._options_server_login = login

	def OptionsServerPassword(self, password: str = None) -> T21_StructResult_String:
		""" Запрос/Установка параметра подключения: Пароль """
		if password is None: return T21_StructResult_String(code = CODES_COMPLETION.COMPLETED, data = self._options_server_password)
		else               :        self._options_server_password = password

	# Механика данных: Состояния
	def StateConnected(self) -> T21_StructResult_Bool:
		""" Запрос состояния подключения """
		result      = T21_StructResult_Bool()
		result.code = CODES_COMPLETION.COMPLETED
		result.data = False

		if self.connection is None: return result

		try    : cursor = self.connection.cursor()
		except : return result

		result.data = True

		return result

	# Механика управления: Управление подключением
	def Connect(self) -> T21_StructResult_Bool:
		""" Подключение к СУБД """
		if self.StateConnected().data:
			return T21_StructResult_Bool(code     = CODES_COMPLETION.COMPLETED,
										 subcodes = {CODES_PROCESSING.SKIP})

		self.connection = None

		try:
			self.connection = psycopg2.connect(host            = self._options_server_ip,
											   port            = self._options_server_tcp_port,
											   dbname          = self._options_server_dbase,
											   user            = self._options_server_login,
											   password        = self._options_server_password,
											   connect_timeout = 5)
		except:
			return T21_StructResult_Bool(code     = CODES_COMPLETION.INTERRUPTED,
										 subcodes = {CODES_DB.ERROR_CONNECTION})

		self.PrepareDisconnect()

		return T21_StructResult_Bool(code = CODES_COMPLETION.COMPLETED,
									 data = True)

	def Disconnect(self) -> T21_StructResult_Bool:
		""" Отключение от СУБД """
		if self.connection is None:
			return T21_StructResult_Bool(code     = CODES_COMPLETION.COMPLETED,
										 subcodes = {CODES_PROCESSING.SKIP},
										 data     = True)

		try:
			self.connection.close()
		except:
			pass

		self.connection = None

		return T21_StructResult_Bool(code = CODES_COMPLETION.COMPLETED,
									 data = True)

	# Механика управления: Выполнение SQL
	def ExecSql(self, sql: str | list[str]) -> T21_StructResult_CursorPostgresql:
		""" Выполнение запроса с кодом """
		self.PrepareConnect()

		if self.connection is None:
			return T21_StructResult_CursorPostgresql(code     = CODES_COMPLETION.INTERRUPTED,
			                                         subcodes = {CODES_DB.ERROR_CONNECTION})

		try:
			sql_cursor      = self.connection.cursor()

			if   type(sql) is str  : sql_cursor.execute(sql + ';')
			elif type(sql) is list : sql_cursor.execute('\n'.join(sql))

			self.connection.commit()

			return T21_StructResult_CursorPostgresql(code   = CODES_COMPLETION.COMPLETED,
			                                         cursor = sql_cursor)

		except psycopg2.IntegrityError:
			self.PrepareDisconnect()
			return T21_StructResult_CursorPostgresql(code     = CODES_COMPLETION.INTERRUPTED,
			                                         subcodes = {CODES_DB.ERROR_DB})

		except psycopg2.ProgrammingError:
			self.PrepareDisconnect()
			return T21_StructResult_CursorPostgresql(code     = CODES_COMPLETION.INTERRUPTED,
			                                         subcodes = {CODES_DB.ERROR_SQL})

		except psycopg2.OperationalError:  # Сюда попадают и ошибки SQL-синтаксиса
			self.PrepareDisconnect()
			return T21_StructResult_CursorPostgresql(code     = CODES_COMPLETION.INTERRUPTED,
			                                         subcodes = {CODES_DB.ERROR_SQL})

		except:
			self.PrepareDisconnect()
			return T21_StructResult_CursorPostgresql(code     = CODES_COMPLETION.INTERRUPTED,
			                                         subcodes = {CODES_DB.ERROR_DB})

	def ExecSqlSelectRowCount(self, sql: str | list[str]) -> T21_StructResult_Int:
		"""Выполнение запроса с числом строк"""
		result_cursor = self.ExecSql(sql)
		if not result_cursor.code == CODES_COMPLETION.COMPLETED:
			self.PrepareDisconnect()

			return T21_StructResult_Int(code     = CODES_COMPLETION.COMPLETED,
										subcodes = result_cursor.subcodes)

		try   :
			cursor      = result_cursor.cursor
			count : int = cursor.rowcount
			cursor.close()
		except:
			return T21_StructResult_Int(code     = CODES_COMPLETION.COMPLETED,
										subcodes = {CODES_DB.ERROR_DB})

		self.PrepareDisconnect()

		return T21_StructResult_Int(code = CODES_COMPLETION.COMPLETED,
									data = count)

	def ExecSqlSelectSingle(self, sql: str) -> T21_StructResult_String:
		"""Выполнение запроса с получением значения"""
		result_cursor = self.ExecSql(sql)
		if not result_cursor.code == CODES_COMPLETION.COMPLETED:
			self.PrepareDisconnect()

			return T21_StructResult_String(code     = result_cursor.code,
										   subcodes = result_cursor.subcodes)

		data = []

		try:
			cursor           = result_cursor.cursor
			data : list[str] = cursor.fetchone()
			cursor.close()
		except Exception as err:
			if not f"{err}" == "no results to fetch": return T21_StructResult_String(code     = CODES_COMPLETION.INTERRUPTED,
											                                         subcodes = {CODES_DB.ERROR_DB})

		self.PrepareDisconnect()

		if (not data) or (data is None):
			return T21_StructResult_String(code     = CODES_COMPLETION.COMPLETED,
										   subcodes = {CODES_DATA.NO_DATA})

		return T21_StructResult_String(code = CODES_COMPLETION.COMPLETED,
									   data = data[0])

	def ExecSqlSelectHList(self, sql: str) -> T21_StructResult_List:
		"""Выполнение запроса с получением горизонтального списка значений"""
		result_cursor = self.ExecSql(sql)
		if not result_cursor.code == CODES_COMPLETION.COMPLETED:
			self.PrepareDisconnect()
			return T21_StructResult_List(code     = result_cursor.code,
										 subcodes = result_cursor.subcodes)

		data = []

		try:
			cursor           = result_cursor.cursor
			data : list[str] = cursor.fetchone()
			cursor.close()
		except Exception as err:
			if not f"{err}" == "no results to fetch": return T21_StructResult_List(code=CODES_COMPLETION.INTERRUPTED,
			                                                                       subcodes={CODES_DB.ERROR_DB})

		self.PrepareDisconnect()

		result      = T21_StructResult_List()
		result.code = CODES_COMPLETION.COMPLETED
		result.data = data[:] if data is not None else []

		match len(result.data):
			case 0: result.subcodes.add(CODES_DATA.NO_DATA)
			case 1: result.subcodes.add(CODES_DATA.SINGLE)
			case _: pass

		return result

	def ExecSqlSelectVList(self, sql: str) -> T21_StructResult_List:
		"""Выполнение запроса с получением вертикального списка значений"""
		result_cursor  = self.ExecSql(sql)
		if not result_cursor.code == CODES_COMPLETION.COMPLETED:
			self.PrepareDisconnect()
			return T21_StructResult_List(code     = result_cursor.code,
										 subcodes = result_cursor.subcodes)

		data = []

		try:
			cursor           = result_cursor.cursor
			data : list[str] = list(map(lambda raw: raw[0], cursor.fetchall()))
			cursor.close()
		except Exception as err:
			if not f"{err}" == "no results to fetch": return T21_StructResult_List(code=CODES_COMPLETION.INTERRUPTED,
			                                                                       subcodes={CODES_DB.ERROR_DB})

		self.PrepareDisconnect()

		result      = T21_StructResult_List()
		result.code = CODES_COMPLETION.COMPLETED
		result.data = data[:] if data is not None else []

		match len(result.data):
			case 0: result.subcodes.add(CODES_DATA.NO_DATA)
			case 1: result.subcodes.add(CODES_DATA.SINGLE)
			case _: pass

		return result

	def ExecSqlSelectMatrix(self, sql: str) -> T21_StructResult_List:
		"""Выполнение запроса с получением матрицы"""
		result_cursor  = self.ExecSql(sql)
		if not result_cursor.code == CODES_COMPLETION.COMPLETED:
			self.PrepareDisconnect()
			return T21_StructResult_List(code     = result_cursor.code,
										 subcodes = result_cursor.subcodes)

		data = []

		try:
			cursor           = result_cursor.cursor
			data : list[str] = cursor.fetchall()
			cursor.close()
		except Exception as err:
			if not f"{err}" == "no results to fetch": return T21_StructResult_List(code     = CODES_COMPLETION.INTERRUPTED,
											                                       subcodes = {CODES_DB.ERROR_DB})

		self.PrepareDisconnect()

		result      = T21_StructResult_List()
		result.code = CODES_COMPLETION.COMPLETED
		result.data = data[:] if data is not None else []

		match len(result.data):
			case 0: result.subcodes.add(CODES_DATA.NO_DATA)
			case 1: result.subcodes.add(CODES_DATA.SINGLE)
			case _: pass

		return result

	# Логика данных: Регистрация класса
	def RegisterClass(self, idc: str) -> T21_StructResult_Bool:
		""" Регистрация класса структурного объекта """
		if not CheckIdc(idc): return T21_StructResult_Bool(code     = CODES_COMPLETION.INTERRUPTED,
		                                                   subcodes = {CODES_DATA.ERROR_CHECK},
		                                                   data     = False)

		result      = T21_StructResult_Bool()
		result.code = CODES_COMPLETION.COMPLETED
		result.data = True

		sql: str = f"CREATE TABLE IF NOT EXISTS {idc} ({CACTUS_STRUCT_DATA.IDS.name_sql} TEXT PRIMARY KEY, {CACTUS_STRUCT_DATA.VLP.name_sql} TEXT NOT NULL, {CACTUS_STRUCT_DATA.VLT.name_sql} INT NOT NULL)"
		result_s_table = self.ExecSql(sql)
		if not result_s_table.code == CODES_COMPLETION.COMPLETED:
			result.code = CODES_COMPLETION.INTERRUPTED
			result.subcodes.add(CODES_PROCESSING.PARTIAL)
			result.subcodes.add(CODES_DB.ERROR_SQL)

		sql: str = f"CREATE TABLE IF NOT EXISTS {idc}_ ({CACTUS_STRUCT_DATA.IDS.name_sql} TEXT, {CACTUS_STRUCT_DATA.VLP.name_sql} TEXT NOT NULL, {CACTUS_STRUCT_DATA.VLT.name_sql} INT NOT NULL)"
		result_s_table = self.ExecSql(sql)
		if not result_s_table.code == CODES_COMPLETION.COMPLETED:
			result.code = CODES_COMPLETION.INTERRUPTED
			result.subcodes.add(CODES_PROCESSING.PARTIAL)
			result.subcodes.add(CODES_DB.ERROR_SQL)

		sql: str = f"CREATE INDEX IF NOT EXISTS index_{idc}_ids_ ON {idc}_ ({CACTUS_STRUCT_DATA.IDS.name_sql})"
		result_s_index = self.ExecSql(sql)
		if not result_s_index.code == CODES_COMPLETION.COMPLETED:
			result.code = CODES_COMPLETION.INTERRUPTED
			result.subcodes.add(CODES_PROCESSING.PARTIAL)
			result.subcodes.add(CODES_DB.ERROR_SQL)

		sql: str = f"CREATE INDEX IF NOT EXISTS index_{idc}_vlt_ ON {idc}_ ({CACTUS_STRUCT_DATA.VLT.name_sql})"
		result_s_index = self.ExecSql(sql)
		if not result_s_index.code == CODES_COMPLETION.COMPLETED:
			result.code = CODES_COMPLETION.INTERRUPTED
			result.subcodes.add(CODES_PROCESSING.PARTIAL)
			result.subcodes.add(CODES_DB.ERROR_SQL)

		return result

	# Логика данных: S-Ячейка
	def DeleteSCell(self, cell: T20_StructCell, flag_capture_delta: bool = False) -> T21_StructResult_StructCell:
		""" Удаление S-Ячейки """
		result_check : bool      = CheckIdc(cell.idc)
		result_check            &= CheckIdo(cell.ido)
		result_check            &= CheckIdp(cell.idp)

		if not result_check:
			return T21_StructResult_StructCell(code     = CODES_COMPLETION.INTERRUPTED,
											   subcodes = {CODES_DATA.ERROR_CHECK})

		cell_start  : T20_StructCell | None = None

		if flag_capture_delta:
			result_cell = self.ReadSCell(cell)
			cell_start  = result_cell.data

		sql         : str                   = f"DELETE FROM {cell.idc} WHERE {CACTUS_STRUCT_DATA.IDS.name_sql} = '{cell.ids}'"
		result_sql                          = self.ExecSqlSelectRowCount(sql)

		if not result_sql.code == CODES_COMPLETION.COMPLETED :
			return T21_StructResult_StructCell(code     = CODES_COMPLETION.INTERRUPTED,
											   subcodes = result_sql.subcodes)

		elif   result_sql.data == 0                          :
			return T21_StructResult_StructCell(code     = CODES_COMPLETION.COMPLETED,
											   subcodes = {CODES_DATA.NO_DATA})

		result                              = T21_StructResult_StructCell()
		result.code                         = CODES_COMPLETION.COMPLETED

		if flag_capture_delta:
			result_cell = self.ReadSCell(cell)
			cell_end    = result_cell.data
			cells       = [cell_start, cell_end]
			cells.remove(None)

			result.data = cells[0]

		return result

	def ReadSCell(self, cell: T20_StructCell) -> T21_StructResult_StructCell:
		""" Запрос S-Ячейки """
		result_check : bool      = CheckIdc(cell.idc)
		result_check            &= CheckIdo(cell.ido)
		result_check            &= CheckIdp(cell.idp)

		if not result_check:
			return T21_StructResult_StructCell(code     = CODES_COMPLETION.INTERRUPTED,
											   subcodes = {CODES_DATA.ERROR_CHECK})

		sql          : str       = f"SELECT {CACTUS_STRUCT_DATA.VLP.name_sql}, {CACTUS_STRUCT_DATA.VLT.name_sql} FROM {cell.idc} WHERE {CACTUS_STRUCT_DATA.IDS.name_sql} = '{cell.ids}'"
		result_sql               = self.ExecSqlSelectHList(sql)

		if not result_sql.code == CODES_COMPLETION.COMPLETED:
			return T21_StructResult_StructCell(code     = CODES_COMPLETION.INTERRUPTED,
											   subcodes = result_sql.subcodes)

		data         : list[str] = result_sql.data
		if len(data) < 2 :
			return T21_StructResult_StructCell(code     = CODES_COMPLETION.COMPLETED,
											   subcodes = {CODES_DATA.NO_DATA})

		result                   = T21_StructResult_StructCell()
		result.data              = CODES_COMPLETION.COMPLETED

		try                                 :
			result_cell     = T20_StructCell()
			result_cell.idc = cell.idc
			result_cell.ido = cell.ido
			result_cell.idp = cell.idp
			result_cell.vlp = data[0]
			result_cell.vlt = int(data[1])
		except                              :
			return T21_StructResult_StructCell(code     = CODES_COMPLETION.INTERRUPTED,
											   subcodes = {CODES_DATA.ERROR_CONVERT})

		result.data = result_cell
		return result

	def SyncSCell(self, cell: T20_StructCell, flag_capture_delta: bool = False) -> T21_StructResult_StructCell:
		""" Синхронизация S-Ячейки """
		result_check : bool      = CheckIdc(cell.idc)
		result_check            &= CheckIdo(cell.ido)
		result_check            &= CheckIdp(cell.idp)

		if not result_check                                  : return T21_StructResult_StructCell(code     = CODES_COMPLETION.INTERRUPTED,
											                                                      subcodes = {CODES_DATA.ERROR_CHECK})

		result_cell              = self.ReadSCell(cell)
		check_error  : bool      = not result_cell.code == CODES_COMPLETION.COMPLETED
		check_error             &= CODES_DATA.NO_DATA in result_cell.subcodes
		if check_error:
			return T21_StructResult_StructCell(code     = CODES_COMPLETION.INTERRUPTED,
											   subcodes = result_cell.subcodes)

		cell_in_container        = result_cell.data

		result_write : bool      = True
		if cell_in_container is not None: result_write = (cell_in_container.vlt < cell.vlt)

		result                   = T21_StructResult_StructCell()
		result.code              = CODES_COMPLETION.COMPLETED

		if not result_write:
			result.subcodes.add(CODES_PROCESSING.SKIP)

			if flag_capture_delta: result.data = cell_in_container

			return result

		result_cell              = self.WriteSCell(cell, False, flag_capture_delta)
		if not result_cell.code == CODES_COMPLETION.COMPLETED: return T21_StructResult_StructCell(code     = CODES_COMPLETION.INTERRUPTED,
											                                                      subcodes = result_cell.subcodes)

		result.subcodes          = result_cell.subcodes

		if flag_capture_delta: result.data = result_cell.data

		return result

	def WriteSCell(self, cell: T20_StructCell, flag_skip: bool = False, flag_capture_delta: bool = False) -> T21_StructResult_StructCell:
		""" Запись S-Ячейки """
		result_check : bool      = CheckIdc(cell.idc)
		result_check            &= CheckIdo(cell.ido)
		result_check            &= CheckIdp(cell.idp)

		if not result_check:
			return T21_StructResult_StructCell(code     = CODES_COMPLETION.INTERRUPTED,
											   subcodes = {CODES_DATA.ERROR_CHECK})

		cell_start   : T20_StructCell | None = None

		if flag_capture_delta: cell_start = self.ReadSCell(cell).data

		sql          : str  = f"INSERT INTO {cell.idc} ({CACTUS_STRUCT_DATA.IDS.name_sql}, {CACTUS_STRUCT_DATA.VLP.name_sql}, {CACTUS_STRUCT_DATA.VLT.name_sql}) VALUES ('{cell.ids}', '{cell.vlp}', {cell.vlt}) "
		if flag_skip : sql += f"ON CONFLICT ({CACTUS_STRUCT_DATA.IDS.name_sql}) DO NOTHING"
		else         : sql += f"ON CONFLICT ({CACTUS_STRUCT_DATA.IDS.name_sql}) DO UPDATE SET {CACTUS_STRUCT_DATA.VLP.name_sql}='{cell.vlp}', {CACTUS_STRUCT_DATA.VLT.name_sql}={cell.vlt}"

		result_sql                           = self.ExecSqlSelectRowCount(sql)

		if not result_sql.code == CODES_COMPLETION.COMPLETED:
			return T21_StructResult_StructCell(code     = CODES_COMPLETION.INTERRUPTED,
											   subcodes = result_sql.subcodes)

		result                               = T21_StructResult_StructCell()
		result.code                          = CODES_COMPLETION.COMPLETED

		if flag_capture_delta:
			cell_end    = self.ReadSCell(cell).data
			result.data = None if cell_end == cell_start else cell_end

			if result.data is None: result.subcodes.add(CODES_PROCESSING.SKIP)
		elif not result_sql.data:
			result.subcodes.add(CODES_PROCESSING.SKIP)

		return result

	# Логика данных: Пакет S-Ячеек
	def DeleteSCells(self, cell_cells: T20_StructCell | list[T20_StructCell], flag_capture_delta: bool = False) -> T21_StructResult_StructCells:
		""" Удаление пакета S-Ячеек """
		result_check : bool = False
		result_check       |= type(cell_cells) is T20_StructCell
		result_check       |= type(cell_cells) is list

		if not result_check:
			return T21_StructResult_StructCells(code     = CODES_COMPLETION.INTERRUPTED,
												subcodes = {CODES_DATA.ERROR_TYPE})

		cells_before : list[T20_StructCell] = []
		cells_after  : list[T20_StructCell] = []

		if flag_capture_delta: cells_before = self.ReadSCells(cell_cells).data

		result            = T21_StructResult_StructCells()

		if   type(cell_cells) is T20_StructCell:
			result_check : bool = CheckIdc(cell_cells.idc)

			if not result_check                                 : return T21_StructResult_StructCells(code     = CODES_COMPLETION.INTERRUPTED,
																	                                  subcodes = {CODES_DATA.ERROR_CHECK})

			sql     : str       = f"DELETE FROM {cell_cells.idc}"

			filters : list[str] = []
			if bool(cell_cells.ido): filters.append(f"({CACTUS_STRUCT_DATA.IDS.name_sql} LIKE '{cell_cells.ido}%')")
			if bool(cell_cells.idp): filters.append(f"({CACTUS_STRUCT_DATA.IDS.name_sql} LIKE '%{cell_cells.idp}')")
			if bool(cell_cells.vlp): filters.append(f"({CACTUS_STRUCT_DATA.VLP.name_sql} LIKE '{cell_cells.vlp}' = '{cell_cells.vlp}')")
			if bool(cell_cells.vlt): filters.append(f"({CACTUS_STRUCT_DATA.VLT.name_sql} LIKE '{cell_cells.vlt}' = '{cell_cells.vlt}')")

			if filters: sql += " WHERE " + ' AND '.join(filters)

			result_sql          = self.ExecSqlSelectMatrix(sql)

			if not result_sql.code == CODES_COMPLETION.COMPLETED: return T21_StructResult_StructCells(code     = CODES_COMPLETION.INTERRUPTED,
																	                                  subcodes = result_sql.subcodes)

			for raw_line in result_sql.data:
				try:
					ids = raw_line[0]
					vlp = raw_line[1]
					vlt = raw_line[2]

					result_cell = T20_StructCell()
					result_cell.idc = cell_cells.idc
					result_cell.ido = IdoFromIds(ids)
					result_cell.idp = IdpFromIds(ids)
					result_cell.vlp = vlp
					result_cell.vlt = int(vlt)
				except:
					result.subcodes.add(CODES_DATA.ERROR_CONVERT)
					result.subcodes.add(CODES_PROCESSING.PARTIAL)

		elif type(cell_cells) is list          :
			filters : dict[str, list[str]] = dict()

			for cell in cell_cells:
				result_check: bool      = CheckIdc(cell.idc)
				result_check           &= CheckIdo(cell.ido)
				result_check           &= CheckIdp(cell.idp)

				if not result_check:
					result.subcodes.add(CODES_DATA.ERROR_CHECK)
					result.subcodes.add(CODES_PROCESSING.PARTIAL)
					continue

				filters_idc : list[str] = filters.get(cell.idc, [])
				filters_idc.append(cell.ids)

				filters[cell.idc]       = filters_idc

			sql    : list[str]            = []
			sql.append("BEGIN;")

			for idc, idss in filters.items():
				select_sql  = f"DELETE FROM {idc} WHERE {CACTUS_STRUCT_DATA.IDS.name_sql} IN ("
				select_sql += ', '.join(f"'{ids}'" for ids in idss)
				select_sql += ");"

				sql.append(select_sql)

			sql.append("COMMIT;")

			result_sql          = self.ExecSqlSelectMatrix(sql)

			if not result_sql.code == CODES_COMPLETION.COMPLETED:
				self.ExecSql("ROLLBACK;")

				return T21_StructResult_StructCells(code     = CODES_COMPLETION.INTERRUPTED,
				                                    subcodes = result_sql.subcodes)

			for raw_line in result_sql.data:
				try:
					ids = raw_line[0]
					vlp = raw_line[1]
					vlt = raw_line[2]

					result_cell = T20_StructCell()
					result_cell.idc = cell_cells.idc
					result_cell.ido = IdoFromIds(ids)
					result_cell.idp = IdpFromIds(ids)
					result_cell.vlp = vlp
					result_cell.vlt = int(vlt)
				except:
					result.subcodes.add(CODES_DATA.ERROR_CONVERT)
					result.subcodes.add(CODES_PROCESSING.PARTIAL)

		if flag_capture_delta:
			cells_after = self.ReadSCells(cell_cells).data

			result.data = DifferenceLists(cells_before, cells_after, True)

			match len(result.data):
				case 0: result.subcodes.add(CODES_DATA.NO_DATA)
				case 1: result.subcodes.add(CODES_DATA.SINGLE)

		return result

	def ReadSCells(self, cell_cells: T20_StructCell | list[T20_StructCell]) -> T21_StructResult_StructCells:
		""" Запрос пакета S-Ячеек """
		result_check : bool = False
		result_check       |= type(cell_cells) is T20_StructCell
		result_check       |= type(cell_cells) is list

		if not result_check:
			return T21_StructResult_StructCells(code     = CODES_COMPLETION.INTERRUPTED,
												subcodes = {CODES_DATA.ERROR_TYPE})

		result            = T21_StructResult_StructCells()

		if   type(cell_cells) is T20_StructCell:
			result_check : bool = CheckIdo(cell_cells.idc)

			if not result_check                                 : return T21_StructResult_StructCells(code     = CODES_COMPLETION.INTERRUPTED,
																	                                  subcodes = {CODES_DATA.ERROR_CHECK})

			sql     : str       = f"SELECT {CACTUS_STRUCT_DATA.IDS.name_sql}, {CACTUS_STRUCT_DATA.VLP.name_sql}, {CACTUS_STRUCT_DATA.VLT.name_sql} FROM {cell_cells.idc}"

			filters : list[str] = []
			if bool(cell_cells.ido): filters.append(f"({CACTUS_STRUCT_DATA.IDS.name_sql} LIKE '{cell_cells.ido}%')")
			if bool(cell_cells.idp): filters.append(f"({CACTUS_STRUCT_DATA.IDS.name_sql} LIKE '%{cell_cells.idp}')")
			if bool(cell_cells.vlp): filters.append(f"({CACTUS_STRUCT_DATA.VLP.name_sql} LIKE '{cell_cells.vlp}' = '{cell_cells.vlp}')")
			if bool(cell_cells.vlt): filters.append(f"({CACTUS_STRUCT_DATA.VLT.name_sql} LIKE '{cell_cells.vlt}' = '{cell_cells.vlt}')")

			if filters: sql += " WHERE " + ' AND '.join(filters)

			result_sql          = self.ExecSqlSelectMatrix(sql)

			if not result_sql.code == CODES_COMPLETION.COMPLETED: return T21_StructResult_StructCells(code     = CODES_COMPLETION.INTERRUPTED,
																	                                  subcodes = result_sql.subcodes)

			for raw_line in result_sql.data:
				try:
					ids = raw_line[0]
					vlp = raw_line[1]
					vlt = raw_line[2]

					result_cell = T20_StructCell()
					result_cell.idc = cell_cells.idc
					result_cell.ido = IdoFromIds(ids)
					result_cell.idp = IdpFromIds(ids)
					result_cell.vlp = vlp
					result_cell.vlt = int(vlt)

					result.data.append(result_cell)
				except:
					result.subcodes.add(CODES_DATA.ERROR_CONVERT)
					result.subcodes.add(CODES_PROCESSING.PARTIAL)

		elif type(cell_cells) is list          :
			filters : dict[str, list[str]] = dict()

			for cell in cell_cells:
				result_check: bool      = CheckIdc(cell.idc)
				result_check           &= CheckIdo(cell.ido)
				result_check           &= CheckIdp(cell.idp)

				if not result_check:
					result.subcodes.add(CODES_DATA.ERROR_CHECK)
					result.subcodes.add(CODES_PROCESSING.PARTIAL)
					continue

				filters_idc : list[str] = filters.get(cell.idc, [])
				filters_idc.append(cell.ids)

				filters[cell.idc]       = filters_idc

			sql    : list[str]            = []

			for idc, idss in filters.items():
				select_sql  = f"SELECT '{idc}' as {CACTUS_STRUCT_DATA.IDC.name_sql}, {CACTUS_STRUCT_DATA.IDS.name_sql}, {CACTUS_STRUCT_DATA.VLP.name_sql}, {CACTUS_STRUCT_DATA.VLT.name_sql} FROM {idc} WHERE {CACTUS_STRUCT_DATA.IDS.name_sql} IN ("
				select_sql += ', '.join(f"'{ids}'" for ids in idss)
				select_sql += ")"

				sql.append(select_sql)

			sql    : str                  = " UNION ALL ".join(sql)

			result_sql          = self.ExecSqlSelectMatrix(sql)

			if not result_sql.code == CODES_COMPLETION.COMPLETED: return T21_StructResult_StructCells(code     = CODES_COMPLETION.INTERRUPTED,
																	                                  subcodes = result_sql.subcodes)

			for raw_line in result_sql.data:
				try:
					idc = raw_line[0]
					ids = raw_line[1]
					vlp = raw_line[2]
					vlt = raw_line[3]

					result_cell = T20_StructCell()
					result_cell.idc = idc
					result_cell.ido = IdoFromIds(ids)
					result_cell.idp = IdpFromIds(ids)
					result_cell.vlp = vlp
					result_cell.vlt = int(vlt)

					result.data.append(result_cell)
				except:
					result.subcodes.add(CODES_DATA.ERROR_CONVERT)
					result.subcodes.add(CODES_PROCESSING.PARTIAL)

		match len(result.data):
			case 0: result.subcodes.add(CODES_DATA.NO_DATA)
			case 1: result.subcodes.add(CODES_DATA.SINGLE)

		return result

	def SyncSCells(self, cells: list[T20_StructCell], flag_capture_delta: bool = False) -> T21_StructResult_StructCells:
		""" Запись пакета S-Ячеек """
		result                              = T21_StructResult_StructCells()

		cells_before : list[T20_StructCell] = []
		cells_after  : list[T20_StructCell] = []

		if flag_capture_delta: cells_before = self.ReadSCells(cells).data

		filters      : dict[str, list[str]] = dict()

		sqls: list[str] = []

		for cell in cells:
			result_check : bool = CheckIdc(cell.idc)
			result_check       &= CheckIdo(cell.ido)
			result_check       &= CheckIdp(cell.idp)

			if not result_check:
				result.subcodes.add(CODES_DATA.ERROR_CHECK)
				result.subcodes.add(CODES_PROCESSING.PARTIAL)
				continue

			sql : str = f"INSERT INTO {cell.idc} ({CACTUS_STRUCT_DATA.IDS.name_sql}, {CACTUS_STRUCT_DATA.VLP.name_sql}, {CACTUS_STRUCT_DATA.VLT.name_sql}) VALUES ('{cell.ids}', '{cell.vlp}', {cell.vlt}) "
			sql      += f"ON CONFLICT ({CACTUS_STRUCT_DATA.IDS.name_sql}) DO UPDATE SET {CACTUS_STRUCT_DATA.VLP.name_sql}='{cell.vlp}', {CACTUS_STRUCT_DATA.VLT.name_sql}={cell.vlt} WHERE {cell.idc}.{CACTUS_STRUCT_DATA.VLT.name_sql} <= {cell.vlt}"
			sql      += f";"

			sqls.append(sql)

		if not sqls: return T21_StructResult_StructCells(code     = CODES_COMPLETION.INTERRUPTED,
			                                             subcodes = {CODES_DATA.ERROR_CHECK})

		sqls.insert(0, "BEGIN;")
		sqls.append("COMMIT;")

		result_sql = self.ExecSql(sqls)

		if not result_sql.code == CODES_COMPLETION.COMPLETED:
			self.ExecSql("ROLLBACK;")

			return T21_StructResult_StructCells(code     = CODES_COMPLETION.INTERRUPTED,
			                                    subcodes = result_sql.subcodes)

		if flag_capture_delta:
			cells_after = self.ReadSCells(cells).data

			result.data = DifferenceLists(cells_before, cells_after)

			match len(result.data):
				case 0: result.subcodes.add(CODES_DATA.NO_DATA)
				case 1: result.subcodes.add(CODES_DATA.SINGLE)

		return result

	def WriteSCells(self, cells: list[T20_StructCell], flag_skip: bool = False,  flag_capture_delta: bool = False) -> T21_StructResult_StructCells:
		""" Запись пакета S-Ячеек """
		result                              = T21_StructResult_StructCells()

		cells_before : list[T20_StructCell] = []
		cells_after  : list[T20_StructCell] = []

		if flag_capture_delta: cells_before = self.ReadSCells(cells).data

		filters      : dict[str, list[str]] = dict()

		sqls: list[str] = []

		for cell in cells:
			result_check: bool = CheckIdc(cell.idc)
			result_check &= CheckIdo(cell.ido)
			result_check &= CheckIdp(cell.idp)

			if not result_check:
				result.subcodes.add(CODES_DATA.ERROR_CHECK)
				result.subcodes.add(CODES_PROCESSING.PARTIAL)
				continue

			sql         : str  = f"INSERT INTO {cell.idc} VALUES ('{cell.ids}', '{cell.vlp}', {cell.vlt}) "
			if flag_skip: sql += f"ON CONFLICT ({CACTUS_STRUCT_DATA.IDS.name_sql}) DO NOTHING"
			else        : sql += f"ON CONFLICT ({CACTUS_STRUCT_DATA.IDS.name_sql}) DO UPDATE SET {CACTUS_STRUCT_DATA.VLP.name_sql}='{cell.vlp}', {CACTUS_STRUCT_DATA.VLT.name_sql}={cell.vlt}"
			sql               += ';'

			sqls.append(sql)

		if not sqls: return T21_StructResult_StructCells(code     = CODES_COMPLETION.INTERRUPTED,
			                                             subcodes = {CODES_DATA.ERROR_CHECK})

		sqls.insert(0, "BEGIN;")
		sqls.append("COMMIT;")

		result_sql = self.ExecSql(sqls)

		if not result_sql.code == CODES_COMPLETION.COMPLETED:
			self.ExecSql("ROLLBACK;")

			return T21_StructResult_StructCells(code     = CODES_COMPLETION.INTERRUPTED,
			                                    subcodes = result_sql.subcodes)

		if flag_capture_delta:
			cells_after = self.ReadSCells(cells).data

			result.data = DifferenceLists(cells_before, cells_after, True)

			match len(result.data):
				case 0: result.subcodes.add(CODES_DATA.NO_DATA)
				case 1: result.subcodes.add(CODES_DATA.SINGLE)

		return result

	# Логика данных: D-Ячейка
	def DeleteDCell(self, cell: T20_StructCell, flag_capture_delta: bool = False) -> T21_StructResult_StructCell:
		""" Удаление D-Ячейки """
		result_check: bool = CheckIdc(cell.idc)
		result_check &= CheckIdo(cell.ido)
		result_check &= CheckIdp(cell.idp)
		result_check &= bool(cell.vlt)

		if not result_check:
			return T21_StructResult_StructCell(code=CODES_COMPLETION.INTERRUPTED,
			                                   subcodes={CODES_DATA.ERROR_CHECK})

		cell_start: T20_StructCell | None = None

		if flag_capture_delta:
			result_cell = self.ReadDCell(cell)
			cell_start = result_cell.data

		sql: str = f"DELETE FROM {cell.idc}_ WHERE ({CACTUS_STRUCT_DATA.IDS.name_sql} = '{cell.ids}') AND ({CACTUS_STRUCT_DATA.VLT.name_sql} = {cell.vlt})"
		result_sql = self.ExecSqlSelectRowCount(sql)

		if not result_sql.code == CODES_COMPLETION.COMPLETED:
			return T21_StructResult_StructCell(code=CODES_COMPLETION.INTERRUPTED,
			                                   subcodes=result_sql.subcodes)

		elif result_sql.data == 0:
			return T21_StructResult_StructCell(code=CODES_COMPLETION.COMPLETED,
			                                   subcodes={CODES_DATA.NO_DATA})

		result = T21_StructResult_StructCell()
		result.code = CODES_COMPLETION.COMPLETED

		if flag_capture_delta:
			result_cell = self.ReadDCell(cell)
			cell_end = result_cell.data
			cells = [cell_start, cell_end]
			cells.remove(None)

			result.data = cells[0]

		return result

	def ReadDCell(self, cell: T20_StructCell) -> T21_StructResult_StructCell:
		""" Запрос D-Ячейки """
		result_check: bool = CheckIdc(cell.idc)
		result_check &= CheckIdo(cell.ido)
		result_check &= CheckIdp(cell.idp)
		result_check &= bool(cell.vlt)

		if not result_check:
			return T21_StructResult_StructCell(code=CODES_COMPLETION.INTERRUPTED,
			                                   subcodes={CODES_DATA.ERROR_CHECK})

		sql: str = f"SELECT {CACTUS_STRUCT_DATA.VLP.name_sql}, {CACTUS_STRUCT_DATA.VLT.name_sql} FROM {cell.idc}_ WHERE ({CACTUS_STRUCT_DATA.IDS.name_sql} = '{cell.ids}') AND ({CACTUS_STRUCT_DATA.VLT.name_sql} = {cell.vlt})"
		result_sql = self.ExecSqlSelectHList(sql)

		if not result_sql.code == CODES_COMPLETION.COMPLETED:
			return T21_StructResult_StructCell(code=CODES_COMPLETION.INTERRUPTED,
			                                   subcodes=result_sql.subcodes)

		data: list[str] = result_sql.data
		if len(data) < 2:
			return T21_StructResult_StructCell(code=CODES_COMPLETION.INTERRUPTED,
			                                   subcodes={CODES_DATA.NO_DATA})

		result = T21_StructResult_StructCell()

		try:
			result_cell = T20_StructCell()
			result_cell.idc = cell.idc
			result_cell.ido = cell.ido
			result_cell.idp = cell.idp
			result_cell.vlp = data[0]
			result_cell.vlt = int(data[1])
		except:
			return T21_StructResult_StructCell(code=CODES_COMPLETION.INTERRUPTED,
			                                   subcodes={CODES_DATA.ERROR_CONVERT})

		result.data = result_cell
		return result

	def WriteDCell(self, cell: T20_StructCell, flag_capture_delta: bool = False) -> T21_StructResult_StructCell:
		""" Запись D-Ячейки """
		result_check: bool = CheckIdc(cell.idc)
		result_check &= CheckIdo(cell.ido)
		result_check &= CheckIdp(cell.idp)
		result_check &= bool(cell.vlt)

		if not result_check:
			return T21_StructResult_StructCell(code=CODES_COMPLETION.INTERRUPTED,
			                                   subcodes={CODES_DATA.ERROR_CHECK})

		cell_start: T20_StructCell | None = None

		if flag_capture_delta: cell_start = self.ReadDCell(cell).data

		sql: str = f"INSERT INTO {cell.idc}_ ({CACTUS_STRUCT_DATA.IDS.name_sql}, {CACTUS_STRUCT_DATA.VLP.name_sql}, {CACTUS_STRUCT_DATA.VLT.name_sql}) SELECT '{cell.ids}', '{cell.vlp}', '{cell.vlt}' WHERE NOT EXISTS (SELECT 1 FROM {cell.idc}_ WHERE {CACTUS_STRUCT_DATA.IDS.name_sql} = '{cell.ids}' AND _vlt = {cell.vlt})"

		result_sql = self.ExecSqlSelectRowCount(sql)

		if not result_sql.code == CODES_COMPLETION.COMPLETED:
			return T21_StructResult_StructCell(code=CODES_COMPLETION.INTERRUPTED,
			                                   subcodes=result_sql.subcodes)

		result = T21_StructResult_StructCell()
		result.code = CODES_COMPLETION.COMPLETED

		if flag_capture_delta:
			cell_end = self.ReadDCell(cell).data
			result.data = None if cell_end == cell_start else cell_end

			if result.data is None: result.subcodes.add(CODES_PROCESSING.SKIP)
		elif not result_sql.data:
			result.subcodes.add(CODES_PROCESSING.SKIP)

		return result

	# Логика данных: Пакет D-Ячеек
	def DeleteDCells(self, cell: T21_VltRange, flag_capture_delta: bool = False) -> T21_StructResult_StructCells:
		""" Удаление пакета D-Ячеек """
		result_check: bool = CheckIdc(cell.idc)
		result_check &= CheckIdo(cell.ido)
		result_check &= CheckIdp(cell.idp)

		if not result_check: return T21_StructResult_StructCells(code=CODES_COMPLETION.INTERRUPTED,
		                                                         subcodes={CODES_DATA.ERROR_CHECK})

		cells_before: list[T20_StructCell] = []
		cells_after: list[T20_StructCell] = []

		if flag_capture_delta: cells_before = self.ReadDCells(cell).data

		result = T21_StructResult_StructCells()

		sql: str = f"DELETE FROM {cell.idc}_"

		filters: list[str] = []
		filters.append(f"({CACTUS_STRUCT_DATA.IDS.name_sql} = '{cell.ids}')")
		if cell.vlt_l: filters.append(f"({CACTUS_STRUCT_DATA.VLT.name_sql} >= '{cell.vlt_l}')")
		if cell.vlt_r: filters.append(f"({CACTUS_STRUCT_DATA.VLT.name_sql} <= '{cell.vlt_r}')")

		if filters: sql += " WHERE " + ' AND '.join(filters)

		result_sql = self.ExecSqlSelectMatrix(sql)

		if not result_sql.code == CODES_COMPLETION.COMPLETED: return T21_StructResult_StructCells(code=CODES_COMPLETION.INTERRUPTED,
		                                                                                          subcodes=result_sql.subcodes)

		if flag_capture_delta:
			cells_after = self.ReadSCells(cell).data

			result.data = DifferenceLists(cells_before, cells_after, True)

			match len(result.data):
				case 0:
					result.subcodes.add(CODES_DATA.NO_DATA)
				case 1:
					result.subcodes.add(CODES_DATA.SINGLE)

		return result

	def ReadDCells(self, cell: T21_VltRange) -> T21_StructResult_StructCells:
		""" Запрос пакета D-Ячеек """
		result_check: bool = CheckIdc(cell.idc)
		result_check &= CheckIdo(cell.ido)
		result_check &= CheckIdp(cell.idp)

		if not result_check: return T21_StructResult_StructCells(code     =  CODES_COMPLETION.INTERRUPTED,
		                                                         subcodes = {CODES_DATA.ERROR_CHECK})

		filters: list[str] = []
		filters.append(f"({CACTUS_STRUCT_DATA.IDS.name_sql} = '{cell.ids}')")
		if cell.vlt_l: filters.append(f"({CACTUS_STRUCT_DATA.VLT.name_sql} >= '{cell.vlt_l}')")
		if cell.vlt_r: filters.append(f"({CACTUS_STRUCT_DATA.VLT.name_sql} <= '{cell.vlt_r}')")

		sql: str = f"SELECT {CACTUS_STRUCT_DATA.VLP.name_sql}, {CACTUS_STRUCT_DATA.VLT.name_sql} FROM {cell.idc}_ WHERE "
		sql     += ' AND '.join(filters)

		result_sql = self.ExecSqlSelectMatrix(sql)

		if not result_sql.code == CODES_COMPLETION.COMPLETED: return T21_StructResult_StructCells(code     = CODES_COMPLETION.INTERRUPTED,
		                                                                                          subcodes = result_sql.subcodes)

		result      = T21_StructResult_StructCells()
		result.code = CODES_COMPLETION.COMPLETED

		for raw_line in result_sql.data:
			try:
				vlp = raw_line[0]
				vlt = raw_line[1]

				result_cell = T20_StructCell()
				result_cell.idc = cell.idc
				result_cell.ido = cell.ido
				result_cell.idp = cell.idp
				result_cell.vlp = vlp
				result_cell.vlt = int(vlt)

				result.data.append(result_cell)
			except:
				result.subcodes.add(CODES_DATA.ERROR_CONVERT)
				result.subcodes.add(CODES_PROCESSING.PARTIAL)

		match len(result.data):
			case 0:
				result.subcodes.add(CODES_DATA.NO_DATA)
			case 1:
				result.subcodes.add(CODES_DATA.SINGLE)

		return result

	# Логика данных: Диапазон VLT
	def ReadVltRange(self, cell: T21_VltRange) -> T21_StructResult_VltRange:
		""" Запрос границ cUT D-Ячейки """
		result_check: bool = CheckIdc(cell.idc)
		result_check &= CheckIdo(cell.ido)
		result_check &= CheckIdp(cell.idp)

		if not result_check: return T21_StructResult_VltRange(code=CODES_COMPLETION.INTERRUPTED,
		                                                      subcodes={CODES_DATA.ERROR_CHECK})

		result = T21_StructResult_VltRange()

		filters: list[str] = []
		filters.append(f"({CACTUS_STRUCT_DATA.IDS.name_sql} = '{cell.ids}')")
		if cell.vlt_l: filters.append(f"({CACTUS_STRUCT_DATA.VLT.name_sql} >= '{cell.vlt_l}')")
		if cell.vlt_r: filters.append(f"({CACTUS_STRUCT_DATA.VLT.name_sql} <= '{cell.vlt_r}')")

		sql: str = f"SELECT MIN({CACTUS_STRUCT_DATA.VLT.name_sql}), MAX({CACTUS_STRUCT_DATA.VLT.name_sql}) FROM {cell.idc}_ WHERE"
		sql += ' AND '.join(filters)

		result_sql = self.ExecSqlSelectHList(sql)

		if not result_sql.code == CODES_COMPLETION.COMPLETED: return T21_StructResult_VltRange(code=CODES_COMPLETION.INTERRUPTED,
		                                                                                       subcodes=result_sql.subcodes)
		try:
			result.data = copy(cell)
			result.data.vlt_l = result_sql.data[0]
			result.data.vlt_r = result_sql.data[1]
		except:
			return T21_StructResult_VltRange(code=CODES_COMPLETION.INTERRUPTED,
			                                 subcodes={CODES_DATA.ERROR_CONVERT})

		return result

	def ReadVlts(self, cell: T21_VltRange) -> T21_StructResult_List:
		""" Запрос списка VLT """
		result_check: bool = CheckIdc(cell.idc)
		result_check &= CheckIdo(cell.ido)
		result_check &= CheckIdp(cell.idp)

		if not result_check: return T21_StructResult_List(code=CODES_COMPLETION.INTERRUPTED,
		                                                  subcodes={CODES_DATA.ERROR_CHECK})

		result = T21_StructResult_List()

		filters: list[str] = []
		filters.append(f"({CACTUS_STRUCT_DATA.IDS.name_sql} = '{cell.ids}')")
		if cell.vlt_l: filters.append(f"({CACTUS_STRUCT_DATA.VLT.name_sql} >= '{cell.vlt_l}')")
		if cell.vlt_r: filters.append(f"({CACTUS_STRUCT_DATA.VLT.name_sql} <= '{cell.vlt_r}')")

		sql: str = f"SELECT DISTINCT {CACTUS_STRUCT_DATA.VLT.name_sql} FROM {cell.idc}_ WHERE"
		sql += ' AND '.join(filters)

		result_sql = self.ExecSqlSelectVList(sql)

		if not result_sql.code == CODES_COMPLETION.COMPLETED: return T21_StructResult_List(code=CODES_COMPLETION.INTERRUPTED,
		                                                                                   subcodes=result_sql.subcodes)

		result.data = result_sql.data

		return result
