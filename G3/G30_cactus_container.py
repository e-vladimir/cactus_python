# КАКТУС: МЕТА-КОНТЕЙНЕР
# 2022-12-01

from G00_cactus_codes  import *
from G00_result_codes  import *
from G20_meta_frame    import C20_MetaFrame
from G30_cactus_struct import T30_StructCell
from G31_cactus_struct import T31_ResultBool,        \
							  T31_ResultList,        \
							  T31_ResultStructCell,  \
							  T31_ResultStructCells, \
							  T31_ResultStructRange, \
							  T31_StructRange


class C30_Container(C20_MetaFrame):
	""" Кактус: Мета-контейнер """

	# СЛУЖЕБНЫЕ МЕТОДЫ
	def Init_00(self):
		super().Init_00()

		self._container_type : int = CONTAINER_NONE

	# УПРАВЛЕНИЕ S-ЯЧЕЙКОЙ
	def DeleteSCell(self, cell: T30_StructCell) -> T31_ResultStructCell:
		""" Удаление S-Ячейки """
		return T31_ResultStructCell(RESULT_WARNING_NOT_IMPLEMENTED)

	def ReadSCell(self, cell: T30_StructCell) -> T31_ResultStructCell:
		""" Запрос S-Ячейки """
		return T31_ResultStructCell(RESULT_WARNING_NOT_IMPLEMENTED)

	def SyncSCell(self, cell: T30_StructCell) -> T31_ResultStructCell:
		""" Синхронизация S-Ячейки """
		return T31_ResultStructCell(RESULT_WARNING_NOT_IMPLEMENTED)

	def WriteSCell(self, cell: T30_StructCell, flag_mode_ignore: bool = False) -> T31_ResultStructCell:
		""" Запись S-Ячейки """
		return T31_ResultStructCell(RESULT_WARNING_NOT_IMPLEMENTED)

	# УПРАВЛЕНИЕ ПАКЕТОМ S-ЯЧЕЕК
	def DeleteSCells(self, cell_cells: T30_StructCell | list[T30_StructCell]) -> T31_ResultStructCells:
		""" Удаление пакета S-Ячеек """
		return T31_ResultStructCells(RESULT_WARNING_NOT_IMPLEMENTED)

	def ReadSCells(self, cell_cells: T30_StructCell | list[T30_StructCell]) -> T31_ResultStructCells:
		""" Запрос пакета S-Ячеек """
		return T31_ResultStructCells(RESULT_WARNING_NOT_IMPLEMENTED)

	def SyncSCells(self, cells: list[T30_StructCell]) -> T31_ResultStructCells:
		""" Запись пакета S-Ячеек """
		return T31_ResultStructCells(RESULT_WARNING_NOT_IMPLEMENTED)

	def WriteSCells(self, cells: list[T30_StructCell]) -> T31_ResultStructCells:
		""" Запись пакета S-Ячеек """
		return T31_ResultStructCells(RESULT_WARNING_NOT_IMPLEMENTED)

	# УПРАВЛЕНИЕ D-ЯЧЕЙКОЙ
	def DeleteDCell(self, cell: T30_StructCell) -> T31_ResultStructCell:
		""" Удаление D-Ячейки """
		return T31_ResultStructCell(RESULT_WARNING_NOT_IMPLEMENTED)

	def ReadDCell(self, cell: T30_StructCell) -> T31_ResultStructCell:
		""" Запрос D-Ячейки """
		return T31_ResultStructCell(RESULT_WARNING_NOT_IMPLEMENTED)

	def WriteDCell(self, cell: T30_StructCell) -> T31_ResultStructCell:
		""" Запись D-Ячейки """
		return T31_ResultStructCell(RESULT_WARNING_NOT_IMPLEMENTED)

	# УПРАВЛЕНИЕ ПАКЕТОМ D-ЯЧЕЕК
	def ReadDCells(self, cell: T31_StructRange) -> T31_ResultStructCells:
		""" Запрос пакета D-Ячеек """
		return T31_ResultStructCells(RESULT_WARNING_NOT_IMPLEMENTED)

	def DeleteDCells(self, cell_cells: T31_StructRange | list[T30_StructCell]) -> T31_ResultStructCells:
		""" Удаление пакета D-Ячеек """
		return T31_ResultStructCells(RESULT_WARNING_NOT_IMPLEMENTED)

	def WriteDCells(self, cells: list[T30_StructCell]) -> T31_ResultStructCells:
		""" Запись пакета D-Ячеек """
		return T31_ResultStructCells(RESULT_WARNING_NOT_IMPLEMENTED)

	# ЗАПРОСЫ D-ДАННЫХ
	def DCutRange(self, cell: T31_StructRange) -> T31_ResultStructRange:
		""" Запрос границ cUT D-Ячейки """
		return T31_ResultStructRange(RESULT_WARNING_NOT_IMPLEMENTED)

	def DCuts(self, cell: T31_StructRange) -> T31_ResultList:
		""" Запрос списка CUT """
		return T31_ResultList(RESULT_WARNING_NOT_IMPLEMENTED)

	# ПРОВЕРКА ВИДА КОНТЕЙНЕРА
	def TypeIsRAM(self) -> T31_ResultBool:
		""" Проверка вида контейнера: RAM """
		return T31_ResultBool(RESULT_OK, self._container_type == CONTAINER_RAM)

	def TypeIsSQLite(self) -> T31_ResultBool:
		""" Проверка вида контейнера: SQLite """
		return T31_ResultBool(RESULT_OK, self._container_type == CONTAINER_SQLITE)

	def TypeIsPostgreSQL(self) -> T31_ResultBool:
		""" Проверка вида контейнера: PostgreSQL """
		return T31_ResultBool(RESULT_OK, self._container_type == CONTAINER_POSTGRESQL)
