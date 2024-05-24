# КАКТУС: КОНТЕЙНЕР-SQL
# 2024-04-03

import psycopg2
import s3m
import sqlite3

from   dataclasses              import dataclass

from   G00_result_codes         import *
from   G00_cactus_codes         import *
from   G10_cactus_validators    import ValidateOci,           \
									   ValidateOid,           \
									   ValidatePid
from   G30_cactus_struct        import T30_ResultCode,        \
									   T30_StructCell
from   G31_cactus_struct        import T31_ResultBool,        \
									   T31_ResultInt,         \
									   T31_ResultList,        \
									   T31_ResultString,      \
									   T31_ResultStructCell,  \
									   T31_ResultStructCells, \
									   T31_StructRange,       \
									   T31_ResultStructRange
from   G31_cactus_container_sql import C31_ContainerSQL


# ТИПЫ ДАННЫХ SQL КОНТЕЙНЕРА
@dataclass
class T31_ResultCursorS3m(T30_ResultCode):
	""" Результат-Курсор """
	cursor : s3m.Cursor = None


# КАКТУС: КОНТЕЙНЕР-SQLite
# 2023-07-12
class C32_ContainerSQLite(C31_ContainerSQL):
	""" Кактус: Контейнер SQLite """

	def Init_00(self):
		super().Init_00()

		self._options_filename : str = ""

	def Init_01(self):
		super().Init_01()

		self._container_type = CONTAINER_SQLITE

	def Init_10(self):
		super().Init_10()

		self.connection : s3m.Connection | None = None

	# УПРАВЛЕНИЕ ПАРАМЕТРАМИ ПОДКЛЮЧЕНИЯ
	def OptionsFilename(self, filename: str = None) -> T31_ResultString:
		""" Запрос/Установка параметра подключения: Имя файла """
		if filename is None: return T31_ResultString(RESULT_OK, self._options_filename)
		self._options_filename = filename

	# ЗАПРОС СОСТОЯНИЯ ПОДКЛЮЧЕНИЯ
	def ConnectionState(self) -> T31_ResultBool:
		""" Запрос состояния подключения """
		if self.connection is None: return T31_ResultBool(RESULT_OK, False)

		try                       : cursor = self.connection.cursor()
		except                    : return T31_ResultBool(RESULT_OK, False)

		return T31_ResultBool(RESULT_OK, True)

	# УПРАВЛЕНИЕ ПОДКЛЮЧЕНИЕМ
	def Connect(self) -> T31_ResultBool:
		""" Подключение к СУБД """
		if not self.ConnectionState().flag:
			self.connection = None

			try                            : self.connection = s3m.Connection(self.OptionsFilename().text, isolation_level=None, check_same_thread=False)
			except sqlite3.OperationalError: return T31_ResultBool(RESULT_ERROR_ACCESS_IO, False)
			except                         : return T31_ResultBool(RESULT_ERROR_ACCESS_CONNECTION, False)

			try   :
				cursor = self.connection.cursor()
				cursor.execute('PRAGMA journal_mode=MEMORY;')
			except: pass

		return T31_ResultBool(RESULT_OK, True)

	def Disconnect(self) -> T31_ResultBool:
		""" Отключение от СУБД """
		if     self.connection is None    : return T31_ResultBool(RESULT_OK, True)

		try                               : self.connection.close()
		except                            : pass

		self.connection = None

		return T31_ResultBool(RESULT_OK, True)

	# УПРАВЛЕНИЕ РЕГИСТРАЦИЕЙ КЛАССА
	def RegisterClass(self, oci: str) -> T31_ResultBool:
		""" Регистрация класса структурного объекта """
		if not ValidateOci(oci)                : return T31_ResultBool(RESULT_ERROR_CHECK_VALIDATE, False)

		sql      : str = f"CREATE TABLE IF NOT EXISTS {oci} ({SQL_SID} TEXT PRIMARY KEY, {SQL_CVL} TEXT NOT NULL, {SQL_CUT} INT NOT NULL)"
		result_s_table = self.ExecSql(sql)
		if not result_s_table.code == RESULT_OK: return T31_ResultBool(result_s_table.code, False)

		sql      : str = f"CREATE TABLE IF NOT EXISTS {oci}_ ({SQL_SID} TEXT, {SQL_CVL} TEXT NOT NULL, {SQL_CUT} INT NOT NULL)"
		result_s_table = self.ExecSql(sql)
		if not result_s_table.code == RESULT_OK: return T31_ResultBool(result_s_table.code, False)

		sql      : str = f"CREATE INDEX IF NOT EXISTS index_{oci}_sid_ ON {oci}_ ({SQL_SID})"
		result_s_index = self.ExecSql(sql)
		if not result_s_index.code == RESULT_OK: return T31_ResultBool(result_s_index.code, False)

		sql      : str = f"CREATE INDEX IF NOT EXISTS index_{oci}_cut_ ON {oci}_ ({SQL_CUT})"
		result_s_index = self.ExecSql(sql)
		if not result_s_index.code == RESULT_OK: return T31_ResultBool(result_s_index.code, False)

		return T31_ResultBool(RESULT_OK, True)

	# ВЫПОЛНЕНИЕ ЗАПРОСОВ
	def ExecSql(self, sql: str | list[str]) -> T31_ResultCursorS3m:
		""" Выполнение запроса с кодом """
		self.PrepareConnect()

		if self.connection is None: return T31_ResultCursorS3m(RESULT_ERROR_ACCESS_CONNECTION)

		try:
			sql_cursor          = self.connection.cursor()

			if   type(sql) is str  : sql_cursor.execute(sql + ';')
			elif type(sql) is list : sql_cursor.executescript('\n'.join(sql))

			self.connection.commit()

			return T31_ResultCursorS3m(RESULT_OK, sql_cursor)

		except sqlite3.IntegrityError:
			self.PrepareDisconnect()
			return T31_ResultCursorS3m(RESULT_ERROR_DATA_STRUCT)

		except sqlite3.ProgrammingError:
			self.PrepareDisconnect()
			return T31_ResultCursorS3m(RESULT_ERROR_SQL)

		except sqlite3.OperationalError:  # Сюда попадают и ошибки SQL-синтаксиса
			self.PrepareDisconnect()
			return T31_ResultCursorS3m(RESULT_ERROR_SQL)

		except:
			self.PrepareDisconnect()
			return T31_ResultCursorS3m(RESULT_ERROR_EXEC)

	def ExecSqlSelectRowCount(self, sql: str | list[str]) -> T31_ResultInt:
		"""Выполнение запроса с числом строк"""
		result_cursor = self.ExecSql(sql)
		if not result_cursor.code == RESULT_OK:
			self.PrepareDisconnect()
			return T31_ResultInt(result_cursor.code)

		try:
			cursor        = result_cursor.cursor
			result : int  = cursor.rowcount
			cursor.close()
		except Exception as error:
			print(error)
			return T31_ResultInt(RESULT_ERROR_ACCESS_IO)

		self.PrepareDisconnect()

		return T31_ResultInt(RESULT_OK, result)

	def ExecSqlSelectSingle(self, sql: str) -> T31_ResultString:
		"""Выполнение запроса с получением значения"""
		result_cursor = self.ExecSql(sql)
		if not result_cursor.code == RESULT_OK:
			self.PrepareDisconnect()
			return T31_ResultString(result_cursor.code)

		try:
			cursor             = result_cursor.cursor
			data   : list[str] = cursor.fetchone()
			cursor.close()
		except Exception as error:
			print(error)
			return T31_ResultString(RESULT_ERROR_ACCESS_IO)

		self.PrepareDisconnect()

		if not data: return T31_ResultString(RESULT_WARNING_NO_DATA)

		result : str       = data[0]
		return T31_ResultString(RESULT_OK, result)

	def ExecSqlSelectHList(self, sql: str) -> T31_ResultList:
		"""Выполнение запроса с получением горизонтального списка значений"""
		result_cursor = self.ExecSql(sql)
		if not result_cursor.code == RESULT_OK:
			self.PrepareDisconnect()
			return T31_ResultList(result_cursor.code)

		try:
			cursor             = result_cursor.cursor
			data   : list[str] = cursor.fetchone()
			cursor.close()
		except Exception as error:
			print(error)
			return T31_ResultList(RESULT_ERROR_ACCESS_IO)

		self.PrepareDisconnect()

		if not data: return T31_ResultList(RESULT_WARNING_NO_DATA)

		return T31_ResultList(RESULT_OK, data)

	def ExecSqlSelectVList(self, sql: str) -> T31_ResultList:
		"""Выполнение запроса с получением вертикального списка значений"""
		result_cursor      = self.ExecSql(sql)
		if not result_cursor.code == RESULT_OK:
			self.PrepareDisconnect()
			return T31_ResultList(result_cursor.code)

		try:
			cursor             = result_cursor.cursor
			result : list[str] = list(map(lambda data: data[0], cursor.fetchall()))
			cursor.close()
		except Exception as error:
			print(error)
			return T31_ResultList(RESULT_ERROR_ACCESS_IO)

		self.PrepareDisconnect()

		if not result: return T31_ResultList(RESULT_WARNING_NO_DATA, result)

		return T31_ResultList(RESULT_OK, result)

	def ExecSqlSelectMatrix(self, sql: str) -> T31_ResultList:
		"""Выполнение запроса с получением матрицы"""
		result_cursor      = self.ExecSql(sql)
		if not result_cursor.code == RESULT_OK:
			self.PrepareDisconnect()
			return T31_ResultList(result_cursor.code)

		try:
			cursor             = result_cursor.cursor
			result : list[str] = cursor.fetchall()
			cursor.close()
		except Exception as error:
			print(error)
			return T31_ResultList(RESULT_ERROR_ACCESS_IO)

		self.PrepareDisconnect()

		if not result: return T31_ResultList(RESULT_WARNING_NO_DATA, result)

		return T31_ResultList(RESULT_OK, result)

	# УПРАВЛЕНИЕ S-ЯЧЕЙКОЙ
	def WriteSCell(self, cell: T30_StructCell, flag_mode_ignore: bool = False) -> T31_ResultStructCell:
		""" Запись S-Ячейки """
		if not ValidateOci(cell.oci): return T31_ResultStructCell(RESULT_ERROR_CHECK_VALIDATE)
		if not ValidateOid(cell.oid): return T31_ResultStructCell(RESULT_ERROR_CHECK_VALIDATE)
		if not ValidatePid(cell.pid): return T31_ResultStructCell(RESULT_ERROR_CHECK_VALIDATE)

		sql : str   = f"INSERT INTO {cell.oci} ({SQL_SID}, {SQL_CVL}, {SQL_CUT}) VALUES ('{cell.sid}', '{cell.cvl}', {cell.cut}) "
		if flag_mode_ignore: sql += f"ON CONFLICT ({SQL_SID}) DO NOTHING"
		else               : sql += f"ON CONFLICT ({SQL_SID}) DO UPDATE SET {SQL_SID}='{cell.sid}', {SQL_CVL}='{cell.cvl}', {SQL_CUT}={cell.cut}"

		result      = self.ExecSql(sql)
		actual_cell = self.ReadSCell(cell)

		return T31_ResultStructCell(result.code, actual_cell.cell)

	def ReadSCell(self, cell: T30_StructCell) -> T31_ResultStructCell:
		""" Запрос S-Ячейки """
		if not ValidateOci(cell.oci)        : return T31_ResultStructCell(RESULT_ERROR_CHECK_VALIDATE)
		if not ValidateOid(cell.oid)        : return T31_ResultStructCell(RESULT_ERROR_CHECK_VALIDATE)
		if not ValidatePid(cell.pid)        : return T31_ResultStructCell(RESULT_ERROR_CHECK_VALIDATE)

		sql  : str       = f"SELECT {SQL_CVL}, {SQL_CUT} FROM {cell.oci} WHERE {SQL_SID} = '{cell.sid}'"

		result_data      = self.ExecSqlSelectHList(sql)
		if not result_data.code == RESULT_OK: return T31_ResultStructCell(result_data.code)

		data : list[str] = result_data.items
		if len(data) < 2                    : return T31_ResultStructCell(RESULT_WARNING_NO_DATA)

		try                                 :
			result           = T30_StructCell()
			result.oci       = cell.oci
			result.oid       = cell.oid
			result.pid       = cell.pid
			result.cvl       = data[0]
			result.cut       = int(data[1])

		except                              : return T31_ResultStructCell(RESULT_ERROR_CONVERT)

		return T31_ResultStructCell(RESULT_OK, result)

	def DeleteSCell(self, cell: T30_StructCell) -> T31_ResultStructCell:
		""" Удаление S-Ячейки """
		if not ValidateOci(cell.oci)        : return T31_ResultStructCell(RESULT_ERROR_CHECK_VALIDATE)
		if not ValidateOid(cell.oid)        : return T31_ResultStructCell(RESULT_ERROR_CHECK_VALIDATE)
		if not ValidatePid(cell.pid)        : return T31_ResultStructCell(RESULT_ERROR_CHECK_VALIDATE)

		sql  : str = f"DELETE FROM {cell.oci} WHERE {SQL_SID} = '{cell.sid}'"
		result     = self.ExecSqlSelectRowCount(sql)
		if not result.code  == RESULT_OK    : return T31_ResultStructCell(result.code)
		if not result.value == 1            : return T31_ResultStructCell(RESULT_WARNING_NO_DATA)

		return T31_ResultStructCell(RESULT_OK, cell)

	def SyncSCell(self, cell: T30_StructCell) -> T31_ResultStructCell:
		""" Синхронизация S-Ячейки """
		result_read       = self.ReadSCell(cell)
		cell_in_container = result_read.cell

		if   cell_in_container.cut <  cell.cut: result = self.WriteSCell(cell)
		else                                  : result = T31_ResultStructCell(RESULT_OK_SKIP)

		cell = self.ReadSCell(cell)

		if not result.code == RESULT_OK: return T31_ResultStructCell(result.code, cell.cell)

		return T31_ResultStructCell(result.code, cell.cell)

	# УПРАВЛЕНИЕ ПАКЕТОМ S-ЯЧЕЕК
	def DeleteSCells(self, cell_cells: T30_StructCell | list[T30_StructCell]) -> T31_ResultStructCells:
		""" Удаление пакета S-Ячеек """
		result                         = T30_ResultCode(RESULT_OK_SKIP)
		cells_0 : list[T30_StructCell] = self.ReadSCells(cell_cells).cells

		if type(cell_cells) is T30_StructCell:
			if not ValidateOci(cell_cells.oci): return T31_ResultStructCells(RESULT_ERROR_CHECK_VALIDATE)

			sql     : str       = f"DELETE FROM {cell_cells.oci}"
			filters : list[str] = []

			if   cell_cells.oid and cell_cells.pid: filters.append(f"{SQL_SID} = '{cell_cells.sid}'")
			elif cell_cells.oid                   : filters.append(f"{SQL_SID} LIKE '{cell_cells.oid}.%'")
			elif cell_cells.pid                   : filters.append(f"{SQL_SID} LIKE '%.{cell_cells.oid}'")

			if   cell_cells.cvl                   : filters.append(f"{SQL_CVL} = '{cell_cells.cvl}'")
			if   cell_cells.cut                   : filters.append(f"{SQL_CUT} = '{cell_cells.cut}'")

			if filters: sql    += f" WHERE {' AND '.join(filters)}"
			result              = self.ExecSql(sql)

		elif type(cell_cells) is list:
			sql          : list[str]            = []

			for cell in cell_cells:
				if not ValidateOci(cell.oci): return T31_ResultStructCells(RESULT_ERROR_CHECK_VALIDATE)
				if not ValidateOid(cell.oid): return T31_ResultStructCells(RESULT_ERROR_CHECK_VALIDATE)
				if not ValidatePid(cell.pid): return T31_ResultStructCells(RESULT_ERROR_CHECK_VALIDATE)

				sql.append(f"DELETE FROM {cell.oci} WHERE {SQL_SID} = '{cell.sid}';")

			sql.insert(0, "BEGIN;")

			result                              = self.ExecSql(sql)

		if not result.code == RESULT_OK   : return T31_ResultStructCells(result.code)

		cells_1 : list[T30_StructCell] = self.ReadSCells(cell_cells).cells
		cells   : list[T30_StructCell] = []

		for cell in cells_0:
			if cell not in cells_1: cells.append(cell)

		return T31_ResultStructCells(result.code, cells)

	def ReadSCells(self, cell_cells: T30_StructCell | list[T30_StructCell]) -> T31_ResultStructCells:
		""" Запрос пакета S-Ячеек """
		cells : list[T30_StructCell] = []

		if type(cell_cells) is T30_StructCell:
			if not ValidateOci(cell_cells.oci): return T31_ResultStructCells(RESULT_ERROR_CHECK_VALIDATE)

			sql     : str       = f"SELECT {SQL_SID}, {SQL_CVL}, {SQL_CUT} FROM {cell_cells.oci}"
			filters : list[str] = []

			if   cell_cells.oid and cell_cells.pid: filters.append(f"{SQL_SID} = '{cell_cells.oid}.{cell_cells.pid}'")
			elif cell_cells.oid                   : filters.append(f"{SQL_SID} LIKE '{cell_cells.oid}.%'")
			elif cell_cells.pid                   : filters.append(f"{SQL_SID} LIKE '%.{cell_cells.oid}'")

			if   cell_cells.cvl                   : filters.append(f"{SQL_CVL} = '{cell_cells.cvl}'")
			if   cell_cells.cut                   : filters.append(f"{SQL_CUT} = '{cell_cells.cut}'")

			if filters:	sql    += f" WHERE {' AND '.join(filters)}"
			result              = self.ExecSqlSelectMatrix(sql)

			if not result.code == RESULT_OK: return T31_ResultStructCells(result.code)

			for raw_data in result.items:
				try:
					oid_pid = raw_data[0].split('.')

					oid     = oid_pid[0]
					pid     = oid_pid[1]
					cvl     = raw_data[1]
					cut     = int(raw_data[2])

					cells.append(T30_StructCell(oci=cell_cells.oci, oid=oid, pid=pid, cvl=cvl, cut=cut))
				except: continue

			if not cells: return T31_ResultStructCells(result.code)
			return T31_ResultStructCells(result.code, cells)

		elif type(cell_cells) is list:
			cells       : dict[str, T30_StructCell] = dict()
			result_cells: list[T30_StructCell]      = []
			oci         : str                       = ""

			for cell in cell_cells:
				if not ValidateOci(cell.oci): continue
				if not ValidateOid(cell.oid): continue
				if not ValidatePid(cell.pid): continue

				cells[cell.sid] = cell
				if not oci: oci = cell.oci

			sql   : str                       = f"SELECT {SQL_SID}, {SQL_CVL}, {SQL_CUT} FROM {oci} "
			if cells:
				sids : list[str] = list(map("'{}'".format, cells.keys()))
				sql             += f"WHERE {SQL_SID} IN ({', '.join(sids)})"

			result              = self.ExecSqlSelectMatrix(sql)

			if not result.code == RESULT_OK: return T31_ResultStructCells(result.code)

			for raw_data in result.items:
				try:
					sid     = raw_data[0]
					oid_pid = sid.split('.')
					oid     = oid_pid[0]
					pid     = oid_pid[1]
					cvl     = raw_data[1]
					cut     = int(raw_data[2])

					result_cells.append(T30_StructCell(oci=oci, oid=oid, pid=pid, cvl=cvl, cut=cut))
				except: continue

			if not cells: return T31_ResultStructCells(result.code)
			return T31_ResultStructCells(result.code, result_cells)

		return T31_ResultStructCells(RESULT_OK_SKIP)

	def SyncSCells(self, cells: list[T30_StructCell]) -> T31_ResultStructCells:
		""" Синхронизация пакета S-Ячеек """
		sql : list[str] = []

		for cell in cells:
			if not ValidateOci(cell.oci): continue
			if not ValidateOid(cell.oid): continue
			if not ValidatePid(cell.pid): continue

			sql_insert : str = f"INSERT INTO {cell.oci} ({SQL_SID}, {SQL_CVL}, {SQL_CUT}) VALUES ('{cell.sid}', '{cell.cvl}', {cell.cut}) "
			sql_insert      += f"ON CONFLICT ({SQL_SID}) DO UPDATE SET {SQL_CVL}='{cell.cvl}', {SQL_CUT}={cell.cut} WHERE {SQL_CUT} < {cell.cut}"
			sql_insert      += f";"

			sql.append(sql_insert)

		if not sql: return T31_ResultStructCells(RESULT_WARNING_NO_DATA)

		sql.insert(0, "BEGIN;")

		result = self.ExecSql(sql)
		if not result.code == RESULT_OK: return T31_ResultStructCells(result.code)

		return self.ReadSCells(cells)

	def WriteSCells(self, cells: list[T30_StructCell]) -> T31_ResultStructCells:
		""" Запись пакета S-Ячеек """
		sql : list[str] = []

		for cell in cells:
			if not ValidateOci(cell.oci): continue
			if not ValidateOid(cell.oid): continue
			if not ValidatePid(cell.pid): continue

			sql_insert : str = f"INSERT INTO {cell.oci} ({SQL_SID}, {SQL_CVL}, {SQL_CUT}) VALUES ('{cell.sid}', '{cell.cvl}', {cell.cut}) "
			sql_insert      += f"ON CONFLICT ({SQL_SID}) DO UPDATE SET {SQL_CVL}='{cell.cvl}', {SQL_CUT}={cell.cut} "
			sql_insert      += f";"

			sql.append(sql_insert)

		if not sql: return T31_ResultStructCells(RESULT_WARNING_NO_DATA)

		sql.insert(0, "BEGIN;")

		result = self.ExecSql(sql)
		if not result.code == RESULT_OK: return T31_ResultStructCells(result.code)

		return self.ReadSCells(cells)

	# УПРАВЛЕНИЕ D-ЯЧЕЙКОЙ
	def DeleteDCell(self, cell: T30_StructCell) -> T31_ResultStructCell:
		""" Удаление D-Ячейки """
		if not ValidateOci(cell.oci): return T31_ResultStructCell(RESULT_ERROR_CHECK_VALIDATE)
		if not ValidateOid(cell.oid): return T31_ResultStructCell(RESULT_ERROR_CHECK_VALIDATE)
		if not ValidatePid(cell.pid): return T31_ResultStructCell(RESULT_ERROR_CHECK_VALIDATE)
		if not cell.cut             : return T31_ResultStructCell(RESULT_ERROR_CHECK_VALIDATE)

		result_cell = self.ReadDCell(cell)
		sql         = f"DELETE FROM {cell.oci}_ WHERE {SQL_SID}='{cell.sid}' AND {SQL_CUT}={cell.cut}"
		result      = self.ExecSql(sql)
		if not result.code == RESULT_OK: return T31_ResultStructCell(result.code, result_cell.cell)

		return result_cell

	def ReadDCell(self, cell: T30_StructCell) -> T31_ResultStructCell:
		""" Запрос D-Ячейки """
		if not ValidateOci(cell.oci): return T31_ResultStructCell(RESULT_ERROR_CHECK_VALIDATE)
		if not ValidateOid(cell.oid): return T31_ResultStructCell(RESULT_ERROR_CHECK_VALIDATE)
		if not ValidatePid(cell.pid): return T31_ResultStructCell(RESULT_ERROR_CHECK_VALIDATE)
		if not cell.cut             : return T31_ResultStructCell(RESULT_ERROR_CHECK_VALIDATE)

		sql    = f"SELECT {SQL_CVL} FROM {cell.oci}_ WHERE {SQL_SID}='{cell.sid}' AND {SQL_CUT}={cell.cut}"
		result = self.ExecSqlSelectSingle(sql)
		if not result.code == RESULT_OK: return T31_ResultStructCell(result.code)

		return T31_ResultStructCell(RESULT_OK, T30_StructCell(oci=cell.oci, oid=cell.oid, pid=cell.pid, cvl=result.text, cut=cell.cut))

	def WriteDCell(self, cell: T30_StructCell) -> T31_ResultStructCell:
		""" Запись D-Ячейки """
		if not ValidateOci(cell.oci): return T31_ResultStructCell(RESULT_ERROR_CHECK_VALIDATE)
		if not ValidateOid(cell.oid): return T31_ResultStructCell(RESULT_ERROR_CHECK_VALIDATE)
		if not ValidatePid(cell.pid): return T31_ResultStructCell(RESULT_ERROR_CHECK_VALIDATE)
		if not cell.cut             : return T31_ResultStructCell(RESULT_ERROR_CHECK_VALIDATE)

		sql         = f"UPDATE {cell.oci}_ SET {SQL_CVL}='{cell.cvl}' WHERE {SQL_SID}='{cell.sid}' AND {SQL_CUT}={cell.cut}"
		result      = self.ExecSqlSelectRowCount(sql)

		if not result.code == RESULT_OK: return T31_ResultStructCell(result.code)
		if     result.value == 0:
			sql         = f"INSERT INTO {cell.oci}_ ({SQL_SID}, {SQL_CVL}, {SQL_CUT}) VALUES ('{cell.sid}', '{cell.cvl}', {cell.cut})"
			result      = self.ExecSql(sql)
			if not result.code == RESULT_OK: return T31_ResultStructCell(result.code)

		result_cell = self.ReadDCell(cell)

		return result_cell

	# УПРАВЛЕНИЕ ПАКЕТОМ D-ЯЧЕЕК
	def ReadDCells(self, cell: T31_StructRange) -> T31_ResultStructCells:
		""" Запрос пакета D-Ячеек """
		if not ValidateOci(cell.oci): return T31_ResultStructCells(RESULT_ERROR_CHECK_VALIDATE)

		cells   : list[T30_StructCell] = []

		filters : list[str]            = []
		if cell.oid and cell.pid: filters.append(f"({SQL_SID}='{cell.sid}')")
		if cell.cut_l           : filters.append(f"({SQL_CUT}>={cell.cut_l})")
		if cell.cut_r           : filters.append(f"({SQL_CUT}<={cell.cut_r})")

		sql     : str                  = f"SELECT {SQL_SID}, {SQL_CVL}, {SQL_CUT} FROM {cell.oci}_ "
		if filters: sql               += f"WHERE " + " AND ".join(filters)

		result                         = self.ExecSqlSelectMatrix(sql)
		if not result.code == RESULT_OK: return T31_ResultStructCells(result.code)

		for raw_data in result.items:
			try:
				sid     = raw_data[0]
				oid_pid = sid.split('.')

				oid     = oid_pid[0]
				pid     = oid_pid[1]
				cvl     = raw_data[1]
				cut     = int(raw_data[2])

				cells.append(T30_StructCell(oci=cell.oci, oid=oid, pid=pid, cvl=cvl, cut=cut))
			except: continue

		if not cells: return T31_ResultStructCells(result.code)
		return T31_ResultStructCells(result.code, cells)

	def DeleteDCells(self, cell_cells: T31_StructRange | list[T30_StructCell]) -> T31_ResultStructCells:
		""" Удаление пакета D-Ячеек """
		result                         = T30_ResultCode(RESULT_OK_SKIP)
		cells_0 : list[T30_StructCell] = self.ReadDCells(cell_cells).cells

		if type(cell_cells) is T31_StructRange:
			if not ValidateOci(cell_cells.oci): return T31_ResultStructCells(RESULT_ERROR_CHECK_VALIDATE)

			sql     : str       = f"DELETE FROM {cell_cells.oci}_"
			filters : list[str] = []

			if   cell_cells.oid and cell_cells.pid: filters.append(f"({SQL_SID} = '{cell_cells.sid}')")
			elif cell_cells.oid                   : filters.append(f"({SQL_SID} LIKE '{cell_cells.oid}.%')")
			elif cell_cells.pid                   : filters.append(f"({SQL_SID} LIKE '%.{cell_cells.oid}')")

			if   cell_cells.cvl                   : filters.append(f"({SQL_CVL} = '{cell_cells.cvl}')")
			if   cell_cells.cut_l                 : filters.append(f"({SQL_CUT} >= {cell_cells.cut_l})")
			if   cell_cells.cut_r                 : filters.append(f"({SQL_CUT} <= {cell_cells.cut_r})")

			if filters: sql    += f" WHERE {' AND '.join(filters)}"
			result              = self.ExecSql(sql)

		elif type(cell_cells) is list:
			sql          : list[str]            = []

			for cell in cell_cells:
				if not ValidateOci(cell.oci): return T31_ResultStructCells(RESULT_ERROR_CHECK_VALIDATE)
				if not ValidateOid(cell.oid): return T31_ResultStructCells(RESULT_ERROR_CHECK_VALIDATE)
				if not ValidatePid(cell.pid): return T31_ResultStructCells(RESULT_ERROR_CHECK_VALIDATE)
				if not cell.cut             : return T31_ResultStructCells(RESULT_ERROR_CHECK_VALIDATE)

				sql.append(f"DELETE FROM {cell.oci}_ WHERE ({SQL_SID} = '{cell.sid}) AND ({SQL_CUT} = {cell.cut})';")

			sql.insert(0, "BEGIN;")

			result                              = self.ExecSql(sql)

		if not result.code == RESULT_OK   : return T31_ResultStructCells(result.code)

		cells_1 : list[T30_StructCell] = self.ReadSCells(cell_cells).cells
		cells   : list[T30_StructCell] = []

		for cell in cells_0:
			if cell not in cells_1: cells.append(cell)

		return T31_ResultStructCells(result.code, cells)

	def WriteDCells(self, cells: list[T30_StructCell]) -> T31_ResultStructCells:
		""" Запись пакета D-Ячеек """
		sql : list[str] = []

		for cell in cells:
			if not ValidateOci(cell.oci): continue
			if not ValidateOid(cell.oid): continue
			if not ValidatePid(cell.pid): continue

			sql_insert : str = f"INSERT INTO {cell.oci}_ ({SQL_SID}, {SQL_CVL}, {SQL_CUT}) VALUES ('{cell.sid}', '{cell.cvl}', {cell.cut}) "
			sql_insert      += f";"

			sql.append(sql_insert)

		if not sql: return T31_ResultStructCells(RESULT_WARNING_NO_DATA)

		sql.insert(0, "BEGIN;")

		result = self.ExecSql(sql)
		if not result.code == RESULT_OK: return T31_ResultStructCells(result.code)

		return self.ReadSCells(cells)

	# ЗАПРОСЫ D-ДАННЫХ
	def DCutRange(self, cell: T31_StructRange) -> T31_ResultStructRange:
		""" Запрос границ cUT D-Ячейки """
		if not ValidateOci(cell.oci): return T31_ResultStructRange(RESULT_ERROR_CHECK_VALIDATE)
		if not ValidateOid(cell.oid): return T31_ResultStructRange(RESULT_ERROR_CHECK_VALIDATE)
		if not ValidatePid(cell.pid): return T31_ResultStructRange(RESULT_ERROR_CHECK_VALIDATE)

		sql    = f"SELECT MIN({SQL_CUT}) AS {SQL_CUT}_0, MAX({SQL_CUT}) AS {SQL_CUT}_1 FROM {cell.oci}_ WHERE {SQL_SID}='{cell.sid}' "
		if cell.cut_l: sql += f"AND ({SQL_CUT} >= {cell.cut_l}) "
		if cell.cut_r: sql += f"AND ({SQL_CUT} <= {cell.cut_r}) "

		result = self.ExecSqlSelectHList(sql)

		try:
			data   = result.items
			cut_l  = int(data[0])
			cut_r  = int(data[1])
		except: return T31_ResultStructRange(RESULT_ERROR_CONVERT)

		return T31_ResultStructRange(result.code, T31_StructRange(oci=cell.oci, oid=cell.oid, pid=cell.pid, cut_l=cut_l, cut_r=cut_r))

	def DCuts(self, cell: T31_StructRange) -> T31_ResultList:
		""" Запрос списка CUT """
		if not ValidateOci(cell.oci)   : return T31_ResultList(RESULT_ERROR_CHECK_VALIDATE)
		if not ValidateOid(cell.oid)   : return T31_ResultList(RESULT_ERROR_CHECK_VALIDATE)
		if not ValidatePid(cell.pid)   : return T31_ResultList(RESULT_ERROR_CHECK_VALIDATE)

		sql    = f"SELECT {SQL_CUT} FROM {cell.oci}_ WHERE {SQL_SID}='{cell.sid}' "
		if cell.cut_l: sql += f"AND ({SQL_CUT} >= {cell.cut_l}) "
		if cell.cut_r: sql += f"AND ({SQL_CUT} <= {cell.cut_r}) "

		result = self.ExecSqlSelectVList(sql)
		if not result.code == RESULT_OK: return T31_ResultList(result.code)
		if not result.items            : return T31_ResultList(RESULT_WARNING_NO_DATA)

		return T31_ResultList(RESULT_OK, result.items)


