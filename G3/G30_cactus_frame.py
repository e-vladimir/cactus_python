# КАКТУС: СТРУКТУРНЫЙ КАРКАС
# 2024-04-03

import datetime

from   G00_cactus_codes                 import *
from   G00_result_codes                 import *
from   G10_cactus_convertors            import BooleanToString,       \
											   DatetimeToString,      \
											   StringsToFloats,       \
											   StringsToIntegers,     \
											   StringToBoolean,       \
											   StringToDateTime,      \
											   StringToFloat,         \
											   StringToInteger,       \
											   UnificationOci
from   G10_cactus_generators            import GenerateID
from   G10_cactus_validators            import ValidateOci,           \
											   ValidateOid,           \
											   ValidatePid
from   G10_datetime                     import CurrentUTime
from   G20_meta_frame                   import C20_MetaFrame
from   G30_cactus_controller_containers import controller_containers
from   G30_cactus_struct                import T30_StructCell,        \
											   T30_ResultCode
from   G31_cactus_struct                import T31_ResultBool,        \
											   T31_ResultDatetime,    \
											   T31_ResultDict,        \
											   T31_ResultFloat,       \
											   T31_ResultInt,         \
											   T31_ResultList,        \
											   T31_ResultRange,       \
											   T31_ResultString,      \
											   T31_ResultStructCell,  \
											   T31_ResultStructCells, \
											   T31_StructRange

# Системные константы
SEPARATOR_LIST : str = '\n'


