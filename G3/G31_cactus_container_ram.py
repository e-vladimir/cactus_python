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

		if cell.sid not in self._s_cells:
			struct_result.subcodes.add(CODES_PROCESSING.SKIP)
			return struct_result

		del self._s_cells[cell.sid]

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
	def DeleteSCells(self, cells: list[T20_StructCell], flag_capture_data: bool = False) -> T21_StructResult_StructCells:
		""" Удаление пакета S-Ячеек """
		struct_result = T21_StructResult_StructCells()

		for cell in cells:
			if not ValidateOci(cell.oci):
				struct_result.subcodes.add(CODES_DATA.ERROR_CHECK)
				continue

			if not ValidateOid(cell.oid):
				struct_result.subcodes.add(CODES_DATA.ERROR_CHECK)
				continue

			if not ValidatePid(cell.pid):
				struct_result.subcodes.add(CODES_DATA.ERROR_CHECK)
				continue

			if cell.sid not in self._s_cells:
				struct_result.subcodes.add(CODES_PROCESSING.PARTIAL)
				continue

			del self._s_cells[cell.sid]

		if not flag_capture_data: return struct_result

		result        = []
		for cell in cells:
			if cell.sid in self._s_cells:
				struct_result.subcodes.add(CODES_PROCESSING.PARTIAL)
				continue

			result.append(cell)

		if not result           : struct_result.subcodes.add(CODES_DATA.NO_DATA)

		struct_result.data = result[:]

		return struct_result

	def ReadSCells(self, cells: list[T20_StructCell], flag_capture_data: bool = False) -> T21_StructResult_StructCells:
		""" Запрос пакета S-Ячеек """
		struct_result = T21_StructResult_StructCells()
		result        = []

		for cell in cells:
			if cell.sid not in self._s_cells:
				struct_result.subcodes.add(CODES_PROCESSING.PARTIAL)
				continue

			result.append(self._s_cells[cell.sid])

		if not result : struct_result.subcodes.add(CODES_DATA.NO_DATA)

		struct_result.data = result[:]

		return struct_result

	def SyncSCells(self, cells: list[T20_StructCell], flag_capture_data: bool = False) -> T21_StructResult_StructCells:
		""" Синхронизация S-Ячеек """
		struct_result = T21_StructResult_StructCells()

		for cell in cells:
			if not ValidateOci(cell.oci):
				struct_result.subcodes.add(CODES_DATA.ERROR_CHECK)
				continue

			if not ValidateOid(cell.oid):
				struct_result.subcodes.add(CODES_DATA.ERROR_CHECK)
				continue

			if not ValidatePid(cell.pid):
				struct_result.subcodes.add(CODES_DATA.ERROR_CHECK)
				continue

			cell_in_container = self._s_cells.get(cell.sid, T20_StructCell)

			if cell_in_container.cut > cell.cut: continue

			self._s_cells[cell.sid] = cell

		if not flag_capture_data: return struct_result

		result        = []
		for cell in cells:
			if cell.sid not in self._s_cells: continue

			result.append(self._s_cells[cell.sid])

		if not result: struct_result.subcodes.add(CODES_DATA.NO_DATA)

		struct_result.data = result[:]

		return struct_result

	def WriteSCells(self, cells: list[T20_StructCell], flag_capture_data: bool = False) -> T21_StructResult_StructCells:
		""" Запись пакета S-Ячеек """
		struct_result = T21_StructResult_StructCells()

		for cell in cells:
			if not ValidateOci(cell.oci):
				struct_result.subcodes.add(CODES_PROCESSING.PARTIAL)
				struct_result.subcodes.add(CODES_DATA.ERROR_CHECK)
				continue

			if not ValidateOid(cell.oid):
				struct_result.subcodes.add(CODES_PROCESSING.PARTIAL)
				struct_result.subcodes.add(CODES_DATA.ERROR_CHECK)
				continue

			if not ValidatePid(cell.pid):
				struct_result.subcodes.add(CODES_PROCESSING.PARTIAL)
				struct_result.subcodes.add(CODES_DATA.ERROR_CHECK)
				continue

			self._s_cells[cell.sid] = cell

		if not flag_capture_data: return struct_result

		result        = []
		for cell in cells:
			if cell.sid not in self._s_cells: continue

			result.append(self._s_cells[cell.sid])

		if not result: struct_result.subcodes.add(CODES_DATA.NO_DATA)

		struct_result.data = result[:]

		return struct_result

	# УПРАВЛЕНИЕ D-ЯЧЕЙКОЙ
	def DeleteDCell(self, cell: T20_StructCell, flag_capture_data: bool = False) -> T21_StructResult_StructCell:
		""" Удаление D-Ячейки """
		struct_result      = T21_StructResult_StructCell()
		struct_result.code = CODES_COMPLETION.INTERRUPTED
		struct_result.subcodes.add(CODES_DATA.ERROR_CHECK)

		if not ValidateOci(cell.oci)              : return struct_result
		if not ValidateOid(cell.oid)              : return struct_result
		if not ValidatePid(cell.pid)              : return struct_result

		struct_result.code = CODES_COMPLETION.COMPLETED
		struct_result.subcodes.add(CODES_PROCESSING.SKIP)
		struct_result.subcodes.clear()

		if cell.sid not in self._d_cells          : return struct_result
		if cell.cut not in self._d_cells[cell.sid]: return struct_result

		del self._d_cells[cell.sid][cell.cut]

		if flag_capture_data: struct_result.data = cell

		return struct_result

	def ReadDCell(self, cell: T20_StructCell, flag_capture_data: bool = False) -> T21_StructResult_StructCell:
		""" Запрос D-Ячейки """
		struct_result      = T21_StructResult_StructCell()
		struct_result.code = CODES_COMPLETION.INTERRUPTED
		struct_result.subcodes.add(CODES_DATA.ERROR_CHECK)

		if not ValidateOci(cell.oci) : return struct_result
		if not ValidateOid(cell.oid) : return struct_result
		if not ValidatePid(cell.pid) : return struct_result

		struct_result.code = CODES_COMPLETION.INTERRUPTED
		struct_result.subcodes.clear()

		if cell.sid not in self._d_cells:
			struct_result.subcodes.add(CODES_DATA.NO_DATA)
			return struct_result

		dcells             = self._d_cells.get(cell.sid, dict())

		if cell.cut not in dcells:
			struct_result.subcodes.add(CODES_DATA.NO_DATA)
			return struct_result

		struct_result.code = CODES_COMPLETION.INTERRUPTED
		struct_result.data = self._d_cells.get(cell.sid, None)

		return struct_result

	def WriteDCell(self, cell: T20_StructCell, flag_capture_data: bool = False) -> T21_StructResult_StructCell:
		""" Запись D-Ячейки """
		struct_result      = T21_StructResult_StructCell()
		struct_result.code = CODES_COMPLETION.INTERRUPTED
		struct_result.subcodes.add(CODES_DATA.ERROR_CHECK)

		if not ValidateOci(cell.oci) : return struct_result
		if not ValidateOid(cell.oid) : return struct_result
		if not ValidatePid(cell.pid) : return struct_result

		struct_result.code = CODES_COMPLETION.INTERRUPTED
		struct_result.subcodes.clear()

		dcells             = self._d_cells.get(cell.sid, dict())
		dcells[cell.cut]   = cell

		self._d_cells[cell.sid] = dcells

		if not flag_capture_data: return struct_result

		struct_result.data = cell

		return struct_result

	# УПРАВЛЕНИЕ ПАКЕТОМ D-ЯЧЕЕК
	def DeleteDCells(self, cutrange_cells: T21_CutRange | list[T20_StructCell], flag_capture_data: bool = False) -> T21_StructResult_StructCells:
		""" Удаление пакета D-Ячеек """
		struct_result    = T21_StructResult_StructCells()
		cells_processing = []

		if   type(cutrange_cells) is list        : cells_processing = cutrange_cells[:]
		elif type(cutrange_cells) is T21_CutRange: cells_processing = self.ReadDCells(cutrange_cells)

		if not cells_processing: struct_result.subcodes.add(CODES_DATA.NO_DATA)

		for cell in cells_processing:
			if not ValidateOci(cell.oci):
				struct_result.subcodes.add(CODES_DATA.ERROR_CHECK)
				struct_result.subcodes.add(CODES_PROCESSING.PARTIAL)
				continue

			if not ValidateOid(cell.oid):
				struct_result.subcodes.add(CODES_DATA.ERROR_CHECK)
				struct_result.subcodes.add(CODES_PROCESSING.PARTIAL)
				continue

			if not ValidatePid(cell.pid):
				struct_result.subcodes.add(CODES_DATA.ERROR_CHECK)
				struct_result.subcodes.add(CODES_PROCESSING.PARTIAL)
				continue

			if cell.sid not in self._d_cells          : continue
			if cell.cut not in self._d_cells[cell.sid]: continue

			del self._d_cells[cell.sid][cell.cut]

		if not flag_capture_data: return struct_result

		result = []

		for cell in cells_processing:
			if cell.sid not in self._d_cells          : continue
			if cell.cut     in self._d_cells[cell.sid]: continue

			result.append(cell)

		struct_result.data = result[:]

		return struct_result

	def ReadDCells(self, cutrange_cells: T21_CutRange | list[T20_StructCell], flag_capture_data: bool = False) -> T21_StructResult_StructCells:
		""" Запрос пакета D-Ячеек """
		struct_result = T21_StructResult_StructCells()
		result        = []

		if type(cutrange_cells)   is T21_CutRange:
			struct_result.code                 = CODES_COMPLETION.INTERRUPTED
			struct_result.subcodes.add(CODES_DATA.ERROR_CHECK)

			if not ValidateOci(cutrange_cells.oci): return struct_result
			if not ValidateOid(cutrange_cells.oid): return struct_result
			if not ValidatePid(cutrange_cells.pid): return struct_result

			struct_result.code                 = CODES_COMPLETION.COMPLETED
			struct_result.subcodes.clear()

			dcells : dict[int, T20_StructCell] = self._d_cells.get(cutrange_cells.sid, dict())

			for cut, dcell in dcells.items():
				if   (cut < cutrange_cells.cut_l)                               : continue
				elif (cut > cutrange_cells.cut_r) and (cutrange_cells.cut_r > 0): continue

				result.append(dcell)

		elif type(cutrange_cells) is list        :
			struct_result.code                 = CODES_COMPLETION.COMPLETED
			struct_result.subcodes.clear()

			dcells : dict[int, T20_StructCell] = self._d_cells.get(cutrange_cells.sid, dict())

			for dcell in cutrange_cells:
				if dcell.cut not in dcells: continue

				result.append(dcells[dcell.cut])

		if not result: struct_result.subcodes.add(CODES_DATA.NO_DATA)

		struct_result.data = result
		return struct_result

	def WriteDCells(self, cells: list[T20_StructCell], flag_capture_data: bool = False) -> T21_StructResult_StructCells:
		""" Запись пакета D-Ячеек """
		struct_result = T21_StructResult_StructCells()

		for dcell in cells:
			if not ValidateOci(dcell.oci):
				struct_result.subcodes.add(CODES_DATA.ERROR_CHECK)
				struct_result.subcodes.add(CODES_PROCESSING.PARTIAL)
				continue

			if not ValidateOid(dcell.oid):
				struct_result.subcodes.add(CODES_DATA.ERROR_CHECK)
				struct_result.subcodes.add(CODES_PROCESSING.PARTIAL)
				continue

			if not ValidatePid(dcell.pid):
				struct_result.subcodes.add(CODES_DATA.ERROR_CHECK)
				struct_result.subcodes.add(CODES_PROCESSING.PARTIAL)
				continue

			dcells            = self._d_cells.get(dcell.sid, dict())
			dcells[dcell.cut] = dcell

			self._d_cells[dcell.sid] = dcells

		if not flag_capture_data: return struct_result

		result        = []

		for dcell in cells:
			if dcell.sid not in self._d_cells           : continue
			if dcell.cut not in self._d_cells[dcell.sid]: continue

			result.append(self._d_cells[dcell.sid][dcell.cut])

		struct_result.data = result[:]
		return struct_result

	# ЗАПРОСЫ D-ДАННЫХ
	def DCutRange(self, cell: T21_CutRange, flag_capture_data: bool = False) -> T21_StructResult_CutRange:
		""" Запрос границ CUT D-Ячейки """
		struct_result      = T21_StructResult_CutRange()

		struct_result.code = CODES_COMPLETION.INTERRUPTED
		struct_result.subcodes.add(CODES_DATA.ERROR_CHECK)

		if not ValidateOci(cell.oci)              : return struct_result
		if not ValidateOid(cell.oid)              : return struct_result
		if not ValidatePid(cell.pid)              : return struct_result

		struct_result.code = CODES_COMPLETION.COMPLETED
		struct_result.subcodes.clear()

		dcells             = self._d_cells[cell.sid].keys()

		if not dcells:
			struct_result.subcodes.add(CODES_DATA.NO_DATA)

		else         :
			struct_result.data.cut_l = min(dcells)
			struct_result.data.cut_r = max(dcells)

		return struct_result

	def DCuts(self, cell: T21_CutRange, flag_capture_data: bool = False) -> T21_StructResult_List:
		""" Запрос списка CUT """
		struct_result = T21_StructResult_List()

		struct_result.code = CODES_COMPLETION.INTERRUPTED
		struct_result.subcodes.add(CODES_DATA.ERROR_CHECK)

		if not ValidateOci(cell.oci): return struct_result
		if not ValidateOid(cell.oid): return struct_result
		if not ValidatePid(cell.pid): return struct_result

		struct_result.code = CODES_COMPLETION.COMPLETED
		struct_result.subcodes.clear()

		dcells = self._d_cells[cell.sid].keys()

		if not dcells:
			struct_result.subcodes.add(CODES_DATA.NO_DATA)

		struct_result.data = sorted(dcells)

		return struct_result
