# КАКТУС: КОНТЕЙНЕР-RAM
# 2022-12-01

from G00_cactus_codes      import CONTAINER_RAM
from G00_result_codes      import *
from G10_cactus_validators import ValidateOci, \
								  ValidateOid, \
								  ValidatePid
from G30_cactus_container  import C30_Container
from G30_cactus_struct     import T30_StructCell
from G31_cactus_struct     import T31_ResultStructCell,  \
								  T31_ResultStructCells, \
								  T31_StructRange,       \
								  T31_ResultStructRange, \
								  T31_ResultList


class C31_ContainerRAM(C30_Container):
	""" Кактус: Контейнер RAM """

	# СЛУЖЕБНЫЕ МЕТОДЫ
	def Init_00(self):
		super().Init_00()

		self._s_cells : dict[str, T30_StructCell]            = dict()
		self._d_cells : dict[str, dict[int, T30_StructCell]] = dict()

	def Init_01(self):
		super().Init_01()

		self._container_type = CONTAINER_RAM

	# УПРАВЛЕНИЕ КОНТЕЙНЕРОМ
	def Clear(self):
		""" Очистка контейнера """
		self._s_cells.clear()
		self._d_cells.clear()

	# УПРАВЛЕНИЕ S-ЯЧЕЙКОЙ
	def DeleteSCell(self, cell: T30_StructCell) -> T31_ResultStructCell:
		""" Удаление S-Ячейки """
		if not ValidateOci(cell.oci) : return T31_ResultStructCell(RESULT_ERROR_CHECK_VALIDATE)
		if not ValidateOid(cell.oid) : return T31_ResultStructCell(RESULT_ERROR_CHECK_VALIDATE)
		if not ValidatePid(cell.pid) : return T31_ResultStructCell(RESULT_ERROR_CHECK_VALIDATE)

		try                          : del self._s_cells[cell.sid]
		except                       : return T31_ResultStructCell(RESULT_WARNING_NO_DATA, cell)

		return T31_ResultStructCell(RESULT_OK, cell)

	def ReadSCell(self, cell: T30_StructCell) -> T31_ResultStructCell:
		""" Запрос S-Ячейки """
		if not ValidateOci(cell.oci)  : return T31_ResultStructCell(RESULT_ERROR_CHECK_VALIDATE)
		if not ValidateOid(cell.oid)  : return T31_ResultStructCell(RESULT_ERROR_CHECK_VALIDATE)
		if not ValidatePid(cell.pid)  : return T31_ResultStructCell(RESULT_ERROR_CHECK_VALIDATE)

		cell_from_container: None | T30_StructCell = self._s_cells.get(cell.sid, None)

		if cell_from_container is None: return T31_ResultStructCell(RESULT_WARNING_NO_DATA, cell)

		return T31_ResultStructCell(RESULT_OK, cell_from_container)

	def SyncSCell(self, cell: T30_StructCell) -> T31_ResultStructCell:
		""" Синхронизация S-Ячейки """
		if not ValidateOci(cell.oci)            : return T31_ResultStructCell(RESULT_ERROR_CHECK_VALIDATE)
		if not ValidateOid(cell.oid)            : return T31_ResultStructCell(RESULT_ERROR_CHECK_VALIDATE)
		if not ValidatePid(cell.pid)            : return T31_ResultStructCell(RESULT_ERROR_CHECK_VALIDATE)

		cell_from_container: None | T30_StructCell = self._s_cells.get(cell.sid, None)

		if cell_from_container is None          : return self.WriteSCell(cell)

		if   cell_from_container.cut  > cell.cut: return T31_ResultStructCell(RESULT_OK, cell_from_container)
		elif cell_from_container.cut == cell.cut: return T31_ResultStructCell(RESULT_OK, cell)

		return self.WriteSCell(cell)

	def WriteSCell(self, cell: T30_StructCell, flag_mode_ignore: bool = False) -> T31_ResultStructCell:
		""" Запись S-Ячейки """
		if not ValidateOci(cell.oci)      : return T31_ResultStructCell(RESULT_ERROR_CHECK_VALIDATE)
		if not ValidateOid(cell.oid)      : return T31_ResultStructCell(RESULT_ERROR_CHECK_VALIDATE)
		if not ValidatePid(cell.pid)      : return T31_ResultStructCell(RESULT_ERROR_CHECK_VALIDATE)

		cell_exist : bool = cell.sid in self._s_cells

		if cell_exist and flag_mode_ignore: return T31_ResultStructCell(RESULT_OK, self._s_cells.get(cell.sid, T30_StructCell()))

		self._s_cells[cell.sid] = cell
		return T31_ResultStructCell(RESULT_OK, cell)

	# УПРАВЛЕНИЕ ПАКЕТОМ S-ЯЧЕЕК
	def DeleteSCells(self, cell_cells: T30_StructCell | list[T30_StructCell]) -> T31_ResultStructCells:
		""" Удаление пакета S-Ячеек """
		result_cells : list[T30_StructCell] = []
		sids         : list[str]            = []

		if type(cell_cells) is T30_StructCell:
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

		if not result_cells: return T31_ResultStructCells(RESULT_WARNING_NO_DATA)

		return T31_ResultStructCells(RESULT_OK, result_cells)

	def ReadSCells(self, cell_cells: T30_StructCell | list[T30_StructCell]) -> T31_ResultStructCells:
		""" Запрос пакета S-Ячеек """
		result_cells : list[T30_StructCell] = []
		sids         : list[str]            = []

		if type(cell_cells) is T30_StructCell:
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

		if not result_cells: return T31_ResultStructCells(RESULT_WARNING_NO_DATA)

		return T31_ResultStructCells(RESULT_OK, result_cells)

	def SyncSCells(self, cells: list[T30_StructCell]) -> T31_ResultStructCells:
		""" Синхронизация S-Ячеек """
		result_cells : list[T30_StructCell] = []
		result_code  : int                  = RESULT_OK

		for cell in cells:
			result_cell = self.SyncSCell(cell)

			if not result_cell.code == RESULT_OK:
				result_code = RESULT_OK_PARTIAL
				continue

			result_cells.append(result_cell.cell)

		if len(result_cells) == 0: return T31_ResultStructCells(RESULT_WARNING_NO_DATA)

		return T31_ResultStructCells(result_code, result_cells)

	def WriteSCells(self, cells: list[T30_StructCell]) -> T31_ResultStructCells:
		""" Запись пакета S-Ячеек """
		result_cells : list[T30_StructCell] = []

		for cell in cells:
			if not ValidateOci(cell.oci): continue
			if not ValidateOid(cell.oid): continue
			if not ValidatePid(cell.pid): continue

			try   : self._s_cells[cell.sid] = cell
			except: continue

			result_cells.append(cell)

		if not result_cells: return T31_ResultStructCells(RESULT_WARNING_NO_DATA)

		return T31_ResultStructCells(RESULT_OK, result_cells)

	# УПРАВЛЕНИЕ D-ЯЧЕЙКОЙ
	def DeleteDCell(self, cell: T30_StructCell) -> T31_ResultStructCell:
		""" Удаление D-Ячейки """
		if not ValidateOci(cell.oci) : return T31_ResultStructCell(RESULT_ERROR_CHECK_VALIDATE)
		if not ValidateOid(cell.oid) : return T31_ResultStructCell(RESULT_ERROR_CHECK_VALIDATE)

		dcells : dict[int, T30_StructCell] = self._d_cells.get(cell.sid, dict())
		try                          : del dcells[cell.cut]
		except                       : return T31_ResultStructCell(RESULT_WARNING_NO_DATA, cell)

		return T31_ResultStructCell(RESULT_OK, cell)

	def ReadDCell(self, cell: T30_StructCell) -> T31_ResultStructCell:
		""" Запрос D-Ячейки """
		if not ValidateOci(cell.oci) : return T31_ResultStructCell(RESULT_ERROR_CHECK_VALIDATE)
		if not ValidateOid(cell.oid) : return T31_ResultStructCell(RESULT_ERROR_CHECK_VALIDATE)
		if not ValidatePid(cell.pid) : return T31_ResultStructCell(RESULT_ERROR_CHECK_VALIDATE)

		dcells : dict[int, T30_StructCell] = self._d_cells.get(cell.sid, dict())
		dcell                              = dcells.get(cell.cut, None)

		if dcell is None             : return T31_ResultStructCell(RESULT_WARNING_NO_DATA, cell)

		return T31_ResultStructCell(RESULT_OK, dcell)

	def WriteDCell(self, cell: T30_StructCell) -> T31_ResultStructCell:
		""" Запись D-Ячейки """
		if not ValidateOci(cell.oci) : return T31_ResultStructCell(RESULT_ERROR_CHECK_VALIDATE)
		if not ValidateOid(cell.oid) : return T31_ResultStructCell(RESULT_ERROR_CHECK_VALIDATE)
		if not ValidatePid(cell.pid) : return T31_ResultStructCell(RESULT_ERROR_CHECK_VALIDATE)

		dcells : dict[int, T30_StructCell] = self._d_cells.get(cell.sid, dict())
		dcells[cell.cut]                   = cell

		self._d_cells[cell.sid] = dcells
		return T31_ResultStructCell(RESULT_OK, cell)

	# УПРАВЛЕНИЕ ПАКЕТОМ D-ЯЧЕЕК
	def DeleteDCells(self, cell_cells: T31_StructRange | list[T30_StructCell]) -> T31_ResultStructCells:
		""" Удаление пакета D-Ячеек """
		cells        : list[T30_StructCell] = []
		result_code  : int                  = RESULT_OK
		result_cells : list[T30_StructCell] = []

		if   type(cell_cells) is T30_StructCell: cells = self.ReadDCells(cell_cells).cells
		elif type(cell_cells) is list          : cells = cell_cells

		for cell in cells:
			if not ValidateOci(cell.oci): continue
			if not ValidateOid(cell.oid): continue
			if not ValidatePid(cell.pid): continue

			result = self.DeleteDCell(cell)

			if not result.code == RESULT_OK:
				result_code = RESULT_OK_PARTIAL
				continue

			result_cells.append(result.cell)

		return T31_ResultStructCells(result_code, result_cells)

	def ReadDCells(self, cell: T31_StructRange) -> T31_ResultStructCells:
		""" Запрос пакета D-Ячеек """
		result : list[T30_StructCell] = []

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

		if not result: return T31_ResultStructCells(RESULT_WARNING_NO_DATA)

		return T31_ResultStructCells(RESULT_OK, result)

	def WriteDCells(self, cells: list[T30_StructCell]) -> T31_ResultStructCells:
		""" Запись пакета D-Ячеек """
		result_code  : int                  = RESULT_OK
		result_cells : list[T30_StructCell] = []

		for cell in cells:
			result = self.WriteDCell(cell)

			if not result.code == RESULT_OK:
				result_code = RESULT_OK_PARTIAL
				continue

			result_cells.append(result.cell)

		return T31_ResultStructCells(result_code, result_cells)

	# ЗАПРОСЫ D-ДАННЫХ
	def DCutRange(self, cell: T31_StructRange) -> T31_ResultStructRange:
		""" Запрос границ cUT D-Ячейки """
		result_cuts         = self.DCuts(cell)
		cuts    : list[int] = result_cuts.items

		if not cuts: return T31_ResultStructRange(RESULT_WARNING_NO_DATA)

		min_cut : int       = min(cuts)
		max_cut : int       = max(cuts)

		return T31_ResultStructRange(RESULT_OK, T31_StructRange(oci=cell.oci, oid=cell.oid, pid=cell.pid, cut_l=min_cut, cut_r=max_cut))

	def DCuts(self, cell: T31_StructRange) -> T31_ResultList:
		""" Запрос списка CUT """
		if not ValidateOci(cell.oci) : return T31_ResultList(RESULT_ERROR_CHECK_VALIDATE)
		if not ValidateOid(cell.oid) : return T31_ResultList(RESULT_ERROR_CHECK_VALIDATE)
		if not ValidatePid(cell.pid) : return T31_ResultList(RESULT_ERROR_CHECK_VALIDATE)

		dcells : dict[int, T30_StructCell] = self._d_cells.get(cell.sid, dict())

		if not dcells                : return T31_ResultList(RESULT_WARNING_NO_DATA)

		result : set[int] = set()

		for cut in dcells.keys():
			if (not cell.cut_l == 0) and cut < cell.cut_l: continue
			if (not cell.cut_r == 0) and cut > cell.cut_r: continue

			result.add(cut)

		return T31_ResultList(RESULT_OK, list(result))
