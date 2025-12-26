# КАКТУС: МЕТА-КОНТЕЙНЕР
# 13 окт 2024

from G00_cactus_codes  import  CONTAINERS
from G00_status_codes  import (CODES_COMPLETION,
                               CODES_PROCESSING)

from G20_cactus_struct import  T20_StructCell
from G20_meta_frame    import  C20_MetaFrame
from G21_cactus_struct import (T21_StructResult_StructCell,
                               T21_StructResult_StructCells,
                               T21_StructResult_VltRange,
                               T21_VltRange)
from G21_struct_result import (T21_StructResult_Bool,
                               T21_StructResult_List)


class C30_Container(C20_MetaFrame):
	""" Кактус: Мета-контейнер """

	# Модель данных
	def Init_00(self):
		super().Init_00()

		self._container_type : CONTAINERS = CONTAINERS.NONE

	# Механика данных: Тип контейнера
	def Type_RAM(self) -> T21_StructResult_Bool:
		""" Проверка вида контейнера: RAM """
		return T21_StructResult_Bool(code = CODES_COMPLETION.COMPLETED,
		                             data = self._container_type == CONTAINERS.RAM)

	def Type_SQLite(self) -> T21_StructResult_Bool:
		""" Проверка вида контейнера: SQLite """
		return T21_StructResult_Bool(code = CODES_COMPLETION.COMPLETED,
		                             data = self._container_type == CONTAINERS.SQLITE)

	def Type_PostgreSQL(self) -> T21_StructResult_Bool:
		""" Проверка вида контейнера: PostgreSQL """
		return T21_StructResult_Bool(code = CODES_COMPLETION.COMPLETED,
		                             data = self._container_type == CONTAINERS.POSTGRESQL)

	# Механика управления
	pass

	# Логика данных: S-Ячейка
	def DeleteSCell(self, cell: T20_StructCell, flag_capture_delta: bool = False) -> T21_StructResult_StructCell:
		""" Удаление S-Ячейки """
		return T21_StructResult_StructCell(code     = CODES_COMPLETION.COMPLETED,
		                                   subcodes = {CODES_PROCESSING.SKIP})

	def ReadSCell(self, cell: T20_StructCell) -> T21_StructResult_StructCell:
		""" Запрос S-Ячейки """
		return T21_StructResult_StructCell(code     = CODES_COMPLETION.COMPLETED,
		                                   subcodes = {CODES_PROCESSING.SKIP})

	def SyncSCell(self, cell: T20_StructCell, flag_capture_delta: bool = False) -> T21_StructResult_StructCell:
		""" Синхронизация S-Ячейки """
		return T21_StructResult_StructCell(code     = CODES_COMPLETION.COMPLETED,
		                                   subcodes = {CODES_PROCESSING.SKIP})

	def WriteSCell(self, cell: T20_StructCell, flag_skip: bool = False, flag_capture_delta: bool = False) -> T21_StructResult_StructCell:
		""" Запись S-Ячейки """
		return T21_StructResult_StructCell(code     = CODES_COMPLETION.COMPLETED,
		                                   subcodes = {CODES_PROCESSING.SKIP})

	# Логика данных: Пакет S-Ячеек
	def DeleteSCells(self, cell_cells: T20_StructCell | list[T20_StructCell], flag_capture_delta: bool = False) -> T21_StructResult_StructCells:
		""" Удаление пакета S-Ячеек """
		return T21_StructResult_StructCells(code     = CODES_COMPLETION.COMPLETED,
		                                    subcodes = {CODES_PROCESSING.SKIP})

	def ReadSCells(self, cell_cells: T20_StructCell | list[T20_StructCell]) -> T21_StructResult_StructCells:
		""" Запрос пакета S-Ячеек """
		return T21_StructResult_StructCells(code     = CODES_COMPLETION.COMPLETED,
		                                    subcodes = {CODES_PROCESSING.SKIP})

	def SyncSCells(self, cells: list[T20_StructCell], flag_capture_delta: bool = False) -> T21_StructResult_StructCells:
		""" Запись пакета S-Ячеек """
		return T21_StructResult_StructCells(code     = CODES_COMPLETION.COMPLETED,
		                                    subcodes = {CODES_PROCESSING.SKIP})

	def WriteSCells(self, cells: list[T20_StructCell], flag_skip: bool = False,  flag_capture_delta: bool = False) -> T21_StructResult_StructCells:
		""" Запись пакета S-Ячеек """
		return T21_StructResult_StructCells(code     = CODES_COMPLETION.COMPLETED,
		                                    subcodes = {CODES_PROCESSING.SKIP})

	# Логика данных: D-Ячейка
	def DeleteDCell(self, cell: T20_StructCell, flag_capture_delta: bool = False) -> T21_StructResult_StructCell:
		""" Удаление D-Ячейки """
		return T21_StructResult_StructCell(code     = CODES_COMPLETION.COMPLETED,
		                                   subcodes = {CODES_PROCESSING.SKIP})

	def ReadDCell(self, cell: T20_StructCell) -> T21_StructResult_StructCell:
		""" Запрос D-Ячейки """
		return T21_StructResult_StructCell(code     = CODES_COMPLETION.COMPLETED,
		                                   subcodes = {CODES_PROCESSING.SKIP})

	def WriteDCell(self, cell: T20_StructCell, flag_capture_delta: bool = False) -> T21_StructResult_StructCell:
		""" Запись D-Ячейки """
		return T21_StructResult_StructCell(code     = CODES_COMPLETION.COMPLETED,
		                                   subcodes = {CODES_PROCESSING.SKIP})

	# Логика данных: Пакет D-Ячеек
	def DeleteDCells(self, cell: T21_VltRange, flag_capture_delta: bool = False) -> T21_StructResult_StructCells:
		""" Удаление пакета D-Ячеек """
		return T21_StructResult_StructCells(code     = CODES_COMPLETION.COMPLETED,
		                                    subcodes = {CODES_PROCESSING.SKIP})

	def ReadDCells(self, cell: T21_VltRange) -> T21_StructResult_StructCells:
		""" Запрос пакета D-Ячеек """
		return T21_StructResult_StructCells(code     = CODES_COMPLETION.COMPLETED,
		                                    subcodes = {CODES_PROCESSING.SKIP})

	# Логика данных: Диапазон VLT
	def ReadVltRange(self, cell: T21_VltRange) -> T21_StructResult_VltRange:
		""" Запрос границ cUT D-Ячейки """
		return T21_StructResult_VltRange(code     = CODES_COMPLETION.COMPLETED,
		                                 subcodes = {CODES_PROCESSING.SKIP})

	def ReadVlts(self, cell: T21_VltRange) -> T21_StructResult_List:
		""" Запрос списка VLT """
		return T21_StructResult_List(code     = CODES_COMPLETION.COMPLETED,
		                             subcodes = {CODES_PROCESSING.SKIP})

	# Логика управления
	pass
