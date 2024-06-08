# КАКТУС: МЕТА-КОНТЕЙНЕР
# 08 июн 2024

from G00_cactus_codes  import CONTAINERS

from G20_meta_frame    import C20_MetaFrame
from G20_cactus_struct import T20_StructCell


class C30_Container(C20_MetaFrame):
	""" Кактус: Мета-контейнер """

	# СЛУЖЕБНЫЕ МЕТОДЫ
	def Init_00(self):
		super().Init_00()

		self._container_type : CONTAINERS = CONTAINERS.CONTAINER_NONE

	# УПРАВЛЕНИЕ S-ЯЧЕЙКОЙ
	def DeleteSCell(self, cell: T20_StructCell) -> T21_ResultStructCell:
		""" Удаление S-Ячейки """
		return T21_ResultStructCell(RESULT_WARNING_NOT_IMPLEMENTED)

	def ReadSCell(self, cell: T20_StructCell) -> T21_ResultStructCell:
		""" Запрос S-Ячейки """
		return T21_ResultStructCell(RESULT_WARNING_NOT_IMPLEMENTED)

	def SyncSCell(self, cell: T20_StructCell) -> T21_ResultStructCell:
		""" Синхронизация S-Ячейки """
		return T21_ResultStructCell(RESULT_WARNING_NOT_IMPLEMENTED)

	def WriteSCell(self, cell: T20_StructCell, flag_mode_ignore: bool = False) -> T21_ResultStructCell:
		""" Запись S-Ячейки """
		return T21_ResultStructCell(RESULT_WARNING_NOT_IMPLEMENTED)

	# УПРАВЛЕНИЕ ПАКЕТОМ S-ЯЧЕЕК
	def DeleteSCells(self, cell_cells: T20_StructCell | list[T20_StructCell]) -> T21_ResultStructCells:
		""" Удаление пакета S-Ячеек """
		return T21_ResultStructCells(RESULT_WARNING_NOT_IMPLEMENTED)

	def ReadSCells(self, cell_cells: T20_StructCell | list[T20_StructCell]) -> T21_ResultStructCells:
		""" Запрос пакета S-Ячеек """
		return T21_ResultStructCells(RESULT_WARNING_NOT_IMPLEMENTED)

	def SyncSCells(self, cells: list[T20_StructCell]) -> T21_ResultStructCells:
		""" Запись пакета S-Ячеек """
		return T21_ResultStructCells(RESULT_WARNING_NOT_IMPLEMENTED)

	def WriteSCells(self, cells: list[T20_StructCell]) -> T21_ResultStructCells:
		""" Запись пакета S-Ячеек """
		return T21_ResultStructCells(RESULT_WARNING_NOT_IMPLEMENTED)

	# УПРАВЛЕНИЕ D-ЯЧЕЙКОЙ
	def DeleteDCell(self, cell: T20_StructCell) -> T21_ResultStructCell:
		""" Удаление D-Ячейки """
		return T21_ResultStructCell(RESULT_WARNING_NOT_IMPLEMENTED)

	def ReadDCell(self, cell: T20_StructCell) -> T21_ResultStructCell:
		""" Запрос D-Ячейки """
		return T21_ResultStructCell(RESULT_WARNING_NOT_IMPLEMENTED)

	def WriteDCell(self, cell: T20_StructCell) -> T21_ResultStructCell:
		""" Запись D-Ячейки """
		return T21_ResultStructCell(RESULT_WARNING_NOT_IMPLEMENTED)

	# УПРАВЛЕНИЕ ПАКЕТОМ D-ЯЧЕЕК
	def ReadDCells(self, cell: T21_StructRange) -> T21_ResultStructCells:
		""" Запрос пакета D-Ячеек """
		return T21_ResultStructCells(RESULT_WARNING_NOT_IMPLEMENTED)

	def DeleteDCells(self, cell_cells: T21_StructRange | list[T20_StructCell]) -> T21_ResultStructCells:
		""" Удаление пакета D-Ячеек """
		return T21_ResultStructCells(RESULT_WARNING_NOT_IMPLEMENTED)

	def WriteDCells(self, cells: list[T20_StructCell]) -> T21_ResultStructCells:
		""" Запись пакета D-Ячеек """
		return T21_ResultStructCells(RESULT_WARNING_NOT_IMPLEMENTED)

	# ЗАПРОСЫ D-ДАННЫХ
	def DCutRange(self, cell: T21_StructRange) -> T21_ResultStructRange:
		""" Запрос границ cUT D-Ячейки """
		return T21_ResultStructRange(RESULT_WARNING_NOT_IMPLEMENTED)

	def DCuts(self, cell: T21_StructRange) -> T21_ResultList:
		""" Запрос списка CUT """
		return T21_ResultList(RESULT_WARNING_NOT_IMPLEMENTED)

	# ПРОВЕРКА ВИДА КОНТЕЙНЕРА
	def TypeIsRAM(self) -> T21_ResultBool:
		""" Проверка вида контейнера: RAM """
		return T21_ResultBool(RESULT_OK, self._container_type == CONTAINER_RAM)

	def TypeIsSQLite(self) -> T21_ResultBool:
		""" Проверка вида контейнера: SQLite """
		return T21_ResultBool(RESULT_OK, self._container_type == CONTAINER_SQLITE)

	def TypeIsPostgreSQL(self) -> T21_ResultBool:
		""" Проверка вида контейнера: PostgreSQL """
		return T21_ResultBool(RESULT_OK, self._container_type == CONTAINER_POSTGRESQL)
