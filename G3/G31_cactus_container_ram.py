# КАКТУС: КОНТЕЙНЕР-RAM
# 08 июл 2024

from copy                  import copy

from G00_cactus_codes      import CONTAINERS
from G00_status_codes      import *

from G10_cactus_check      import *
from G10_list              import DifferenceLists

from G21_cactus_struct     import *

from G30_cactus_container  import C30_Container


class C31_ContainerRAM(C30_Container):
	""" Кактус: Контейнер RAM """

	# Модель данных
	def Init_00(self):
		super().Init_00()

		self._s_cells : dict[str,           T20_StructCell]  = dict()
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
		result_check  : bool                = CheckIdo(cell.ido)
		result_check                       &= CheckIdp(cell.idp)

		if not result_check:
			return T21_StructResult_StructCell(code     = CODES_COMPLETION.INTERRUPTED,
			                                   subcodes = {CODES_DATA.ERROR_CHECK})

		result_exist : bool                 = cell.ids in self._s_cells

		if not result_exist:
			return T21_StructResult_StructCell(code     = CODES_COMPLETION.COMPLETED,
											   subcodes = {CODES_PROCESSING.SKIP, CODES_DATA.NO_DATA})

		cell_start  : T20_StructCell | None = None
		cell_end    : T20_StructCell | None = None

		if flag_capture_delta: cell_start = self.ReadSCell(cell).data

		del self._s_cells[cell.ids]

		result                              = T21_StructResult_StructCell()
		result.code                         = CODES_COMPLETION.COMPLETED

		if flag_capture_delta:
			cell_end = self.ReadSCell(cell).data
			cells    = [cell_start, cell_end]
			cells.remove(None)

			result.data = cells[0]

		return result

	def ReadSCell(self, cell: T20_StructCell) -> T21_StructResult_StructCell:
		""" Запрос S-Ячейки """
		result_check : bool = CheckIdo(cell.ido)
		result_check       &= CheckIdp(cell.idp)

		if not result_check:
			return T21_StructResult_StructCell(code     = CODES_COMPLETION.INTERRUPTED,
											   subcodes = {CODES_DATA.ERROR_CHECK})

		result_exist : bool = cell.ids in self._s_cells

		if not result_exist:
			return T21_StructResult_StructCell(code     = CODES_COMPLETION.INTERRUPTED,
			                                   subcodes = {CODES_DATA.NO_DATA})

		return T21_StructResult_StructCell(code = CODES_COMPLETION.COMPLETED,
										   data = copy(self._s_cells[cell.ids]))

	def SyncSCell(self, cell: T20_StructCell, flag_capture_delta: bool = False) -> T21_StructResult_StructCell:
		""" Синхронизация S-Ячейки """
		result_check : bool = CheckIdo(cell.ido)
		result_check       &= CheckIdp(cell.idp)

		if not result_check:
			return T21_StructResult_StructCell(code     = CODES_COMPLETION.INTERRUPTED,
											   subcodes = {CODES_DATA.ERROR_CHECK})

		cell_in_container   = self._s_cells.get(cell.ids, None)

		result_write : bool = True
		if cell_in_container is not None: result_write = (cell_in_container.vlt < cell.vlt)

		result              = T21_StructResult_StructCell()
		result.code         = CODES_COMPLETION.COMPLETED

		if not result_write:
			result.subcodes.add(CODES_PROCESSING.SKIP)

			if flag_capture_delta: result.data = cell_in_container

			return result

		result = self.WriteSCell(cell, False, flag_capture_delta)

		return result

	def WriteSCell(self, cell: T20_StructCell, flag_skip: bool = False, flag_capture_delta: bool = False) -> T21_StructResult_StructCell:
		""" Запись S-Ячейки """
		result_check : bool                  = CheckIdo(cell.ido)
		result_check                        &= CheckIdp(cell.idp)

		if not result_check:
			return T21_StructResult_StructCell(code     = CODES_COMPLETION.INTERRUPTED,
											   subcodes = {CODES_DATA.ERROR_CHECK})

		result_exist : bool                  = cell.ids in self._s_cells

		if flag_skip and result_exist:
			return T21_StructResult_StructCell(code     = CODES_COMPLETION.COMPLETED,
											   subcodes = {CODES_PROCESSING.SKIP})

		cell_start   : T20_StructCell | None = None
		cell_end     : T20_StructCell | None = None

		if flag_capture_delta: cell_start = self.ReadSCell(cell).data

		self._s_cells[cell.ids] = copy(cell)

		result                              = T21_StructResult_StructCell()
		result.code                         = CODES_COMPLETION.COMPLETED

		if flag_capture_delta:
			cell_end    = self.ReadSCell(cell).data
			result.data = None if cell_end == cell_start else cell_end

		return result

	# Логика данных: S-Ячейки
	def DeleteSCells(self, cell_cells: T20_StructCell | list[T20_StructCell], flag_transaction_mode: bool = False, flag_capture_delta: bool = False) -> T21_StructResult_StructCells:
		""" Удаление пакета S-Ячеек """
		result                               = T21_StructResult_StructCells()
		result.code                          = CODES_COMPLETION.COMPLETED

		cells_before  : list[T20_StructCell] = []
		cells_after   : list[T20_StructCell] = []

		if flag_capture_delta:
			result_read  = self.ReadSCells(cell_cells)
			if not result_read.code == CODES_COMPLETION.COMPLETED: return T21_StructResult_StructCells(code     = CODES_COMPLETION.INTERRUPTED,
			                                                                                           subcodes = result_read.subcodes)
			cells_before = result_read.data

		if   type(cell_cells) is T20_StructCell:
			for ids in list(self._s_cells.keys()):
				try   :
					cell = self._s_cells.get(ids)

					if cell_cells.idc and not (cell.idc == cell_cells.idc): continue
					if cell_cells.ido and not (cell.ido == cell_cells.ido): continue
					if cell_cells.idp and not (cell.idp == cell_cells.idp): continue
					if cell_cells.vlp and not (cell.vlp == cell_cells.vlp): continue
					if cell_cells.vlt and not (cell.vlt == cell_cells.vlt): continue

					del self._s_cells[ids]
				except:
					result.subcodes.add(CODES_PROCESSING.PARTIAL)

		elif type(cell_cells) is list          :
			for cell in cell_cells:
				try   :
					del self._s_cells[cell.ids]
				except:
					result.subcodes.add(CODES_PROCESSING.PARTIAL)

		if flag_capture_delta:
			result_read = self.ReadSCells(cell_cells)
			if not result_read.code == CODES_COMPLETION.COMPLETED: return T21_StructResult_StructCells(code     = CODES_COMPLETION.INTERRUPTED,
			                                                                                           subcodes = result_read.subcodes)
			cells_after = result_read.data
			result.data = DifferenceLists(cells_before, cells_after, True)

		match len(result.data):
			case 0: result.subcodes.add(CODES_DATA.NO_DATA)
			case 1: result.subcodes.add(CODES_DATA.SINGLE)

		return result

	def ReadSCells(self, cell_cells: T20_StructCell | list[T20_StructCell]) -> T21_StructResult_StructCells:
		""" Запрос пакета S-Ячеек """
		result      = T21_StructResult_StructCells()
		result.code = CODES_COMPLETION.COMPLETED

		if type(cell_cells) is T20_StructCell:
			for ids, cell in self._s_cells.items():
				if cell_cells.idc and not (cell.idc == cell_cells.idc): continue
				if cell_cells.ido and not (cell.ido == cell_cells.ido): continue
				if cell_cells.idp and not (cell.idp == cell_cells.idp): continue
				if cell_cells.vlp and not (cell.vlp == cell_cells.vlp): continue
				if cell_cells.vlt and not (cell.vlt == cell_cells.vlt): continue

				result.data.append(copy(cell))

		elif type(cell_cells) is list:
			for cell in cell_cells:
				result_check : bool = CheckIdo(cell.ido)
				result_check       &= CheckIdp(cell.idp)

				if not result_check                 : continue
				if     cell.ids not in self._s_cells: continue

				result.data.append(copy(self._s_cells[cell.ids]))

		else:
			result.code = CODES_COMPLETION.INTERRUPTED
			result.subcodes.add(CODES_PROCESSING.SKIP)
			result.subcodes.add(CODES_DATA.ERROR_TYPE)

		match len(result.data):
			case 0: result.subcodes.add(CODES_DATA.NO_DATA)
			case 1: result.subcodes.add(CODES_DATA.SINGLE)

		return result

	def WriteSCells(self, cells: list[T20_StructCell], flag_transaction_mode: bool = False, flag_skip: bool = False,  flag_capture_delta: bool = False) -> T21_StructResult_StructCells:
		""" Запись пакета S-Ячеек """
		result                              = T21_StructResult_StructCells()
		result.code                         = CODES_COMPLETION.COMPLETED

		cells_before : list[T20_StructCell] = []
		cells_after  : list[T20_StructCell] = []

		if flag_capture_delta:
			result_read  = self.ReadSCells(cells)
			if not result_read.code == CODES_COMPLETION.COMPLETED: return T21_StructResult_StructCells(code     = CODES_COMPLETION.INTERRUPTED,
			                                                                                           subcodes = result_read.subcodes)
			cells_before = result_read.data

		for cell in cells:
			result_check : bool = CheckIdo(cell.ido)
			result_check       &= CheckIdp(cell.idp)

			if not result_check:
				result.subcodes.add(CODES_DATA.ERROR_CHECK)
				result.subcodes.add(CODES_PROCESSING.PARTIAL)
				continue

			result_exist : bool = cell.ids in self._s_cells

			if flag_skip and result_exist:
				result.subcodes.add(CODES_PROCESSING.SKIP)
				result.subcodes.add(CODES_PROCESSING.PARTIAL)
				continue

			self._s_cells[cell.ids] = copy(cell)

		if flag_capture_delta:
			result_read = self.ReadSCells(cells)
			if not result_read.code == CODES_COMPLETION.COMPLETED: return T21_StructResult_StructCells(code     = CODES_COMPLETION.INTERRUPTED,
			                                                                                           subcodes = result_read.subcodes)
			cells_after = result_read.data
			result.data = DifferenceLists(cells_before, cells_after)

			match len(result.data):
				case 0: result.subcodes.add(CODES_DATA.NO_DATA)
				case 1: result.subcodes.add(CODES_DATA.SINGLE)

		return result

	# Логика данных: D-Ячейка
	def DeleteDCell(self, cell: T20_StructCell, flag_capture_delta: bool = False) -> T21_StructResult_StructCell:
		""" Удаление D-Ячейки """
		result_check : bool                      = CheckIdo(cell.ido)
		result_check                            &= CheckIdp(cell.idp)
		result_check                            &= bool(cell.vlt)

		if not result_check:
			return T21_StructResult_StructCell(code     = CODES_COMPLETION.INTERRUPTED,
											   subcodes = {CODES_DATA.ERROR_CHECK})

		dcells       : dict[int, T20_StructCell] = self._d_cells.get(cell.ids, dict())

		result_exist : bool                      = cell.vlt in dcells

		if not result_exist:
			return T21_StructResult_StructCell(code     = CODES_COMPLETION.COMPLETED,
											   subcodes = {CODES_PROCESSING.SKIP, CODES_DATA.NO_DATA})

		cell_start  : T20_StructCell | None = None
		cell_end    : T20_StructCell | None = None

		if flag_capture_delta: cell_start = self.ReadDCell(cell).data

		del dcells[cell.vlt]

		result                              = T21_StructResult_StructCell()
		result.code                         = CODES_COMPLETION.COMPLETED

		if flag_capture_delta:
			cell_end = self.ReadSCell(cell).data
			cells    = [cell_start, cell_end]
			cells.remove(None)

			result.data = cells[0]

		return result

	def ReadDCell(self, cell: T20_StructCell) -> T21_StructResult_StructCell:
		""" Запрос D-Ячейки """
		result_check : bool                      = CheckIdo(cell.ido)
		result_check                            &= CheckIdp(cell.idp)
		result_check                            &= bool(cell.vlt)

		if not result_check:
			return T21_StructResult_StructCell(code     = CODES_COMPLETION.INTERRUPTED,
											   subcodes = {CODES_DATA.ERROR_CHECK})

		dcells       : dict[int, T20_StructCell] = self._d_cells.get(cell.ids, dict())

		result_exist : bool                      = cell.vlt in dcells

		if not result_exist:
			return T21_StructResult_StructCell(code     = CODES_COMPLETION.INTERRUPTED,
											   subcodes = {CODES_DATA.NO_DATA})

		return T21_StructResult_StructCell(code = CODES_COMPLETION.COMPLETED,
		                                   data = copy(dcells[cell.vlt]))

	def WriteDCell(self, cell: T20_StructCell, flag_capture_delta: bool = False) -> T21_StructResult_StructCell:
		""" Запись D-Ячейки """
		result_check : bool                      = CheckIdo(cell.ido)
		result_check                            &= CheckIdp(cell.idp)
		result_check                            &= bool(cell.vlt)

		if not result_check:
			return T21_StructResult_StructCell(code     = CODES_COMPLETION.INTERRUPTED,
											   subcodes = {CODES_DATA.ERROR_CHECK})

		dcells       : dict[int, T20_StructCell] = self._d_cells.get(cell.ids, dict())

		cell_start  : T20_StructCell | None = None
		cell_end    : T20_StructCell | None = None

		if flag_capture_delta: cell_start = self.ReadDCell(cell).data

		dcells[cell.vlt] = cell
		self._d_cells[cell.ids] = dcells

		result                              = T21_StructResult_StructCell()
		result.code                         = CODES_COMPLETION.COMPLETED

		if flag_capture_delta:
			cell_end = self.ReadDCell(cell).data

			cells    = [cell_start, cell_end]
			cells.remove(None)

			result.data = cells[0]

		return result
	# Логика управления
	pass
