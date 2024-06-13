# КАКТУС: МЕТА-КОНТЕЙНЕР
# 12 июн 2024

from G00_cactus_codes      import  CONTAINERS
from G00_status_codes      import *
from G10_cactus_validators import *

from G20_meta_frame        import  C20_MetaFrame
from G21_cactus_struct     import *
from G21_struct_result     import *


class C30_Container(C20_MetaFrame):
	""" Кактус: Мета-контейнер """

	# Модель данных
	def Init_00(self):
		super().Init_00()

		self._container_type : CONTAINERS = CONTAINERS.CONTAINER_NONE

	# Механика данных
	# ПРОВЕРКА ВИДА КОНТЕЙНЕРА
	def Type_RAM(self) -> T21_StructResult_Bool:
		""" Проверка вида контейнера: RAM """
		return T21_StructResult_Bool(data=self._container_type == CONTAINERS.CONTAINER_RAM)

	def Type_SQLite(self) -> T21_StructResult_Bool:
		""" Проверка вида контейнера: SQLite """
		return T21_StructResult_Bool(data=self._container_type == CONTAINERS.CONTAINER_SQLITE)

	def Type_PostgreSQL(self) -> T21_StructResult_Bool:
		""" Проверка вида контейнера: PostgreSQL """
		return T21_StructResult_Bool(data=self._container_type == CONTAINERS.CONTAINER_POSTGRESQL)

	# Механика управления
	pass

	# Логика данных: S-Ячейка
	def DeleteSCell(self, cell: T20_StructCell, flag_capture_data: bool = False) -> T21_StructResult_StructCell:
		""" Удаление S-Ячейки """
		return T21_StructResult_StructCell(subcodes={CODES_PROCESSING.SKIP})

	def ReadSCell(self, cell: T20_StructCell, flag_capture_data: bool = False) -> T21_StructResult_StructCell:
		""" Запрос S-Ячейки """
		return T21_StructResult_StructCell(subcodes={CODES_PROCESSING.SKIP})

	def SyncSCell(self, cell: T20_StructCell, flag_capture_data: bool = False) -> T21_StructResult_StructCell:
		""" Синхронизация S-Ячейки """
		struct_result       = T21_StructResult_StructCell()
		struct_result.code  = CODES_COMPLETION.INTERRUPTED
		struct_result.subcodes.add(CODES_DATA.ERROR_CHECK)

		if not ValidateOci(cell.oci) : return struct_result
		if not ValidateOid(cell.oid) : return struct_result
		if not ValidatePid(cell.pid) : return struct_result

		struct_result.code = CODES_COMPLETION.COMPLETED
		struct_result.subcodes.clear()

		read_from_container = self.ReadSCell(cell)
		cell_from_container = read_from_container.data

		if cell_from_container.cut < cell.cut:
			write_to_container = self.WriteSCell(cell)
			struct_result.code     = write_to_container.code
			struct_result.subcodes = write_to_container.subcodes

		else:
			struct_result.subcodes.add(CODES_PROCESSING.SKIP)

		if flag_capture_data:
			struct_result.data = self.ReadSCell(cell).data

		return struct_result

	def WriteSCell(self, cell: T20_StructCell, flag_mode_ignore: bool = False, flag_capture_data: bool = False) -> T21_StructResult_StructCell:
		""" Запись S-Ячейки """
		return T21_StructResult_StructCell(subcodes={CODES_PROCESSING.SKIP})

	# Логика данных: S-Ячейки
	def DeleteSCells(self, cell_cells: T20_StructCell | list[T20_StructCell], flag_capture_data: bool = False) -> T21_StructResult_StructCells:
		""" Удаление пакета S-Ячеек """
		return T21_StructResult_StructCells(subcodes={CODES_PROCESSING.SKIP})

	def ReadSCells(self, cell_cells: T20_StructCell | list[T20_StructCell], flag_capture_data: bool = False) -> T21_StructResult_StructCells:
		""" Запрос пакета S-Ячеек """
		return T21_StructResult_StructCells(subcodes={CODES_PROCESSING.SKIP})

	def SyncSCells(self, cells: list[T20_StructCell], flag_capture_data: bool = False) -> T21_StructResult_StructCells:
		""" Запись пакета S-Ячеек """
		return T21_StructResult_StructCells(subcodes={CODES_PROCESSING.SKIP})

	def WriteSCells(self, cells: list[T20_StructCell], flag_capture_data: bool = False) -> T21_StructResult_StructCells:
		""" Запись пакета S-Ячеек """
		return T21_StructResult_StructCells(subcodes={CODES_PROCESSING.SKIP})

	# Логика данных: D-Ячейка
	def DeleteDCell(self, cell: T20_StructCell, flag_capture_data: bool = False) -> T21_StructResult_StructCell:
		""" Удаление D-Ячейки """
		return T21_StructResult_StructCell(subcodes={CODES_PROCESSING.SKIP})

	def ReadDCell(self, cell: T20_StructCell, flag_capture_data: bool = False) -> T21_StructResult_StructCell:
		""" Запрос D-Ячейки """
		return T21_StructResult_StructCell(subcodes={CODES_PROCESSING.SKIP})

	def WriteDCell(self, cell: T20_StructCell, flag_capture_data: bool = False) -> T21_StructResult_StructCell:
		""" Запись D-Ячейки """
		return T21_StructResult_StructCell(subcodes={CODES_PROCESSING.SKIP})

	# Логика данных: D-Ячейки
	def DeleteDCells(self, cutrange_cells: T21_CutRange | list[T20_StructCell], flag_capture_data: bool = False) -> T21_StructResult_StructCells:
		""" Удаление пакета D-Ячеек """
		return T21_StructResult_StructCells(subcodes={CODES_PROCESSING.SKIP})

	def ReadDCells(self, cutrange_cells: T21_CutRange | list[T20_StructCell], flag_capture_data: bool = False) -> T21_StructResult_StructCells:
		""" Запрос пакета D-Ячеек """
		return T21_StructResult_StructCells(subcodes={CODES_PROCESSING.SKIP})

	def WriteDCells(self, cells: list[T20_StructCell], flag_capture_data: bool = False) -> T21_StructResult_StructCells:
		""" Запись пакета D-Ячеек """
		return T21_StructResult_StructCells(subcodes={CODES_PROCESSING.SKIP})

	# Логика данных: Запрос данных
	def DCutRange(self, cell: T21_CutRange, flag_capture_data: bool = False) -> T21_StructResult_CutRange:
		""" Запрос границ cUT D-Ячейки """
		return T21_StructResult_CutRange(subcodes={CODES_PROCESSING.SKIP})

	def DCuts(self, cell: T21_CutRange, flag_capture_data: bool = False) -> T21_StructResult_List:
		""" Запрос списка CUT """
		return T21_StructResult_List(subcodes={CODES_PROCESSING.SKIP})

	# Логика управления
	pass
