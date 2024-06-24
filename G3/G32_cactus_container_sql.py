# КАКТУС: КОНТЕЙНЕР-SQL
# 24 июн 2024

import psycopg2
import sqlite3

from   copy                     import copy

from   G00_cactus_codes         import *
from   G00_status_codes         import *

from   G10_cactus_validators    import *
from   G10_list                 import DifferenceLists

from   G21_cactus_struct        import *
from   G21_struct_result        import *

from   G31_cactus_container_sql import C31_ContainerSQL


# КАКТУС: КОНТЕЙНЕР-SQLite
class C32_ContainerSQLite(C31_ContainerSQL):
	""" Кактус: Контейнер SQLite """

	# Модель данных
	def Init_00(self):
		super().Init_00()

		self._options_filename : str = ""

	def Init_01(self):
		super().Init_01()

		self._container_type = CONTAINERS.CONTAINER_SQLITE

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
		
		try   :
			self.connection = s3m.Connection(path              = self.OptionsFilename().data,
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
	def ExecSql(self, sql: str | list[str]) -> T31_StructResult_CursorS3m:
		""" Выполнение запроса с кодом """
		self.PrepareConnect()

		if self.connection is None:
			return T31_StructResult_CursorS3m(code     = CODES_COMPLETION.INTERRUPTED,
		                                      subcodes = {CODES_DB.ERROR_CONNECTION})

		try:
			sql_cursor      = self.connection.cursor()

			if   type(sql) is str  : sql_cursor.execute(sql + ';')
			elif type(sql) is list : sql_cursor.executescript('\n'.join(sql))

			self.connection.commit()

			return T31_StructResult_CursorS3m(code   = CODES_COMPLETION.COMPLETED,
			                                  cursor = sql_cursor)

		except sqlite3.IntegrityError:
			self.PrepareDisconnect()
			return T31_StructResult_CursorS3m(code     = CODES_COMPLETION.INTERRUPTED,
			                                  subcodes = {CODES_DB.ERROR_DB})

		except sqlite3.ProgrammingError:
			self.PrepareDisconnect()
			return T31_StructResult_CursorS3m(code     = CODES_COMPLETION.INTERRUPTED,
			                                  subcodes = {CODES_DB.ERROR_SQL})

		except sqlite3.OperationalError:  # Сюда попадают и ошибки SQL-синтаксиса
			self.PrepareDisconnect()
			return T31_StructResult_CursorS3m(code     = CODES_COMPLETION.INTERRUPTED,
			                                  subcodes = {CODES_DB.ERROR_SQL})

		except:
			self.PrepareDisconnect()
			return T31_StructResult_CursorS3m(code     = CODES_COMPLETION.INTERRUPTED,
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

		try:
			cursor           = result_cursor.cursor
			data : list[str] = cursor.fetchone()
			cursor.close()
		except:
			return T21_StructResult_String(code     = CODES_COMPLETION.INTERRUPTED,
			                               subcodes = {CODES_DB.ERROR_DB})

		self.PrepareDisconnect()

		if not data:
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
		result.data = data[:]

		match len(data):
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
		result.data = data[:]

		match len(data):
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
		result.data = data[:]

		match len(data):
			case 0: result.subcodes.add(CODES_DATA.NO_DATA)
			case 1: result.subcodes.add(CODES_DATA.SINGLE)
			case _: pass

		return result

	# Логика данных: Управление регистрацией класса
	def RegisterClass(self, oci: str) -> T21_StructResult_Bool:
		""" Регистрация класса структурного объекта """
		if not ValidateOci(oci): return T21_StructResult_Bool(code     = CODES_COMPLETION.INTERRUPTED,
								                              subcodes = {CODES_DATA.ERROR_CHECK},
								                              data     = False)

		result      = T21_StructResult_Bool()
		result.code = CODES_COMPLETION.COMPLETED
		result.data = True

		sql      : str = f"CREATE TABLE IF NOT EXISTS {oci} ({CACTUS_STRUCT_DATA.SID.name_sql} TEXT PRIMARY KEY, {CACTUS_STRUCT_DATA.CVL.name_sql} TEXT NOT NULL, {CACTUS_STRUCT_DATA.CUT.name_sql} INT NOT NULL)"
		result_s_table = self.ExecSql(sql)
		if not result_s_table.code == CODES_COMPLETION.COMPLETED:
			result.code = CODES_COMPLETION.INTERRUPTED
			result.subcodes.add(CODES_PROCESSING.PARTIAL)
			result.subcodes.add(CODES_DB.ERROR_SQL)

		sql      : str = f"CREATE TABLE IF NOT EXISTS {oci}_ ({CACTUS_STRUCT_DATA.SID.name_sql} TEXT, {CACTUS_STRUCT_DATA.CVL.name_sql} TEXT NOT NULL, {CACTUS_STRUCT_DATA.CUT.name_sql} INT NOT NULL)"
		result_s_table = self.ExecSql(sql)
		if not result_s_table.code == CODES_COMPLETION.COMPLETED:
			result.code = CODES_COMPLETION.INTERRUPTED
			result.subcodes.add(CODES_PROCESSING.PARTIAL)
			result.subcodes.add(CODES_DB.ERROR_SQL)

		sql      : str = f"CREATE INDEX IF NOT EXISTS index_{oci}_sid_ ON {oci}_ ({CACTUS_STRUCT_DATA.SID.name_sql})"
		result_s_index = self.ExecSql(sql)
		if not result_s_index.code == CODES_COMPLETION.COMPLETED:
			result.code = CODES_COMPLETION.INTERRUPTED
			result.subcodes.add(CODES_PROCESSING.PARTIAL)
			result.subcodes.add(CODES_DB.ERROR_SQL)

		sql      : str = f"CREATE INDEX IF NOT EXISTS index_{oci}_cut_ ON {oci}_ ({CACTUS_STRUCT_DATA.CUT.name_sql})"
		result_s_index = self.ExecSql(sql)
		if not result_s_index.code == CODES_COMPLETION.COMPLETED:
			result.code = CODES_COMPLETION.INTERRUPTED
			result.subcodes.add(CODES_PROCESSING.PARTIAL)
			result.subcodes.add(CODES_DB.ERROR_SQL)

		return result

	# Логика данных: Управление S-Ячейкой
	def DeleteSCell(self, cell: T20_StructCell, flag_capture_delta: bool = False) -> T21_StructResult_StructCell:
		""" Удаление S-Ячейки """
		result_check  : bool                = ValidateOid(cell.oid)
		result_check                       &= ValidatePid(cell.pid)

		if not result_check:
			return T21_StructResult_StructCell(code     = CODES_COMPLETION.INTERRUPTED,
											   subcodes = {CODES_DATA.ERROR_CHECK})

		cell_start  : T20_StructCell | None = None

		if flag_capture_delta:
			result_cell = self.ReadSCell(cell)

			if not result_cell.code == CODES_COMPLETION.COMPLETED:
				return T21_StructResult_StructCell(code     = CODES_COMPLETION.INTERRUPTED,
				                                   subcodes = result_cell.subcodes)

			cell_start  = result_cell.data

		sql         : str                   = f"DELETE FROM {cell.oci} WHERE {CACTUS_STRUCT_DATA.SID.name_sql} = '{cell.sid}'"
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

			if not result_cell.code == CODES_COMPLETION.COMPLETED:
				return T21_StructResult_StructCell(code     = CODES_COMPLETION.INTERRUPTED,
				                                   subcodes = result_cell.subcodes)
			cell_end    = result_cell.data
			cells       = [cell_start, cell_end]
			cells.remove(None)

			result.data = cells[0]

		return result

	def ReadSCell(self, cell: T20_StructCell) -> T21_StructResult_StructCell:
		""" Запрос S-Ячейки """
		result_check : bool      = ValidateOid(cell.oid)
		result_check            &= ValidatePid(cell.pid)

		if not result_check:
			return T21_StructResult_StructCell(code     = CODES_COMPLETION.INTERRUPTED,
			                                   subcodes = {CODES_DATA.ERROR_CHECK})

		sql          : str       = f"SELECT {CACTUS_STRUCT_DATA.CVL.name_sql}, {CACTUS_STRUCT_DATA.CUT.name_sql} FROM {cell.oci} WHERE {CACTUS_STRUCT_DATA.SID.name_sql} = '{cell.sid}'"
		result_sql               = self.ExecSqlSelectHList(sql)

		if not result_sql.code == CODES_COMPLETION.COMPLETED:
			return T21_StructResult_StructCell(code     = CODES_COMPLETION.INTERRUPTED,
			                                   subcodes = result_sql.subcodes)

		data         : list[str] = result_sql.data
		if len(data) < 2 :
			return T21_StructResult_StructCell(code     = CODES_COMPLETION.INTERRUPTED,
			                                   subcodes = {CODES_DATA.NOT_ENOUGH})

		result                   = T21_StructResult_StructCell()

		try                                 :
			result_cell     = T20_StructCell()
			result_cell.oci = cell.oci
			result_cell.oid = cell.oid
			result_cell.pid = cell.pid
			result_cell.cvl = data[0]
			result_cell.cut = int(data[1])
		except                              :
			return T21_StructResult_StructCell(code     = CODES_COMPLETION.INTERRUPTED,
			                                   subcodes = {CODES_DATA.ERROR_CONVERT})

		result.data = result_cell
		return result

	def SyncSCell(self, cell: T20_StructCell, flag_capture_delta: bool = False) -> T21_StructResult_StructCell:
		""" Синхронизация S-Ячейки """
		result_check : bool = ValidateOid(cell.oid)
		result_check       &= ValidatePid(cell.pid)

		if not result_check:
			return T21_StructResult_StructCell(code     = CODES_COMPLETION.INTERRUPTED,
			                                   subcodes = {CODES_DATA.ERROR_CHECK})

		result_cell         = self.ReadSCell(cell)
		if not result_cell.code == CODES_COMPLETION.COMPLETED:
			return T21_StructResult_StructCell(code     = CODES_COMPLETION.INTERRUPTED,
			                                   subcodes = result_cell.subcodes)

		cell_in_container   = result_cell.data

		result_write : bool = True
		if cell_in_container is not None: result_write = (cell_in_container.cut < cell.cut)

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
		result_check : bool                  = ValidateOid(cell.oid)
		result_check                        &= ValidatePid(cell.pid)

		if not result_check:
			return T21_StructResult_StructCell(code     = CODES_COMPLETION.INTERRUPTED,
			                                   subcodes = {CODES_DATA.ERROR_CHECK})

		cell_start   : T20_StructCell | None = None

		if flag_capture_delta: cell_start = self.ReadSCell(cell).data

		sql          : str  = f"INSERT INTO {cell.oci} ({CACTUS_STRUCT_DATA.SID.name_sql}, {CACTUS_STRUCT_DATA.CVL.name_sql}, {CACTUS_STRUCT_DATA.CUT.name_sql}) VALUES ('{cell.sid}', '{cell.cvl}', {cell.cut}) "
		if flag_skip : sql += f"ON CONFLICT ({CACTUS_STRUCT_DATA.SID.name_sql}) DO NOTHING"
		else         : sql += f"ON CONFLICT ({CACTUS_STRUCT_DATA.SID.name_sql}) DO UPDATE SET {CACTUS_STRUCT_DATA.SID.name_sql}='{cell.sid}', {CACTUS_STRUCT_DATA.CVL.name_sql}='{cell.cvl}', {CACTUS_STRUCT_DATA.CUT.name_sql}={cell.cut}"

		result_sql                           = self.ExecSql(sql)

		if not result_sql.code == CODES_COMPLETION.COMPLETED:
			return T21_StructResult_StructCell(code     = CODES_COMPLETION.INTERRUPTED,
			                                   subcodes = result_sql.subcodes)

		result                               = T21_StructResult_StructCell()
		result.code                          = CODES_COMPLETION.COMPLETED

		if flag_capture_delta:
			cell_end    = self.ReadSCell(cell).data
			result.data = None if cell_end == cell_start else cell_end

		return result

	# Логика данных: Управление пакетом S-Ячеек
	def DeleteSCells(self, cell_cells: T20_StructCell | list[T20_StructCell], flag_capture_delta: bool = False) -> T21_StructResult_StructCells:
		""" Удаление пакета S-Ячеек """
		result                             = T21_StructResult_StructCells()
		result.code                        = CODES_COMPLETION.COMPLETED

		cells_start : list[T20_StructCell] = []

		if flag_capture_delta:
			result_cells = self.ReadSCells(cell_cells)

			if not result_cells.code == CODES_COMPLETION.COMPLETED:
				return T21_StructResult_StructCells(code     = CODES_COMPLETION.INTERRUPTED,
				                                    subcodes = result_cells.subcodes)

			cells_start  = result_cells.data

		if type(cell_cells) is T20_StructCell:
			if not ValidateOci(cell_cells.oci): return T21_StructResult_StructCells(code     = CODES_COMPLETION.INTERRUPTED,
			                                                                        subcodes = {CODES_DATA.ERROR_CHECK})

			sql     : str   = f"DELETE FROM {cell_cells.oci}"
			filters : list[str] = []

			if   cell_cells.oid and cell_cells.pid: filters.append(f"{CACTUS_STRUCT_DATA.SID.name_sql} = '{cell_cells.sid}'")
			elif cell_cells.oid                   : filters.append(f"{CACTUS_STRUCT_DATA.SID.name_sql} LIKE '{cell_cells.oid}.%'")
			elif cell_cells.pid                   : filters.append(f"{CACTUS_STRUCT_DATA.SID.name_sql} LIKE '%.{cell_cells.oid}'")

			if   cell_cells.cvl                   : filters.append(f"{CACTUS_STRUCT_DATA.CVL.name_sql} = '{cell_cells.cvl}'")
			if   cell_cells.cut                   : filters.append(f"{CACTUS_STRUCT_DATA.CUT.name_sql} = '{cell_cells.cut}'")

			if filters: sql += f" WHERE {' AND '.join(filters)}"
			result_sql       = self.ExecSql(sql)

			if not result_sql.code == CODES_COMPLETION.COMPLETED:
				return T21_StructResult_StructCells(code     = CODES_COMPLETION.INTERRUPTED,
				                                    subcodes = result_sql.subcodes)

		elif type(cell_cells) is list:
			sql : list[str] = []

			for cell in cell_cells:
				result_check  = ValidateOci(cell.oci)
				result_check &= ValidateOid(cell.oid)
				result_check &= ValidatePid(cell.pid)

				if not result_check:
					result.subcodes.add(CODES_PROCESSING.PARTIAL)
					result.subcodes.add(CODES_DATA.ERROR_CHECK)
					continue

				sql.append(f"DELETE FROM {cell.oci} WHERE {CACTUS_STRUCT_DATA.SID.name_sql} = '{cell.sid}';")

			sql.insert(0, "BEGIN;")

			result_sql      = self.ExecSql(sql)

			if not result_sql.code == CODES_COMPLETION.COMPLETED:
				return T21_StructResult_StructCells(code     = CODES_COMPLETION.INTERRUPTED,
				                                    subcodes = result_sql.subcodes)

		else:
			return T21_StructResult_StructCells(code     = CODES_COMPLETION.INTERRUPTED,
			                                    subcodes = {CODES_PROCESSING.SKIP, CODES_DATA.ERROR_TYPE})

		if flag_capture_delta:
			result_cells = self.ReadSCells(cell_cells)

			if not result_cells.code == CODES_COMPLETION.COMPLETED:
				return T21_StructResult_StructCells(code     = CODES_COMPLETION.INTERRUPTED,
				                                    subcodes = result_cells.subcodes)

			cells_end   = result_cells.data
			result.data = DifferenceLists(cells_start, cells_end, True)

		return result

	def ReadSCells(self, cell_cells: T20_StructCell | list[T20_StructCell]) -> T21_StructResult_StructCells:
		""" Запрос пакета S-Ячеек """
		result      = T21_StructResult_StructCells()
		result.code = CODES_COMPLETION.COMPLETED

		if type(cell_cells) is T20_StructCell:
			cells   : list[T20_StructCell] = []

			if not ValidateOci(cell_cells.oci)                  :
				return T21_StructResult_StructCells(code     = CODES_COMPLETION.INTERRUPTED,
			                                        subcodes = {CODES_DATA.ERROR_CHECK})

			sql     : str                  = f"SELECT {CACTUS_STRUCT_DATA.SID.name_sql}, {CACTUS_STRUCT_DATA.CVL.name_sql}, {CACTUS_STRUCT_DATA.CUT.name_sql} FROM {cell_cells.oci}"
			filters : list[str]            = []

			if   cell_cells.oid and cell_cells.pid: filters.append(f"{CACTUS_STRUCT_DATA.SID.name_sql} = '{cell_cells.oid}.{cell_cells.pid}'")
			elif cell_cells.oid                   : filters.append(f"{CACTUS_STRUCT_DATA.SID.name_sql} LIKE '{cell_cells.oid}.%'")
			elif cell_cells.pid                   : filters.append(f"{CACTUS_STRUCT_DATA.SID.name_sql} LIKE '%.{cell_cells.oid}'")

			if   cell_cells.cvl                   : filters.append(f"{CACTUS_STRUCT_DATA.CVL.name_sql} = '{cell_cells.cvl}'")
			if   cell_cells.cut                   : filters.append(f"{CACTUS_STRUCT_DATA.CUT.name_sql} = '{cell_cells.cut}'")

			if filters:	sql               += f" WHERE {' AND '.join(filters)}"
			result_sql                     = self.ExecSqlSelectMatrix(sql)

			if not result_sql.code == CODES_COMPLETION.COMPLETED:
				return T21_StructResult_StructCells(code     = CODES_COMPLETION.INTERRUPTED,
				                                    subcodes = result_sql.subcodes)

			for raw_data in result_sql.data:
				try:
					oid_pid = raw_data[0].split('.')

					oid     = oid_pid[0]
					pid     = oid_pid[1]
					cvl     = raw_data[1]
					cut     = int(raw_data[2])

					cells.append(T20_StructCell(oci=cell_cells.oci, oid=oid, pid=pid, cvl=cvl, cut=cut))
				except:
					result.subcodes.add(CODES_DATA.ERROR_CONVERT)
					result.subcodes.add(CODES_PROCESSING.PARTIAL)

			match len(cells):
				case 0: result.subcodes.add(CODES_DATA.NO_DATA)
				case 1: result.subcodes.add(CODES_DATA.SINGLE)

			return result

		elif type(cell_cells) is list:
			cells       : dict[str, T20_StructCell] = dict()
			result_cells: list[T20_StructCell]      = []
			oci         : str                       = ""

			for cell in cell_cells:
				result_check  = ValidateOci(cell.oci)
				result_check &= ValidateOid(cell.oid)
				result_check &= ValidatePid(cell.pid)

				if not result_check:
					result.subcodes.add(CODES_PROCESSING.PARTIAL)
					result.subcodes.add(CODES_DATA.ERROR_CHECK)
					continue

				cells[cell.sid] = cell
				if not oci: oci = cell.oci

			sql         : str                       = f"SELECT {CACTUS_STRUCT_DATA.SID.name_sql}, {CACTUS_STRUCT_DATA.CVL.name_sql}, {CACTUS_STRUCT_DATA.CUT.name_sql} FROM {oci} "
			if cells:
				sids : list[str] = list(map("'{}'".format, cells.keys()))
				sql             += f"WHERE {CACTUS_STRUCT_DATA.SID.name_sql} IN ({', '.join(sids)})"

			result_sql                              = self.ExecSqlSelectMatrix(sql)

			if not result_sql.code == CODES_COMPLETION.COMPLETED:
				return T21_StructResult_StructCells(code     = result.code,
				                                    subcodes = result_sql.subcodes)

			for raw_data in result_sql.data:
				try:
					sid     = raw_data[0]
					oid_pid = sid.split('.')
					oid     = oid_pid[0]
					pid     = oid_pid[1]
					cvl     = raw_data[1]
					cut     = int(raw_data[2])

					result_cells.append(T20_StructCell(oci=oci, oid=oid, pid=pid, cvl=cvl, cut=cut))
				except:
					result.subcodes.add(CODES_DATA.ERROR_CONVERT)
					result.subcodes.add(CODES_PROCESSING.PARTIAL)

			match len(cells):
				case 0: result.subcodes.add(CODES_DATA.NO_DATA)
				case 1:	result.subcodes.add(CODES_DATA.SINGLE)

			return result

		else:
			return T21_StructResult_StructCells(code     = CODES_COMPLETION.COMPLETED,
			                                    subcodes = {CODES_PROCESSING.SKIP, CODES_DATA.ERROR_TYPE})

	def SyncSCells(self, cells: list[T20_StructCell], flag_capture_delta: bool = False) -> T21_StructResult_StructCells:
		""" Запись пакета S-Ячеек """
		result                             = T21_StructResult_StructCells()
		result.code                        = CODES_COMPLETION.COMPLETED

		cells_start : list[T20_StructCell] = []

		if flag_capture_delta:
			result_cells = self.ReadSCells(cells)

			if not result_cells.code == CODES_COMPLETION.COMPLETED:
				return T21_StructResult_StructCells(code     = CODES_COMPLETION.INTERRUPTED,
				                                    subcodes = result_cells.subcodes)

			cells_start  = result_cells.data

		sql : list[str] = []

		for cell in cells:
			result_check = ValidateOci(cell.oci)
			result_check &= ValidateOid(cell.oid)
			result_check &= ValidatePid(cell.pid)

			if not result_check:
				result.subcodes.add(CODES_PROCESSING.PARTIAL)
				result.subcodes.add(CODES_DATA.ERROR_CHECK)
				continue

			sql_insert : str = f"INSERT INTO {cell.oci} ({CACTUS_STRUCT_DATA.SID.name_sql}, {CACTUS_STRUCT_DATA.CVL.name_sql}, {CACTUS_STRUCT_DATA.CUT.name_sql}) VALUES ('{cell.sid}', '{cell.cvl}', {cell.cut}) "
			sql_insert      += f"ON CONFLICT ({CACTUS_STRUCT_DATA.SID.name_sql}) DO UPDATE SET {CACTUS_STRUCT_DATA.CVL.name_sql}='{cell.cvl}', {CACTUS_STRUCT_DATA.CUT.name_sql}={cell.cut} WHERE {CACTUS_STRUCT_DATA.CUT.name_sql} < {cell.cut}"
			sql_insert      += f";"

			sql.append(sql_insert)

		if not sql:
			return T21_StructResult_StructCells(code     = CODES_COMPLETION.INTERRUPTED,
			                                    subcodes = {CODES_DATA.NO_DATA})

		sql.insert(0, "BEGIN;")

		result_sql          = self.ExecSql(sql)
		if not result_sql.code == CODES_COMPLETION.COMPLETED:
			return T21_StructResult_StructCells(code     = CODES_COMPLETION.INTERRUPTED,
			                                    subcodes = result.subcodes)

		if flag_capture_delta:
			result_cells = self.ReadSCells(cells)

			if not result_cells.code == CODES_COMPLETION.COMPLETED:
				return T21_StructResult_StructCells(code     = CODES_COMPLETION.INTERRUPTED,
				                                    subcodes = result_cells.subcodes)

			cells_end   = result_cells.data
			result.data = DifferenceLists(cells_start, cells_end)

		return result

	def WriteSCells(self, cells: list[T20_StructCell], flag_skip: bool = False, flag_capture_delta: bool = False) -> T21_StructResult_StructCells:
		""" Запись пакета S-Ячеек """
		result                             = T21_StructResult_StructCells()
		result.code                        = CODES_COMPLETION.COMPLETED

		cells_start : list[T20_StructCell] = []

		if flag_capture_delta:
			result_cells = self.ReadSCells(cells)

			if not result_cells.code == CODES_COMPLETION.COMPLETED:
				return T21_StructResult_StructCells(code     = CODES_COMPLETION.INTERRUPTED,
				                                    subcodes = result_cells.subcodes)

			cells_start  = result_cells.data

		sql         : list[str]            = []

		for cell in cells:
			result_check              = ValidateOci(cell.oci)
			result_check             &= ValidateOid(cell.oid)
			result_check             &= ValidatePid(cell.pid)

			if not result_check:
				result.subcodes.add(CODES_PROCESSING.PARTIAL)
				result.subcodes.add(CODES_DATA.ERROR_CHECK)
				continue

			sql_insert : str          = f"INSERT INTO {cell.oci} ({CACTUS_STRUCT_DATA.SID.name_sql}, {CACTUS_STRUCT_DATA.CVL.name_sql}, {CACTUS_STRUCT_DATA.CUT.name_sql}) VALUES ('{cell.sid}', '{cell.cvl}', {cell.cut}) "
			if flag_skip: sql_insert += f"ON CONFLICT ({CACTUS_STRUCT_DATA.SID.name_sql}) DO NOTHING"
			else        : sql_insert += f"ON CONFLICT ({CACTUS_STRUCT_DATA.SID.name_sql}) DO UPDATE SET {CACTUS_STRUCT_DATA.SID.name_sql}='{cell.sid}', {CACTUS_STRUCT_DATA.CVL.name_sql}='{cell.cvl}', {CACTUS_STRUCT_DATA.CUT.name_sql}={cell.cut}"

			sql.append(sql_insert)

		if not sql:
			return T21_StructResult_StructCells(code     = CODES_COMPLETION.INTERRUPTED,
			                                    subcodes = {CODES_DATA.NO_DATA})

		sql.insert(0, "BEGIN;")

		result_sql                         = self.ExecSql(sql)
		if not result_sql.code == CODES_COMPLETION.COMPLETED:
			return T21_StructResult_StructCells(code     = CODES_COMPLETION.INTERRUPTED,
			                                    subcodes = result.subcodes)

		if flag_capture_delta:
			result_cells = self.ReadSCells(cells)

			if not result_cells.code == CODES_COMPLETION.COMPLETED:
				return T21_StructResult_StructCells(code     = CODES_COMPLETION.INTERRUPTED,
				                                    subcodes = result_cells.subcodes)

			cells_end    = result_cells.data
			result.data  = DifferenceLists(cells_start, cells_end)

		return result

	# Логика данных: Управление D-Ячейкой
	def DeleteDCell(self, cell: T20_StructCell, flag_capture_delta: bool = False) -> T21_StructResult_StructCell:
		""" Удаление D-Ячейки """
		result_check : bool                  = ValidateOid(cell.oci)
		result_check                        &= ValidatePid(cell.oid)
		result_check                        &= ValidatePid(cell.pid)
		result_check                        &= bool(cell.cut)

		if not result_check:
			return T21_StructResult_StructCell(code     = CODES_COMPLETION.INTERRUPTED,
			                                   subcodes = {CODES_DATA.ERROR_CHECK})

		cell_start   : T20_StructCell | None = None

		if flag_capture_delta:
			result_cell = self.ReadDCell(cell)

			if not result_cell.code == CODES_COMPLETION.COMPLETED:
				return T21_StructResult_StructCell(code     = CODES_COMPLETION.INTERRUPTED,
				                                   subcodes = result_cell.subcodes)

			cell_start  = result_cell.data

		sql                                  = f"DELETE FROM {cell.oci}_ WHERE {CACTUS_STRUCT_DATA.SID.name_sql}='{cell.sid}' AND {CACTUS_STRUCT_DATA.CUT.name_sql}={cell.cut}"
		result_sql                          = self.ExecSqlSelectRowCount(sql)

		if not result_sql.code == CODES_COMPLETION.COMPLETED :
			return T21_StructResult_StructCell(code     = CODES_COMPLETION.INTERRUPTED,
			                                   subcodes = result_sql.subcodes)

		elif   result_sql.data == 0                          :
			return T21_StructResult_StructCell(code     = CODES_COMPLETION.COMPLETED,
			                                   subcodes = {CODES_DATA.NO_DATA})

		result                               = T21_StructResult_StructCell()
		result.code                          = CODES_COMPLETION.COMPLETED

		if not result_sql.code == CODES_COMPLETION.COMPLETED :
			return T21_StructResult_StructCell(code     = CODES_COMPLETION.INTERRUPTED,
			                                   subcodes = result_sql.subcodes)

		if flag_capture_delta:
			result_cell = self.ReadDCell(cell)

			if not result_cell.code == CODES_COMPLETION.COMPLETED:
				return T21_StructResult_StructCell(code     = CODES_COMPLETION.INTERRUPTED,
				                                   subcodes = result_cell.subcodes)
			cell_end    = result_cell.data
			cells       = [cell_start, cell_end]
			cells.remove(None)

			result.data = cells[0]

		return result

	def ReadDCell(self, cell: T20_StructCell) -> T21_StructResult_StructCell:
		""" Запрос D-Ячейки """
		result_check : bool      = ValidateOid(cell.oid)
		result_check            &= ValidatePid(cell.pid)
		result_check            &= bool(cell.cut)

		if not result_check:
			return T21_StructResult_StructCell(code     = CODES_COMPLETION.INTERRUPTED,
			                                   subcodes = {CODES_DATA.ERROR_CHECK})

		sql                      = f"SELECT {CACTUS_STRUCT_DATA.CVL.name_sql} FROM {cell.oci}_ WHERE {CACTUS_STRUCT_DATA.SID.name_sql}='{cell.sid}' AND {CACTUS_STRUCT_DATA.CUT.name_sql}={cell.cut}"
		result_sql               = self.ExecSqlSelectHList(sql)

		if not result_sql.code == CODES_COMPLETION.COMPLETED:
			return T21_StructResult_StructCell(code     = CODES_COMPLETION.INTERRUPTED,
			                                   subcodes = result_sql.subcodes)

		if CODES_DATA.NO_DATA in result_sql.subcodes:
			return T21_StructResult_StructCell(code     = CODES_COMPLETION.INTERRUPTED,
			                                   subcodes = {CODES_DATA.NOT_ENOUGH})

		data         : list[str] = result_sql.data

		result_cell              = copy(cell)
		result_cell.cvl          = data[0]

		result                   = T21_StructResult_StructCell()
		result.code              = CODES_COMPLETION.COMPLETED
		result.data              = result_cell

		return result

	def WriteDCell(self, cell: T20_StructCell, flag_capture_delta: bool = False) -> T21_StructResult_StructCell:
		""" Запись D-Ячейки """
		result_check : bool                  = ValidateOid(cell.oci)
		result_check                        &= ValidatePid(cell.oid)
		result_check                        &= ValidatePid(cell.pid)
		result_check                        &= bool(cell.cut)

		if not result_check:
			return T21_StructResult_StructCell(code     = CODES_COMPLETION.INTERRUPTED,
			                                   subcodes = {CODES_DATA.ERROR_CHECK})

		cell_start   : T20_StructCell | None = None

		if flag_capture_delta:
			result_cell = self.ReadDCell(cell)

			if not result_cell.code == CODES_COMPLETION.COMPLETED:
				return T21_StructResult_StructCell(code     = CODES_COMPLETION.INTERRUPTED,
				                                   subcodes = result_cell.subcodes)

			cell_start  = result_cell.data

		sql        = f"UPDATE {cell.oci}_ SET {CACTUS_STRUCT_DATA.CVL.name_sql}='{cell.cvl}' WHERE {CACTUS_STRUCT_DATA.SID.name_sql}='{cell.sid}' AND {CACTUS_STRUCT_DATA.CUT.name_sql}={cell.cut}"
		result_sql = self.ExecSqlSelectRowCount(sql)

		if not result_sql.code == CODES_COMPLETION.COMPLETED :
			return T21_StructResult_StructCell(code     = CODES_COMPLETION.INTERRUPTED,
			                                   subcodes = result_sql.subcodes)

		elif   result_sql.data == 0                          :
			return T21_StructResult_StructCell(code     = CODES_COMPLETION.COMPLETED,
			                                   subcodes = {CODES_DATA.NO_DATA})

		result                               = T21_StructResult_StructCell()
		result.code                          = CODES_COMPLETION.COMPLETED

		if not result_sql.code == CODES_COMPLETION.COMPLETED :
			return T21_StructResult_StructCell(code     = CODES_COMPLETION.INTERRUPTED,
			                                   subcodes = result_sql.subcodes)

		if flag_capture_delta:
			result_cell = self.ReadDCell(cell)

			if not result_cell.code == CODES_COMPLETION.COMPLETED:
				return T21_StructResult_StructCell(code     = CODES_COMPLETION.INTERRUPTED,
				                                   subcodes = result_cell.subcodes)
			cell_end    = result_cell.data
			cells       = [cell_start, cell_end]
			cells.remove(None)

			result.data = cells[0]

		return result

	# Логика данных: Управление пакетом D-Ячеек
	def DeleteDCells(self, cell: T21_CutRange, flag_capture_delta: bool = False) -> T21_StructResult_StructCells:
		""" Удаление пакета D-Ячеек """
		result                             = T21_StructResult_StructCells()
		result.code                        = CODES_COMPLETION.COMPLETED

		cells_start : list[T20_StructCell] = []

		if flag_capture_delta:
			result_cells = self.ReadDCells(cell)

			if not result_cells.code == CODES_COMPLETION.COMPLETED:
				return T21_StructResult_StructCells(code     = CODES_COMPLETION.INTERRUPTED,
				                                    subcodes = result_cells.subcodes)

			cells_start  = result_cells.data

		result_check : bool      = ValidateOid(cell.oid)
		result_check            &= ValidatePid(cell.pid)
		result_check            &= bool(cell.oci)

		if not result_check:
			return T21_StructResult_StructCells(code     = CODES_COMPLETION.INTERRUPTED,
			                                    subcodes = {CODES_DATA.ERROR_CHECK})

		filters      : list[str] = []
		filters.append(f"({CACTUS_STRUCT_DATA.SID.name_sql} = '{cell.sid}')")

		if   cell.cut_l : filters.append(f"({CACTUS_STRUCT_DATA.CUT.name_sql} >= {cell.cut_l})")
		if   cell.cut_r : filters.append(f"({CACTUS_STRUCT_DATA.CUT.name_sql} <= {cell.cut_r})")

		sql          : str       = f"DELETE FROM {cell.oci}_"
		sql                     += f" WHERE {' AND '.join(filters)}"

		result_sql               = self.ExecSql(sql)

		if not result_sql.code == CODES_COMPLETION.COMPLETED :
			return T21_StructResult_StructCells(code     = CODES_COMPLETION.INTERRUPTED,
			                                    subcodes = result_sql.subcodes)

		if flag_capture_delta:
			result_cells = self.ReadDCells(cell)

			if not result_cells.code == CODES_COMPLETION.COMPLETED:
				return T21_StructResult_StructCells(code     = CODES_COMPLETION.INTERRUPTED,
				                                    subcodes = result_cells.subcodes)

			cells_end   = result_cells.data
			result.data = DifferenceLists(cells_start, cells_end, True)

		return result

	def ReadDCells(self, cell: T21_CutRange) -> T21_StructResult_StructCells:
		""" Запрос пакета D-Ячеек """
		result      = T21_StructResult_StructCells()
		result.code = CODES_COMPLETION.COMPLETED

		result_check : bool      = ValidateOid(cell.oid)
		result_check            &= ValidatePid(cell.pid)
		result_check            &= bool(cell.oci)

		if not result_check:
			return T21_StructResult_StructCells(code     = CODES_COMPLETION.INTERRUPTED,
			                                    subcodes = {CODES_DATA.ERROR_CHECK})

		filters      : list[str] = []
		filters.append(f"({CACTUS_STRUCT_DATA.SID.name_sql} = '{cell.sid}')")

		if cell.cut_l: filters.append(f"({CACTUS_STRUCT_DATA.CUT.name_sql} >= {cell.cut_l})")
		if cell.cut_r: filters.append(f"({CACTUS_STRUCT_DATA.CUT.name_sql} <= {cell.cut_r})")

		sql          : str       = f"SELECT {CACTUS_STRUCT_DATA.SID.name_sql}, {CACTUS_STRUCT_DATA.CVL.name_sql}, {CACTUS_STRUCT_DATA.CUT.name_sql} FROM {cell.oci}_ "
		sql                     += f"WHERE " + (" AND ".join(filters))

		result_sql               = self.ExecSqlSelectMatrix(sql)

		if not result_sql.code == CODES_COMPLETION.COMPLETED:
			return T21_StructResult_StructCells(code     = CODES_COMPLETION.INTERRUPTED,
			                                    subcodes = result.subcodes)

		for raw_data in result_sql.data:
			try:
				sid     = raw_data[0]
				oid_pid = sid.split('.')

				oid     = oid_pid[0]
				pid     = oid_pid[1]
				cvl     = raw_data[1]
				cut     = int(raw_data[2])

				result.data.append(T20_StructCell(oci=cell.oci, oid=oid, pid=pid, cvl=cvl, cut=cut))
			except:
				result.subcodes.add(CODES_PROCESSING.PARTIAL)
				result.subcodes.add(CODES_DATA.ERROR_CONVERT)

		match len(result.data):
			case 0: result.subcodes.add(CODES_DATA.NO_DATA)
			case 1: result.subcodes.add(CODES_DATA.SINGLE)

		return result

	# Логика данных: Выборки D-Ячеек
	def ReadDCutRange(self, cell: T21_CutRange) -> T21_StructResult_CutRange:
		""" Запрос границ CUT D-Ячейки """
		result_check : bool      = ValidateOid(cell.oid)
		result_check            &= ValidatePid(cell.pid)
		result_check            &= bool(cell.oci)

		if not result_check:
			return T21_StructResult_CutRange(code     = CODES_COMPLETION.INTERRUPTED,
			                                 subcodes = {CODES_DATA.ERROR_CHECK})

		sql    = f"SELECT MIN({CACTUS_STRUCT_DATA.CUT.name_sql}) AS {CACTUS_STRUCT_DATA.CUT.name_sql}_0, MAX({CACTUS_STRUCT_DATA.CUT.name_sql}) AS {CACTUS_STRUCT_DATA.CUT.name_sql}_1 FROM {cell.oci}_ WHERE {CACTUS_STRUCT_DATA.SID.name_sql}='{cell.sid}' "
		if cell.cut_l: sql += f"AND ({CACTUS_STRUCT_DATA.CUT.name_sql} >= {cell.cut_l}) "
		if cell.cut_r: sql += f"AND ({CACTUS_STRUCT_DATA.CUT.name_sql} <= {cell.cut_r}) "

		result_sql = self.ExecSqlSelectHList(sql)

		if not result_sql.code == CODES_COMPLETION.COMPLETED:
			return T21_StructResult_CutRange(code     = CODES_COMPLETION.INTERRUPTED,
			                                 subcodes = result_sql.subcodes)

		try:
			data   = result_sql.data
			cut_l  = int(data[0])
			cut_r  = int(data[1])
		except:
			return T21_StructResult_CutRange(code     = CODES_COMPLETION.INTERRUPTED,
			                                 subcodes = {CODES_DATA.ERROR_CONVERT})

		return T21_StructResult_CutRange(code = CODES_COMPLETION.COMPLETED,
		                                 data = T21_CutRange(oci=cell.oci, oid=cell.oid, pid=cell.pid, cut_l=cut_l, cut_r=cut_r))

	def ReadDCuts(self, cell: T21_CutRange) -> T21_StructResult_List:
		""" Запрос списка CUT """
		result_check : bool      = ValidateOid(cell.oid)
		result_check            &= ValidatePid(cell.pid)
		result_check            &= bool(cell.oci)

		if not result_check:
			return T21_StructResult_List(code     = CODES_COMPLETION.INTERRUPTED,
			                             subcodes = {CODES_DATA.ERROR_CHECK})

		sql          : str       = f"SELECT {CACTUS_STRUCT_DATA.CUT.name_sql} FROM {cell.oci}_ WHERE {CACTUS_STRUCT_DATA.SID.name_sql}='{cell.sid}' "
		if cell.cut_l: sql += f"AND ({CACTUS_STRUCT_DATA.CUT.name_sql} >= {cell.cut_l}) "
		if cell.cut_r: sql += f"AND ({CACTUS_STRUCT_DATA.CUT.name_sql} <= {cell.cut_r}) "

		result_sql = self.ExecSqlSelectVList(sql)

		if not result_sql.code == CODES_COMPLETION.COMPLETED:
			return T21_StructResult_List(code     = CODES_COMPLETION.INTERRUPTED,
			                             subcodes = result_sql.subcodes)

		result      = T21_StructResult_List()
		result.code = CODES_COMPLETION.COMPLETED
		result.data = result_sql.data

		match len(result_sql.data):
			case 0: result.subcodes.add(CODES_DATA.NO_DATA)
			case 1: result.subcodes.add(CODES_DATA.SINGLE)

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

		self._container_type = CONTAINERS.CONTAINER_POSTGRESQL

	def Init_10(self):
		super().Init_10()

		self.connection : psycopg2.connection | None = None

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
		if self.connection is None: return T21_StructResult_Bool(code = CODES_COMPLETION.COMPLETED, data = False)

		try                       : cursor = self.connection.cursor()
		except                    : return T21_StructResult_Bool(code = CODES_COMPLETION.COMPLETED, data = False)

		return T21_StructResult_Bool(code = CODES_COMPLETION.COMPLETED, data = True)

	# Логика данных: Управление подключением
	def Connect(self) -> T21_StructResult_Bool:
		""" Подключение к СУБД """
		if not self.StateConnected().data:
			try                             : self.connection = psycopg2.connect(host=self._options_server_ip, port=self._options_server_tcp_port, dbname=self._options_server_dbase, user=self._options_server_login, password=self._options_server_password, connect_timeout=5)
			except                          : return T21_StructResult_Bool(code = CODES_COMPLETION.INTERRUPTED, subcodes = [CODES_DB.ERROR_DB], data = False)

		return T21_StructResult_Bool(code = CODES_COMPLETION.COMPLETED, data = True)

	def Disconnect(self) -> T21_StructResult_Bool:
		""" Отключение от СУБД """
		if     self.connection is None    : return T21_StructResult_Bool(code = CODES_COMPLETION.COMPLETED, data = True)

		try                               : self.connection.close()
		except                            : pass

		self.connection = None

		return T21_StructResult_Bool(code = CODES_COMPLETION.COMPLETED, data = True)

	# УПРАВЛЕНИЕ РЕГИСТРАЦИЕЙ КЛАССА
	def RegisterClass(self, oci: str) -> T21_StructResult_Bool:
		""" Регистрация класса структурного объекта """
		if not ValidateOci(oci)                                 : return T21_StructResult_Bool(code = CODES_COMPLETION.INTERRUPTED, subcodes = [CODES_DATA.ERROR_CHECK], data = False)

		sql      : str = f"CREATE TABLE IF NOT EXISTS {oci} ({CACTUS_STRUCT_DATA.SID.name_sql} TEXT PRIMARY KEY, {CACTUS_STRUCT_DATA.CVL.name_sql} TEXT, {CACTUS_STRUCT_DATA.CUT.name_sql} INT)"
		result_s_table = self.ExecSql(sql)
		if not result_s_table.code == CODES_COMPLETION.COMPLETED: return T21_StructResult_Bool(code = result_s_table.code, subcodes = result_s_table.subcodes, data = False)

		sql      : str = f"CREATE INDEX IF NOT EXISTS index_{oci}_sid ON {oci} ({CACTUS_STRUCT_DATA.SID.name_sql})"
		result_s_index = self.ExecSql(sql)
		if not result_s_index.code == CODES_COMPLETION.COMPLETED: return T21_StructResult_Bool(code = result_s_table.code, subcodes = result_s_table.subcodes, data = False)

		sql      : str = f"CREATE TABLE IF NOT EXISTS {oci}_ ({CACTUS_STRUCT_DATA.SID.name_sql} TEXT, {CACTUS_STRUCT_DATA.CVL.name_sql} TEXT, {CACTUS_STRUCT_DATA.CUT.name_sql} INT)"
		result_s_table = self.ExecSql(sql)
		if not result_s_table.code == CODES_COMPLETION.COMPLETED: return T21_StructResult_Bool(code = result_s_table.code, subcodes = result_s_table.subcodes, data = False)

		sql      : str = f"CREATE INDEX IF NOT EXISTS index_{oci}_sid_ ON {oci}_ ({CACTUS_STRUCT_DATA.SID.name_sql})"
		result_s_index = self.ExecSql(sql)
		if not result_s_index.code == CODES_COMPLETION.COMPLETED: return T21_StructResult_Bool(code = result_s_index.code, subcodes = result_s_index.subcodes, data = False)

		sql      : str = f"CREATE INDEX IF NOT EXISTS index_{oci}_cut_ ON {oci}_ ({CACTUS_STRUCT_DATA.CUT.name_sql})"
		result_s_index = self.ExecSql(sql)
		if not result_s_index.code == CODES_COMPLETION.COMPLETED: return T21_StructResult_Bool(code = result_s_index.code, subcodes = result_s_index.subcodes, data = False)

		return T21_StructResult_Bool(code = CODES_COMPLETION.COMPLETED, data = True)

	# ВЫПОЛНЕНИЕ ЗАПРОСОВ
	def ExecSql(self, sql: str | list[str]) -> T31_StructResult_CursorS3m:
		""" Выполнение запроса с кодом """
		self.PrepareConnect()

		if self.connection is None: return T31_StructResult_CursorS3m(code = CODES_COMPLETION.INTERRUPTED, subcodes = [CODES_DB.ERROR_CONNECTION])

		try:
			sql_cursor      = self.connection.cursor()

			if   type(sql) is str  : sql_cursor.execute(sql + ';')
			elif type(sql) is list : sql_cursor.execute('\n'.join(sql))

			self.connection.commit()

			return T31_StructResult_CursorS3m(code = CODES_COMPLETION.COMPLETED, data = sql_cursor)

		except sqlite3.IntegrityError:
			self.PrepareDisconnect()
			return T31_StructResult_CursorS3m(code = CODES_COMPLETION.INTERRUPTED, subcodes = [CODES_DB.ERROR_DB])

		except sqlite3.ProgrammingError:
			self.PrepareDisconnect()
			return T31_StructResult_CursorS3m(code = CODES_COMPLETION.INTERRUPTED, subcodes = [CODES_DB.ERROR_SQL])

		except sqlite3.OperationalError:  # Сюда попадают и ошибки SQL-синтаксиса
			self.PrepareDisconnect()
			return T31_StructResult_CursorS3m(code = CODES_COMPLETION.INTERRUPTED, subcodes = [CODES_DB.ERROR_SQL])

		except:
			self.PrepareDisconnect()
			return T31_StructResult_CursorS3m(code = CODES_COMPLETION.INTERRUPTED, subcodes = [CODES_DB.ERROR_DB])

	def ExecSqlSelectRowCount(self, sql: str | list[str]) -> T21_StructResult_Int:
		"""Выполнение запроса с числом строк"""
		result_cursor = self.ExecSql(sql)
		if not result_cursor.code == CODES_COMPLETION.COMPLETED:
			self.PrepareDisconnect()
			return T21_StructResult_Int(code = result_cursor.code, subcodes = result_cursor.subcodes)

		cursor        = result_cursor.cursor
		result : int  = cursor.rowcount
		cursor.close()

		self.PrepareDisconnect()

		return T21_StructResult_Int(code = CODES_COMPLETION.COMPLETED, data = result)

	def ExecSqlSelectSingle(self, sql: str) -> T21_StructResult_String:
		"""Выполнение запроса с получением значения"""
		result_cursor = self.ExecSql(sql)
		if not result_cursor.code == CODES_COMPLETION.COMPLETED:
			self.PrepareDisconnect()
			return T21_StructResult_String(code = result_cursor.code, subcodes = result_cursor.subcodes)

		cursor             = result_cursor.cursor
		data   : list[str] = cursor.fetchone()
		cursor.close()

		self.PrepareDisconnect()

		if not data: return T21_StructResult_String(code = CODES_COMPLETION.INTERRUPTED, subcodes = [CODES_DATA.NO_DATA])

		result : str       = data[0]
		return T21_StructResult_String(code = CODES_COMPLETION.COMPLETED, data = result)

	def ExecSqlSelectHList(self, sql: str) -> T21_StructResult_List:
		"""Выполнение запроса с получением горизонтального списка значений"""
		result_cursor = self.ExecSql(sql)
		if not result_cursor.code == CODES_COMPLETION.COMPLETED:
			self.PrepareDisconnect()
			return T21_StructResult_List(code = result_cursor.code, subcodes = result_cursor.subcodes)

		cursor         = result_cursor.cursor
		data   : list[str] = cursor.fetchone()
		cursor.close()

		self.PrepareDisconnect()

		match len(data):
			case 0: return T21_StructResult_List(code = CODES_COMPLETION.COMPLETED, subcodes = [CODES_DATA.NO_DATA])
			case 1: return T21_StructResult_List(code = CODES_COMPLETION.COMPLETED, subcodes = [CODES_DATA.SINGLE])
			case _: return T21_StructResult_List(code = CODES_COMPLETION.COMPLETED, data = data)

	def ExecSqlSelectVList(self, sql: str) -> T21_StructResult_List:
		"""Выполнение запроса с получением вертикального списка значений"""
		result_cursor    = self.ExecSql(sql)
		if not result_cursor.code == CODES_COMPLETION.COMPLETED:
			self.PrepareDisconnect()
			return T21_StructResult_List(code = result_cursor.code, subcodes = result_cursor.subcodes)

		cursor           = result_cursor.cursor
		data : list[str] = list(map(lambda data: data[0], cursor.fetchall()))
		cursor.close()

		self.PrepareDisconnect()

		match len(data):
			case 0: return T21_StructResult_List(code = CODES_COMPLETION.COMPLETED, subcodes = [CODES_DATA.NO_DATA])
			case 1: return T21_StructResult_List(code = CODES_COMPLETION.COMPLETED, subcodes = [CODES_DATA.SINGLE])
			case _: return T21_StructResult_List(code = CODES_COMPLETION.COMPLETED, data = data)

	def ExecSqlSelectMatrix(self, sql: str) -> T21_StructResult_List:
		"""Выполнение запроса с получением матрицы"""
		result_cursor    = self.ExecSql(sql)
		if not result_cursor.code == CODES_COMPLETION.COMPLETED:
			self.PrepareDisconnect()
			return T21_StructResult_List(code = result_cursor.code, subcodes = result_cursor.subcodes)

		cursor           = result_cursor.cursor
		data : list[str] = cursor.fetchall()
		cursor.close()

		self.PrepareDisconnect()

		match len(data):
			case 0: return T21_StructResult_List(code = CODES_COMPLETION.COMPLETED, subcodes = [CODES_DATA.NO_DATA])
			case 1: return T21_StructResult_List(code = CODES_COMPLETION.COMPLETED, subcodes = [CODES_DATA.SINGLE])
			case _: return T21_StructResult_List(code = CODES_COMPLETION.COMPLETED, data = data)

	# УПРАВЛЕНИЕ S-ЯЧЕЙКОЙ
	def ReadSCell(self, cell: T20_StructCell) -> T21_StructResult_StructCell:
		""" Запрос S-Ячейки """
		if not ValidateOci(cell.oci): return T21_StructResult_StructCell(code = CODES_COMPLETION.INTERRUPTED, subcodes = [CODES_DATA.ERROR_CHECK])
		if not ValidateOid(cell.oid): return T21_StructResult_StructCell(code = CODES_COMPLETION.INTERRUPTED, subcodes = [CODES_DATA.ERROR_CHECK])
		if not ValidatePid(cell.pid): return T21_StructResult_StructCell(code = CODES_COMPLETION.INTERRUPTED, subcodes = [CODES_DATA.ERROR_CHECK])

		sql  : str   = f"SELECT {CACTUS_STRUCT_DATA.CVL.name_sql}, {CACTUS_STRUCT_DATA.CUT.name_sql} FROM {cell.oci} WHERE {CACTUS_STRUCT_DATA.SID.name_sql} = '{cell.sid}'"

		result_data  = self.ExecSqlSelectHList(sql)
		if not result_data.code == CODES_COMPLETION.COMPLETED: return T21_StructResult_StructCell(result_data.code)

		data : list[str] = result_data.data
		if len(data) < 2                    : return T21_StructResult_StructCell(code = CODES_COMPLETION.INTERRUPTED, subcodes = [CODES_DATA.NOT_ENOUGH])

		try                                 :
			result       = T20_StructCell()
			result.oci   = cell.oci
			result.oid   = cell.oid
			result.pid   = cell.pid
			result.cvl   = data[0]
			result.cut   = int(data[1])

		except                              : return T21_StructResult_StructCell(code = CODES_COMPLETION.INTERRUPTED, subcodes = [CODES_DATA.ERROR_CONVERT])

		return T21_StructResult_StructCell(code = CODES_COMPLETION.COMPLETED, data = result)

	def DeleteSCell(self, cell: T20_StructCell) -> T21_StructResult_StructCell:
		""" Удаление S-Ячейки """
		if not ValidateOci(cell.oci): return T21_StructResult_StructCell(code = CODES_COMPLETION.INTERRUPTED, subcodes = [CODES_DATA.ERROR_CHECK])
		if not ValidateOid(cell.oid): return T21_StructResult_StructCell(code = CODES_COMPLETION.INTERRUPTED, subcodes = [CODES_DATA.ERROR_CHECK])
		if not ValidatePid(cell.pid): return T21_StructResult_StructCell(code = CODES_COMPLETION.INTERRUPTED, subcodes = [CODES_DATA.ERROR_CHECK])

		sql  : str = f"DELETE FROM {cell.oci} WHERE {CACTUS_STRUCT_DATA.SID.name_sql} = '{cell.sid}'"
		result = self.ExecSqlSelectRowCount(sql)
		if not result.code == CODES_COMPLETION.COMPLETED : return T21_StructResult_StructCell(code = CODES_COMPLETION.INTERRUPTED, subcodes = result.subcodes)
		if not result.data == 1                          : return T21_StructResult_StructCell(code = CODES_COMPLETION.COMPLETED, subcodes = [CODES_DATA.NO_DATA])

		return T21_StructResult_StructCell(code = CODES_COMPLETION.COMPLETED, data = cell)

	def SyncSCell(self, cell: T20_StructCell) -> T21_StructResult_StructCell:
		""" Синхронизация S-Ячейки """
		result_read       = self.ReadSCell(cell)

		cell_in_container = result_read.data
		if cell_in_container.cut >  cell.cut: return T21_StructResult_StructCell(code = CODES_COMPLETION.COMPLETED, subcodes = [CODES_PROCESSING.SKIP], data = cell)

		return self.WriteSCell(cell)

	def WriteSCell(self, cell: T20_StructCell, flag_ignore: bool = False) -> T21_StructResult_StructCell:
		""" Запись S-Ячейки """
		if not ValidateOci(cell.oci): return T21_StructResult_StructCell(code = CODES_COMPLETION.INTERRUPTED, subcodes = [CODES_DATA.ERROR_CHECK])
		if not ValidateOid(cell.oid): return T21_StructResult_StructCell(code = CODES_COMPLETION.INTERRUPTED, subcodes = [CODES_DATA.ERROR_CHECK])
		if not ValidatePid(cell.pid): return T21_StructResult_StructCell(code = CODES_COMPLETION.INTERRUPTED, subcodes = [CODES_DATA.ERROR_CHECK])

		sql : str   = f"INSERT INTO {cell.oci} ({CACTUS_STRUCT_DATA.SID.name_sql}, {CACTUS_STRUCT_DATA.CVL.name_sql}, {CACTUS_STRUCT_DATA.CUT.name_sql}) VALUES ('{cell.sid}', '{cell.cvl}', {cell.cut}) "
		if flag_ignore: sql += f"ON CONFLICT ({CACTUS_STRUCT_DATA.SID.name_sql}) DO NOTHING"
		else               : sql += f"ON CONFLICT ({CACTUS_STRUCT_DATA.SID.name_sql}) DO UPDATE SET {CACTUS_STRUCT_DATA.SID.name_sql}='{cell.sid}', {CACTUS_STRUCT_DATA.CVL.name_sql}='{cell.cvl}', {CACTUS_STRUCT_DATA.CUT.name_sql}={cell.cut}"

		result      = self.ExecSql(sql)
		actual_cell = self.ReadSCell(cell)

		return T21_StructResult_StructCell(code = CODES_COMPLETION.COMPLETED, data = actual_cell.data)

	# УПРАВЛЕНИЕ ПАКЕТОМ S-ЯЧЕЕК
	def DeleteSCells(self, cell_cells: T20_StructCell | list[T20_StructCell]) -> T21_StructResult_StructCells:
		""" Удаление пакета S-Ячеек """
		cells_0 : list[T20_StructCell] = self.ReadSCells(cell_cells).data

		if type(cell_cells) is T20_StructCell:
			if not ValidateOci(cell_cells.oci): return T21_StructResult_StructCells(code = CODES_COMPLETION.INTERRUPTED, subcodes = [CODES_DATA.ERROR_CHECK])

			sql     : str       = f"DELETE FROM {cell_cells.oci}"
			filters : list[str] = []

			if   cell_cells.oid and cell_cells.pid: filters.append(f"{CACTUS_STRUCT_DATA.SID.name_sql} = '{cell_cells.sid}'")
			elif cell_cells.oid                   : filters.append(f"{CACTUS_STRUCT_DATA.SID.name_sql} LIKE '{cell_cells.oid}.%'")
			elif cell_cells.pid                   : filters.append(f"{CACTUS_STRUCT_DATA.SID.name_sql} LIKE '%.{cell_cells.oid}'")

			if   cell_cells.cvl                   : filters.append(f"{CACTUS_STRUCT_DATA.CVL.name_sql} = '{cell_cells.cvl}'")
			if   cell_cells.cut                   : filters.append(f"{CACTUS_STRUCT_DATA.CUT.name_sql} = '{cell_cells.cut}'")

			if filters: sql += f" WHERE {' AND '.join(filters)}"
			result              = self.ExecSql(sql)

		elif type(cell_cells) is list:
			sql : list[str] = []

			for cell in cell_cells:
				if not ValidateOci(cell.oci): return T21_StructResult_StructCells(code = CODES_COMPLETION.INTERRUPTED, subcodes = [CODES_DATA.ERROR_CHECK])
				if not ValidateOid(cell.oid): return T21_StructResult_StructCells(code = CODES_COMPLETION.INTERRUPTED, subcodes = [CODES_DATA.ERROR_CHECK])
				if not ValidatePid(cell.pid): return T21_StructResult_StructCells(code = CODES_COMPLETION.INTERRUPTED, subcodes = [CODES_DATA.ERROR_CHECK])

				sql.append(f"DELETE FROM {cell.oci} WHERE {CACTUS_STRUCT_DATA.SID.name_sql} = '{cell.sid}';")

			sql.insert(0, "BEGIN;")

			result          = self.ExecSql(sql)

		else:
			return T21_StructResult_StructCells(code = CODES_COMPLETION.INTERRUPTED, subcodes = [CODES_DATA.ERROR_TYPE])

		if not result.code == CODES_COMPLETION.COMPLETED   : return T21_StructResult_StructCells(code = CODES_COMPLETION.INTERRUPTED, subcodes = result.subcodes)

		cells_1 : list[T20_StructCell] = self.ReadSCells(cell_cells).data
		cells   : list[T20_StructCell] = []

		for cell in cells_0:
			if cell not in cells_1: cells.append(cell)

		match len(cells):
			case 0: return T21_StructResult_StructCells(code = CODES_COMPLETION.COMPLETED, subcodes = [CODES_DATA.NO_DATA])
			case 1: return T21_StructResult_StructCells(code = CODES_COMPLETION.COMPLETED, subcodes = [CODES_DATA.SINGLE])
			case _: return T21_StructResult_StructCells(code = CODES_COMPLETION.COMPLETED, data = cells)

	def ReadSCells(self, cell_cells: T20_StructCell | list[T20_StructCell]) -> T21_StructResult_StructCells:
		""" Запрос пакета S-Ячеек """
		if type(cell_cells) is T20_StructCell:
			cells: list[T20_StructCell] = []

			if not ValidateOci(cell_cells.oci): return T21_StructResult_StructCells(code = CODES_COMPLETION.INTERRUPTED, subcodes = [CODES_DATA.ERROR_CHECK])

			sql     : str   = f"SELECT {CACTUS_STRUCT_DATA.SID.name_sql}, {CACTUS_STRUCT_DATA.CVL.name_sql}, {CACTUS_STRUCT_DATA.CUT.name_sql} FROM {cell_cells.oci}"
			filters : list[str] = []

			if   cell_cells.oid and cell_cells.pid: filters.append(f"{CACTUS_STRUCT_DATA.SID.name_sql} = '{cell_cells.oid}.{cell_cells.pid}'")
			elif cell_cells.oid                   : filters.append(f"{CACTUS_STRUCT_DATA.SID.name_sql} LIKE '{cell_cells.oid}.%'")
			elif cell_cells.pid                   : filters.append(f"{CACTUS_STRUCT_DATA.SID.name_sql} LIKE '%.{cell_cells.oid}'")

			if   cell_cells.cvl                   : filters.append(f"{CACTUS_STRUCT_DATA.CVL.name_sql} = '{cell_cells.cvl}'")
			if   cell_cells.cut                   : filters.append(f"{CACTUS_STRUCT_DATA.CUT.name_sql} = '{cell_cells.cut}'")

			if filters:	sql    += f" WHERE {' AND '.join(filters)}"
			result          = self.ExecSqlSelectMatrix(sql)

			if not result.code == CODES_COMPLETION.COMPLETED: return T21_StructResult_StructCells(result.code)

			for raw_data in result.data:
				try:
					oid_pid = raw_data[0].split('.')

					oid = oid_pid[0]
					pid = oid_pid[1]
					cvl = raw_data[1]
					cut = int(raw_data[2])

					cells.append(T20_StructCell(oci=cell_cells.oci, oid=oid, pid=pid, cvl=cvl, cut=cut))
				except: continue

			match len(cells):
				case 0: return T21_StructResult_StructCells(code = CODES_COMPLETION.COMPLETED, subcodes = [CODES_DATA.NO_DATA])
				case 1: return T21_StructResult_StructCells(code = CODES_COMPLETION.COMPLETED, subcodes = [CODES_DATA.SINGLE])
				case _: return T21_StructResult_StructCells(code = CODES_COMPLETION.COMPLETED, data = cells)

		elif type(cell_cells) is list:
			cells       : dict[str, T20_StructCell] = dict()
			result_cells: list[T20_StructCell]  = []
			oci         : str                   = ""

			for cell in cell_cells:
				if not ValidateOci(cell.oci): continue
				if not ValidateOid(cell.oid): continue
				if not ValidatePid(cell.pid): continue

				cells[cell.sid] = cell
				if not oci: oci = cell.oci

			sql   : str                   = f"SELECT {CACTUS_STRUCT_DATA.SID.name_sql}, {CACTUS_STRUCT_DATA.CVL.name_sql}, {CACTUS_STRUCT_DATA.CUT.name_sql} FROM {oci} "
			if cells:
				sids : list[str] = list(map("'{}'".format, cells.keys()))
				sql             += f"WHERE {CACTUS_STRUCT_DATA.SID.name_sql} IN ({', '.join(sids)})"

			result          = self.ExecSqlSelectMatrix(sql)

			if not result.code == CODES_COMPLETION.COMPLETED: return T21_StructResult_StructCells(result.code)

			for raw_data in result.data:
				try:
					sid = raw_data[0]
					oid_pid = sid.split('.')
					oid = oid_pid[0]
					pid = oid_pid[1]
					cvl = raw_data[1]
					cut = int(raw_data[2])

					result_cells.append(T20_StructCell(oci=oci, oid=oid, pid=pid, cvl=cvl, cut=cut))
				except: continue

			match len(cells):
				case 0: return T21_StructResult_StructCells(code = CODES_COMPLETION.COMPLETED, subcodes = [CODES_DATA.NO_DATA])
				case 1: return T21_StructResult_StructCells(code = CODES_COMPLETION.COMPLETED, subcodes = [CODES_DATA.SINGLE])
				case _: return T21_StructResult_StructCells(code = CODES_COMPLETION.COMPLETED, data = result_cells)

		return T21_StructResult_StructCells(code = CODES_COMPLETION.COMPLETED, subcodes = [CODES_PROCESSING.SKIP])

	def SyncSCells(self, cells: list[T20_StructCell]) -> T21_StructResult_StructCells:
		""" Синхронизация пакета S-Ячеек """
		sql : list[str] = []

		for cell in cells:
			if not ValidateOci(cell.oci): continue
			if not ValidateOid(cell.oid): continue
			if not ValidatePid(cell.pid): continue

			sql_insert : str = f"INSERT INTO {cell.oci} ({CACTUS_STRUCT_DATA.SID.name_sql}, {CACTUS_STRUCT_DATA.CVL.name_sql}, {CACTUS_STRUCT_DATA.CUT.name_sql}) VALUES ('{cell.sid}', '{cell.cvl}', {cell.cut}) "
			sql_insert      += f"ON CONFLICT ({CACTUS_STRUCT_DATA.SID.name_sql}) DO UPDATE SET {CACTUS_STRUCT_DATA.CVL.name_sql}='{cell.cvl}', {CACTUS_STRUCT_DATA.CUT.name_sql}={cell.cut} WHERE {cell.oci}.{CACTUS_STRUCT_DATA.CUT.name_sql} < {cell.cut}"
			sql_insert      += f";"

			sql.append(sql_insert)

		if not sql: return T21_StructResult_StructCells(code = CODES_COMPLETION.INTERRUPTED, subcodes = [CODES_DATA.NO_DATA])

		sql.insert(0, "BEGIN;")

		result = self.ExecSql(sql)
		if not result.code == CODES_COMPLETION.COMPLETED: return T21_StructResult_StructCells(code = CODES_COMPLETION.INTERRUPTED, subcodes = result.subcodes, data = cells)

		return self.ReadSCells(cells)

	def WriteSCells(self, cells: list[T20_StructCell]) -> T21_StructResult_StructCells:
		""" Запись пакета S-Ячеек """
		sql : list[str] = []

		for cell in cells:
			if not ValidateOci(cell.oci): continue
			if not ValidateOid(cell.oid): continue
			if not ValidatePid(cell.pid): continue

			sql_insert : str = f"INSERT INTO {cell.oci} ({CACTUS_STRUCT_DATA.SID.name_sql}, {CACTUS_STRUCT_DATA.CVL.name_sql}, {CACTUS_STRUCT_DATA.CUT.name_sql}) VALUES ('{cell.sid}', '{cell.cvl}', {cell.cut}) "
			sql_insert      += f"ON CONFLICT ({CACTUS_STRUCT_DATA.SID.name_sql}) DO UPDATE SET {CACTUS_STRUCT_DATA.CVL.name_sql}='{cell.cvl}', {CACTUS_STRUCT_DATA.CUT.name_sql}={cell.cut} "
			sql_insert      += f";"

			sql.append(sql_insert)

		if not sql: return T21_StructResult_StructCells(code = CODES_COMPLETION.INTERRUPTED, subcodes = [CODES_DATA.NO_DATA])

		sql.insert(0, "BEGIN;")
		sql.append("COMMIT;")

		result = self.ExecSql(sql)
		if not result.code == CODES_COMPLETION.COMPLETED: return T21_StructResult_StructCells(code = CODES_COMPLETION.INTERRUPTED, subcodes = result.subcodes, data = cells)

		return self.ReadSCells(cells)

	# УПРАВЛЕНИЕ D-ЯЧЕЙКОЙ
	def DeleteDCell(self, cell: T20_StructCell) -> T21_StructResult_StructCell:
		""" Удаление D-Ячейки """
		if not ValidateOci(cell.oci): return T21_StructResult_StructCell(code = CODES_COMPLETION.INTERRUPTED, subcodes = [CODES_DATA.ERROR_CHECK])
		if not ValidateOid(cell.oid): return T21_StructResult_StructCell(code = CODES_COMPLETION.INTERRUPTED, subcodes = [CODES_DATA.ERROR_CHECK])
		if not ValidatePid(cell.pid): return T21_StructResult_StructCell(code = CODES_COMPLETION.INTERRUPTED, subcodes = [CODES_DATA.ERROR_CHECK])
		if not cell.cut             : return T21_StructResult_StructCell(code = CODES_COMPLETION.INTERRUPTED, subcodes = [CODES_DATA.ERROR_CHECK])

		result_cell = self.ReadDCell(cell)
		sql     = f"DELETE FROM {cell.oci}_ WHERE {CACTUS_STRUCT_DATA.SID.name_sql}='{cell.sid}' AND {CACTUS_STRUCT_DATA.CUT.name_sql}={cell.cut}"
		result  = self.ExecSql(sql)
		if not result.code == CODES_COMPLETION.COMPLETED: return T21_StructResult_StructCell(code = result.code, data = result_cell.data)

		return result_cell

	def ReadDCell(self, cell: T20_StructCell) -> T21_StructResult_StructCell:
		""" Запрос D-Ячейки """
		if not ValidateOci(cell.oci): return T21_StructResult_StructCell(code = CODES_COMPLETION.INTERRUPTED, subcodes = [CODES_DATA.ERROR_CHECK])
		if not ValidateOid(cell.oid): return T21_StructResult_StructCell(code = CODES_COMPLETION.INTERRUPTED, subcodes = [CODES_DATA.ERROR_CHECK])
		if not ValidatePid(cell.pid): return T21_StructResult_StructCell(code = CODES_COMPLETION.INTERRUPTED, subcodes = [CODES_DATA.ERROR_CHECK])
		if not cell.cut             : return T21_StructResult_StructCell(code = CODES_COMPLETION.INTERRUPTED, subcodes = [CODES_DATA.ERROR_CHECK])

		sql    = f"SELECT {CACTUS_STRUCT_DATA.CVL.name_sql} FROM {cell.oci}_ WHERE {CACTUS_STRUCT_DATA.SID.name_sql}='{cell.sid}' AND {CACTUS_STRUCT_DATA.CUT.name_sql}={cell.cut}"
		result = self.ExecSqlSelectSingle(sql)
		if not result.code == CODES_COMPLETION.COMPLETED: return T21_StructResult_StructCell(code = CODES_COMPLETION.INTERRUPTED, subcodes = result.subcodes)

		return T21_StructResult_StructCell(code = CODES_COMPLETION.COMPLETED, data = T20_StructCell(oci=cell.oci, oid=cell.oid, pid=cell.pid, cvl=result.text, cut=cell.cut))

	def WriteDCell(self, cell: T20_StructCell) -> T21_StructResult_StructCell:
		""" Запись D-Ячейки """
		if not ValidateOci(cell.oci): return T21_StructResult_StructCell(code = CODES_COMPLETION.INTERRUPTED, subcodes = [CODES_DATA.ERROR_CHECK])
		if not ValidateOid(cell.oid): return T21_StructResult_StructCell(code = CODES_COMPLETION.INTERRUPTED, subcodes = [CODES_DATA.ERROR_CHECK])
		if not ValidatePid(cell.pid): return T21_StructResult_StructCell(code = CODES_COMPLETION.INTERRUPTED, subcodes = [CODES_DATA.ERROR_CHECK])
		if not cell.cut             : return T21_StructResult_StructCell(code = CODES_COMPLETION.INTERRUPTED, subcodes = [CODES_DATA.ERROR_CHECK])

		sql     = f"UPDATE {cell.oci}_ SET {CACTUS_STRUCT_DATA.CVL.name_sql}='{cell.cvl}' WHERE {CACTUS_STRUCT_DATA.SID.name_sql}='{cell.sid}' AND {CACTUS_STRUCT_DATA.CUT.name_sql}={cell.cut}"
		result  = self.ExecSqlSelectRowCount(sql)

		if not result.code == CODES_COMPLETION.COMPLETED: return T21_StructResult_StructCell(code = CODES_COMPLETION.INTERRUPTED, subcodes = result.subcodes)
		if     result.data == 0:
			sql     = f"INSERT INTO {cell.oci}_ ({CACTUS_STRUCT_DATA.SID.name_sql}, {CACTUS_STRUCT_DATA.CVL.name_sql}, {CACTUS_STRUCT_DATA.CUT.name_sql}) VALUES ('{cell.sid}', '{cell.cvl}', {cell.cut})"
			result  = self.ExecSql(sql)
			if not result.code == CODES_COMPLETION.COMPLETED: return T21_StructResult_StructCell(code = CODES_COMPLETION.INTERRUPTED, subcodes = result.subcodes)

		return self.ReadDCell(cell)

	# УПРАВЛЕНИЕ ПАКЕТОМ D-ЯЧЕЕК
	def ReadDCells(self, cell: T21_CutRange) -> T21_StructResult_StructCells:
		""" Запрос пакета D-Ячеек """
		if not ValidateOci(cell.oci): return T21_StructResult_StructCells(code = CODES_COMPLETION.INTERRUPTED, subcodes = [CODES_DATA.ERROR_CHECK])

		cells   : list[T20_StructCell] = []

		filters : list[str]        = []
		if cell.oid and cell.pid: filters.append(f"({CACTUS_STRUCT_DATA.SID.name_sql}='{cell.sid}')")
		if cell.cut_l           : filters.append(f"({CACTUS_STRUCT_DATA.CUT.name_sql}>={cell.cut_l})")
		if cell.cut_r           : filters.append(f"({CACTUS_STRUCT_DATA.CUT.name_sql}<={cell.cut_r})")

		sql     : str              = f"SELECT {CACTUS_STRUCT_DATA.SID.name_sql}, {CACTUS_STRUCT_DATA.CVL.name_sql}, {CACTUS_STRUCT_DATA.CUT.name_sql} FROM {cell.oci}_ "
		if filters: sql               += f"WHERE " + " AND ".join(filters)

		result                     = self.ExecSqlSelectMatrix(sql)
		if not result.code == CODES_COMPLETION.COMPLETED: return T21_StructResult_StructCells(code = CODES_COMPLETION.INTERRUPTED, subcodes = result.subcodes)

		for raw_data in result.data:
			try:
				sid = raw_data[0]
				oid_pid = sid.split('.')

				oid = oid_pid[0]
				pid = oid_pid[1]
				cvl = raw_data[1]
				cut = int(raw_data[2])

				cells.append(T20_StructCell(oci=cell.oci, oid=oid, pid=pid, cvl=cvl, cut=cut))
			except: continue

		match len(cells):
			case 0: return T21_StructResult_StructCells(code = CODES_COMPLETION.COMPLETED, subcodes = [CODES_DATA.NO_DATA])
			case 1: return T21_StructResult_StructCells(code = CODES_COMPLETION.COMPLETED, subcodes = [CODES_DATA.SINGLE])
			case _: return T21_StructResult_StructCells(code = CODES_COMPLETION.COMPLETED, data = cells)

	def DeleteDCells(self, cell_cells: T21_CutRange | list[T20_StructCell]) -> T21_StructResult_StructCells:
		""" Удаление пакета D-Ячеек """
		cells_0 : list[T20_StructCell] = self.ReadDCells(cell_cells).data

		if type(cell_cells) is T21_CutRange:
			if not ValidateOci(cell_cells.oci): return T21_StructResult_StructCells(code = CODES_COMPLETION.INTERRUPTED, subcodes = [CODES_DATA.ERROR_CHECK])

			sql     : str   = f"DELETE FROM {cell_cells.oci}_"
			filters : list[str] = []

			if   cell_cells.oid and cell_cells.pid: filters.append(f"({CACTUS_STRUCT_DATA.SID.name_sql} = '{cell_cells.sid}')")
			elif cell_cells.oid                   : filters.append(f"({CACTUS_STRUCT_DATA.SID.name_sql} LIKE '{cell_cells.oid}.%')")
			elif cell_cells.pid                   : filters.append(f"({CACTUS_STRUCT_DATA.SID.name_sql} LIKE '%.{cell_cells.oid}')")

			if   cell_cells.cvl                   : filters.append(f"({CACTUS_STRUCT_DATA.CVL.name_sql} = '{cell_cells.cvl}')")
			if   cell_cells.cut_l                 : filters.append(f"({CACTUS_STRUCT_DATA.CUT.name_sql} >= {cell_cells.cut_l})")
			if   cell_cells.cut_r                 : filters.append(f"({CACTUS_STRUCT_DATA.CUT.name_sql} <= {cell_cells.cut_r})")

			if filters: sql    += f" WHERE {' AND '.join(filters)}"
			result          = self.ExecSql(sql)

		elif type(cell_cells) is list:
			sql          : list[str]        = []

			for cell in cell_cells:
				if not ValidateOci(cell.oci): return T21_StructResult_StructCells(code = CODES_COMPLETION.INTERRUPTED, subcodes = [CODES_DATA.ERROR_CHECK])
				if not ValidateOid(cell.oid): return T21_StructResult_StructCells(code = CODES_COMPLETION.INTERRUPTED, subcodes = [CODES_DATA.ERROR_CHECK])
				if not ValidatePid(cell.pid): return T21_StructResult_StructCells(code = CODES_COMPLETION.INTERRUPTED, subcodes = [CODES_DATA.ERROR_CHECK])
				if not cell.cut             : return T21_StructResult_StructCells(code = CODES_COMPLETION.INTERRUPTED, subcodes = [CODES_DATA.ERROR_CHECK])

				sql.append(f"DELETE FROM {cell.oci}_ WHERE ({CACTUS_STRUCT_DATA.SID.name_sql} = '{cell.sid}) AND ({CACTUS_STRUCT_DATA.CUT.name_sql} = {cell.cut})';")

			sql.insert(0, "BEGIN;")

			result                          = self.ExecSql(sql)

		else:
			return T21_StructResult_StructCells(code = CODES_COMPLETION.INTERRUPTED, subcodes = [CODES_DATA.ERROR_TYPE])

		if not result.code == CODES_COMPLETION.COMPLETED: return T21_StructResult_StructCells(code = CODES_COMPLETION.INTERRUPTED, subcodes = result.subcodes)

		cells_1 : list[T20_StructCell] = self.ReadSCells(cell_cells).data
		cells   : list[T20_StructCell] = []

		for cell in cells_0:
			if cell not in cells_1: cells.append(cell)

		match len(cells):
			case 0: return T21_StructResult_StructCells(code = CODES_COMPLETION.COMPLETED, subcodes = [CODES_DATA.NO_DATA])
			case 1: return T21_StructResult_StructCells(code = CODES_COMPLETION.COMPLETED, subcodes = [CODES_DATA.SINGLE])
			case _: return T21_StructResult_StructCells(code = CODES_COMPLETION.COMPLETED, data = cells)

	def WriteDCells(self, cells: list[T20_StructCell]) -> T21_StructResult_StructCells:
		""" Запись пакета D-Ячеек """
		sql : list[str] = []

		for cell in cells:
			if not ValidateOci(cell.oci): continue
			if not ValidateOid(cell.oid): continue
			if not ValidatePid(cell.pid): continue

			sql_insert : str = f"INSERT INTO {cell.oci}_ ({CACTUS_STRUCT_DATA.SID.name_sql}, {CACTUS_STRUCT_DATA.CVL.name_sql}, {CACTUS_STRUCT_DATA.CUT.name_sql}) VALUES ('{cell.sid}', '{cell.cvl}', {cell.cut}) "
			sql_insert      += f";"

			sql.append(sql_insert)

		if not sql: return T21_StructResult_StructCells(code = CODES_COMPLETION.INTERRUPTED, subcodes = [CODES_DATA.NO_DATA])

		sql.insert(0, "BEGIN;")

		result = self.ExecSql(sql)
		if not result.code == CODES_COMPLETION.COMPLETED: return T21_StructResult_StructCells(code = CODES_COMPLETION.INTERRUPTED, subcodes = result.subcodes)

		return self.ReadSCells(cells)

	# ЗАПРОСЫ D-ДАННЫХ
	def ReadDCutRange(self, cell: T21_CutRange) -> T21_StructResult_CutRange:
		""" Запрос границ cUT D-Ячейки """
		if not ValidateOci(cell.oci): return T21_StructResult_CutRange(code = CODES_COMPLETION.INTERRUPTED, subcodes = [CODES_DATA.ERROR_CHECK])
		if not ValidateOid(cell.oid): return T21_StructResult_CutRange(code = CODES_COMPLETION.INTERRUPTED, subcodes = [CODES_DATA.ERROR_CHECK])
		if not ValidatePid(cell.pid): return T21_StructResult_CutRange(code = CODES_COMPLETION.INTERRUPTED, subcodes = [CODES_DATA.ERROR_CHECK])

		sql    = f"SELECT MIN({CACTUS_STRUCT_DATA.CUT.name_sql}) AS {CACTUS_STRUCT_DATA.CUT.name_sql}_0, MAX({CACTUS_STRUCT_DATA.CUT.name_sql}) AS {CACTUS_STRUCT_DATA.CUT.name_sql}_1 FROM {cell.oci}_ WHERE {CACTUS_STRUCT_DATA.SID.name_sql}='{cell.sid}' "
		if cell.cut_l: sql += f"AND ({CACTUS_STRUCT_DATA.CUT.name_sql} >= {cell.cut_l}) "
		if cell.cut_r: sql += f"AND ({CACTUS_STRUCT_DATA.CUT.name_sql} <= {cell.cut_r}) "

		result = self.ExecSqlSelectHList(sql)

		try:
			data   = result.data
			cut_l  = int(data[0])
			cut_r  = int(data[1])
		except: return T21_StructResult_CutRange(code = CODES_COMPLETION.INTERRUPTED, subcodes = [CODES_DATA.ERROR_CONVERT])

		return T21_StructResult_CutRange(code = result.code, data = T21_CutRange(oci=cell.oci, oid=cell.oid, pid=cell.pid, cut_l=cut_l, cut_r=cut_r))

	def ReadDCuts(self, cell: T21_CutRange) -> T21_StructResult_List:
		""" Запрос списка CUT """
		if not ValidateOci(cell.oci)   : return T21_StructResult_List(code = CODES_COMPLETION.INTERRUPTED, subcodes = [CODES_DATA.ERROR_CHECK])
		if not ValidateOid(cell.oid)   : return T21_StructResult_List(code = CODES_COMPLETION.INTERRUPTED, subcodes = [CODES_DATA.ERROR_CHECK])
		if not ValidatePid(cell.pid)   : return T21_StructResult_List(code = CODES_COMPLETION.INTERRUPTED, subcodes = [CODES_DATA.ERROR_CHECK])

		sql    = f"SELECT {CACTUS_STRUCT_DATA.CUT.name_sql} FROM {cell.oci}_ WHERE {CACTUS_STRUCT_DATA.SID.name_sql}='{cell.sid}' "
		if cell.cut_l: sql += f"AND ({CACTUS_STRUCT_DATA.CUT.name_sql} >= {cell.cut_l}) "
		if cell.cut_r: sql += f"AND ({CACTUS_STRUCT_DATA.CUT.name_sql} <= {cell.cut_r}) "

		return self.ExecSqlSelectVList(sql)