# КАКТУС: КОНТЕЙНЕР-PostgreSQL
# 2023-01-30
class C32_ContainerPostgreSQL(C31_ContainerSQL):
	""" Кактус: Контейнер PostgreSQL """

	def Init_00(self):
		super().Init_00()

		self._options_server_ip       : str = ""
		self._options_server_tcp_port : int = 5432
		self._options_server_dbase    : str = ""
		self._options_server_login    : str = ""
		self._options_server_password : str = ""

	def Init_01(self):
		super().Init_01()

		self._container_type = CONTAINER_POSTGRESQL

	def Init_10(self):
		super().Init_10()

		self.connection : psycopg2.connection | None = None

	# УПРАВЛЕНИЕ ПАРАМЕТРАМИ ПОДКЛЮЧЕНИЯ
	def OptionsServerIp(self, ip: str = None) -> T31_ResultString:
		""" Запрос/Установка параметра подключения: IP сервера """
		if ip is None: return T31_ResultString(RESULT_OK, self._options_server_ip)
		self._options_server_ip = ip

	def OptionsServerTcpPort(self, tcp_port: int = None) -> T31_ResultInt:
		""" Запрос/Установка параметра подключения: TCP-порт """
		if tcp_port is None: return T31_ResultInt(RESULT_OK, self._options_server_tcp_port)
		self._options_server_tcp_port = tcp_port

	def OptionsServerDBase(self, basename: str = None) -> T31_ResultString:
		""" Запрос/Установка параметра подключения: Имя схемы """
		if basename is None: return T31_ResultString(RESULT_OK, self._options_server_dbase)
		self._options_server_dbase = basename

	def OptionsServerLogin(self, login: str = None) -> T31_ResultString:
		""" Запрос/Установка параметра подключения: Логин """
		if login is None: return T31_ResultString(RESULT_OK, self._options_server_login)
		self._options_server_login = login

	def OptionsServerPassword(self, password: str = None) -> T31_ResultString:
		""" Запрос/Установка параметра подключения: Пароль """
		if password is None: return T31_ResultString(RESULT_OK, self._options_server_password)
		self._options_server_password = password

	# ЗАПРОС СОСТОЯНИЯ ПОДКЛЮЧЕНИЯ
	def ConnectionState(self) -> T31_ResultBool:
		""" Запрос состояния подключения """
		if self.connection is None: return T31_ResultBool(RESULT_OK, False)

		try                       : cursor = self.connection.cursor()
		except                    : return T31_ResultBool(RESULT_OK, False)

		return T31_ResultBool(RESULT_OK, True)

	# УПРАВЛЕНИЕ ПОДКЛЮЧЕНИЕМ
	def Connect(self) -> T31_ResultBool:
		""" Подключение к СУБД """
		if not self.ConnectionState().flag:
			try                             : self.connection = psycopg2.connect(host            = self.OptionsServerIp().text,
									                                             port            = self.OptionsServerTcpPort().value,
									                                             dbname          = self.OptionsServerDBase().text,
									                                             user            = self.OptionsServerLogin().text,
									                                             password        = self.OptionsServerPassword().text,
									                                             connect_timeout = 5)
			except psycopg2.OperationalError: return T31_ResultBool(RESULT_ERROR_ACCESS_IO,         False)
			except                          : return T31_ResultBool(RESULT_ERROR_ACCESS_CONNECTION, False)

		return T31_ResultBool(RESULT_OK, True)

	def Disconnect(self) -> T31_ResultBool:
		""" Отключение от СУБД """
		if     self.connection is None    : return T31_ResultBool(RESULT_OK, True)

		try                               : self.connection.close()
		except                            : pass

		self.connection = None

		return T31_ResultBool(RESULT_OK, True)

	# УПРАВЛЕНИЕ РЕГИСТРАЦИЕЙ КЛАССА
	def RegisterClass(self, oci: str) -> T31_ResultBool:
		""" Регистрация класса структурного объекта """
		if not ValidateOci(oci)                : return T31_ResultBool(RESULT_ERROR_CHECK_VALIDATE, False)

		sql      : str = f"CREATE TABLE IF NOT EXISTS {oci} ({SQL_SID} TEXT PRIMARY KEY, {SQL_CVL} TEXT, {SQL_CUT} INT)"
		result_s_table = self.ExecSql(sql)
		if not result_s_table.code == RESULT_OK: return T31_ResultBool(result_s_table.code, False)

		sql      : str = f"CREATE INDEX IF NOT EXISTS index_{oci}_sid ON {oci} ({SQL_SID})"
		result_s_index = self.ExecSql(sql)
		if not result_s_index.code == RESULT_OK: return T31_ResultBool(result_s_index.code, False)

		sql      : str = f"CREATE TABLE IF NOT EXISTS {oci}_ ({SQL_SID} TEXT, {SQL_CVL} TEXT, {SQL_CUT} INT)"
		result_s_table = self.ExecSql(sql)
		if not result_s_table.code == RESULT_OK: return T31_ResultBool(result_s_table.code, False)

		sql      : str = f"CREATE INDEX IF NOT EXISTS index_{oci}_sid_ ON {oci}_ ({SQL_SID})"
		result_s_index = self.ExecSql(sql)
		if not result_s_index.code == RESULT_OK: return T31_ResultBool(result_s_index.code, False)

		sql      : str = f"CREATE INDEX IF NOT EXISTS index_{oci}_cut_ ON {oci}_ ({SQL_CUT})"
		result_s_index = self.ExecSql(sql)
		if not result_s_index.code == RESULT_OK: return T31_ResultBool(result_s_index.code, False)

		return T31_ResultBool(RESULT_OK, True)

	# ВЫПОЛНЕНИЕ ЗАПРОСОВ
	def ExecSql(self, sql: str | list[str]) -> T31_ResultCursorS3m:
		""" Выполнение запроса с кодом """
		self.PrepareConnect()

		if self.connection is None: return T31_ResultCursorS3m(RESULT_ERROR_ACCESS_CONNECTION)

		try:
			sql_cursor          = self.connection.cursor()

			if   type(sql) is str  : sql_cursor.execute(sql + ';')
			elif type(sql) is list : sql_cursor.execute('\n'.join(sql))
			# elif type(sql) is list : sql_cursor.executescript('\n'.join(sql))

			self.connection.commit()

			return T31_ResultCursorS3m(RESULT_OK, sql_cursor)

		except sqlite3.IntegrityError:
			self.PrepareDisconnect()
			return T31_ResultCursorS3m(RESULT_ERROR_DATA_STRUCT)

		except sqlite3.ProgrammingError:
			self.PrepareDisconnect()
			return T31_ResultCursorS3m(RESULT_ERROR_SQL)

		except sqlite3.OperationalError:  # Сюда попадают и ошибки SQL-синтаксиса
			self.PrepareDisconnect()
			return T31_ResultCursorS3m(RESULT_ERROR_SQL)

		except:
			self.PrepareDisconnect()
			return T31_ResultCursorS3m(RESULT_ERROR_EXEC)

	def ExecSqlSelectRowCount(self, sql: str | list[str]) -> T31_ResultInt:
		"""Выполнение запроса с числом строк"""
		result_cursor = self.ExecSql(sql)
		if not result_cursor.code == RESULT_OK:
			self.PrepareDisconnect()
			return T31_ResultInt(result_cursor.code)

		cursor        = result_cursor.cursor
		result : int  = cursor.rowcount
		cursor.close()

		self.PrepareDisconnect()

		return T31_ResultInt(RESULT_OK, result)

	def ExecSqlSelectSingle(self, sql: str) -> T31_ResultString:
		"""Выполнение запроса с получением значения"""
		result_cursor = self.ExecSql(sql)
		if not result_cursor.code == RESULT_OK:
			self.PrepareDisconnect()
			return T31_ResultString(result_cursor.code)

		cursor             = result_cursor.cursor
		data   : list[str] = cursor.fetchone()
		cursor.close()

		self.PrepareDisconnect()

		if not data: return T31_ResultString(RESULT_WARNING_NO_DATA)

		result : str       = data[0]
		return T31_ResultString(RESULT_OK, result)

	def ExecSqlSelectHList(self, sql: str) -> T31_ResultList:
		"""Выполнение запроса с получением горизонтального списка значений"""
		result_cursor = self.ExecSql(sql)
		if not result_cursor.code == RESULT_OK:
			self.PrepareDisconnect()
			return T31_ResultList(result_cursor.code)

		cursor             = result_cursor.cursor
		data   : list[str] = cursor.fetchone()
		cursor.close()

		self.PrepareDisconnect()

		if not data: return T31_ResultList(RESULT_WARNING_NO_DATA)

		return T31_ResultList(RESULT_OK, data)

	def ExecSqlSelectVList(self, sql: str) -> T31_ResultList:
		"""Выполнение запроса с получением вертикального списка значений"""
		result_cursor      = self.ExecSql(sql)
		if not result_cursor.code == RESULT_OK:
			self.PrepareDisconnect()
			return T31_ResultList(result_cursor.code)

		cursor             = result_cursor.cursor
		result : list[str] = list(map(lambda data: data[0], cursor.fetchall()))
		cursor.close()

		self.PrepareDisconnect()

		if not result: return T31_ResultList(RESULT_WARNING_NO_DATA, result)

		return T31_ResultList(RESULT_OK, result)

	def ExecSqlSelectMatrix(self, sql: str) -> T31_ResultList:
		"""Выполнение запроса с получением матрицы"""
		result_cursor      = self.ExecSql(sql)
		if not result_cursor.code == RESULT_OK:
			self.PrepareDisconnect()
			return T31_ResultList(result_cursor.code)

		cursor             = result_cursor.cursor
		result : list[str] = cursor.fetchall()
		cursor.close()

		self.PrepareDisconnect()

		if not result: return T31_ResultList(RESULT_WARNING_NO_DATA, result)

		return T31_ResultList(RESULT_OK, result)

	# УПРАВЛЕНИЕ S-ЯЧЕЙКОЙ
	def WriteSCell(self, cell: T30_StructCell, flag_mode_ignore: bool = False) -> T31_ResultStructCell:
		""" Запись S-Ячейки """
		if not ValidateOci(cell.oci): return T31_ResultStructCell(RESULT_ERROR_CHECK_VALIDATE)
		if not ValidateOid(cell.oid): return T31_ResultStructCell(RESULT_ERROR_CHECK_VALIDATE)
		if not ValidatePid(cell.pid): return T31_ResultStructCell(RESULT_ERROR_CHECK_VALIDATE)

		sql : str   = f"INSERT INTO {cell.oci} ({SQL_SID}, {SQL_CVL}, {SQL_CUT}) VALUES ('{cell.sid}', '{cell.cvl}', {cell.cut}) "
		if flag_mode_ignore: sql += f"ON CONFLICT ({SQL_SID}) DO NOTHING"
		else               : sql += f"ON CONFLICT ({SQL_SID}) DO UPDATE SET {SQL_SID}='{cell.sid}', {SQL_CVL}='{cell.cvl}', {SQL_CUT}={cell.cut}"

		result      = self.ExecSql(sql)
		actual_cell = self.ReadSCell(cell)

		return T31_ResultStructCell(result.code, actual_cell.cell)

	def ReadSCell(self, cell: T30_StructCell) -> T31_ResultStructCell:
		""" Запрос S-Ячейки """
		if not ValidateOci(cell.oci)        : return T31_ResultStructCell(RESULT_ERROR_CHECK_VALIDATE)
		if not ValidateOid(cell.oid)        : return T31_ResultStructCell(RESULT_ERROR_CHECK_VALIDATE)
		if not ValidatePid(cell.pid)        : return T31_ResultStructCell(RESULT_ERROR_CHECK_VALIDATE)

		sql  : str       = f"SELECT {SQL_CVL}, {SQL_CUT} FROM {cell.oci} WHERE {SQL_SID} = '{cell.sid}'"

		result_data      = self.ExecSqlSelectHList(sql)
		if not result_data.code == RESULT_OK: return T31_ResultStructCell(result_data.code)

		data : list[str] = result_data.items
		if len(data) < 2                    : return T31_ResultStructCell(RESULT_WARNING_NO_DATA)

		try                                 :
			result           = T30_StructCell()
			result.oci       = cell.oci
			result.oid       = cell.oid
			result.pid       = cell.pid
			result.cvl       = data[0]
			result.cut       = int(data[1])

		except                              : return T31_ResultStructCell(RESULT_ERROR_CONVERT)

		return T31_ResultStructCell(RESULT_OK, result)

	def DeleteSCell(self, cell: T30_StructCell) -> T31_ResultStructCell:
		""" Удаление S-Ячейки """
		if not ValidateOci(cell.oci)        : return T31_ResultStructCell(RESULT_ERROR_CHECK_VALIDATE)
		if not ValidateOid(cell.oid)        : return T31_ResultStructCell(RESULT_ERROR_CHECK_VALIDATE)
		if not ValidatePid(cell.pid)        : return T31_ResultStructCell(RESULT_ERROR_CHECK_VALIDATE)

		sql  : str = f"DELETE FROM {cell.oci} WHERE {SQL_SID} = '{cell.sid}'"
		result     = self.ExecSqlSelectRowCount(sql)
		if not result.code  == RESULT_OK    : return T31_ResultStructCell(result.code)
		if not result.value == 1            : return T31_ResultStructCell(RESULT_WARNING_NO_DATA)

		return T31_ResultStructCell(RESULT_OK, cell)

	def SyncSCell(self, cell: T30_StructCell) -> T31_ResultStructCell:
		""" Синхронизация S-Ячейки """
		result_read       = self.ReadSCell(cell)

		cell_in_container = result_read.cell
		if cell_in_container.cut >  cell.cut: return T31_ResultStructCell(RESULT_OK_SKIP, cell)

		result            = self.WriteSCell(cell)
		return self.ReadSCell(cell)

	# УПРАВЛЕНИЕ ПАКЕТОМ S-ЯЧЕЕК
	def DeleteSCells(self, cell_cells: T30_StructCell | list[T30_StructCell]) -> T31_ResultStructCells:
		""" Удаление пакета S-Ячеек """
		result                         = T30_ResultCode(RESULT_OK_SKIP)
		cells_0 : list[T30_StructCell] = self.ReadSCells(cell_cells).cells

		if type(cell_cells) is T30_StructCell:
			if not ValidateOci(cell_cells.oci): return T31_ResultStructCells(RESULT_ERROR_CHECK_VALIDATE)

			sql     : str       = f"DELETE FROM {cell_cells.oci}"
			filters : list[str] = []

			if   cell_cells.oid and cell_cells.pid: filters.append(f"{SQL_SID} = '{cell_cells.sid}'")
			elif cell_cells.oid                   : filters.append(f"{SQL_SID} LIKE '{cell_cells.oid}.%'")
			elif cell_cells.pid                   : filters.append(f"{SQL_SID} LIKE '%.{cell_cells.oid}'")

			if   cell_cells.cvl                   : filters.append(f"{SQL_CVL} = '{cell_cells.cvl}'")
			if   cell_cells.cut                   : filters.append(f"{SQL_CUT} = '{cell_cells.cut}'")

			if filters: sql    += f" WHERE {' AND '.join(filters)}"
			result              = self.ExecSql(sql)

		elif type(cell_cells) is list:
			sql          : list[str]            = []

			for cell in cell_cells:
				if not ValidateOci(cell.oci): return T31_ResultStructCells(RESULT_ERROR_CHECK_VALIDATE)
				if not ValidateOid(cell.oid): return T31_ResultStructCells(RESULT_ERROR_CHECK_VALIDATE)
				if not ValidatePid(cell.pid): return T31_ResultStructCells(RESULT_ERROR_CHECK_VALIDATE)

				sql.append(f"DELETE FROM {cell.oci} WHERE {SQL_SID} = '{cell.sid}';")

			sql.insert(0, "BEGIN;")

			result                              = self.ExecSql(sql)

		if not result.code == RESULT_OK   : return T31_ResultStructCells(result.code)

		cells_1 : list[T30_StructCell] = self.ReadSCells(cell_cells).cells
		cells   : list[T30_StructCell] = []

		for cell in cells_0:
			if cell not in cells_1: cells.append(cell)

		return T31_ResultStructCells(result.code, cells)

	def ReadSCells(self, cell_cells: T30_StructCell | list[T30_StructCell]) -> T31_ResultStructCells:
		""" Запрос пакета S-Ячеек """
		cells : list[T30_StructCell] = []

		if type(cell_cells) is T30_StructCell:
			if not ValidateOci(cell_cells.oci): return T31_ResultStructCells(RESULT_ERROR_CHECK_VALIDATE)

			sql     : str       = f"SELECT {SQL_SID}, {SQL_CVL}, {SQL_CUT} FROM {cell_cells.oci}"
			filters : list[str] = []

			if   cell_cells.oid and cell_cells.pid: filters.append(f"{SQL_SID} = '{cell_cells.oid}.{cell_cells.pid}'")
			elif cell_cells.oid                   : filters.append(f"{SQL_SID} LIKE '{cell_cells.oid}.%'")
			elif cell_cells.pid                   : filters.append(f"{SQL_SID} LIKE '%.{cell_cells.oid}'")

			if   cell_cells.cvl                   : filters.append(f"{SQL_CVL} = '{cell_cells.cvl}'")
			if   cell_cells.cut                   : filters.append(f"{SQL_CUT} = '{cell_cells.cut}'")

			if filters:	sql    += f" WHERE {' AND '.join(filters)}"
			result              = self.ExecSqlSelectMatrix(sql)

			if not result.code == RESULT_OK: return T31_ResultStructCells(result.code)

			for raw_data in result.items:
				try:
					oid_pid = raw_data[0].split('.')

					oid     = oid_pid[0]
					pid     = oid_pid[1]
					cvl     = raw_data[1]
					cut     = int(raw_data[2])

					cells.append(T30_StructCell(oci=cell_cells.oci, oid=oid, pid=pid, cvl=cvl, cut=cut))
				except: continue

			if not cells: return T31_ResultStructCells(result.code)
			return T31_ResultStructCells(result.code, cells)

		elif type(cell_cells) is list:
			cells       : dict[str, T30_StructCell] = dict()
			result_cells: list[T30_StructCell]      = []
			oci         : str                       = ""

			for cell in cell_cells:
				if not ValidateOci(cell.oci): continue
				if not ValidateOid(cell.oid): continue
				if not ValidatePid(cell.pid): continue

				cells[cell.sid] = cell
				if not oci: oci = cell.oci

			sql   : str                       = f"SELECT {SQL_SID}, {SQL_CVL}, {SQL_CUT} FROM {oci} "
			if cells:
				sids : list[str] = list(map("'{}'".format, cells.keys()))
				sql             += f"WHERE {SQL_SID} IN ({', '.join(sids)})"

			result              = self.ExecSqlSelectMatrix(sql)

			if not result.code == RESULT_OK: return T31_ResultStructCells(result.code)

			for raw_data in result.items:
				try:
					sid     = raw_data[0]
					oid_pid = sid.split('.')
					oid     = oid_pid[0]
					pid     = oid_pid[1]
					cvl     = raw_data[1]
					cut     = int(raw_data[2])

					result_cells.append(T30_StructCell(oci=oci, oid=oid, pid=pid, cvl=cvl, cut=cut))
				except: continue

			if not cells: return T31_ResultStructCells(result.code)
			return T31_ResultStructCells(result.code, result_cells)

		return T31_ResultStructCells(RESULT_OK_SKIP)

	def SyncSCells(self, cells: list[T30_StructCell]) -> T31_ResultStructCells:
		""" Синхронизация пакета S-Ячеек """
		sql : list[str] = []

		for cell in cells:
			if not ValidateOci(cell.oci): continue
			if not ValidateOid(cell.oid): continue
			if not ValidatePid(cell.pid): continue

			sql_insert : str = f"INSERT INTO {cell.oci} ({SQL_SID}, {SQL_CVL}, {SQL_CUT}) VALUES ('{cell.sid}', '{cell.cvl}', {cell.cut}) "
			sql_insert      += f"ON CONFLICT ({SQL_SID}) DO UPDATE SET {SQL_CVL}='{cell.cvl}', {SQL_CUT}={cell.cut} WHERE {cell.oci}.{SQL_CUT} < {cell.cut}"
			sql_insert      += f";"

			sql.append(sql_insert)

		if not sql: return T31_ResultStructCells(RESULT_WARNING_NO_DATA)

		sql.insert(0, "BEGIN;")

		result = self.ExecSql(sql)
		if not result.code == RESULT_OK: return T31_ResultStructCells(result.code)

		return self.ReadSCells(cells)

	def WriteSCells(self, cells: list[T30_StructCell]) -> T31_ResultStructCells:
		""" Запись пакета S-Ячеек """
		sql : list[str] = []

		for cell in cells:
			if not ValidateOci(cell.oci): continue
			if not ValidateOid(cell.oid): continue
			if not ValidatePid(cell.pid): continue

			sql_insert : str = f"INSERT INTO {cell.oci} ({SQL_SID}, {SQL_CVL}, {SQL_CUT}) VALUES ('{cell.sid}', '{cell.cvl}', {cell.cut}) "
			sql_insert      += f"ON CONFLICT ({SQL_SID}) DO UPDATE SET {SQL_CVL}='{cell.cvl}', {SQL_CUT}={cell.cut} "
			sql_insert      += f";"

			sql.append(sql_insert)

		if not sql: return T31_ResultStructCells(RESULT_WARNING_NO_DATA)

		sql.insert(0, "BEGIN;")
		sql.append("COMMIT;")

		result = self.ExecSql(sql)
		if not result.code == RESULT_OK: return T31_ResultStructCells(result.code)

		return self.ReadSCells(cells)

	# УПРАВЛЕНИЕ D-ЯЧЕЙКОЙ
	def DeleteDCell(self, cell: T30_StructCell) -> T31_ResultStructCell:
		""" Удаление D-Ячейки """
		if not ValidateOci(cell.oci): return T31_ResultStructCell(RESULT_ERROR_CHECK_VALIDATE)
		if not ValidateOid(cell.oid): return T31_ResultStructCell(RESULT_ERROR_CHECK_VALIDATE)
		if not ValidatePid(cell.pid): return T31_ResultStructCell(RESULT_ERROR_CHECK_VALIDATE)
		if not cell.cut             : return T31_ResultStructCell(RESULT_ERROR_CHECK_VALIDATE)

		result_cell = self.ReadDCell(cell)
		sql         = f"DELETE FROM {cell.oci}_ WHERE {SQL_SID}='{cell.sid}' AND {SQL_CUT}={cell.cut}"
		result      = self.ExecSql(sql)
		if not result.code == RESULT_OK: return T31_ResultStructCell(result.code, result_cell.cell)

		return result_cell

	def ReadDCell(self, cell: T30_StructCell) -> T31_ResultStructCell:
		""" Запрос D-Ячейки """
		if not ValidateOci(cell.oci): return T31_ResultStructCell(RESULT_ERROR_CHECK_VALIDATE)
		if not ValidateOid(cell.oid): return T31_ResultStructCell(RESULT_ERROR_CHECK_VALIDATE)
		if not ValidatePid(cell.pid): return T31_ResultStructCell(RESULT_ERROR_CHECK_VALIDATE)
		if not cell.cut             : return T31_ResultStructCell(RESULT_ERROR_CHECK_VALIDATE)

		sql    = f"SELECT {SQL_CVL} FROM {cell.oci}_ WHERE {SQL_SID}='{cell.sid}' AND {SQL_CUT}={cell.cut}"
		result = self.ExecSqlSelectSingle(sql)
		if not result.code == RESULT_OK: return T31_ResultStructCell(result.code)

		return T31_ResultStructCell(RESULT_OK, T30_StructCell(oci=cell.oci, oid=cell.oid, pid=cell.pid, cvl=result.text, cut=cell.cut))

	def WriteDCell(self, cell: T30_StructCell) -> T31_ResultStructCell:
		""" Запись D-Ячейки """
		if not ValidateOci(cell.oci): return T31_ResultStructCell(RESULT_ERROR_CHECK_VALIDATE)
		if not ValidateOid(cell.oid): return T31_ResultStructCell(RESULT_ERROR_CHECK_VALIDATE)
		if not ValidatePid(cell.pid): return T31_ResultStructCell(RESULT_ERROR_CHECK_VALIDATE)
		if not cell.cut             : return T31_ResultStructCell(RESULT_ERROR_CHECK_VALIDATE)

		sql         = f"UPDATE {cell.oci}_ SET {SQL_CVL}='{cell.cvl}' WHERE {SQL_SID}='{cell.sid}' AND {SQL_CUT}={cell.cut}"
		result      = self.ExecSqlSelectRowCount(sql)

		if not result.code == RESULT_OK: return T31_ResultStructCell(result.code)
		if     result.value == 0:
			sql         = f"INSERT INTO {cell.oci}_ ({SQL_SID}, {SQL_CVL}, {SQL_CUT}) VALUES ('{cell.sid}', '{cell.cvl}', {cell.cut})"
			result      = self.ExecSql(sql)
			if not result.code == RESULT_OK: return T31_ResultStructCell(result.code)

		result_cell = self.ReadDCell(cell)

		return result_cell

	# УПРАВЛЕНИЕ ПАКЕТОМ D-ЯЧЕЕК
	def ReadDCells(self, cell: T31_StructRange) -> T31_ResultStructCells:
		""" Запрос пакета D-Ячеек """
		if not ValidateOci(cell.oci): return T31_ResultStructCells(RESULT_ERROR_CHECK_VALIDATE)

		cells   : list[T30_StructCell] = []

		filters : list[str]            = []
		if cell.oid and cell.pid: filters.append(f"({SQL_SID}='{cell.sid}')")
		if cell.cut_l           : filters.append(f"({SQL_CUT}>={cell.cut_l})")
		if cell.cut_r           : filters.append(f"({SQL_CUT}<={cell.cut_r})")

		sql     : str                  = f"SELECT {SQL_SID}, {SQL_CVL}, {SQL_CUT} FROM {cell.oci}_ "
		if filters: sql               += f"WHERE " + " AND ".join(filters)

		result                         = self.ExecSqlSelectMatrix(sql)
		if not result.code == RESULT_OK: return T31_ResultStructCells(result.code)

		for raw_data in result.items:
			try:
				sid     = raw_data[0]
				oid_pid = sid.split('.')

				oid     = oid_pid[0]
				pid     = oid_pid[1]
				cvl     = raw_data[1]
				cut     = int(raw_data[2])

				cells.append(T30_StructCell(oci=cell.oci, oid=oid, pid=pid, cvl=cvl, cut=cut))
			except: continue

		if not cells: return T31_ResultStructCells(result.code)
		return T31_ResultStructCells(result.code, cells)

	def DeleteDCells(self, cell_cells: T31_StructRange | list[T30_StructCell]) -> T31_ResultStructCells:
		""" Удаление пакета D-Ячеек """
		result                         = T30_ResultCode(RESULT_OK_SKIP)
		cells_0 : list[T30_StructCell] = self.ReadDCells(cell_cells).cells

		if type(cell_cells) is T31_StructRange:
			if not ValidateOci(cell_cells.oci): return T31_ResultStructCells(RESULT_ERROR_CHECK_VALIDATE)

			sql     : str       = f"DELETE FROM {cell_cells.oci}_"
			filters : list[str] = []

			if   cell_cells.oid and cell_cells.pid: filters.append(f"({SQL_SID} = '{cell_cells.sid}')")
			elif cell_cells.oid                   : filters.append(f"({SQL_SID} LIKE '{cell_cells.oid}.%')")
			elif cell_cells.pid                   : filters.append(f"({SQL_SID} LIKE '%.{cell_cells.oid}')")

			if   cell_cells.cvl                   : filters.append(f"({SQL_CVL} = '{cell_cells.cvl}')")
			if   cell_cells.cut_l                 : filters.append(f"({SQL_CUT} >= {cell_cells.cut_l})")
			if   cell_cells.cut_r                 : filters.append(f"({SQL_CUT} <= {cell_cells.cut_r})")

			if filters: sql    += f" WHERE {' AND '.join(filters)}"
			result              = self.ExecSql(sql)

		elif type(cell_cells) is list:
			sql          : list[str]            = []

			for cell in cell_cells:
				if not ValidateOci(cell.oci): return T31_ResultStructCells(RESULT_ERROR_CHECK_VALIDATE)
				if not ValidateOid(cell.oid): return T31_ResultStructCells(RESULT_ERROR_CHECK_VALIDATE)
				if not ValidatePid(cell.pid): return T31_ResultStructCells(RESULT_ERROR_CHECK_VALIDATE)
				if not cell.cut             : return T31_ResultStructCells(RESULT_ERROR_CHECK_VALIDATE)

				sql.append(f"DELETE FROM {cell.oci}_ WHERE ({SQL_SID} = '{cell.sid}) AND ({SQL_CUT} = {cell.cut})';")

			sql.insert(0, "BEGIN;")

			result                              = self.ExecSql(sql)

		if not result.code == RESULT_OK   : return T31_ResultStructCells(result.code)

		cells_1 : list[T30_StructCell] = self.ReadSCells(cell_cells).cells
		cells   : list[T30_StructCell] = []

		for cell in cells_0:
			if cell not in cells_1: cells.append(cell)

		return T31_ResultStructCells(result.code, cells)

	def WriteDCells(self, cells: list[T30_StructCell]) -> T31_ResultStructCells:
		""" Запись пакета D-Ячеек """
		sql : list[str] = []

		for cell in cells:
			if not ValidateOci(cell.oci): continue
			if not ValidateOid(cell.oid): continue
			if not ValidatePid(cell.pid): continue

			sql_insert : str = f"INSERT INTO {cell.oci}_ ({SQL_SID}, {SQL_CVL}, {SQL_CUT}) VALUES ('{cell.sid}', '{cell.cvl}', {cell.cut}) "
			sql_insert      += f";"

			sql.append(sql_insert)

		if not sql: return T31_ResultStructCells(RESULT_WARNING_NO_DATA)

		sql.insert(0, "BEGIN;")

		result = self.ExecSql(sql)
		if not result.code == RESULT_OK: return T31_ResultStructCells(result.code)

		return self.ReadSCells(cells)

	# ЗАПРОСЫ D-ДАННЫХ
	def DCutRange(self, cell: T31_StructRange) -> T31_ResultStructRange:
		""" Запрос границ cUT D-Ячейки """
		if not ValidateOci(cell.oci): return T31_ResultStructRange(RESULT_ERROR_CHECK_VALIDATE)
		if not ValidateOid(cell.oid): return T31_ResultStructRange(RESULT_ERROR_CHECK_VALIDATE)
		if not ValidatePid(cell.pid): return T31_ResultStructRange(RESULT_ERROR_CHECK_VALIDATE)

		sql    = f"SELECT MIN({SQL_CUT}) AS {SQL_CUT}_0, MAX({SQL_CUT}) AS {SQL_CUT}_1 FROM {cell.oci}_ WHERE {SQL_SID}='{cell.sid}' "
		if cell.cut_l: sql += f"AND ({SQL_CUT} >= {cell.cut_l}) "
		if cell.cut_r: sql += f"AND ({SQL_CUT} <= {cell.cut_r}) "

		result = self.ExecSqlSelectHList(sql)

		try:
			data   = result.items
			cut_l  = int(data[0])
			cut_r  = int(data[1])
		except: return T31_ResultStructRange(RESULT_ERROR_CONVERT)

		return T31_ResultStructRange(result.code, T31_StructRange(oci=cell.oci, oid=cell.oid, pid=cell.pid, cut_l=cut_l, cut_r=cut_r))

	def DCuts(self, cell: T31_StructRange) -> T31_ResultList:
		""" Запрос списка CUT """
		if not ValidateOci(cell.oci)   : return T31_ResultList(RESULT_ERROR_CHECK_VALIDATE)
		if not ValidateOid(cell.oid)   : return T31_ResultList(RESULT_ERROR_CHECK_VALIDATE)
		if not ValidatePid(cell.pid)   : return T31_ResultList(RESULT_ERROR_CHECK_VALIDATE)

		sql    = f"SELECT {SQL_CUT} FROM {cell.oci}_ WHERE {SQL_SID}='{cell.sid}' "
		if cell.cut_l: sql += f"AND ({SQL_CUT} >= {cell.cut_l}) "
		if cell.cut_r: sql += f"AND ({SQL_CUT} <= {cell.cut_r}) "

		result = self.ExecSqlSelectVList(sql)
		if not result.code == RESULT_OK: return T31_ResultList(result.code)
		if not result.items            : return T31_ResultList(RESULT_WARNING_NO_DATA)

		return T31_ResultList(RESULT_OK, result.items)
