# КАКТУС: КОНТЕЙНЕР-RAM
# 09 июн 2024

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
	def DeleteSCell(self, cell: T20_StructCell) -> T21_StructResult_StructCell:
		""" Удаление S-Ячейки """
		if not ValidateOci(cell.oci) : return T21_StructResult_StructCell(code     = CODES_COMPLETION.INTERRUPTED,
		                                                                  subcodes = [CODES_DATA.ERROR_CHECK],
		                                                                  data     = cell)

		if not ValidateOid(cell.oid) : return T21_StructResult_StructCell(code     = CODES_COMPLETION.INTERRUPTED,
		                                                                  subcodes = [CODES_DATA.ERROR_CHECK],
		                                                                  data     = cell)

		if not ValidatePid(cell.pid) : return T21_StructResult_StructCell(code     = CODES_COMPLETION.INTERRUPTED,
		                                                                  subcodes = [CODES_DATA.ERROR_CHECK],
		                                                                  data     = cell)

		try                          : del self._s_cells[cell.sid]
		except                       : return T21_StructResult_StructCell(code     = CODES_COMPLETION.COMPLETED,
		                                                                  subcodes = [CODES_DATA.NO_DATA],
		                                                                  data     = cell)

		T21_StructResult_StructCell(code = CODES_COMPLETION.COMPLETED,
		                            data = cell)

	def ReadSCell(self, cell: T20_StructCell) -> T21_StructResult_StructCell:
		""" Запрос S-Ячейки """
		if not ValidateOci(cell.oci) : return T21_StructResult_StructCell(code     = CODES_COMPLETION.INTERRUPTED,
		                                                                  subcodes = [CODES_DATA.ERROR_CHECK],
		                                                                  data     = cell)

		if not ValidateOid(cell.oid) : return T21_StructResult_StructCell(code     = CODES_COMPLETION.INTERRUPTED,
		                                                                  subcodes = [CODES_DATA.ERROR_CHECK],
		                                                                  data     = cell)

		if not ValidatePid(cell.pid) : return T21_StructResult_StructCell(code     = CODES_COMPLETION.INTERRUPTED,
		                                                                  subcodes = [CODES_DATA.ERROR_CHECK],
		                                                                  data     = cell)

		cell_from_container: None | T20_StructCell = self._s_cells.get(cell.sid, None)

		if cell_from_container is None: return T21_StructResult_StructCell(code    = CODES_COMPLETION.COMPLETED,
		                                                                   subcodes = [CODES_DATA.NO_DATA],
		                                                                   data     = cell)

		T21_StructResult_StructCell(code = CODES_COMPLETION.COMPLETED,
		                            data = cell_from_container)

	def SyncSCell(self, cell: T20_StructCell) -> T21_StructResult_StructCell:
		""" Синхронизация S-Ячейки """
		if not ValidateOci(cell.oci) : return T21_StructResult_StructCell(code     = CODES_COMPLETION.INTERRUPTED,
		                                                                  subcodes = [CODES_DATA.ERROR_CHECK],
		                                                                  data     = cell)

		if not ValidateOid(cell.oid) : return T21_StructResult_StructCell(code     = CODES_COMPLETION.INTERRUPTED,
		                                                                  subcodes = [CODES_DATA.ERROR_CHECK],
		                                                                  data     = cell)

		if not ValidatePid(cell.pid) : return T21_StructResult_StructCell(code     = CODES_COMPLETION.INTERRUPTED,
		                                                                  subcodes = [CODES_DATA.ERROR_CHECK],
		                                                                  data     = cell)

		cell_from_container: None | T20_StructCell = self._s_cells.get(cell.sid, None)

		if cell_from_container is None          : return self.WriteSCell(cell)

		if   cell_from_container.cut  > cell.cut: return T21_StructResult_StructCell(code = CODES_COMPLETION.COMPLETED,
		                                                                             data = cell_from_container)

		elif cell_from_container.cut == cell.cut: return T21_StructResult_StructCell(code = CODES_COMPLETION.COMPLETED,
		                                                                             data = cell)

		return self.WriteSCell(cell)

	def WriteSCell(self, cell: T20_StructCell, flag_mode_ignore: bool = False) -> T21_StructResult_StructCell:
		""" Запись S-Ячейки """
		if not ValidateOci(cell.oci) : return T21_StructResult_StructCell(code     = CODES_COMPLETION.INTERRUPTED,
		                                                                  subcodes = [CODES_DATA.ERROR_CHECK],
		                                                                  data     = cell)

		if not ValidateOid(cell.oid) : return T21_StructResult_StructCell(code     = CODES_COMPLETION.INTERRUPTED,
		                                                                  subcodes = [CODES_DATA.ERROR_CHECK],
		                                                                  data     = cell)

		if not ValidatePid(cell.pid) : return T21_StructResult_StructCell(code     = CODES_COMPLETION.INTERRUPTED,
		                                                                  subcodes = [CODES_DATA.ERROR_CHECK],
		                                                                  data     = cell)

		cell_exist : bool = cell.sid in self._s_cells

		if cell_exist and flag_mode_ignore: return T21_StructResult_StructCell(code = CODES_COMPLETION.COMPLETED,
		                                                                       data = self._s_cells.get(cell.sid, T20_StructCell()))

		self._s_cells[cell.sid] = cell
		return T21_StructResult_StructCell(code = CODES_COMPLETION.COMPLETED,
		                                   data = cell)

	# УПРАВЛЕНИЕ ПАКЕТОМ S-ЯЧЕЕК
	def DeleteSCells(self, cell_cells: T20_StructCell | list[T20_StructCell]) -> T21_StructResult_StructCells:
		""" Удаление пакета S-Ячеек """
		result_cells : list[T20_StructCell] = []
		sids         : list[str]            = []

		if type(cell_cells) is T20_StructCell:
			for cell in self._s_cells.values():
				if cell_cells.oci and not cell_cells.oci == cell.oci: continue
				if cell_cells.oid and not cell_cells.oid == cell.oid: continue
				if cell_cells.pid and not cell_cells.pid == cell.pid: continue
				if cell_cells.cvl and not cell_cells.cvl == cell.cvl: continue
				if cell_cells.cut and not cell_cells.cut == cell.cut: continue

				sids.append(cell.sid)

		elif type(cell_cells) is list:
			for cell in cell_cells:
				if not ValidateOci(cell.oci): continue
				if not ValidateOid(cell.oid): continue
				if not ValidatePid(cell.pid): continue

				sids.append(cell.sid)

		for sid in sids:
			try   :
				cell = self._s_cells[sid]
				del self._s_cells[sid]
				result_cells.append(cell)
			except: continue

		if not result_cells: return T21_StructResult_StructCells(code     = CODES_COMPLETION.COMPLETED,
		                                                         subcodes = [CODES_DATA.NO_DATA])

		return T21_StructResult_StructCells(code = CODES_COMPLETION.COMPLETED,
		                                    data = result_cells)

	def ReadSCells(self, cell_cells: T20_StructCell | list[T20_StructCell]) -> T21_StructResult_StructCells:
		""" Запрос пакета S-Ячеек """
		result_cells : list[T20_StructCell] = []
		sids         : list[str]            = []

		if type(cell_cells) is T20_StructCell:
			for cell in self._s_cells.values():
				if cell_cells.oci and not cell_cells.oci == cell.oci: continue
				if cell_cells.oid and not cell_cells.oid == cell.oid: continue
				if cell_cells.pid and not cell_cells.pid == cell.pid: continue
				if cell_cells.cvl and not cell_cells.cvl == cell.cvl: continue
				if cell_cells.cut and not cell_cells.cut == cell.cut: continue

				sids.append(cell.sid)

		elif type(cell_cells) is list:
			for cell in cell_cells:
				if not ValidateOci(cell.oci): continue
				if not ValidateOid(cell.oid): continue
				if not ValidatePid(cell.pid): continue

				sids.append(cell.sid)

		for sid in sids:
			try   :	result_cells.append(self._s_cells[sid])
			except: continue

		if not result_cells: return T21_StructResult_StructCells(code     = CODES_COMPLETION.COMPLETED,
		                                                         subcodes = [CODES_DATA.NO_DATA])

		return T21_StructResult_StructCells(code = CODES_COMPLETION.COMPLETED,
		                                    data = result_cells)

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
	def DeleteDCells(self, cell_cells: T21_StructRange | list[T20_StructCell]) -> T21_StructResult_StructCells:
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

	def ReadDCells(self, cell: T21_StructRange) -> T21_StructResult_StructCells:
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
	def DCutRange(self, cell: T21_StructRange) -> T21_StructResult_StructRange:
		""" Запрос границ cUT D-Ячейки """
		result_cuts         = self.DCuts(cell)
		cuts    : list[int] = result_cuts.data

		if not cuts: return T21_StructResult_StructRange(code     = CODES_COMPLETION.COMPLETED,
		                                                 subcodes = [CODES_DATA.NO_DATA])

		min_cut : int       = min(cuts)
		max_cut : int       = max(cuts)

		result              = T21_StructRange(oci   = cell.oci,
		                                      oid   = cell.oid,
		                                      pid   = cell.pid,
		                                      cut_l = min_cut,
		                                      cut_r = max_cut)

		return T21_StructResult_StructRange(code = CODES_COMPLETION.COMPLETED,
		                                    data = result)

	def DCuts(self, cell: T21_StructRange) -> T21_StructResult_List:
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
