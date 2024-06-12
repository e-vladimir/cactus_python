# КАКТУС: КОНТЕЙНЕР-RAM
# 12 июн 2024

from G00_cactus_codes      import CONTAINERS
from G00_status_codes      import *

from G10_cactus_validators import *
from G21_cactus_struct     import *
from G21_struct_result     import T21_StructResult_List
from G30_cactus_container  import C30_Container
from G20_cactus_struct     import T20_StructCell


class C31_ContainerRAM(C30_Container):
	""" Кактус: Контейнер RAM """

	# СЛУЖЕБНЫЕ МЕТОДЫ
	def Init_00(self):
		super().Init_00()

		self._s_cells : dict[str, T20_StructCell]            = dict()
		self._d_cells : dict[str, dict[int, T20_StructCell]] = dict()

	def Init_01(self):
		super().Init_01()

		self._container_type = CONTAINERS.CONTAINER_RAM

	# УПРАВЛЕНИЕ КОНТЕЙНЕРОМ
	def Clear(self):
		""" Очистка контейнера """
		self._s_cells.clear()
		self._d_cells.clear()

	# УПРАВЛЕНИЕ S-ЯЧЕЙКОЙ
	def DeleteSCell(self, cell: T20_StructCell, flag_capture_data: bool = False) -> T21_StructResult_StructCell:
		""" Удаление S-Ячейки """
		struct_result      = T21_StructResult_StructCell()
		struct_result.code = CODES_COMPLETION.INTERRUPTED
		struct_result.subcodes.add(CODES_DATA.ERROR_CHECK)

		if not ValidateOci(cell.oci) : return struct_result
		if not ValidateOid(cell.oid) : return struct_result
		if not ValidatePid(cell.pid) : return struct_result

		struct_result.code = CODES_COMPLETION.COMPLETED
		struct_result.subcodes.clear()

		try    : del self._s_cells[cell.sid]
		except : struct_result.subcodes.add(CODES_DATA.NO_DATA)

		if flag_capture_data: struct_result.data = cell

		return struct_result

	def ReadSCell(self, cell: T20_StructCell, flag_capture_data: bool = False) -> T21_StructResult_StructCell:
		""" Запрос S-Ячейки """
		struct_result                            = T21_StructResult_StructCell()
		struct_result.code                       = CODES_COMPLETION.INTERRUPTED
		struct_result.subcodes.add(CODES_DATA.ERROR_CHECK)
		struct_result.data                       = cell

		if not ValidateOci(cell.oci) : return struct_result
		if not ValidateOid(cell.oid) : return struct_result
		if not ValidatePid(cell.pid) : return struct_result

		struct_result.code                       = CODES_COMPLETION.COMPLETED
		struct_result.subcodes.clear()

		cell_in_container: None | T20_StructCell = self._s_cells.get(cell.sid, None)

		if cell_in_container is None: struct_result.subcodes.add(CODES_DATA.NO_DATA)
		else                        : struct_result.data = cell_in_container

		return struct_result

	def WriteSCell(self, cell: T20_StructCell, flag_mode_ignore: bool = False, flag_capture_data: bool = False) -> T21_StructResult_StructCell:
		""" Запись S-Ячейки """
		struct_result      = T21_StructResult_StructCell()
		struct_result.code = CODES_COMPLETION.INTERRUPTED
		struct_result.subcodes.add(CODES_DATA.ERROR_CHECK)

		if not ValidateOci(cell.oci) : return struct_result
		if not ValidateOid(cell.oid) : return struct_result
		if not ValidatePid(cell.pid) : return struct_result

		struct_result.code = CODES_COMPLETION.COMPLETED
		struct_result.subcodes.clear()

		if   not flag_mode_ignore         : self._s_cells[cell.sid] = cell
		elif     cell.sid in self._s_cells: struct_result.subcodes.add(CODES_PROCESSING.SKIP)

		if   flag_capture_data            : struct_result.data = self._s_cells[cell.sid]

		return struct_result

	# УПРАВЛЕНИЕ ПАКЕТОМ S-ЯЧЕЕК
	def DeleteSCells(self, cell_cells: T20_StructCell | list[T20_StructCell], flag_capture_data: bool = False) -> T21_StructResult_StructCells:
		""" Удаление пакета S-Ячеек """
		struct_result = T21_StructResult_StructCells()

		if type(cell_cells) is T20_StructCell: cell_cells = [cell_cells]

		for cell in cell_cells:
			if cell.sid not in self._s_cells:
				struct_result.subcodes.add(CODES_PROCESSING.PARTIAL)
				continue

			del self._s_cells[cell.sid]

		if not flag_capture_data: return struct_result

		result        = []
		for cell in cell_cells:
			if cell.sid in self._s_cells: continue

			result.append(cell)

		if not result           : struct_result.subcodes.add(CODES_DATA.NO_DATA)

		struct_result.data = result[:]

		return struct_result

	def ReadSCells(self, cell_cells: T20_StructCell | list[T20_StructCell], flag_capture_data: bool = False) -> T21_StructResult_StructCells:
		""" Запрос пакета S-Ячеек """
		pass

	def SyncSCells(self, cells: list[T20_StructCell]) -> T21_StructResult_StructCells:
		""" Синхронизация S-Ячеек """
		result_cells : list[T20_StructCell] = []
		subcodes     : set[CODES]     = set()

		for cell in cells:
			result_cell = self.SyncSCell(cell)

			if not result_cell.code == CODES_COMPLETION.COMPLETED:
				subcodes.add(CODES_PROCESSING.SKIP)
				continue

			result_cells.append(result_cell.data)

		if len(result_cells) == 0: subcodes.add(CODES_DATA.NO_DATA)

		return T21_StructResult_StructCells(code     = CODES_COMPLETION.COMPLETED,
		                                    subcodes = list(subcodes),
		                                    data     = result_cells)

	def WriteSCells(self, cells: list[T20_StructCell]) -> T21_StructResult_StructCells:
		""" Запись пакета S-Ячеек """
		result_cells : list[T20_StructCell] = []
		subcodes     : set[CODES]     = set()

		for cell in cells:
			if not ValidateOci(cell.oci):
				subcodes.add(CODES_DATA.ERROR_CHECK)
				subcodes.add(CODES_PROCESSING.SKIP)
				continue

			if not ValidateOid(cell.oid):
				subcodes.add(CODES_DATA.ERROR_CHECK)
				subcodes.add(CODES_PROCESSING.SKIP)
				continue

			if not ValidatePid(cell.pid):
				subcodes.add(CODES_DATA.ERROR_CHECK)
				subcodes.add(CODES_PROCESSING.SKIP)
				continue

			try   :
				self._s_cells[cell.sid] = cell

			except:
				subcodes.add(CODES_PROCESSING.SKIP)

			result_cells.append(cell)

		if not result_cells: subcodes.add(CODES_DATA.NO_DATA)

		return T21_StructResult_StructCells(code     = CODES_COMPLETION.COMPLETED,
		                                    subcodes = list(subcodes),
		                                    data     = result_cells)

	# УПРАВЛЕНИЕ D-ЯЧЕЙКОЙ
	def DeleteDCell(self, cell: T20_StructCell) -> T21_StructResult_StructCell:
		""" Удаление D-Ячейки """
		if not ValidateOci(cell.oci) : return T21_StructResult_StructCell(code     = CODES_COMPLETION.INTERRUPTED,
		                                                                  subcodes = [CODES_DATA.ERROR_CHECK],
		                                                                  data     = cell)

		if not ValidateOid(cell.oid) : return T21_StructResult_StructCell(code     = CODES_COMPLETION.INTERRUPTED,
		                                                                  subcodes = [CODES_DATA.ERROR_CHECK],
		                                                                  data     = cell)

		dcells : dict[int, T20_StructCell] = self._d_cells.get(cell.sid, dict())
		try                          : del dcells[cell.cut]
		except                       : return T21_StructResult_StructCell(code     = CODES_COMPLETION.COMPLETED,
		                                                                  subcodes = [CODES_DATA.NO_DATA],
		                                                                  data     = cell)

		return T21_StructResult_StructCell(code = CODES_COMPLETION.COMPLETED,
		                                   data = cell)

	def ReadDCell(self, cell: T20_StructCell) -> T21_StructResult_StructCell:
		""" Запрос D-Ячейки """
		if not ValidateOci(cell.oci) : return T21_StructResult_StructCell(code     = CODES_COMPLETION.INTERRUPTED,
		                                                                  subcodes = [CODES_DATA.ERROR_CHECK],
		                                                                  data     = cell)

		if not ValidateOid(cell.oid) : return T21_StructResult_StructCell(code     = CODES_COMPLETION.INTERRUPTED,
		                                                                  subcodes = [CODES_DATA.ERROR_CHECK],
		                                                                  data     = cell)

		if not ValidatePid(cell.pid) : return T21_StructResult_StructCell(code     = CODES_COMPLETION.INTERRUPTED,
		                                                                  subcodes = [CODES_DATA.ERROR_CHECK],
		                                                                  data     = cell)

		dcells : dict[int, T20_StructCell] = self._d_cells.get(cell.sid, dict())
		dcell                              = dcells.get(cell.cut, None)

		if dcell is None             : return T21_StructResult_StructCell(code     = CODES_COMPLETION.COMPLETED,
		                                                                  subcodes = [CODES_DATA.NO_DATA],
		                                                                  data     = cell)

		return T21_StructResult_StructCell(code = CODES_COMPLETION.COMPLETED,
		                                   data = dcell)

	def WriteDCell(self, cell: T20_StructCell) -> T21_StructResult_StructCell:
		""" Запись D-Ячейки """
		if not ValidateOci(cell.oci) : return T21_StructResult_StructCell(code     = CODES_COMPLETION.INTERRUPTED,
		                                                                  subcodes = [CODES_DATA.ERROR_CHECK],
		                                                                  data     = cell)

		if not ValidateOid(cell.oid) : return T21_StructResult_StructCell(code     = CODES_COMPLETION.INTERRUPTED,
		                                                                  subcodes = [CODES_DATA.ERROR_CHECK],
		                                                                  data     = cell)

		if not ValidatePid(cell.pid) : return T21_StructResult_StructCell(code     = CODES_COMPLETION.INTERRUPTED,
		                                                                  subcodes = [CODES_DATA.ERROR_CHECK],
		                                                                  data     = cell)

		dcells : dict[int, T20_StructCell] = self._d_cells.get(cell.sid, dict())
		dcells[cell.cut]                   = cell

		self._d_cells[cell.sid] = dcells
		return T21_StructResult_StructCell(code = CODES_COMPLETION.COMPLETED,
		                                   data = cell)

	# УПРАВЛЕНИЕ ПАКЕТОМ D-ЯЧЕЕК
	def DeleteDCells(self, cell_cells: T21_CutRange | list[T20_StructCell]) -> T21_StructResult_StructCells:
		""" Удаление пакета D-Ячеек """
		cells        : list[T20_StructCell] = []
		result_cells : list[T20_StructCell] = []
		subcodes     : set[CODES]     = set()

		if   type(cell_cells) is T20_StructCell: cells = self.ReadDCells(cell_cells).data
		elif type(cell_cells) is list          : cells = cell_cells

		for cell in cells:
			if not ValidateOci(cell.oci):
				subcodes.add(CODES_DATA.ERROR_CHECK)
				subcodes.add(CODES_PROCESSING.SKIP)
				continue

			if not ValidateOid(cell.oid):
				subcodes.add(CODES_DATA.ERROR_CHECK)
				subcodes.add(CODES_PROCESSING.SKIP)
				continue

			if not ValidatePid(cell.pid):
				subcodes.add(CODES_DATA.ERROR_CHECK)
				subcodes.add(CODES_PROCESSING.SKIP)
				continue

			result = self.DeleteDCell(cell)

			if not result.code == CODES_COMPLETION.COMPLETED:
				subcodes.add(CODES_PROCESSING.SKIP)
				continue

			result_cells.append(result.data)

		if not result_cells: subcodes.add(CODES_DATA.NO_DATA)

		return T21_StructResult_StructCells(code     = CODES_COMPLETION.COMPLETED,
		                                    subcodes = list(subcodes),
		                                    data     = result_cells)

	def ReadDCells(self, cell: T21_CutRange) -> T21_StructResult_StructCells:
		""" Запрос пакета D-Ячеек """
		result : list[T20_StructCell] = []

		for dcells in self._d_cells.values():
			for dcell in dcells.values():
				if cell.oci   and not dcell.oci == cell.oci  : continue
				if cell.oid   and not dcell.oid == cell.oid  : continue
				if cell.pid   and not dcell.pid == cell.pid  : continue
				if cell.cvl   and not dcell.cvl == cell.cvl  : continue
				if cell.cut   and not dcell.cut == cell.cut  : continue
				if cell.cut_l and not dcell.cut >= cell.cut_l: continue
				if cell.cut_r and not dcell.cut <= cell.cut_r: continue

				result.append(dcell)

		if not result: return T21_StructResult_StructCells(code     = CODES_COMPLETION.COMPLETED,
		                                                   subcodes = [CODES_DATA.NO_DATA])

		return T21_StructResult_StructCells(code = CODES_COMPLETION.COMPLETED,
		                                    data = result)

	def WriteDCells(self, cells: list[T20_StructCell]) -> T21_StructResult_StructCells:
		""" Запись пакета D-Ячеек """
		subcodes     : set[CODES]           = set()
		result_cells : list[T20_StructCell] = []

		for cell in cells:
			result = self.WriteDCell(cell)

			if not result.code == CODES_COMPLETION.COMPLETED:
				subcodes = subcodes.union(result.subcodes)
				continue

			result_cells.append(result.data)

		return T21_StructResult_StructCells(code     = CODES_COMPLETION.COMPLETED,
		                                    subcodes = list(subcodes),
		                                    data     = result_cells)

	# ЗАПРОСЫ D-ДАННЫХ
	def DCutRange(self, cell: T21_CutRange) -> T21_StructResult_CutRange:
		""" Запрос границ cUT D-Ячейки """
		result_cuts         = self.DCuts(cell)
		cuts    : list[int] = result_cuts.data

		if not cuts: return T21_StructResult_CutRange(code     = CODES_COMPLETION.COMPLETED,
		                                              subcodes = [CODES_DATA.NO_DATA])

		min_cut : int       = min(cuts)
		max_cut : int       = max(cuts)

		result              = T21_CutRange(oci   = cell.oci,
		                                   oid   = cell.oid,
		                                   pid   = cell.pid,
		                                   cut_l = min_cut,
		                                   cut_r = max_cut)

		return T21_StructResult_CutRange(code = CODES_COMPLETION.COMPLETED,
		                                 data = result)

	def DCuts(self, cell: T21_CutRange) -> T21_StructResult_List:
		""" Запрос списка CUT """
		if not ValidateOci(cell.oci) : return T21_StructResult_List(code     = CODES_COMPLETION.INTERRUPTED,
		                                                            subcodes = [CODES_DATA.ERROR_CHECK])

		if not ValidateOid(cell.oid) : return T21_StructResult_List(code     = CODES_COMPLETION.INTERRUPTED,
		                                                            subcodes = [CODES_DATA.ERROR_CHECK])

		if not ValidatePid(cell.pid) : return T21_StructResult_List(code     = CODES_COMPLETION.INTERRUPTED,
		                                                            subcodes = [CODES_DATA.ERROR_CHECK])

		dcells : dict[int, T20_StructCell] = self._d_cells.get(cell.sid, dict())

		if not dcells                : return T21_StructResult_List(code     = CODES_COMPLETION.COMPLETED,
		                                                            subcodes = [CODES_DATA.NO_DATA])

		result : set[int] = set()

		for cut in dcells.keys():
			if (not cell.cut_l == 0) and cut < cell.cut_l: continue
			if (not cell.cut_r == 0) and cut > cell.cut_r: continue

			result.add(cut)

		return T21_StructResult_List(code = CODES_COMPLETION.COMPLETED,
		                             data = list(result))
