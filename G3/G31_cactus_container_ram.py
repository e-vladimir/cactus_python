# КАКТУС: КОНТЕЙНЕР-RAM
# 08 июл 2024

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
		result_check  : bool                = ValidateIdo(cell.ido)
		result_check                       &= ValidateIdp(cell.idp)

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
		result_check : bool = ValidateIdo(cell.ido)
		result_check       &= ValidateIdp(cell.idp)

		if not result_check:
			return T21_StructResult_StructCell(code     = CODES_COMPLETION.INTERRUPTED,
											   subcodes = {CODES_DATA.ERROR_CHECK})

		result_exist : bool = cell.ids in self._s_cells

		if not result_exist:
			return T21_StructResult_StructCell(code     = CODES_COMPLETION.COMPLETED,
			                                   subcodes = {CODES_PROCESSING.SKIP, CODES_DATA.NO_DATA})

		return T21_StructResult_StructCell(code = CODES_COMPLETION.COMPLETED,
										   data = self._s_cells[cell.ids])

	def SyncSCell(self, cell: T20_StructCell, flag_capture_delta: bool = False) -> T21_StructResult_StructCell:
		""" Синхронизация S-Ячейки """
		result_check : bool = ValidateIdo(cell.ido)
		result_check       &= ValidateIdp(cell.idp)

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
		result_check : bool                  = ValidateIdo(cell.ido)
		result_check                        &= ValidateIdp(cell.idp)

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
		result_cells                        = self.ReadSCells(cell_cells)

		cells_start  : list[T20_StructCell] = result_cells.data
		cells_end    : list[T20_StructCell] = []

		for cell in cells_start: del self._s_cells[cell.ids]

		result                              = T21_StructResult_StructCells()
		result.code                         = CODES_COMPLETION.COMPLETED

		if flag_capture_delta:
			cells_end   = self.ReadSCells(cell_cells).data
			result.data = DifferenceLists(cells_start, cells_end, True)

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
				result_check : bool = ValidateIdo(cell.ido)
				result_check       &= ValidateIdp(cell.idp)

				if not result_check                 : continue
				if     cell.ids not in self._s_cells: continue

				result.data.append(copy(self._s_cells[cell.ids]))

		else:
			result.code = CODES_COMPLETION.INTERRUPTED
			result.subcodes.add(CODES_PROCESSING.SKIP)
			result.subcodes.add(CODES_DATA.ERROR_TYPE)

		return result

	def SyncSCells(self, cells: list[T20_StructCell], flag_transaction_mode: bool = False, flag_capture_delta: bool = False) -> T21_StructResult_StructCells:
		""" Запись пакета S-Ячеек """
		result                             = T21_StructResult_StructCells()
		result.code                        = CODES_COMPLETION.COMPLETED

		cells_start : list[T20_StructCell] = []
		cells_end   : list[T20_StructCell] = []

		if flag_capture_delta: cells_start = self.ReadSCells(cells).data

		for cell in cells:
			result_check  = ValidateIdc(cell.idc)
			result_check &= ValidateIdo(cell.ido)
			result_check &= ValidateIdp(cell.idp)

			if not result_check:
				result.subcodes.add(CODES_PROCESSING.PARTIAL)
				result.subcodes.add(CODES_DATA.ERROR_CHECK)
				continue

			cell_in_container = self._s_cells.get(cell.ids, None)

			result_write: bool = True
			if cell_in_container is not None: result_write = (cell_in_container.vlt < cell.vlt)

			if not result_write:
				result.subcodes.add(CODES_PROCESSING.PARTIAL)
				continue

			self._s_cells[cell.ids] = copy(cell)

		if flag_capture_delta:
			cells_end   = self.ReadSCells(cells).data
			result.data = DifferenceLists(cells_start, cells_end)

		return result

	def WriteSCells(self, cells: list[T20_StructCell], flag_transaction_mode: bool = False, flag_skip: bool = False,  flag_capture_delta: bool = False) -> T21_StructResult_StructCells:
		""" Запись пакета S-Ячеек """
		result                             = T21_StructResult_StructCells()
		result.code                        = CODES_COMPLETION.COMPLETED

		cells_start : list[T20_StructCell] = []
		cells_end   : list[T20_StructCell] = []

		if flag_capture_delta: cells_start = self.ReadSCells(cells).data

		for cell in cells:
			result_check  = ValidateIdc(cell.idc)
			result_check &= ValidateIdo(cell.ido)
			result_check &= ValidateIdp(cell.idp)

			if not result_check:
				result.subcodes.add(CODES_PROCESSING.PARTIAL)
				result.subcodes.add(CODES_DATA.ERROR_CHECK)
				continue

			result_exist : bool = cell.ids in self._s_cells

			if result_exist and flag_skip:
				result.subcodes.add(CODES_PROCESSING.PARTIAL)
				continue

			self._s_cells[cell.ids] = copy(cell)

		if flag_capture_delta:
			cells_end   = self.ReadSCells(cells).data
			result.data = DifferenceLists(cells_start, cells_end)

		return result

	# Логика данных: D-Ячейка
	def DeleteDCell(self, cell: T20_StructCell, flag_capture_delta: bool = False) -> T21_StructResult_StructCell:
		""" Удаление D-Ячейки """
		result_check : bool                  = ValidateIdo(cell.ido)
		result_check                        &= ValidateIdp(cell.idp)
		result_check                        &= bool(cell.vlt)

		if not result_check:
			return T21_StructResult_StructCell(code     = CODES_COMPLETION.INTERRUPTED,
			                                   subcodes = {CODES_DATA.ERROR_CHECK})

		cell_start   : T20_StructCell | None = None
		cell_end     : T20_StructCell | None = None

		if flag_capture_delta: cell_start = self.ReadDCell(cell).data

		result_exist : bool                  = cell.ids in self._d_cells

		if not result_exist:
			return T21_StructResult_StructCell(code     = CODES_COMPLETION.COMPLETED,
			                                   subcodes = {CODES_DATA.NO_DATA, CODES_PROCESSING.SKIP})

		ddata                                = self._d_cells[cell.ids]

		result_exist : bool                  = cell.vlt in ddata

		if not result_exist:
			return T21_StructResult_StructCell(code     = CODES_COMPLETION.COMPLETED,
			                                   subcodes = {CODES_DATA.NO_DATA, CODES_PROCESSING.SKIP})

		del ddata[cell.vlt]
		self._d_cells[cell.ids] = ddata

		result                               = T21_StructResult_StructCell()
		result.code                          = CODES_COMPLETION.COMPLETED

		if flag_capture_delta:
			cell_end    = self.ReadDCell(cell).data
			cells    = [cell_start, cell_end]
			cells.remove(None)

			result.data = cells[0]

		return result

	def ReadDCell(self, cell: T20_StructCell) -> T21_StructResult_StructCell:
		""" Запрос D-Ячейки """
		result              = T21_StructResult_StructCell()
		result.code         = CODES_COMPLETION.COMPLETED

		result_check : bool = ValidateIdo(cell.ido)
		result_check       &= ValidateIdp(cell.idp)
		result_check       &= bool(cell.vlt)

		if not result_check:
			return T21_StructResult_StructCell(code     = CODES_COMPLETION.INTERRUPTED,
			                                   subcodes = {CODES_DATA.ERROR_CHECK})

		result_exist : bool = cell.ids in self._d_cells

		if not result_exist:
			return T21_StructResult_StructCell(code     = CODES_COMPLETION.COMPLETED,
			                                   subcodes = {CODES_DATA.NO_DATA})

		ddata               = self._d_cells[cell.ids]

		result_exist : bool = cell.vlt in ddata

		if not result_exist:
			return T21_StructResult_StructCell(code     = CODES_COMPLETION.COMPLETED,
			                                   subcodes = {CODES_DATA.NO_DATA})

		result.data = ddata[cell.vlt]

		return result

	def WriteDCell(self, cell: T20_StructCell, flag_capture_delta: bool = False) -> T21_StructResult_StructCell:
		""" Запись D-Ячейки """
		result_check : bool                  = ValidateIdo(cell.ido)
		result_check                        &= ValidateIdp(cell.idp)

		if not result_check:
			return T21_StructResult_StructCell(code     = CODES_COMPLETION.INTERRUPTED,
			                                   subcodes = {CODES_DATA.ERROR_CHECK})

		cell_start   : T20_StructCell | None = None
		cell_end     : T20_StructCell | None = None

		if flag_capture_delta: cell_start = self.ReadDCell(cell).data

		ddata                                = self._d_cells.get(cell.ids, dict())
		ddata[cell.vlt]                      = copy(cell)
		self._d_cells[cell.ids] = ddata

		result                               = T21_StructResult_StructCell()
		result.code                          = CODES_COMPLETION.COMPLETED

		if flag_capture_delta:
			cell_end    = self.ReadDCell(cell).data
			result.data = None if cell_end == cell_start else cell_end

		return result

	# Логика данных: D-Ячейки
	def DeleteDCells(self, cell: T21_VltRange, flag_transaction_mode: bool = False, flag_capture_delta: bool = False) -> T21_StructResult_StructCells:
		""" Удаление пакета D-Ячеек """
		result                             = T21_StructResult_StructCells()
		result.code                        = CODES_COMPLETION.COMPLETED

		cells_start : list[T20_StructCell] = []

		if flag_capture_delta: cells_start = self.ReadDCells(cell).data

		result_check : bool = ValidateIdo(cell.ido)
		result_check       &= ValidateIdp(cell.idp)

		if not result_check:
			return T21_StructResult_StructCells(code     = CODES_COMPLETION.INTERRUPTED,
			                                    subcodes = {CODES_DATA.ERROR_CHECK})

		ddata = self._d_cells.get(cell.ids, dict())

		for ids in list(ddata.keys()):
			cell_in_container = ddata[ids]

			if cell.vlt_l + cell.vlt_r > 0:
				if not CheckBetween(cell.vlt_l, cell_in_container.vlt, cell.vlt_r, True): continue

			del ddata[ids]

		if flag_capture_delta:
			cells_end   = self.ReadDCells(cell).data
			result.data = DifferenceLists(cells_start, cells_end, True)

			if not result.data:
				result.subcodes.add(CODES_DATA.NO_DATA)

		return result

	def ReadDCells(self, cell: T21_VltRange) -> T21_StructResult_StructCells:
		""" Запрос пакета D-Ячеек """
		result      = T21_StructResult_StructCells()
		result.code = CODES_COMPLETION.COMPLETED

		result_check : bool = ValidateIdo(cell.ido)
		result_check       &= ValidateIdp(cell.idp)

		if not result_check:
			return T21_StructResult_StructCells(code     = CODES_COMPLETION.INTERRUPTED,
			                                    subcodes = {CODES_DATA.ERROR_CHECK})

		ddata = self._d_cells.get(cell.ids, dict())

		for ids, cell_in_container in ddata.items():
			if cell.vlt_l + cell.vlt_r > 0:
				if not CheckBetween(cell.vlt_l, cell_in_container.vlt, cell.vlt_r, True): continue

			result.data.append(copy(cell_in_container))

		match len(result.data):
			case 0: result.subcodes.add(CODES_DATA.NO_DATA)
			case 1: result.subcodes.add(CODES_DATA.SINGLE)

		return result

	def WriteDCells(self, cell: T21_VltRange, flag_transaction_mode: bool = False, flag_capture_delta: bool = False) -> T21_StructResult_StructCells:
		""" Запись пакета D-Ячеек """
		return T21_StructResult_StructCells(code     = CODES_COMPLETION.COMPLETED,
		                                    subcodes = {CODES_PROCESSING.SKIP})

	# Логика данных: Запрос данных
	def ReadDVltRange(self, cell: T21_VltRange) -> T21_StructResult_VltRange:
		""" Запрос границ cUT D-Ячейки """
		result            = T21_StructResult_VltRange()
		result.code       = CODES_COMPLETION.COMPLETED

		result_vlts       = self.ReadDVlts(cell)

		result.code       = result_vlts.code
		result.subcodes   = result_vlts.subcodes

		if not result_vlts.data:
			result.subcodes.add(CODES_DATA.NO_DATA)

			return result

		result.data       = copy(cell)
		result.data.vlt_l = min(result_vlts.data)
		result.data.vlt_r = max(result_vlts.data)

		return result

	def ReadDVlts(self, cell: T21_VltRange) -> T21_StructResult_List:
		""" Запрос списка VLT """
		result_check : bool = ValidateIdo(cell.ido)
		result_check       &= ValidateIdp(cell.idp)

		if not result_check:
			return T21_StructResult_List(code     = CODES_COMPLETION.INTERRUPTED,
			                             subcodes = {CODES_DATA.ERROR_CHECK})

		result              = T21_StructResult_List()
		result.code         = CODES_COMPLETION.COMPLETED

		ddata               = self._d_cells.get(cell.ids, dict())

		for ids, dcell in ddata.items():
			if cell.idc   and not (dcell.idc == cell.idc)  : continue
			if cell.ido   and not (dcell.ido == cell.ido)  : continue
			if cell.idp   and not (dcell.idp == cell.idp)  : continue
			if cell.vlp   and not (dcell.vlp == cell.vlp)  : continue
			if cell.vlt   and not (dcell.vlt == cell.vlt)  : continue
			if cell.vlt_l and not (dcell.vlt >  cell.vlt_l): continue
			if cell.vlt_r and not (dcell.vlt <  cell.vlt_r): continue

			if dcell.vlt   in result.data                   : continue

			result.data.append(dcell.vlt)

		return result

	# Логика управления
	pass
