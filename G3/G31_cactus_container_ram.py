# КАКТУС: КОНТЕЙНЕР-RAM
# 25 июл 2024

from copy                 import  copy

from G00_cactus_codes     import  CONTAINERS
from G00_status_codes     import (CODES_COMPLETION,
                                  CODES_DATA,
                                  CODES_PROCESSING)

from G10_cactus_check     import (CheckIdo,
                                  CheckIdp)
from G10_list             import  DifferenceLists

from G20_cactus_struct    import  T20_StructCell
from G21_cactus_struct    import (T21_StructResult_StructCell,
                                  T21_StructResult_StructCells,
                                  T21_StructResult_VltRange,
                                  T21_VltRange)
from G21_struct_result    import  T21_StructResult_List

from G30_cactus_container import  C30_Container


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

	# Логика данных: Пакет S-Ячеек
	def DeleteSCells(self, cell_cells: T20_StructCell | list[T20_StructCell], flag_capture_delta: bool = False) -> T21_StructResult_StructCells:
		""" Удаление пакета S-Ячеек """
		result_check : bool                 = False
		result_check                       |= type(cell_cells) is T20_StructCell
		result_check                       |= type(cell_cells) is list

		if not result_check:
			return T21_StructResult_StructCells(code     = CODES_COMPLETION.INTERRUPTED,
			                                    subcodes = {CODES_DATA.ERROR_TYPE})

		result                              = T21_StructResult_StructCells()

		cells_before : list[T20_StructCell] = []
		cells_after  : list[T20_StructCell] = []

		if flag_capture_delta: cells_before = self.ReadSCells(cell_cells).data

		if   type(cell_cells) is T20_StructCell:
			idss : list[str] = []

			for scell in self._s_cells.values():
				result_skip: bool = False
				result_skip      |= bool(cell_cells.idc) and not (scell.idc == cell_cells.idc)
				result_skip      |= bool(cell_cells.ido) and not (scell.ido == cell_cells.ido)
				result_skip      |= bool(cell_cells.idp) and not (scell.idp == cell_cells.idp)
				result_skip      |= bool(cell_cells.vlp) and not (scell.vlp == cell_cells.vlp)
				result_skip      |= bool(cell_cells.vlt) and not (scell.vlt == cell_cells.vlt)

				if result_skip: continue

				idss.append(scell.ids)

			for ids in idss:
				del self._s_cells[ids]

		elif type(cell_cells) is list:
			for scell in cell_cells:
				result_check: bool = CheckIdo(scell.ido)
				result_check      &= CheckIdp(scell.idp)

				if not result_check:
					result.subcodes.add(CODES_PROCESSING.PARTIAL)
					result.subcodes.add(CODES_DATA.ERROR_CHECK)

					continue

				try   : del self._s_cells[scell.ids]
				except:	result.subcodes.add(CODES_PROCESSING.PARTIAL)

		if flag_capture_delta:
			cells_after = self.ReadSCells(cell_cells).data

			result.data = DifferenceLists(cells_before, cells_after, True)

			match len(result.data):
				case 0: result.subcodes.add(CODES_DATA.NO_DATA)
				case 1: result.subcodes.add(CODES_DATA.SINGLE)

		return result

	def ReadSCells(self, cell_cells: T20_StructCell | list[T20_StructCell]) -> T21_StructResult_StructCells:
		""" Запрос пакета S-Ячеек """
		result_check : bool = False
		result_check       |= type(cell_cells) is T20_StructCell
		result_check       |= type(cell_cells) is list

		if not result_check:
			return T21_StructResult_StructCells(code     = CODES_COMPLETION.INTERRUPTED,
			                                    subcodes = {CODES_DATA.ERROR_TYPE})

		result            = T21_StructResult_StructCells()

		if   type(cell_cells) is T20_StructCell:
			for scell in self._s_cells.values():
				result_skip: bool = False
				result_skip      |= bool(cell_cells.idc) and not (scell.idc == cell_cells.idc)
				result_skip      |= bool(cell_cells.ido) and not (scell.ido == cell_cells.ido)
				result_skip      |= bool(cell_cells.idp) and not (scell.idp == cell_cells.idp)
				result_skip      |= bool(cell_cells.vlp) and not (scell.vlp == cell_cells.vlp)
				result_skip      |= bool(cell_cells.vlt) and not (scell.vlt == cell_cells.vlt)

				if result_skip: continue

				result.data.append(copy(scell))

		elif type(cell_cells) is list:
			for cell in cell_cells:
				result_check: bool = CheckIdo(cell.ido)
				result_check      &= CheckIdp(cell.idp)

				if not result_check:
					result.subcodes.add(CODES_PROCESSING.PARTIAL)
					result.subcodes.add(CODES_DATA.ERROR_CHECK)

					continue

				try   :	result.data.append(copy(self._s_cells[cell.ids]))
				except:	result.subcodes.add(CODES_PROCESSING.PARTIAL)

		match len(result.data):
			case 0: result.subcodes.add(CODES_DATA.NO_DATA)
			case 1: result.subcodes.add(CODES_DATA.SINGLE)

		return result

	def SyncSCells(self, cells: list[T20_StructCell], flag_capture_delta: bool = False) -> T21_StructResult_StructCells:
		""" Запись пакета S-Ячеек """
		result                              = T21_StructResult_StructCells()

		cells_before : list[T20_StructCell] = []
		cells_after  : list[T20_StructCell] = []

		if flag_capture_delta: cells_before = self.ReadSCells(cells).data

		for cell in cells:
			try   :
				result_check: bool = CheckIdo(cell.ido)
				result_check      &= CheckIdp(cell.idp)

				if not result_check:
					result.subcodes.add(CODES_PROCESSING.PARTIAL)
					result.subcodes.add(CODES_DATA.ERROR_CHECK)

					continue

				cell_in_container  = self._s_cells.get(cell.ids, T20_StructCell(vlt=-1))

				result_skip : bool = cell_in_container.vlt > cell.vlt

				if result_skip:
					result.subcodes.add(CODES_PROCESSING.PARTIAL)

					continue

				self._s_cells[cell.ids] = copy(cell)

			except: result.subcodes.add(CODES_PROCESSING.PARTIAL)

		if flag_capture_delta:
			cells_after = self.ReadSCells(cells).data

			result.data = DifferenceLists(cells_before, cells_after)

			match len(result.data):
				case 0: result.subcodes.add(CODES_DATA.NO_DATA)
				case 1: result.subcodes.add(CODES_DATA.SINGLE)

		return result

	def WriteSCells(self, cells: list[T20_StructCell], flag_skip: bool = False,  flag_capture_delta: bool = False) -> T21_StructResult_StructCells:
		""" Запись пакета S-Ячеек """
		result                              = T21_StructResult_StructCells()

		cells_before : list[T20_StructCell] = []
		cells_after  : list[T20_StructCell] = []

		if flag_capture_delta: cells_before = self.ReadSCells(cells).data

		for cell in cells:
			try   :
				result_check: bool = CheckIdo(cell.ido)
				result_check      &= CheckIdp(cell.idp)

				if not result_check:
					result.subcodes.add(CODES_PROCESSING.PARTIAL)
					result.subcodes.add(CODES_DATA.ERROR_CHECK)

					continue

				if flag_skip and cell.ids in self._s_cells:
					result.subcodes.add(CODES_PROCESSING.PARTIAL)

					continue

				self._s_cells[cell.ids] = copy(cell)

			except: result.subcodes.add(CODES_PROCESSING.PARTIAL)

		if flag_capture_delta:
			cells_after = self.ReadSCells(cells).data

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

		if cell.vlt in dcells:
			return T21_StructResult_StructCell(code     = CODES_COMPLETION.COMPLETED,
											   subcodes = {CODES_PROCESSING.SKIP})

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

	# Логика данных: Пакет D-Ячеек
	def DeleteDCells(self, cell: T21_VltRange, flag_capture_delta: bool = False) -> T21_StructResult_StructCells:
		""" Удаление пакета D-Ячеек """
		result_check : bool                      = CheckIdo(cell.ido)
		result_check                            &= CheckIdp(cell.idp)

		if not result_check:
			return T21_StructResult_StructCells(code     = CODES_COMPLETION.INTERRUPTED,
			                                    subcodes = {CODES_DATA.ERROR_CHECK})

		result                                   = T21_StructResult_StructCells()

		cells_before : list[T20_StructCell]      = []
		cells_after  : list[T20_StructCell]      = []

		if flag_capture_delta: cells_before = self.ReadDCells(cell).data

		dcells = self._d_cells.get(cell.ids, dict())

		for vlt in list(dcells.keys()):
			result_skip  = False
			result_skip |= bool(cell.vlt_l) and vlt >= cell.vlt_l
			result_skip |= bool(cell.vlt_r) and vlt <= cell.vlt_r

			if result_skip: continue

			del dcells[vlt]

		if flag_capture_delta:
			cells_after = self.ReadDCells(cell).data

			result.data = DifferenceLists(cells_before, cells_after, True)

			match len(result.data):
				case 0: result.subcodes.add(CODES_DATA.NO_DATA)
				case 1: result.subcodes.add(CODES_DATA.SINGLE)

		return result

	def ReadDCells(self, cell: T21_VltRange) -> T21_StructResult_StructCells:
		""" Запрос пакета D-Ячеек """
		result_check : bool                      = CheckIdo(cell.ido)
		result_check                            &= CheckIdp(cell.idp)

		if not result_check:
			return T21_StructResult_StructCells(code     = CODES_COMPLETION.INTERRUPTED,
			                                    subcodes = {CODES_DATA.ERROR_CHECK})

		result                                   = T21_StructResult_StructCells()

		cells_before : list[T20_StructCell]      = []
		cells_after  : list[T20_StructCell]      = []

		dcells = self._d_cells.get(cell.ids, dict())

		for vlt in list(dcells.keys()):
			result_skip  = False
			result_skip |= bool(cell.vlt_l) and vlt >= cell.vlt_l
			result_skip |= bool(cell.vlt_r) and vlt <= cell.vlt_r

			if result_skip: continue

			result.data.append(dcells[vlt])

		match len(result.data):
			case 0: result.subcodes.add(CODES_DATA.NO_DATA)
			case 1: result.subcodes.add(CODES_DATA.SINGLE)

		return result

	# Логика данных: Диапазон VLT
	def ReadVltRange(self, cell: T21_VltRange) -> T21_StructResult_VltRange:
		""" Запрос границ cUT D-Ячейки """
		result                                   = T21_StructResult_VltRange()
		result.data                              = T21_VltRange()

		result_check : bool                      = CheckIdo(cell.ido)
		result_check                            &= CheckIdp(cell.idp)

		if not result_check:
			return T21_StructResult_VltRange(code     = CODES_COMPLETION.INTERRUPTED,
										     subcodes = {CODES_DATA.ERROR_CHECK})

		dcells       : dict[int, T20_StructCell] = self._d_cells.get(cell.ids, dict())

		if not dcells: result.subcodes.add(CODES_DATA.NO_DATA)

		vlt_min      : int | None                = None
		vlt_max      : int | None                = None

		for dcell in dcells.values():
			if bool(cell.vlt_l) and (dcell.vlt < cell.vlt_l): continue
			if bool(cell.vlt_r) and (dcell.vlt > cell.vlt_r): continue

			if vlt_min is None: vlt_min = dcell.vlt
			if vlt_max is None: vlt_max = dcell.vlt

			vlt_min = min(vlt_min, dcell.vlt)
			vlt_max = max(vlt_max, dcell.vlt)

		result.data.vlt_l = vlt_min
		result.data.vlt_r = vlt_max

		return result

	def ReadVlts(self, cell: T21_VltRange) -> T21_StructResult_List:
		""" Запрос списка VLT """
		result                                   = T21_StructResult_List()

		result_check : bool                      = CheckIdo(cell.ido)
		result_check                            &= CheckIdp(cell.idp)

		if not result_check:
			return T21_StructResult_List(code     = CODES_COMPLETION.INTERRUPTED,
										 subcodes = {CODES_DATA.ERROR_CHECK})

		dcells       : dict[int, T20_StructCell] = self._d_cells.get(cell.ids, dict())

		for dcell in dcells.values():
			if bool(cell.vlt_l) and (dcell.vlt < cell.vlt_l): continue
			if bool(cell.vlt_r) and (dcell.vlt > cell.vlt_r): continue

			result.data.append(dcell.vlt)

		match len(result.data):
			case 0: result.subcodes.add(CODES_DATA.NO_DATA)
			case 1: result.subcodes.add(CODES_DATA.SINGLE)

		return result

	# Логика управления
	pass