class C30_StructFrame(C20_MetaFrame):
	""" КАКТУС: СТРУКТУРНЫЙ ОБЪЕКТ """

	_oci : str = ""

	def __init__(self, oid: str = ""):
		super().__init__()

		self.Oid(oid)

		self.InitFields()

	def Init_00(self):
		super().Init_00()

		self._oid : str = ""

	# УПРАВЛЕНИЕ OCI
	@classmethod
	def Oci(cls) -> T31_ResultString:
		""" Запрос oci """
		translated_oci: str = UnificationOci(cls._oci)
		result_code   : int = RESULT_ERROR_CHECK_VALIDATE if not ValidateOci(translated_oci) else RESULT_OK

		return T31_ResultString(result_code, translated_oci)

	# УПРАВЛЕНИЕ OID
	def Oid(self, oid: str = None) -> T31_ResultString:
		""" Запрос/Установка oid """
		if oid is None:
			if not ValidateOid(self._oid): return T31_ResultString(RESULT_ERROR_CHECK_VALIDATE, self._oid)

			return T31_ResultString(RESULT_OK, self._oid)

		if not ValidateOid(oid): return T31_ResultString(RESULT_ERROR_CHECK_VALIDATE, oid)
		self._oid = oid

		return T31_ResultString(RESULT_OK, self._oid)

	def GenerateOid(self) -> T31_ResultString:
		""" Генерация OID """
		return self.Oid(GenerateID())

	# УПРАВЛЕНИЕ РЕГИСТРАЦИЕЙ ОБЪЕКТА
	def RegisterObject(self, container_name: str) -> T30_ResultCode:
		""" Регистрация объекта в контейнере """
		cell      = T30_StructCell()
		cell.oci  = self.Oci().text
		cell.oid  = self.Oid().text
		cell.pid  = OCI
		cell.cvl  = self.Oci().text
		cell.cut  = CurrentUTime()

		container = controller_containers.GetContainer(container_name)
		if container is None: return T30_ResultCode(RESULT_ERROR_ACCESS_CONNECTION)

		return T30_ResultCode(container.WriteSCell(cell, True).code)

	def DeleteObject(self, container_name: str) -> T30_ResultCode:
		""" Удаление объекта из контейнера """
		cell      = T30_StructCell()
		cell.oci  = self.Oci().text
		cell.oid  = self.Oid().text

		container = controller_containers.GetContainer(container_name)

		if container is None: return T30_ResultCode(RESULT_ERROR_ACCESS_CONNECTION)

		return T30_ResultCode(container.DeleteSCells(cell).code)

	# УПРАВЛЕНИЕ РЕГИСТРАЦИЕЙ КЛАССА
	@classmethod
	def RegisterClass(cls, container_name: str) -> T30_ResultCode:
		""" Регистрация класса в контейнере """
		container = controller_containers.GetContainer(container_name)
		code      = RESULT_WARNING_NOT_IMPLEMENTED

		if   container is None                : code = RESULT_WARNING_NOT_IMPLEMENTED
		elif container.TypeIsRAM().flag       : code = RESULT_WARNING_NOT_IMPLEMENTED
		elif container.TypeIsSQLite().flag    : code = container.RegisterClass(cls.Oci().text).code
		elif container.TypeIsPostgreSQL().flag: code = container.RegisterClass(cls.Oci().text).code

		return T30_ResultCode(code)

	# УПРАВЛЕНИЕ S-ДАННЫМИ
	def CopyToContainer(self, container_name_src: str, container_name_dst: str) -> T30_ResultCode:
		""" Копирование S-Ячеек из контейнера в контейнер """
		container_src                    = controller_containers.GetContainer(container_name_src)
		if container_src is None          : return T30_ResultCode(RESULT_ERROR_ACCESS_CONNECTION)

		container_dst                    = controller_containers.GetContainer(container_name_dst)
		if container_dst is None          : return T30_ResultCode(RESULT_ERROR_ACCESS_CONNECTION)

		obj_cell : T30_StructCell        = T30_StructCell(oci=self.Oci().text, oid=self.Oid().text)
		cells_src: T31_ResultStructCells = container_src.ReadSCells(obj_cell)

		if not cells_src.code == RESULT_OK: return T30_ResultCode(cells_src.code)

		return T30_ResultCode(container_dst.WriteSCells(cells_src.cells).code)

	def SyncBetweenContainers(self, container_name_1: str, container_name_2: str) -> T30_ResultCode:
		""" Синхронизация S-Ячеек между контейнерами """
		container_1                            = controller_containers.GetContainer(container_name_1)
		if container_1 is None          : return T30_ResultCode(RESULT_ERROR_ACCESS_CONNECTION)

		container_2                            = controller_containers.GetContainer(container_name_2)
		if container_2 is None          : return T30_ResultCode(RESULT_ERROR_ACCESS_CONNECTION)

		cell_object: T30_StructCell            = T30_StructCell(oci=self.Oci().text, oid=self.Oid().text)

		cells_1    : T31_ResultStructCells     = container_1.ReadSCells(cell_object)
		if not cells_1.code == RESULT_OK: return T30_ResultCode(cells_1.code)

		cells_2    : T31_ResultStructCells     = container_2.ReadSCells(cell_object)
		if not cells_2.code == RESULT_OK: return T30_ResultCode(cells_2.code)

		cells      : dict[str, T30_StructCell] = dict()

		for cell_raw in (cells_1.cells + cells_2.cells):
			cell = cells.get(cell_raw.sid, cell_raw)

			if cell_raw.cut > cell.cut:
				cell.cvl = cell_raw.cvl
				cell.cut = cell_raw.cut

			cells[cell.sid] = cell

		cells      : list[T30_StructCell]      = list(cells.values())

		result     : T31_ResultStructCells     = container_1.SyncSCells(cells)
		if not result.code == RESULT_OK: return T30_ResultCode(result.code)

		result     : T31_ResultStructCells     = container_2.SyncSCells(cells)
		if not result.code == RESULT_OK: return T30_ResultCode(result.code)

		return T30_ResultCode(RESULT_OK)

	# ЗАПРОСЫ OID
	@classmethod
	def Oids(self, container_name: str) -> T31_ResultList:
		""" Запрос списка OID объектов класса из контейнера """
		container                        = controller_containers.GetContainer(container_name)
		if container is None              : return T31_ResultList(RESULT_ERROR_ACCESS_CONNECTION)

		cls_cell : T30_StructCell        = T30_StructCell(oci=self.Oci().text)
		cells_raw: T31_ResultStructCells = container.ReadSCells(cls_cell)
		if not cells_raw.code == RESULT_OK: return T31_ResultList(cells_raw.code)

		oids     : list[str]             = list(set(map(lambda cell: cell.oid, cells_raw.cells)))
		if not oids                       : return T31_ResultList(RESULT_WARNING_NO_DATA)

		return T31_ResultList(RESULT_OK, oids)

	# ЗАПРОСЫ S-ДАННЫХ
	def Pids(self, container_name: str) -> T31_ResultList:
		""" Запрос списка PID S-Ячеек из контейнера """
		if not ValidateOid(self._oid)     : return T31_ResultList(RESULT_ERROR_CHECK_VALIDATE)

		container                        = controller_containers.GetContainer(container_name)
		if container is None              : return T31_ResultList(RESULT_ERROR_ACCESS_CONNECTION)

		cls_cell : T30_StructCell        = T30_StructCell(oci=self.Oci().text, oid=self.Oid().text)
		cells_raw: T31_ResultStructCells = container.ReadSCells(cls_cell)
		if not cells_raw.code == RESULT_OK: return T31_ResultList(cells_raw.code)

		oids     : list[str]             = list(set(map(lambda cell: cell.pid, cells_raw.cells)))
		if not oids                       : return T31_ResultList(RESULT_WARNING_NO_DATA)

		return T31_ResultList(RESULT_OK, oids)

	# УПРАВЛЕНИЕ СТРУКТУРНЫМИ ПАРАМЕТРАМИ
	def InitFields(self):
		""" Инициализация структурных параметров """
		pass


