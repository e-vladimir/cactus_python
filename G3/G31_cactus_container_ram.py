# КАКТУС: КОНТЕЙНЕР-RAM
# 16 июн 2024

from copy                  import copy

from G00_cactus_codes      import CONTAINERS
from G00_status_codes      import *

from G10_cactus_validators import *
from G10_list              import DifferenceLists

from G21_cactus_struct     import *
from G21_struct_result     import T21_StructResult_List

from G30_cactus_container  import C30_Container


class C31_ContainerRAM(C30_Container):
	""" Кактус: Контейнер RAM """

	# Модель данных
	def Init_00(self):
		super().Init_00()

		self._s_cells : dict[str, T20_StructCell]            = dict()
		self._d_cells : dict[str, dict[int, T20_StructCell]] = dict()

	def Init_01(self):
		super().Init_01()

		self._container_type = CONTAINERS.CONTAINER_RAM

	# Механика данных
	def Clear(self):
		""" Очистка контейнера """
		self._s_cells.clear()
		self._d_cells.clear()

	# Механика управления
	pass

	# Логика данных: S-Ячейка
	def DeleteSCell(self, cell: T20_StructCell, flag_capture_delta: bool = False) -> T21_StructResult_StructCell:
		""" Удаление S-Ячейки """
		result                              = T21_StructResult_StructCell()

		result_check  : bool                = ValidateOid(cell.oid)
		result_check                       &= ValidatePid(cell.pid)

		if not result_check:
			result.code = CODES_COMPLETION.INTERRUPTED
			result.subcodes.add(CODES_DATA.ERROR_CHECK)

			return result

		result_exist : bool                 = cell.sid in self._s_cells

		if not result_exist:
			result.code = CODES_COMPLETION.COMPLETED
			result.subcodes.add(CODES_PROCESSING.SKIP)
			result.subcodes.add(CODES_DATA.NO_DATA)

			return result

		cells_start  : list[T20_StructCell] = []
		cells_end    : list[T20_StructCell] = []

		if flag_capture_delta: cells_start = self.ReadSCells(cell).data

		del self._s_cells[cell.sid]

		if flag_capture_delta:
			cells_end   = self.ReadSCells(cell).data
			cells_delta = DifferenceLists(cells_start, cells_end)

			result.data = None if not cells_delta else cells_delta[0]

		return result

	def ReadSCell(self, cell: T20_StructCell) -> T21_StructResult_StructCell:
		""" Запрос S-Ячейки """
		result      = T21_StructResult_StructCell()

		result_check : bool = ValidateOid(cell.oid)
		result_check       &= ValidatePid(cell.pid)

		if not result_check:
			result.code = CODES_COMPLETION.INTERRUPTED
			result.subcodes.add(CODES_DATA.ERROR_CHECK)

			return result

		result_exist : bool = cell.sid in self._s_cells

		if not result_exist:
			result.code = CODES_COMPLETION.COMPLETED
			result.subcodes.add(CODES_PROCESSING.SKIP)
			result.subcodes.add(CODES_DATA.NO_DATA)

			return result

		result.data = self._s_cells[cell.sid]

		return result

	def SyncSCell(self, cell: T20_StructCell, flag_capture_delta: bool = False) -> T21_StructResult_StructCell:
		""" Синхронизация S-Ячейки """
		result              = T21_StructResult_StructCell()

		result_check : bool = ValidateOid(cell.oid)
		result_check       &= ValidatePid(cell.pid)

		if not result_check:
			result.code = CODES_COMPLETION.INTERRUPTED
			result.subcodes.add(CODES_DATA.ERROR_CHECK)

			return result

		result_read        = self.ReadSCell(cell)
		if not result_read.code == CODES_COMPLETION.COMPLETED:
			result.code = CODES_COMPLETION.INTERRUPTED
			result.subcodes = result_read.subcodes

			return result

		cell_in_container  = T20_StructCell() if result_read.data is None else result_read.data

		if cell_in_container.cut > cell.cut:
			result.code = CODES_COMPLETION.COMPLETED
			result.subcodes.add(CODES_PROCESSING.SKIP)
			result.data = cell_in_container

			return result

		result = self.WriteSCell(cell, flag_ignore=False, flag_capture_delta=flag_capture_delta)

		return result

	def WriteSCell(self, cell: T20_StructCell, flag_ignore: bool = False, flag_capture_delta: bool = False) -> T21_StructResult_StructCell:
		""" Запись S-Ячейки """
		result      = T21_StructResult_StructCell()

		result_check : bool = ValidateOid(cell.oid)
		result_check       &= ValidatePid(cell.pid)

		if not result_check:
			result.code = CODES_COMPLETION.INTERRUPTED
			result.subcodes.add(CODES_DATA.ERROR_CHECK)

			return result

		result_exist : bool = cell.sid in self._s_cells

		if flag_ignore and result_exist:
			result.code = CODES_COMPLETION.COMPLETED
			result.subcodes.add(CODES_PROCESSING.SKIP)

			return result

		cells_start  : list[T20_StructCell] = []
		cells_end    : list[T20_StructCell] = []

		if flag_capture_delta: cells_start = self.ReadSCells(cell).data

		self._s_cells[cell.sid] = copy(cell)

		if flag_capture_delta:
			cells_end = self.ReadSCells(cell).data
			cells_delta = DifferenceLists(cells_start, cells_end)

			result.data = None if not cells_delta else cells_delta[0]

		return result

	# Логика данных: S-Ячейки
	def DeleteSCells(self, cell_cells: T20_StructCell | list[T20_StructCell], flag_capture_delta: bool = False) -> T21_StructResult_StructCells:
		""" Удаление пакета S-Ячеек """
		result      = T21_StructResult_StructCells()
		return result

	def ReadSCells(self, cell_cells: T20_StructCell | list[T20_StructCell]) -> T21_StructResult_StructCells:
		""" Запрос пакета S-Ячеек """
		result      = T21_StructResult_StructCells()

		if type(cell_cells) is T20_StructCell:
			for sid, cell in self._s_cells.items():
				if cell_cells.oci and not (cell.oci == cell_cells.oci): continue
				if cell_cells.oid and not (cell.oid == cell_cells.oid): continue
				if cell_cells.pid and not (cell.pid == cell_cells.pid): continue
				if cell_cells.cvl and not (cell.cvl == cell_cells.cvl): continue
				if cell_cells.cut and not (cell.cut == cell_cells.cut): continue

				result.data.append(cell)

		elif type(cell_cells) is list:
			for cell in cell_cells:
				result_check : bool = ValidateOid(cell.oid)
				result_check       &= ValidatePid(cell.pid)

				if not result_check: continue

				result.data.append(cell)

		else:
			result.code = CODES_COMPLETION.INTERRUPTED
			result.subcodes.add(CODES_PROCESSING.SKIP)
			result.subcodes.add(CODES_DATA.ERROR_TYPE)

		return result

	def SyncSCells(self, cell_cells: T20_StructCell | list[T20_StructCell], flag_capture_delta: bool = False) -> T21_StructResult_StructCells:
		""" Запись пакета S-Ячеек """
		result      = T21_StructResult_StructCells()
		return result

	def WriteSCells(self, cells: list[T20_StructCell], flag_capture_delta: bool = False) -> T21_StructResult_StructCells:
		""" Запись пакета S-Ячеек """
		result      = T21_StructResult_StructCells()
		return result

	# Логика данных: D-Ячейка
	def DeleteDCell(self, cell: T20_StructCell, flag_capture_delta: bool = False) -> T21_StructResult_StructCell:
		""" Удаление D-Ячейки """
		result      = T21_StructResult_StructCell()
		return result

	def ReadDCell(self, cell: T20_StructCell) -> T21_StructResult_StructCell:
		""" Запрос D-Ячейки """
		result      = T21_StructResult_StructCell()
		return result

	def WriteDCell(self, cell: T20_StructCell, flag_capture_delta: bool = False) -> T21_StructResult_StructCell:
		""" Запись D-Ячейки """
		result      = T21_StructResult_StructCell()
		return result

	# Логика данных: D-Ячейки
	def DeleteDCells(self, range_cell_cells: T21_CutRange | T20_StructCell | list[T20_StructCell], flag_capture_delta: bool = False) -> T21_StructResult_StructCells:
		""" Удаление пакета D-Ячеек """
		result      = T21_StructResult_StructCells()
		return result

	def ReadDCells(self, range_cell_cells: T21_CutRange | T20_StructCell | list[T20_StructCell]) -> T21_StructResult_StructCells:
		""" Запрос пакета D-Ячеек """
		result      = T21_StructResult_StructCells()
		return result

	def WriteDCells(self, cells: list[T20_StructCell], flag_capture_delta: bool = False) -> T21_StructResult_StructCells:
		""" Запись пакета D-Ячеек """
		result      = T21_StructResult_StructCells()
		return result

	# Логика данных: Запрос данных
	def ReadDCutRange(self, cell: T21_CutRange, flag_capture_delta: bool = False) -> T21_StructResult_CutRange:
		""" Запрос границ cUT D-Ячейки """
		result      = T21_StructResult_CutRange()
		return result

	def ReadDCuts(self, cell: T21_CutRange, flag_capture_delta: bool = False) -> T21_StructResult_List:
		""" Запрос списка CUT """
		result      = T21_StructResult_CutRange()
		return result

	# Логика управления
	pass
