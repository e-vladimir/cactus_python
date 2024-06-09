# КАКТУС: МЕТА-КОНТЕЙНЕР
# 09 июн 2024

from G00_cactus_codes  import  CONTAINERS
from G00_status_codes  import (CODES_COMPLETION,
                               CODES_PROCESSING)

from G20_meta_frame    import  C20_MetaFrame
from G20_cactus_struct import  T20_StructCell
from G21_cactus_struct import (T21_StructResult_StructCell,
                               T21_StructResult_StructCells,
                               T21_StructRange,
                               T21_StructResult_StructRange)
from G21_struct_result import (T21_StructResult_Bool,
                               T21_StructResult_List)


class C30_Container(C20_MetaFrame):
	""" Кактус: Мета-контейнер """

	# СЛУЖЕБНЫЕ МЕТОДЫ
	def Init_00(self):
		super().Init_00()

		self._container_type : CONTAINERS = CONTAINERS.CONTAINER_NONE

	# УПРАВЛЕНИЕ S-ЯЧЕЙКОЙ
	def DeleteSCell(self, cell: T20_StructCell) -> T21_StructResult_StructCell:
		""" Удаление S-Ячейки """
		return T21_StructResult_StructCell(code     = CODES_COMPLETION.COMPLETED,
		                                   subcodes = [CODES_PROCESSING.SKIP],
		                                   data     = cell)

	def ReadSCell(self, cell: T20_StructCell) -> T21_StructResult_StructCell:
		""" Запрос S-Ячейки """
		return T21_StructResult_StructCell(code     = CODES_COMPLETION.COMPLETED,
		                                   subcodes = [CODES_PROCESSING.SKIP],
		                                   data     = cell)

	def SyncSCell(self, cell: T20_StructCell) -> T21_StructResult_StructCell:
		""" Синхронизация S-Ячейки """
		return T21_StructResult_StructCell(code     = CODES_COMPLETION.COMPLETED,
		                                   subcodes = [CODES_PROCESSING.SKIP],
		                                   data     = cell)

	def WriteSCell(self, cell: T20_StructCell, flag_mode_ignore: bool = False) -> T21_StructResult_StructCell:
		""" Запись S-Ячейки """
		return T21_StructResult_StructCell(code     = CODES_COMPLETION.COMPLETED,
		                                   subcodes = [CODES_PROCESSING.SKIP],
		                                   data     = cell)

	# УПРАВЛЕНИЕ ПАКЕТОМ S-ЯЧЕЕК
	def DeleteSCells(self, cell_cells: T20_StructCell | list[T20_StructCell]) -> T21_StructResult_StructCells:
		""" Удаление пакета S-Ячеек """
		return T21_StructResult_StructCells(code=CODES_COMPLETION.COMPLETED, subcodes=[CODES_PROCESSING.SKIP], data=[])

	def ReadSCells(self, cell_cells: T20_StructCell | list[T20_StructCell]) -> T21_StructResult_StructCells:
		""" Запрос пакета S-Ячеек """
		return T21_StructResult_StructCells(code=CODES_COMPLETION.COMPLETED, subcodes=[CODES_PROCESSING.SKIP], data=[])

	def SyncSCells(self, cells: list[T20_StructCell]) -> T21_StructResult_StructCells:
		""" Запись пакета S-Ячеек """
		return T21_StructResult_StructCells(code=CODES_COMPLETION.COMPLETED, subcodes=[CODES_PROCESSING.SKIP], data=[])

	def WriteSCells(self, cells: list[T20_StructCell]) -> T21_StructResult_StructCells:
		""" Запись пакета S-Ячеек """
		return T21_StructResult_StructCells(code=CODES_COMPLETION.COMPLETED, subcodes=[CODES_PROCESSING.SKIP], data=[])

	# УПРАВЛЕНИЕ D-ЯЧЕЙКОЙ
	def DeleteDCell(self, cell: T20_StructCell) -> T21_StructResult_StructCell:
		""" Удаление D-Ячейки """
		return T21_StructResult_StructCell(code     = CODES_COMPLETION.COMPLETED,
		                                   subcodes = [CODES_PROCESSING.SKIP],
		                                   data     = cell)

	def ReadDCell(self, cell: T20_StructCell) -> T21_StructResult_StructCell:
		""" Запрос D-Ячейки """
		return T21_StructResult_StructCell(code     = CODES_COMPLETION.COMPLETED,
		                                   subcodes = [CODES_PROCESSING.SKIP],
		                                   data     = cell)

	def WriteDCell(self, cell: T20_StructCell) -> T21_StructResult_StructCell:
		""" Запись D-Ячейки """
		return T21_StructResult_StructCell(code     = CODES_COMPLETION.COMPLETED,
		                                   subcodes = [CODES_PROCESSING.SKIP],
		                                   data     = cell)

	# УПРАВЛЕНИЕ ПАКЕТОМ D-ЯЧЕЕК
	def ReadDCells(self, cell: T21_StructRange) -> T21_StructResult_StructCells:
		""" Запрос пакета D-Ячеек """
		return T21_StructResult_StructCells(code     = CODES_COMPLETION.COMPLETED,
		                                    subcodes = [CODES_PROCESSING.SKIP],
		                                    data     = [])

	def DeleteDCells(self, cell_cells: T21_StructRange | list[T20_StructCell]) -> T21_StructResult_StructCells:
		""" Удаление пакета D-Ячеек """
		return T21_StructResult_StructCells(code     = CODES_COMPLETION.COMPLETED,
		                                    subcodes = [CODES_PROCESSING.SKIP],
		                                    data     = [])

	def WriteDCells(self, cells: list[T20_StructCell]) -> T21_StructResult_StructCells:
		""" Запись пакета D-Ячеек """
		return T21_StructResult_StructCells(code     = CODES_COMPLETION.COMPLETED,
		                                    subcodes = [CODES_PROCESSING.SKIP],
		                                    data     = [])

	# ЗАПРОСЫ D-ДАННЫХ
	def DCutRange(self, cell: T21_StructRange) -> T21_StructResult_StructRange:
		""" Запрос границ cUT D-Ячейки """
		return T21_StructResult_StructRange(code     = CODES_COMPLETION.COMPLETED,
		                                    subcodes = [CODES_PROCESSING.SKIP],
		                                    data     = cell)

	def DCuts(self, cell: T21_StructRange) -> T21_StructResult_List:
		""" Запрос списка CUT """
		return T21_StructResult_List(code     = CODES_COMPLETION.COMPLETED,
		                             subcodes = [CODES_PROCESSING.SKIP],
		                             data     = [])

	# ПРОВЕРКА ВИДА КОНТЕЙНЕРА
	def Type_RAM(self) -> T21_StructResult_Bool:
		""" Проверка вида контейнера: RAM """
		return T21_StructResult_Bool(code     = CODES_COMPLETION.COMPLETED,
		                             subcodes = [],
		                             data     = self._container_type == CONTAINERS.CONTAINER_RAM)

	def Type_SQLite(self) -> T21_StructResult_Bool:
		""" Проверка вида контейнера: SQLite """
		return T21_StructResult_Bool(code     = CODES_COMPLETION.COMPLETED,
		                             subcodes = [],
		                             data     = self._container_type == CONTAINERS.CONTAINER_SQLITE)

	def Type_PostgreSQL(self) -> T21_StructResult_Bool:
		""" Проверка вида контейнера: PostgreSQL """
		return T21_StructResult_Bool(code     = CODES_COMPLETION.COMPLETED,
		                             subcodes = [],
		                             data     = self._container_type == CONTAINERS.CONTAINER_POSTGRESQL)
