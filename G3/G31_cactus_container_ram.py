# КАКТУС: КОНТЕЙНЕР-RAM
# 21 июн 2024

from copy                  import copy

from G00_cactus_codes      import CONTAINERS
from G00_status_codes      import *

from G10_cactus_validators import *
from G10_list              import DifferenceLists
from G10_math_linear       import CheckBetween

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

		cell_start  : T20_StructCell | None = None
		cell_end    : T20_StructCell | None = None

		if flag_capture_delta: cell_start = self.ReadSCell(cell).data

		del self._s_cells[cell.sid]

		if flag_capture_delta:
			cell_end = self.ReadSCell(cell).data
			cells    = [cell_start, cell_end]
			cells.remove(None)

			result.data = cells[0]

		return result

	def ReadSCell(self, cell: T20_StructCell) -> T21_StructResult_StructCell:
		""" Запрос S-Ячейки """
		result              = T21_StructResult_StructCell()

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

		cell_in_container   = self._s_cells.get(cell.sid, None)

		result_write : bool = True
		if cell_in_container is not None: result_write = (cell_in_container.cut < cell.cut)

		if not result_write:
			result.code = CODES_COMPLETION.COMPLETED
			result.subcodes.add(CODES_PROCESSING.SKIP)
			result.data = cell_in_container

			return result

		result = self.WriteSCell(cell, False, flag_capture_delta)

		return result

	def WriteSCell(self, cell: T20_StructCell, flag_skip: bool = False, flag_capture_delta: bool = False) -> T21_StructResult_StructCell:
		""" Запись S-Ячейки """
		result                              = T21_StructResult_StructCell()

		result_check : bool                 = ValidateOid(cell.oid)
		result_check                       &= ValidatePid(cell.pid)

		if not result_check:
			result.code = CODES_COMPLETION.INTERRUPTED
			result.subcodes.add(CODES_DATA.ERROR_CHECK)

			return result

		result_exist : bool                  = cell.sid in self._s_cells

		if flag_skip and result_exist:
			result.code = CODES_COMPLETION.COMPLETED
			result.subcodes.add(CODES_PROCESSING.SKIP)

			return result

		cell_start   : T20_StructCell | None = None
		cell_end     : T20_StructCell | None = None

		if flag_capture_delta: cell_start = self.ReadSCell(cell).data

		self._s_cells[cell.sid] = copy(cell)

		if flag_capture_delta:
			cell_end    = self.ReadSCell(cell).data
			result.data = None if cell_end == cell_start else cell_end

		return result

	# Логика данных: S-Ячейки
	def DeleteSCells(self, cell_cells: T20_StructCell | list[T20_StructCell], flag_capture_delta: bool = False) -> T21_StructResult_StructCells:
		""" Удаление пакета S-Ячеек """
		result      = T21_StructResult_StructCells()

		result_cells                        = self.ReadSCells(cell_cells)
		cells_start  : list[T20_StructCell] = result_cells.data
		cells_end    : list[T20_StructCell] = []

		for cell in cells_start: del self._s_cells[cell.sid]

		if flag_capture_delta:
			cells_end   = self.ReadSCells(cell_cells).data
			result.data = DifferenceLists(cells_start, cells_end, True)

		return result

	def ReadSCells(self, cell_cells: T20_StructCell | list[T20_StructCell]) -> T21_StructResult_StructCells:
		""" Запрос пакета S-Ячеек """
		result = T21_StructResult_StructCells()

		if type(cell_cells) is T20_StructCell:
			for sid, cell in self._s_cells.items():
				if cell_cells.oci and not (cell.oci == cell_cells.oci): continue
				if cell_cells.oid and not (cell.oid == cell_cells.oid): continue
				if cell_cells.pid and not (cell.pid == cell_cells.pid): continue
				if cell_cells.cvl and not (cell.cvl == cell_cells.cvl): continue
				if cell_cells.cut and not (cell.cut == cell_cells.cut): continue

				result.data.append(copy(cell))

		elif type(cell_cells) is list:
			for cell in cell_cells:
				result_check : bool = ValidateOid(cell.oid)
				result_check       &= ValidatePid(cell.pid)

				if not result_check                 : continue
				if     cell.sid not in self._s_cells: continue

				result.data.append(copy(self._s_cells[cell.sid]))

		else:
			result.code = CODES_COMPLETION.INTERRUPTED
			result.subcodes.add(CODES_PROCESSING.SKIP)
			result.subcodes.add(CODES_DATA.ERROR_TYPE)

		return result

	def SyncSCells(self, cells: list[T20_StructCell], flag_capture_delta: bool = False) -> T21_StructResult_StructCells:
		""" Запись пакета S-Ячеек """
		result                             = T21_StructResult_StructCells()

		cells_start : list[T20_StructCell] = []
		cells_end   : list[T20_StructCell] = []

		if flag_capture_delta: cells_start = self.ReadSCells(cells).data

		for cell in cells:
			result_check  = ValidateOci(cell.oci)
			result_check &= ValidateOid(cell.oid)
			result_check &= ValidatePid(cell.pid)

			if not result_check:
				result.subcodes.add(CODES_PROCESSING.PARTIAL)
				result.subcodes.add(CODES_DATA.ERROR_CHECK)
				continue

			cell_in_container = self._s_cells.get(cell.sid, None)

			result_write: bool = True
			if cell_in_container is not None: result_write = (cell_in_container.cut < cell.cut)

			if not result_write:
				result.subcodes.add(CODES_PROCESSING.PARTIAL)
				continue

			self._s_cells[cell.sid] = copy(cell)

		if flag_capture_delta:
			cells_end   = self.ReadSCells(cells).data
			result.data = DifferenceLists(cells_start, cells_end)

		return result

	def WriteSCells(self, cells: list[T20_StructCell], flag_skip: bool = False, flag_capture_delta: bool = False) -> T21_StructResult_StructCells:
		""" Запись пакета S-Ячеек """
		result                             = T21_StructResult_StructCells()

		cells_start : list[T20_StructCell] = []
		cells_end   : list[T20_StructCell] = []

		if flag_capture_delta: cells_start = self.ReadSCells(cells).data

		for cell in cells:
			result_check  = ValidateOci(cell.oci)
			result_check &= ValidateOid(cell.oid)
			result_check &= ValidatePid(cell.pid)

			if not result_check:
				result.subcodes.add(CODES_PROCESSING.PARTIAL)
				result.subcodes.add(CODES_DATA.ERROR_CHECK)
				continue

			result_exist : bool = cell.sid in self._s_cells

			if result_exist and flag_skip:
				result.subcodes.add(CODES_PROCESSING.PARTIAL)
				continue

			self._s_cells[cell.sid] = copy(cell)

		if flag_capture_delta:
			cells_end   = self.ReadSCells(cells).data
			result.data = DifferenceLists(cells_start, cells_end)

		return result

	# Логика данных: D-Ячейка
	def DeleteDCell(self, cell: T20_StructCell, flag_capture_delta: bool = False) -> T21_StructResult_StructCell:
		""" Удаление D-Ячейки """
		result      = T21_StructResult_StructCell()

		result_check : bool                  = ValidateOid(cell.oid)
		result_check                        &= ValidatePid(cell.pid)

		if not result_check:
			result.code = CODES_COMPLETION.INTERRUPTED
			result.subcodes.add(CODES_DATA.ERROR_CHECK)

			return result

		cell_start   : T20_StructCell | None = None
		cell_end     : T20_StructCell | None = None

		if flag_capture_delta: cell_start = self.ReadDCell(cell).data

		result_exist : bool = cell.sid in self._d_cells

		if not result_exist:
			result.code = CODES_COMPLETION.COMPLETED
			result.subcodes.add(CODES_DATA.NO_DATA)
			result.subcodes.add(CODES_PROCESSING.SKIP)

			return result

		ddata               = self._d_cells[cell.sid]

		result_exist : bool = cell.cut in ddata

		if not result_exist:
			result.code = CODES_COMPLETION.COMPLETED
			result.subcodes.add(CODES_DATA.NO_DATA)
			result.subcodes.add(CODES_PROCESSING.SKIP)

			return result

		del ddata[cell.cut]
		self._d_cells[cell.sid] = ddata

		if flag_capture_delta:
			cell_end    = self.ReadDCell(cell).data
			cells    = [cell_start, cell_end]
			cells.remove(None)

			result.data = cells[0]

		return result

	def ReadDCell(self, cell: T20_StructCell) -> T21_StructResult_StructCell:
		""" Запрос D-Ячейки """
		result      = T21_StructResult_StructCell()

		result_check : bool = ValidateOid(cell.oid)
		result_check       &= ValidatePid(cell.pid)

		if not result_check:
			result.code = CODES_COMPLETION.INTERRUPTED
			result.subcodes.add(CODES_DATA.ERROR_CHECK)

			return result

		result_exist : bool = cell.sid in self._d_cells

		if not result_exist:
			result.code = CODES_COMPLETION.COMPLETED
			result.subcodes.add(CODES_DATA.NO_DATA)

			return result

		ddata               = self._d_cells[cell.sid]

		result_exist : bool = cell.cut in ddata

		if not result_exist:
			result.code = CODES_COMPLETION.COMPLETED
			result.subcodes.add(CODES_DATA.NO_DATA)

			return result

		result.data = ddata[cell.cut]

		return result

	def WriteDCell(self, cell: T20_StructCell, flag_capture_delta: bool = False) -> T21_StructResult_StructCell:
		""" Запись D-Ячейки """
		result                               = T21_StructResult_StructCell()

		result_check : bool                  = ValidateOid(cell.oid)
		result_check                        &= ValidatePid(cell.pid)

		if not result_check:
			result.code = CODES_COMPLETION.INTERRUPTED
			result.subcodes.add(CODES_DATA.ERROR_CHECK)

			return result

		cell_start   : T20_StructCell | None = None
		cell_end     : T20_StructCell | None = None

		if flag_capture_delta: cell_start = self.ReadDCell(cell).data

		ddata                                = self._d_cells.get(cell.sid, dict())
		ddata[cell.cut]                      = copy(cell)
		self._d_cells[cell.sid] = ddata

		if flag_capture_delta:
			cell_end    = self.ReadDCell(cell).data
			result.data = None if cell_end == cell_start else cell_end

		return result

	# Логика данных: D-Ячейки
	def DeleteDCells(self, range_cell_cells: T20_StructCell | list[T20_StructCell] | T21_CutRange, flag_capture_delta: bool = False) -> T21_StructResult_StructCells:
		""" Удаление пакета D-Ячеек """
		result      = T21_StructResult_StructCells()
		return result

	def ReadDCells(self, range_cell_cells: T20_StructCell | list[T20_StructCell] | T21_CutRange) -> T21_StructResult_StructCells:
		""" Запрос пакета D-Ячеек """
		result      = T21_StructResult_StructCells()

		if   type(range_cell_cells) is T20_StructCell:
			result_check : bool = ValidateOid(range_cell_cells.oid)
			result_check       &= ValidatePid(range_cell_cells.pid)

			if not result_check:
				result.code = CODES_COMPLETION.INTERRUPTED
				result.subcodes.add(CODES_DATA.ERROR_CHECK)
				return result

			ddata = self._d_cells.get(range_cell_cells.sid, dict())

			for sid, cell in ddata.items():
				if range_cell_cells.oci and not (cell.oci == range_cell_cells.oci): continue
				if range_cell_cells.oid and not (cell.oid == range_cell_cells.oid): continue
				if range_cell_cells.pid and not (cell.pid == range_cell_cells.pid): continue
				if range_cell_cells.cvl and not (cell.cvl == range_cell_cells.cvl): continue
				if range_cell_cells.cut and not (cell.cut == range_cell_cells.cut): continue

				result.data.append(copy(cell))

		elif type(range_cell_cells) is list          :
			for cell in range_cell_cells:
				result_check: bool = ValidateOid(cell.oid)
				result_check &= ValidatePid(cell.pid)

				if not result_check:
					result.subcodes.add(CODES_DATA.ERROR_CHECK)
					continue

				ddata = self._d_cells.get(cell.sid, dict())

				if cell.cut not in ddata: continue

				result.data.append(copy(ddata[cell.cut]))

		elif type(range_cell_cells) is T21_CutRange  :
			result_check : bool = ValidateOid(range_cell_cells.oid)
			result_check       &= ValidatePid(range_cell_cells.pid)

			if not result_check:
				result.code = CODES_COMPLETION.INTERRUPTED
				result.subcodes.add(CODES_DATA.ERROR_CHECK)
				return result

			ddata = self._d_cells.get(range_cell_cells.sid, dict())

			cut_l = range_cell_cells.cut_l
			cut_r = range_cell_cells.cut_r

			for sid, cell in ddata.items():
				if not CheckBetween(cut_l, cell.cut, cut_r, True): continue

				result.data.append(copy(cell))

		else                                         :
			result.code = CODES_COMPLETION.INTERRUPTED
			result.subcodes.add(CODES_PROCESSING.SKIP)
			result.subcodes.add(CODES_DATA.ERROR_TYPE)

		return result

	def WriteDCells(self, cells: list[T20_StructCell], flag_capture_delta: bool = False) -> T21_StructResult_StructCells:
		""" Запись пакета D-Ячеек """
		result      = T21_StructResult_StructCells()

		cells_start : list[T20_StructCell] = []
		cells_end   : list[T20_StructCell] = []

		if flag_capture_delta: cells_start = self.ReadDCells(cells).data

		for cell in cells:
			result_check  = ValidateOci(cell.oci)
			result_check &= ValidateOid(cell.oid)
			result_check &= ValidatePid(cell.pid)

			if not result_check:
				result.subcodes.add(CODES_PROCESSING.PARTIAL)
				result.subcodes.add(CODES_DATA.ERROR_CHECK)
				continue

			ddata = self._d_cells.get(cell.sid, dict())
			ddata[cell.cut] = copy(cell)
			self._d_cells[cell.sid] = ddata

		if flag_capture_delta:
			cells_end   = self.ReadDCells(cells).data
			result.data = DifferenceLists(cells_start, cells_end)

		return result

	# Логика данных: Запрос данных
	def ReadDCutRange(self, cell: T21_CutRange) -> T21_StructResult_CutRange:
		""" Запрос границ cUT D-Ячейки """
		result            = T21_StructResult_CutRange()

		result_cuts       = self.ReadDCuts(cell)

		result.code       = result_cuts.code
		result.subcodes   = result_cuts.subcodes

		if not result_cuts.data: return result

		result.data       = copy(cell)
		result.data.cut_l = min(result_cuts.data)
		result.data.cut_r = max(result_cuts.data)

		return result

	def ReadDCuts(self, cell: T21_CutRange) -> T21_StructResult_List:
		""" Запрос списка CUT """
		result              = T21_StructResult_List()

		result_check : bool = ValidateOid(cell.oid)
		result_check       &= ValidatePid(cell.pid)

		if not result_check:
			result.code = CODES_COMPLETION.INTERRUPTED
			result.subcodes.add(CODES_DATA.ERROR_CHECK)
			return result

		ddata               = self._d_cells.get(cell.sid, dict())

		for sid, dcell in ddata.items():
			if cell.oci   and not (dcell.oci == cell.oci)  : continue
			if cell.oid   and not (dcell.oid == cell.oid)  : continue
			if cell.pid   and not (dcell.pid == cell.pid)  : continue
			if cell.cvl   and not (dcell.cvl == cell.cvl)  : continue
			if cell.cut   and not (dcell.cut == cell.cut)  : continue
			if cell.cut_l and not (dcell.cut >  cell.cut_l): continue
			if cell.cut_r and not (dcell.cut <  cell.cut_r): continue

			if dcell.cut   in result.data                   : continue

			result.data.append(dcell.cut)

		return result

	# Логика управления
	pass