class C30_StructField(C20_MetaFrame):
	""" КАКТУС: СТРУКТУРНЫЙ ПАРАМЕТР """
	""" 2022-11-19 """

	def __init__(self, struct_frame: C30_StructFrame, pid: str, default_cvl: any = None):
		super().__init__()

		self._pid         = pid
		self.struct_frame = struct_frame

		if default_cvl is not None: self.DefaultCvl(default_cvl)

	def Init_00(self):
		super().Init_00()
		self._default_cvl: str = ""
		self._pid        : str = ""

	def Init_10(self):
		super().Init_10()
		self.struct_frame : C30_StructFrame | None = None

	# ЗАПРОСЫ ИДЕНТИФИКАТОРОВ
	def Sid(self) -> T31_ResultString:
		""" Запрос SID """
		oid: T31_ResultString = T31_ResultString()
		pid: T31_ResultString = self.Pid()
		sid: str              = f"{oid.text}.{pid.text}"

		if self.struct_frame is None: return T31_ResultString(RESULT_ERROR_DATA_STRUCT, sid)

		oid                   = self.struct_frame.Oid()
		sid                   = f"{oid.text}.{pid.text}"
		if not oid.code == RESULT_OK: return T31_ResultString(oid.code, sid)

		return T31_ResultString(RESULT_OK, sid)

	def Cid(self) -> T31_ResultString:
		""" Запрос CID """
		oci: T31_ResultString = T31_ResultString()
		oid: T31_ResultString = T31_ResultString()
		pid: T31_ResultString = self.Pid()
		cid: str              = f"{oci.text}.{oid.text}.{pid.text}"

		if self.struct_frame is None: return T31_ResultString(RESULT_ERROR_DATA_STRUCT, cid)

		oci                   = self.struct_frame.Oci()
		oid                   = self.struct_frame.Oid()
		cid: str              = f"{oci.text}.{oid.text}.{pid.text}"
		if not oci.code == RESULT_OK: return T31_ResultString(oci.code, cid)
		if not oid.code == RESULT_OK: return T31_ResultString(oid.code, cid)

		return T31_ResultString(RESULT_OK, cid)

	def Pid(self) -> T31_ResultString:
		""" Запрос PID """
		if not ValidatePid(self._pid): return T31_ResultString(RESULT_ERROR_CHECK_VALIDATE, self._pid)

		return T31_ResultString(RESULT_OK, self._pid)

	# УПРАВЛЕНИЕ ЗНАЧЕНИЕМ ПО-УМОЛЧАНИЮ
	def DefaultCvl(self, cvl: any = None) -> T31_ResultString:
		""" Запрос/Установка значения параметра по умолчанию """
		if cvl is None: return T31_ResultString(RESULT_OK, self._default_cvl)

		if   type(cvl) is int  : self._default_cvl = f"{cvl}"
		elif type(cvl) is float: self._default_cvl = f"{cvl:0.5f}"
		elif type(cvl) is bool : self._default_cvl = BooleanToString(cvl)
		elif type(cvl) is list : self._default_cvl = SEPARATOR_LIST.join(list(map(str, cvl)))
		elif type(cvl) is str  : self._default_cvl = cvl

	# КОНВЕРТАЦИЯ ИЗ ТИПА ДАННЫХ
	def _WriteCvlInSCell(self, container_name_dst: str, cvl: str, cut: int = 0) -> T30_ResultCode:
		""" Системный метод записи данных для конверторов """
		container = controller_containers.GetContainer(container_name_dst)
		if container is None        : return T30_ResultCode(RESULT_ERROR_ACCESS_CONNECTION)

		if self.struct_frame is None: return T30_ResultCode(RESULT_ERROR_DATA_STRUCT)

		oid       = self.struct_frame.Oid()
		if not oid.code == RESULT_OK: return T30_ResultCode(oid.code)

		oci       = self.struct_frame.Oci()
		if not oci.code == RESULT_OK: return T30_ResultCode(oci.code)

		pid       = self.Pid()
		if not pid.code == RESULT_OK: return T30_ResultCode(pid.code)

		if cut == 0: cut = CurrentUTime()

		cell      = T30_StructCell(oci=oci.text, oid=oid.text, pid=pid.text, cvl=cvl, cut=cut)

		return T30_ResultCode(container.WriteSCell(cell).code)

	def FromBoolean(self, container_name_dst: str, flag: bool) -> T30_ResultCode:
		""" Из логического значения """
		try   : data = BooleanToString(flag)
		except: return T30_ResultCode(RESULT_ERROR_CONVERT)

		return self._WriteCvlInSCell(container_name_dst, data)

	def FromDatetime(self, container_name_dst: str, dtime: datetime.datetime) -> T30_ResultCode:
		""" Из логического значения """
		try   : data = DatetimeToString(dtime)
		except: return T30_ResultCode(RESULT_ERROR_CONVERT)

		return self._WriteCvlInSCell(container_name_dst, data)

	def FromInteger(self, container_name_dst: str, value: int) -> T30_ResultCode:
		""" Из целого числа """
		try   : data = f"{value:d}"
		except: return T30_ResultCode(RESULT_ERROR_CONVERT)

		return self._WriteCvlInSCell(container_name_dst, data)

	def FromFloat(self, container_name_dst: str, value: float) -> T30_ResultCode:
		""" Из дробного числа """
		try               : data = f"{value:0.5f}"
		except SyntaxError: return T30_ResultCode(RESULT_ERROR_CONVERT)

		return self._WriteCvlInSCell(container_name_dst, data)

	def FromString(self, container_name_dst: str, text: str) -> T30_ResultCode:
		""" Из строки """
		return self._WriteCvlInSCell(container_name_dst, text)

	# КОНВЕРТАЦИЯ ИЗ СПИСКА ТИПА ДАННЫХ
	def FromBooleans(self, container_name_dst: str, data: list[bool]) -> T30_ResultCode:
		""" Из списка логических значений """
		try   : data = SEPARATOR_LIST.join(list(map(BooleanToString, data)))
		except: return T30_ResultCode(RESULT_ERROR_CONVERT)

		return self._WriteCvlInSCell(container_name_dst, data)

	def FromDatetimes(self, container_name_dst: str, data: list[datetime.datetime]) -> T30_ResultCode:
		""" Из списка логических значений """
		try   : data = SEPARATOR_LIST.join(list(map(DatetimeToString, data)))
		except: return T30_ResultCode(RESULT_ERROR_CONVERT)

		return self._WriteCvlInSCell(container_name_dst, data)

	def FromIntegers(self, container_name_dst: str, data: list[int]) -> T30_ResultCode:
		""" Из списка целых чисел """
		try   : data = SEPARATOR_LIST.join(list(map(format, data)))
		except: return T30_ResultCode(RESULT_ERROR_CONVERT)

		return self._WriteCvlInSCell(container_name_dst, data)

	def FromFloats(self, container_name_dst: str, data: list[float]) -> T30_ResultCode:
		""" Из списка дробных чисел """
		try   : data = SEPARATOR_LIST.join(list(map("{:0.5f}".format, data)))
		except: return T30_ResultCode(RESULT_ERROR_CONVERT)

		return self._WriteCvlInSCell(container_name_dst, data)

	def FromStrings(self, container_name_dst: str, data: list[str]) -> T30_ResultCode:
		""" Из списка строк """
		try   : data = SEPARATOR_LIST.join(data)
		except: return T30_ResultCode(RESULT_ERROR_CONVERT)

		return self._WriteCvlInSCell(container_name_dst, data)

	# КОНВЕРТАЦИЯ В ТИП ДАННЫХ
	def _ReadCvlSCell(self, container_name_src: str) -> T31_ResultString:
		""" Системный метод чтения данных для конверторов """
		container = controller_containers.GetContainer(container_name_src)
		if container is None        : return T31_ResultString(RESULT_ERROR_ACCESS_CONNECTION)

		if self.struct_frame is None: return T31_ResultString(RESULT_ERROR_DATA_STRUCT)

		oid       = self.struct_frame.Oid()
		if not oid.code == RESULT_OK: return T31_ResultString(oid.code)

		oci       = self.struct_frame.Oci()
		if not oci.code == RESULT_OK: return T31_ResultString(oci.code)

		pid       = self.Pid()
		if not pid.code == RESULT_OK: return T31_ResultString(pid.code)

		cell_src  = T30_StructCell(oci=oci.text, oid=oid.text, pid=pid.text)
		cell      = container.ReadSCell(cell_src)

		return T31_ResultString(cell.code, cell.cell.cvl)

	def ToBoolean(self, container_name_src: str) -> T31_ResultBool:
		""" В логическое значение """
		result = self._ReadCvlSCell(container_name_src)
		value  = result.text if result.code == RESULT_OK else self.DefaultCvl().text

		try   : return T31_ResultBool(result.code, StringToBoolean(value))
		except: return T31_ResultBool(RESULT_ERROR_CONVERT)

	def ToDatetime(self, container_name_src: str) -> T31_ResultDatetime:
		""" В Datetime """
		result  = self._ReadCvlSCell(container_name_src)
		value   = result.text if result.code == RESULT_OK else self.DefaultCvl().text

		convert = StringToDateTime(value)
		if convert is None:	return T31_ResultDatetime(RESULT_ERROR_CONVERT)

		return T31_ResultDatetime(result.code, convert)

	def ToInteger(self, container_name_src: str) -> T31_ResultInt:
		""" В целое число """
		result = self._ReadCvlSCell(container_name_src)
		value  = result.text if result.code == RESULT_OK else self.DefaultCvl().text

		try   : return T31_ResultInt(result.code, StringToInteger(value))
		except: return T31_ResultInt(RESULT_ERROR_CONVERT)

	def ToFloat(self, container_name_src: str) -> T31_ResultFloat:
		""" В дробное число """
		result = self._ReadCvlSCell(container_name_src)
		value  = result.text if result.code == RESULT_OK else self.DefaultCvl().text

		try   : return T31_ResultFloat(result.code, StringToFloat(value))
		except: return T31_ResultFloat(RESULT_ERROR_CONVERT)

	def ToString(self, container_name_src: str) -> T31_ResultString:
		""" В строку """
		result = self._ReadCvlSCell(container_name_src)
		value  = result.text if result.code == RESULT_OK else self.DefaultCvl().text

		return T31_ResultString(result.code, value)

	# КОНВЕРТАЦИЯ В СПИСОК ТИПА ДАННЫХ
	def ToBooleans(self, container_name_src : str) -> T31_ResultList:
		""" В список логических значений """
		result = self._ReadCvlSCell(container_name_src)
		value  = result.text if result.code == RESULT_OK else self.DefaultCvl().text

		if not value.strip(): return T31_ResultList(result.code, [])

		try   : return T31_ResultList(result.code, list(map(StringToBoolean, value.split(SEPARATOR_LIST))))
		except: return T31_ResultList(RESULT_ERROR_CONVERT)

	def ToDatetimes(self, container_name_src : str) -> T31_ResultList:
		""" В список Datetime """
		result = self._ReadCvlSCell(container_name_src)
		value  = result.text if result.code == RESULT_OK else self.DefaultCvl().text

		if not value.strip(): return T31_ResultList(result.code, [])

		try   : return T31_ResultList(result.code, list(map(StringToDateTime, value.split(SEPARATOR_LIST))))
		except: return T31_ResultList(RESULT_ERROR_CONVERT)

	def ToIntegers(self, container_name_src: str) -> T31_ResultList:
		""" В список целых чисел """
		result = self._ReadCvlSCell(container_name_src)
		value  = result.text if result.code == RESULT_OK else self.DefaultCvl().text

		if not value.strip(): return T31_ResultList(result.code, [])

		try   : return T31_ResultList(result.code, StringsToIntegers(value.split(SEPARATOR_LIST)))
		except: return T31_ResultList(RESULT_ERROR_CONVERT)

	def ToFloats(self, container_name_src: str) -> T31_ResultList:
		""" В список дробных чисел """
		result = self._ReadCvlSCell(container_name_src)
		value  = result.text if result.code == RESULT_OK else self.DefaultCvl().text

		if not value.strip(): return T31_ResultList(result.code, [])

		data   = value.replace(',', '.')

		try   : return T31_ResultList(result.code, StringsToFloats(data.split(SEPARATOR_LIST)))
		except: return T31_ResultList(RESULT_ERROR_CONVERT)

	def ToStrings(self, container_name_src: str) -> T31_ResultList:
		""" В список строк """
		result = self._ReadCvlSCell(container_name_src)
		value  = result.text if result.code == RESULT_OK else self.DefaultCvl().text

		if not value.strip(): return T31_ResultList(result.code, [])

		try   : return T31_ResultList(result.code, list(value.split(SEPARATOR_LIST)))
		except: return T31_ResultList(RESULT_ERROR_CONVERT)

	# УПРАВЛЕНИЕ S-ДАННЫМИ
	def Cut(self, container_name_src: str) -> T31_ResultInt:
		""" Запрос cut """
		container = controller_containers.GetContainer(container_name_src)
		if container is None        : return T31_ResultInt(RESULT_ERROR_ACCESS_CONNECTION)

		if self.struct_frame is None: return T31_ResultInt(RESULT_ERROR_DATA_STRUCT)

		oid       = self.struct_frame.Oid()
		if not oid.code == RESULT_OK: return T31_ResultInt(oid.code)

		oci       = self.struct_frame.Oci()
		if not oci.code == RESULT_OK: return T31_ResultInt(oci.code)

		pid       = self.Pid()
		if not pid.code == RESULT_OK: return T31_ResultInt(pid.code)

		cell_src  = T30_StructCell(oci=oci.text, oid=oid.text, pid=pid.text)
		cell      = container.ReadSCell(cell_src)

		return T31_ResultInt(cell.code, cell.cell.cut)

	def CopyToContainer(self, container_name_src: str, container_name_dst: str) -> T30_ResultCode:
		""" Копирование S-Ячейки из контейнера в контейнер """
		container_src                   = controller_containers.GetContainer(container_name_src)
		if container_src is None         : return T31_ResultStructCell(RESULT_ERROR_ACCESS_CONNECTION)

		container_dst                   = controller_containers.GetContainer(container_name_dst)
		if container_dst is None         : return T31_ResultStructCell(RESULT_ERROR_ACCESS_CONNECTION)

		oid                             = self.struct_frame.Oid()
		if not oid.code == RESULT_OK     : return T31_ResultStructCell(oid.code)

		oci                             = self.struct_frame.Oci()
		if not oci.code == RESULT_OK     : return T31_ResultStructCell(oci.code)

		pid                             = self.Pid()
		if not pid.code == RESULT_OK     : return T31_ResultStructCell(pid.code)

		cell     : T30_StructCell       = T30_StructCell(oci=oci.text, oid=oid.text, pid=pid.text)
		cell_src : T31_ResultStructCell = container_src.ReadSCell(cell)

		if not cell_src.code == RESULT_OK: return T31_ResultStructCell(cell_src.code)

		return container_dst.WriteSCell(cell_src.cell, False)

	def SyncBetweenContainers(self, container_name_1: str, container_name_2: str) -> T30_ResultCode:
		""" Синхронизация S-Ячейки между контейнерами """
		container_1                   = controller_containers.GetContainer(container_name_1)
		if container_1 is None              : return T31_ResultStructCell(RESULT_ERROR_ACCESS_CONNECTION)

		container_2                   = controller_containers.GetContainer(container_name_2)
		if container_2 is None              : return T31_ResultStructCell(RESULT_ERROR_ACCESS_CONNECTION)

		oid                           = self.struct_frame.Oid()
		if not oid.code == RESULT_OK        : return T31_ResultStructCell(oid.code)

		oci                           = self.struct_frame.Oci()
		if not oci.code == RESULT_OK        : return T31_ResultStructCell(oci.code)

		pid                           = self.Pid()
		if not pid.code == RESULT_OK        : return T31_ResultStructCell(pid.code)

		cell   : T30_StructCell       = T30_StructCell(oci=oci.text, oid=oid.text, pid=pid.text)
		cell_1 : T31_ResultStructCell = container_1.ReadSCell(cell)
		if not cell_1.code == RESULT_OK     : return T31_ResultStructCell(cell_1.code)

		cell_2 : T31_ResultStructCell = container_2.ReadSCell(cell)
		if not cell_2.code == RESULT_OK     : return T31_ResultStructCell(cell_2.code)

		if cell_1.cell.cut > cell_2.cell.cut: return container_2.SyncSCell(cell_1.cell)
		if cell_2.cell.cut > cell_1.cell.cut: return container_1.SyncSCell(cell_2.cell)

		return T30_ResultCode(RESULT_OK)

	def DeleteFromContainer(self, container_name_src: str) -> T30_ResultCode:
		""" Удаление S-Ячейки из контейнера """
		container_src                   = controller_containers.GetContainer(container_name_src)
		if container_src is None         : return T31_ResultStructCell(RESULT_ERROR_ACCESS_CONNECTION)

		oid                             = self.struct_frame.Oid()
		if not oid.code == RESULT_OK     : return T31_ResultStructCell(oid.code)

		oci                             = self.struct_frame.Oci()
		if not oci.code == RESULT_OK     : return T31_ResultStructCell(oci.code)

		pid                             = self.Pid()
		if not pid.code == RESULT_OK     : return T31_ResultStructCell(pid.code)

		cell     : T30_StructCell       = T30_StructCell(oci=oci.text, oid=oid.text, pid=pid.text)
		cell_src : T31_ResultStructCell = container_src.ReadSCell(cell)

		if not cell_src.code == RESULT_OK: return T31_ResultStructCell(cell_src.code)

		return container_src.DeleteSCell(cell_src.cell)

	# УПРАВЛЕНИЕ D-ДАННЫМИ
	def WriteCvl(self, container_name_dst: str, cvl: str, cut: int = 0) -> T30_ResultCode:
		""" Добавление записи D-Данных """
		container = controller_containers.GetContainer(container_name_dst)
		if container is None        : return T30_ResultCode(RESULT_ERROR_ACCESS_CONNECTION)

		if self.struct_frame is None: return T30_ResultCode(RESULT_ERROR_DATA_STRUCT)

		oid       = self.struct_frame.Oid()
		if not oid.code == RESULT_OK: return T30_ResultCode(oid.code)

		oci       = self.struct_frame.Oci()
		if not oci.code == RESULT_OK: return T30_ResultCode(oci.code)

		pid       = self.Pid()
		if not pid.code == RESULT_OK: return T30_ResultCode(pid.code)

		if cut == 0: cut = CurrentUTime()

		cell      = T30_StructCell(oci=oci.text, oid=oid.text, pid=pid.text, cvl=cvl, cut=cut)
		result    = container.WriteDCell(cell)

		return T30_ResultCode(result.code)

	def ReadCvl(self, container_name_src: str, cut: int = 0) -> T31_ResultString:
		""" Запрос записи D-Данных """
		container = controller_containers.GetContainer(container_name_src)
		if container is None        : return T31_ResultString(RESULT_ERROR_ACCESS_CONNECTION)

		if self.struct_frame is None: return T31_ResultString(RESULT_ERROR_DATA_STRUCT)

		oid       = self.struct_frame.Oid()
		if not oid.code == RESULT_OK: return T31_ResultString(oid.code)

		oci       = self.struct_frame.Oci()
		if not oci.code == RESULT_OK: return T31_ResultString(oci.code)

		pid       = self.Pid()
		if not pid.code == RESULT_OK: return T31_ResultString(pid.code)

		if cut == 0:
			cuts = self.CutRange(container_name_src)
			if not cuts.code == RESULT_OK: return T31_ResultString(cuts.code)
			if not cuts                  : return T31_ResultString(RESULT_WARNING_NO_DATA)

			cut = cuts.cut_r

		cell      = T30_StructCell(oci=oci.text, oid=oid.text, pid=pid.text, cut=cut)
		result    = container.ReadDCell(cell)

		return T31_ResultString(result.code, result.cell.cvl)

	def CutRange(self, container_name_src: str, cut_l: int = 0, cut_r: int = 0) -> T31_ResultRange:
		""" Запрос границ cut D-Данных """
		container = controller_containers.GetContainer(container_name_src)
		if container is None          : return T31_ResultRange(RESULT_ERROR_ACCESS_CONNECTION)

		if self.struct_frame is None  : return T31_ResultRange(RESULT_ERROR_DATA_STRUCT)

		oid       = self.struct_frame.Oid()
		if not oid.code == RESULT_OK  : return T31_ResultRange(oid.code)

		oci       = self.struct_frame.Oci()
		if not oci.code == RESULT_OK  : return T31_ResultRange(oci.code)

		pid       = self.Pid()
		if not pid.code == RESULT_OK  : return T31_ResultRange(pid.code)

		cell      = T31_StructRange(oci=oci.text, oid=oid.text, pid=pid.text, cut_l=cut_l, cut_r=cut_r)
		result    = container.DCutRange(cell)

		return T31_ResultRange(result.code, cut_l=result.range.cut_l, cut_r=result.range.cut_r)

	def Cuts(self, container_name_src: str, cut_l: int = 0, cut_r: int = 0) -> T31_ResultList:
		""" Запрос списка cut в диапазоне cut D-Данных """
		container = controller_containers.GetContainer(container_name_src)
		if container is None          : return T31_ResultList(RESULT_ERROR_ACCESS_CONNECTION)

		if self.struct_frame is None  : return T31_ResultList(RESULT_ERROR_DATA_STRUCT)

		oid       = self.struct_frame.Oid()
		if not oid.code == RESULT_OK  : return T31_ResultList(oid.code)

		oci       = self.struct_frame.Oci()
		if not oci.code == RESULT_OK  : return T31_ResultList(oci.code)

		pid       = self.Pid()
		if not pid.code == RESULT_OK  : return T31_ResultList(pid.code)

		cell      = T31_StructRange(oci=oci.text, oid=oid.text, pid=pid.text, cut_l=cut_l, cut_r=cut_r)

		return container.DCuts(cell)

	def Cvls(self, container_name_src: str, cut_l: int = 0, cut_r: int = 0) -> T31_ResultDict:
		""" Запрос cvl/cut в диапазоне cut D-Данных """
		container = controller_containers.GetContainer(container_name_src)
		if container is None          : return T31_ResultDict(RESULT_ERROR_ACCESS_CONNECTION)

		if self.struct_frame is None  : return T31_ResultDict(RESULT_ERROR_DATA_STRUCT)

		oid                     = self.struct_frame.Oid()
		if not oid.code == RESULT_OK  : return T31_ResultDict(oid.code)

		oci                     = self.struct_frame.Oci()
		if not oci.code == RESULT_OK  : return T31_ResultDict(oci.code)

		pid                     = self.Pid()
		if not pid.code == RESULT_OK  : return T31_ResultDict(pid.code)

		cell                    = T31_StructRange(oci=oci.text, oid=oid.text, pid=pid.text, cut_l=cut_l, cut_r=cut_r)
		dcells                  = container.ReadDCells(cell)
		result : dict[int, str] = dict()

		for cell in dcells.cells: result[cell.cut] = cell.cvl

		return T31_ResultDict(dcells.code, result)
