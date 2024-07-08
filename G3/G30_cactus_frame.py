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
											   UnificationIdc
from   G10_cactus_generators            import GenerateID
from   G10_cactus_validators            import ValidateIdc,           \
											   ValidateIdo,           \
											   ValidateIdp
from   G10_datetime                     import CurrentUTime
from   G20_meta_frame                   import C20_MetaFrame
from   G30_cactus_controller_containers import controller_containers
from G20_cactus_struct import T20_StructCell,        \
											   T20_ResultCode
from G21_struct_result import T21_ResultBool,        \
											   T21_ResultDatetime,    \
											   T21_ResultDict,        \
											   T21_ResultFloat,       \
											   T21_ResultInt,         \
											   T21_ResultList,        \
											   T21_ResultRange,       \
											   T21_ResultString,      \
											   T21_ResultStructCell,  \
											   T21_ResultStructCells, \
											   T21_StructRange

# Системные константы
SEPARATOR_LIST : str = '\n'


class C30_StructFrame(C20_MetaFrame):
	""" КАКТУС: СТРУКТУРНЫЙ ОБЪЕКТ """

	_idc : str = ""

	def __init__(self, ido: str = ""):
		super().__init__()

		self.Ido(ido)

		self.InitFields()

	def Init_00(self):
		super().Init_00()

		self._ido : str = ""

	# УПРАВЛЕНИЕ IDC
	@classmethod
	def Idc(cls) -> T21_ResultString:
		""" Запрос idc """
		translated_idc: str = UnificationIdc(cls._idc)
		result_code   : int = RESULT_ERROR_CHECK_VALIDATE if not ValidateIdc(translated_idc) else RESULT_OK

		return T21_ResultString(result_code, translated_idc)

	# УПРАВЛЕНИЕ IDO
	def Ido(self, ido: str = None) -> T21_ResultString:
		""" Запрос/Установка ido """
		if ido is None:
			if not ValidateIdo(self._ido): return T21_ResultString(RESULT_ERROR_CHECK_VALIDATE, self._ido)

			return T21_ResultString(RESULT_OK, self._ido)

		if not ValidateIdo(ido): return T21_ResultString(RESULT_ERROR_CHECK_VALIDATE, ido)
		self._ido = ido

		return T21_ResultString(RESULT_OK, self._ido)

	def GenerateIdo(self) -> T21_ResultString:
		""" Генерация IDO """
		return self.Ido(GenerateID())

	# УПРАВЛЕНИЕ РЕГИСТРАЦИЕЙ ОБЪЕКТА
	def RegisterObject(self, container_name: str) -> T20_ResultCode:
		""" Регистрация объекта в контейнере """
		cell      = T20_StructCell()
		cell.idc  = self.Idc().text
		cell.ido  = self.Ido().text
		cell.idp  = IDC
		cell.vlp  = self.Idc().text
		cell.vlt  = CurrentUTime()

		container = controller_containers.Container(container_name)
		if container is None: return T20_ResultCode(RESULT_ERROR_ACCESS_CONNECTION)

		return T20_ResultCode(container.WriteSCell(cell, True).code)

	def DeleteObject(self, container_name: str) -> T20_ResultCode:
		""" Удаление объекта из контейнера """
		cell      = T20_StructCell()
		cell.idc  = self.Idc().text
		cell.ido  = self.Ido().text

		container = controller_containers.Container(container_name)

		if container is None: return T20_ResultCode(RESULT_ERROR_ACCESS_CONNECTION)

		return T20_ResultCode(container.DeleteSCells(cell).code)

	# УПРАВЛЕНИЕ РЕГИСТРАЦИЕЙ КЛАССА
	@classmethod
	def RegisterClass(cls, container_name: str) -> T20_ResultCode:
		""" Регистрация класса в контейнере """
		container = controller_containers.Container(container_name)
		code      = RESULT_WARNING_NOT_IMPLEMENTED

		if   container is None                : code = RESULT_WARNING_NOT_IMPLEMENTED
		elif container.Type_RAM().flag       : code = RESULT_WARNING_NOT_IMPLEMENTED
		elif container.Type_SQLite().flag    : code = container.RegisterClass(cls.Idc().text).code
		elif container.Type_PostgreSQL().flag: code = container.RegisterClass(cls.Idc().text).code

		return T20_ResultCode(code)

	# УПРАВЛЕНИЕ S-ДАННЫМИ
	def CopyToContainer(self, container_name_src: str, container_name_dst: str) -> T20_ResultCode:
		""" Копирование S-Ячеек из контейнера в контейнер """
		container_src                    = controller_containers.Container(container_name_src)
		if container_src is None          : return T20_ResultCode(RESULT_ERROR_ACCESS_CONNECTION)

		container_dst                    = controller_containers.Container(container_name_dst)
		if container_dst is None          : return T20_ResultCode(RESULT_ERROR_ACCESS_CONNECTION)

		obj_cell : T20_StructCell        = T20_StructCell(idc=self.Idc().text, ido=self.Ido().text)
		cells_src: T21_ResultStructCells = container_src.ReadSCells(obj_cell)

		if not cells_src.code == RESULT_OK: return T20_ResultCode(cells_src.code)

		return T20_ResultCode(container_dst.WriteSCells(cells_src.cells).code)

	def SyncBetweenContainers(self, container_name_1: str, container_name_2: str) -> T20_ResultCode:
		""" Синхронизация S-Ячеек между контейнерами """
		container_1                            = controller_containers.Container(container_name_1)
		if container_1 is None          : return T20_ResultCode(RESULT_ERROR_ACCESS_CONNECTION)

		container_2                            = controller_containers.Container(container_name_2)
		if container_2 is None          : return T20_ResultCode(RESULT_ERROR_ACCESS_CONNECTION)

		cell_object: T20_StructCell            = T20_StructCell(idc=self.Idc().text, ido=self.Ido().text)

		cells_1    : T21_ResultStructCells     = container_1.ReadSCells(cell_object)
		if not cells_1.code == RESULT_OK: return T20_ResultCode(cells_1.code)

		cells_2    : T21_ResultStructCells     = container_2.ReadSCells(cell_object)
		if not cells_2.code == RESULT_OK: return T20_ResultCode(cells_2.code)

		cells      : dict[str, T20_StructCell] = dict()

		for cell_raw in (cells_1.cells + cells_2.cells):
			cell = cells.get(cell_raw.ids, cell_raw)

			if cell_raw.vlt > cell.vlt:
				cell.vlp = cell_raw.vlp
				cell.vlt = cell_raw.vlt

			cells[cell.ids] = cell

		cells      : list[T20_StructCell]      = list(cells.values())

		result     : T21_ResultStructCells     = container_1.SyncSCells(cells)
		if not result.code == RESULT_OK: return T20_ResultCode(result.code)

		result     : T21_ResultStructCells     = container_2.SyncSCells(cells)
		if not result.code == RESULT_OK: return T20_ResultCode(result.code)

		return T20_ResultCode(RESULT_OK)

	# ЗАПРОСЫ IDO
	@classmethod
	def Idos(self, container_name: str) -> T21_ResultList:
		""" Запрос списка IDO объектов класса из контейнера """
		container                        = controller_containers.Container(container_name)
		if container is None              : return T21_ResultList(RESULT_ERROR_ACCESS_CONNECTION)

		cls_cell : T20_StructCell        = T20_StructCell(idc=self.Idc().text)
		cells_raw: T21_ResultStructCells = container.ReadSCells(cls_cell)
		if not cells_raw.code == RESULT_OK: return T21_ResultList(cells_raw.code)

		idos     : list[str]             = list(set(map(lambda cell: cell.ido, cells_raw.cells)))
		if not idos                       : return T21_ResultList(RESULT_WARNING_NO_DATA)

		return T21_ResultList(RESULT_OK, idos)

	# ЗАПРОСЫ S-ДАННЫХ
	def Idps(self, container_name: str) -> T21_ResultList:
		""" Запрос списка IDP S-Ячеек из контейнера """
		if not ValidateIdo(self._ido)     : return T21_ResultList(RESULT_ERROR_CHECK_VALIDATE)

		container                        = controller_containers.Container(container_name)
		if container is None              : return T21_ResultList(RESULT_ERROR_ACCESS_CONNECTION)

		cls_cell : T20_StructCell        = T20_StructCell(idc=self.Idc().text, ido=self.Ido().text)
		cells_raw: T21_ResultStructCells = container.ReadSCells(cls_cell)
		if not cells_raw.code == RESULT_OK: return T21_ResultList(cells_raw.code)

		idos     : list[str]             = list(set(map(lambda cell: cell.idp, cells_raw.cells)))
		if not idos                       : return T21_ResultList(RESULT_WARNING_NO_DATA)

		return T21_ResultList(RESULT_OK, idos)

	# УПРАВЛЕНИЕ СТРУКТУРНЫМИ ПАРАМЕТРАМИ
	def InitFields(self):
		""" Инициализация структурных параметров """
		pass


class C30_StructField(C20_MetaFrame):
	""" КАКТУС: СТРУКТУРНЫЙ ПАРАМЕТР """
	""" 2022-11-19 """

	def __init__(self, struct_frame: C30_StructFrame, idp: str, default_vlp: any = None):
		super().__init__()

		self._idp         = idp
		self.struct_frame = struct_frame

		if default_vlp is not None: self.DefaultVlp(default_vlp)

	def Init_00(self):
		super().Init_00()
		self._default_vlp: str = ""
		self._idp        : str = ""

	def Init_10(self):
		super().Init_10()
		self.struct_frame : C30_StructFrame | None = None

	# ЗАПРОСЫ ИДЕНТИФИКАТОРОВ
	def Ids(self) -> T21_ResultString:
		""" Запрос IDS """
		ido: T21_ResultString = T21_ResultString()
		idp: T21_ResultString = self.Idp()
		ids: str              = f"{ido.text}.{idp.text}"

		if self.struct_frame is None: return T21_ResultString(RESULT_ERROR_DATA_STRUCT, ids)

		ido                   = self.struct_frame.Ido()
		ids                   = f"{ido.text}.{idp.text}"
		if not ido.code == RESULT_OK: return T21_ResultString(ido.code, ids)

		return T21_ResultString(RESULT_OK, ids)

	def Idf(self) -> T21_ResultString:
		""" Запрос IDF """
		idc: T21_ResultString = T21_ResultString()
		ido: T21_ResultString = T21_ResultString()
		idp: T21_ResultString = self.Idp()
		idf: str              = f"{idc.text}.{ido.text}.{idp.text}"

		if self.struct_frame is None: return T21_ResultString(RESULT_ERROR_DATA_STRUCT, idf)

		idc                   = self.struct_frame.Idc()
		ido                   = self.struct_frame.Ido()
		idf: str              = f"{idc.text}.{ido.text}.{idp.text}"
		if not idc.code == RESULT_OK: return T21_ResultString(idc.code, idf)
		if not ido.code == RESULT_OK: return T21_ResultString(ido.code, idf)

		return T21_ResultString(RESULT_OK, idf)

	def Idp(self) -> T21_ResultString:
		""" Запрос IDP """
		if not ValidateIdp(self._idp): return T21_ResultString(RESULT_ERROR_CHECK_VALIDATE, self._idp)

		return T21_ResultString(RESULT_OK, self._idp)

	# УПРАВЛЕНИЕ ЗНАЧЕНИЕМ ПО-УМОЛЧАНИЮ
	def DefaultVlp(self, vlp: any = None) -> T21_ResultString:
		""" Запрос/Установка значения параметра по умолчанию """
		if vlp is None: return T21_ResultString(RESULT_OK, self._default_vlp)

		if   type(vlp) is int  : self._default_vlp = f"{vlp}"
		elif type(vlp) is float: self._default_vlp = f"{vlp:0.5f}"
		elif type(vlp) is bool : self._default_vlp = BooleanToString(vlp)
		elif type(vlp) is list : self._default_vlp = SEPARATOR_LIST.join(list(map(str, vlp)))
		elif type(vlp) is str  : self._default_vlp = vlp

	# КОНВЕРТАЦИЯ ИЗ ТИПА ДАННЫХ
	def _WriteVlpInSCell(self, container_name_dst: str, vlp: str, vlt: int = 0) -> T20_ResultCode:
		""" Системный метод записи данных для конверторов """
		container = controller_containers.Container(container_name_dst)
		if container is None        : return T20_ResultCode(RESULT_ERROR_ACCESS_CONNECTION)

		if self.struct_frame is None: return T20_ResultCode(RESULT_ERROR_DATA_STRUCT)

		ido       = self.struct_frame.Ido()
		if not ido.code == RESULT_OK: return T20_ResultCode(ido.code)

		idc       = self.struct_frame.Idc()
		if not idc.code == RESULT_OK: return T20_ResultCode(idc.code)

		idp       = self.Idp()
		if not idp.code == RESULT_OK: return T20_ResultCode(idp.code)

		if vlt == 0: vlt = CurrentUTime()

		cell      = T20_StructCell(idc=idc.text, ido=ido.text, idp=idp.text, vlp=vlp, vlt=vlt)

		return T20_ResultCode(container.WriteSCell(cell).code)

	def FromBoolean(self, container_name_dst: str, flag: bool) -> T20_ResultCode:
		""" Из логического значения """
		try   : data = BooleanToString(flag)
		except: return T20_ResultCode(RESULT_ERROR_CONVERT)

		return self._WriteVlpInSCell(container_name_dst, data)

	def FromDatetime(self, container_name_dst: str, dtime: datetime.datetime) -> T20_ResultCode:
		""" Из логического значения """
		try   : data = DatetimeToString(dtime)
		except: return T20_ResultCode(RESULT_ERROR_CONVERT)

		return self._WriteVlpInSCell(container_name_dst, data)

	def FromInteger(self, container_name_dst: str, value: int) -> T20_ResultCode:
		""" Из целого числа """
		try   : data = f"{value:d}"
		except: return T20_ResultCode(RESULT_ERROR_CONVERT)

		return self._WriteVlpInSCell(container_name_dst, data)

	def FromFloat(self, container_name_dst: str, value: float) -> T20_ResultCode:
		""" Из дробного числа """
		try               : data = f"{value:0.5f}"
		except SyntaxError: return T20_ResultCode(RESULT_ERROR_CONVERT)

		return self._WriteVlpInSCell(container_name_dst, data)

	def FromString(self, container_name_dst: str, text: str) -> T20_ResultCode:
		""" Из строки """
		return self._WriteVlpInSCell(container_name_dst, text)

	# КОНВЕРТАЦИЯ ИЗ СПИСКА ТИПА ДАННЫХ
	def FromBooleans(self, container_name_dst: str, data: list[bool]) -> T20_ResultCode:
		""" Из списка логических значений """
		try   : data = SEPARATOR_LIST.join(list(map(BooleanToString, data)))
		except: return T20_ResultCode(RESULT_ERROR_CONVERT)

		return self._WriteVlpInSCell(container_name_dst, data)

	def FromDatetimes(self, container_name_dst: str, data: list[datetime.datetime]) -> T20_ResultCode:
		""" Из списка логических значений """
		try   : data = SEPARATOR_LIST.join(list(map(DatetimeToString, data)))
		except: return T20_ResultCode(RESULT_ERROR_CONVERT)

		return self._WriteVlpInSCell(container_name_dst, data)

	def FromIntegers(self, container_name_dst: str, data: list[int]) -> T20_ResultCode:
		""" Из списка целых чисел """
		try   : data = SEPARATOR_LIST.join(list(map(format, data)))
		except: return T20_ResultCode(RESULT_ERROR_CONVERT)

		return self._WriteVlpInSCell(container_name_dst, data)

	def FromFloats(self, container_name_dst: str, data: list[float]) -> T20_ResultCode:
		""" Из списка дробных чисел """
		try   : data = SEPARATOR_LIST.join(list(map("{:0.5f}".format, data)))
		except: return T20_ResultCode(RESULT_ERROR_CONVERT)

		return self._WriteVlpInSCell(container_name_dst, data)

	def FromStrings(self, container_name_dst: str, data: list[str]) -> T20_ResultCode:
		""" Из списка строк """
		try   : data = SEPARATOR_LIST.join(data)
		except: return T20_ResultCode(RESULT_ERROR_CONVERT)

		return self._WriteVlpInSCell(container_name_dst, data)

	# КОНВЕРТАЦИЯ В ТИП ДАННЫХ
	def _ReadVlpSCell(self, container_name_src: str) -> T21_ResultString:
		""" Системный метод чтения данных для конверторов """
		container = controller_containers.Container(container_name_src)
		if container is None        : return T21_ResultString(RESULT_ERROR_ACCESS_CONNECTION)

		if self.struct_frame is None: return T21_ResultString(RESULT_ERROR_DATA_STRUCT)

		ido       = self.struct_frame.Ido()
		if not ido.code == RESULT_OK: return T21_ResultString(ido.code)

		idc       = self.struct_frame.Idc()
		if not idc.code == RESULT_OK: return T21_ResultString(idc.code)

		idp       = self.Idp()
		if not idp.code == RESULT_OK: return T21_ResultString(idp.code)

		cell_src  = T20_StructCell(idc=idc.text, ido=ido.text, idp=idp.text)
		cell      = container.ReadSCell(cell_src)

		return T21_ResultString(cell.code, cell.cell.vlp)

	def ToBoolean(self, container_name_src: str) -> T21_ResultBool:
		""" В логическое значение """
		result = self._ReadVlpSCell(container_name_src)
		value  = result.text if result.code == RESULT_OK else self.DefaultVlp().text

		try   : return T21_ResultBool(result.code, StringToBoolean(value))
		except: return T21_ResultBool(RESULT_ERROR_CONVERT)

	def ToDatetime(self, container_name_src: str) -> T21_ResultDatetime:
		""" В Datetime """
		result  = self._ReadVlpSCell(container_name_src)
		value   = result.text if result.code == RESULT_OK else self.DefaultVlp().text

		convert = StringToDateTime(value)
		if convert is None:	return T21_ResultDatetime(RESULT_ERROR_CONVERT)

		return T21_ResultDatetime(result.code, convert)

	def ToInteger(self, container_name_src: str) -> T21_ResultInt:
		""" В целое число """
		result = self._ReadVlpSCell(container_name_src)
		value  = result.text if result.code == RESULT_OK else self.DefaultVlp().text

		try   : return T21_ResultInt(result.code, StringToInteger(value))
		except: return T21_ResultInt(RESULT_ERROR_CONVERT)

	def ToFloat(self, container_name_src: str) -> T21_ResultFloat:
		""" В дробное число """
		result = self._ReadVlpSCell(container_name_src)
		value  = result.text if result.code == RESULT_OK else self.DefaultVlp().text

		try   : return T21_ResultFloat(result.code, StringToFloat(value))
		except: return T21_ResultFloat(RESULT_ERROR_CONVERT)

	def ToString(self, container_name_src: str) -> T21_ResultString:
		""" В строку """
		result = self._ReadVlpSCell(container_name_src)
		value  = result.text if result.code == RESULT_OK else self.DefaultVlp().text

		return T21_ResultString(result.code, value)

	# КОНВЕРТАЦИЯ В СПИСОК ТИПА ДАННЫХ
	def ToBooleans(self, container_name_src : str) -> T21_ResultList:
		""" В список логических значений """
		result = self._ReadVlpSCell(container_name_src)
		value  = result.text if result.code == RESULT_OK else self.DefaultVlp().text

		if not value.strip(): return T21_ResultList(result.code, [])

		try   : return T21_ResultList(result.code, list(map(StringToBoolean, value.split(SEPARATOR_LIST))))
		except: return T21_ResultList(RESULT_ERROR_CONVERT)

	def ToDatetimes(self, container_name_src : str) -> T21_ResultList:
		""" В список Datetime """
		result = self._ReadVlpSCell(container_name_src)
		value  = result.text if result.code == RESULT_OK else self.DefaultVlp().text

		if not value.strip(): return T21_ResultList(result.code, [])

		try   : return T21_ResultList(result.code, list(map(StringToDateTime, value.split(SEPARATOR_LIST))))
		except: return T21_ResultList(RESULT_ERROR_CONVERT)

	def ToIntegers(self, container_name_src: str) -> T21_ResultList:
		""" В список целых чисел """
		result = self._ReadVlpSCell(container_name_src)
		value  = result.text if result.code == RESULT_OK else self.DefaultVlp().text

		if not value.strip(): return T21_ResultList(result.code, [])

		try   : return T21_ResultList(result.code, StringsToIntegers(value.split(SEPARATOR_LIST)))
		except: return T21_ResultList(RESULT_ERROR_CONVERT)

	def ToFloats(self, container_name_src: str) -> T21_ResultList:
		""" В список дробных чисел """
		result = self._ReadVlpSCell(container_name_src)
		value  = result.text if result.code == RESULT_OK else self.DefaultVlp().text

		if not value.strip(): return T21_ResultList(result.code, [])

		data   = value.replace(',', '.')

		try   : return T21_ResultList(result.code, StringsToFloats(data.split(SEPARATOR_LIST)))
		except: return T21_ResultList(RESULT_ERROR_CONVERT)

	def ToStrings(self, container_name_src: str) -> T21_ResultList:
		""" В список строк """
		result = self._ReadVlpSCell(container_name_src)
		value  = result.text if result.code == RESULT_OK else self.DefaultVlp().text

		if not value.strip(): return T21_ResultList(result.code, [])

		try   : return T21_ResultList(result.code, list(value.split(SEPARATOR_LIST)))
		except: return T21_ResultList(RESULT_ERROR_CONVERT)

	# УПРАВЛЕНИЕ S-ДАННЫМИ
	def Vlt(self, container_name_src: str) -> T21_ResultInt:
		""" Запрос vlt """
		container = controller_containers.Container(container_name_src)
		if container is None        : return T21_ResultInt(RESULT_ERROR_ACCESS_CONNECTION)

		if self.struct_frame is None: return T21_ResultInt(RESULT_ERROR_DATA_STRUCT)

		ido       = self.struct_frame.Ido()
		if not ido.code == RESULT_OK: return T21_ResultInt(ido.code)

		idc       = self.struct_frame.Idc()
		if not idc.code == RESULT_OK: return T21_ResultInt(idc.code)

		idp       = self.Idp()
		if not idp.code == RESULT_OK: return T21_ResultInt(idp.code)

		cell_src  = T20_StructCell(idc=idc.text, ido=ido.text, idp=idp.text)
		cell      = container.ReadSCell(cell_src)

		return T21_ResultInt(cell.code, cell.cell.vlt)

	def CopyToContainer(self, container_name_src: str, container_name_dst: str) -> T20_ResultCode:
		""" Копирование S-Ячейки из контейнера в контейнер """
		container_src                   = controller_containers.Container(container_name_src)
		if container_src is None         : return T21_ResultStructCell(RESULT_ERROR_ACCESS_CONNECTION)

		container_dst                   = controller_containers.Container(container_name_dst)
		if container_dst is None         : return T21_ResultStructCell(RESULT_ERROR_ACCESS_CONNECTION)

		ido                             = self.struct_frame.Ido()
		if not ido.code == RESULT_OK     : return T21_ResultStructCell(ido.code)

		idc                             = self.struct_frame.Idc()
		if not idc.code == RESULT_OK     : return T21_ResultStructCell(idc.code)

		idp                             = self.Idp()
		if not idp.code == RESULT_OK     : return T21_ResultStructCell(idp.code)

		cell     : T20_StructCell       = T20_StructCell(idc=idc.text, ido=ido.text, idp=idp.text)
		cell_src : T21_ResultStructCell = container_src.ReadSCell(cell)

		if not cell_src.code == RESULT_OK: return T21_ResultStructCell(cell_src.code)

		return container_dst.WriteSCell(cell_src.cell, False)

	def SyncBetweenContainers(self, container_name_1: str, container_name_2: str) -> T20_ResultCode:
		""" Синхронизация S-Ячейки между контейнерами """
		container_1                   = controller_containers.Container(container_name_1)
		if container_1 is None              : return T21_ResultStructCell(RESULT_ERROR_ACCESS_CONNECTION)

		container_2                   = controller_containers.Container(container_name_2)
		if container_2 is None              : return T21_ResultStructCell(RESULT_ERROR_ACCESS_CONNECTION)

		ido                           = self.struct_frame.Ido()
		if not ido.code == RESULT_OK        : return T21_ResultStructCell(ido.code)

		idc                           = self.struct_frame.Idc()
		if not idc.code == RESULT_OK        : return T21_ResultStructCell(idc.code)

		idp                           = self.Idp()
		if not idp.code == RESULT_OK        : return T21_ResultStructCell(idp.code)

		cell   : T20_StructCell       = T20_StructCell(idc=idc.text, ido=ido.text, idp=idp.text)
		cell_1 : T21_ResultStructCell = container_1.ReadSCell(cell)
		if not cell_1.code == RESULT_OK     : return T21_ResultStructCell(cell_1.code)

		cell_2 : T21_ResultStructCell = container_2.ReadSCell(cell)
		if not cell_2.code == RESULT_OK     : return T21_ResultStructCell(cell_2.code)

		if cell_1.cell.vlt > cell_2.cell.vlt: return container_2.SyncSCell(cell_1.cell)
		if cell_2.cell.vlt > cell_1.cell.vlt: return container_1.SyncSCell(cell_2.cell)

		return T20_ResultCode(RESULT_OK)

	def DeleteFromContainer(self, container_name_src: str) -> T20_ResultCode:
		""" Удаление S-Ячейки из контейнера """
		container_src                   = controller_containers.Container(container_name_src)
		if container_src is None         : return T21_ResultStructCell(RESULT_ERROR_ACCESS_CONNECTION)

		ido                             = self.struct_frame.Ido()
		if not ido.code == RESULT_OK     : return T21_ResultStructCell(ido.code)

		idc                             = self.struct_frame.Idc()
		if not idc.code == RESULT_OK     : return T21_ResultStructCell(idc.code)

		idp                             = self.Idp()
		if not idp.code == RESULT_OK     : return T21_ResultStructCell(idp.code)

		cell     : T20_StructCell       = T20_StructCell(idc=idc.text, ido=ido.text, idp=idp.text)
		cell_src : T21_ResultStructCell = container_src.ReadSCell(cell)

		if not cell_src.code == RESULT_OK: return T21_ResultStructCell(cell_src.code)

		return container_src.DeleteSCell(cell_src.cell)

	# УПРАВЛЕНИЕ D-ДАННЫМИ
	def WriteVlp(self, container_name_dst: str, vlp: str, vlt: int = 0) -> T20_ResultCode:
		""" Добавление записи D-Данных """
		container = controller_containers.Container(container_name_dst)
		if container is None        : return T20_ResultCode(RESULT_ERROR_ACCESS_CONNECTION)

		if self.struct_frame is None: return T20_ResultCode(RESULT_ERROR_DATA_STRUCT)

		ido       = self.struct_frame.Ido()
		if not ido.code == RESULT_OK: return T20_ResultCode(ido.code)

		idc       = self.struct_frame.Idc()
		if not idc.code == RESULT_OK: return T20_ResultCode(idc.code)

		idp       = self.Idp()
		if not idp.code == RESULT_OK: return T20_ResultCode(idp.code)

		if vlt == 0: vlt = CurrentUTime()

		cell      = T20_StructCell(idc=idc.text, ido=ido.text, idp=idp.text, vlp=vlp, vlt=vlt)
		result    = container.WriteDCell(cell)

		return T20_ResultCode(result.code)

	def ReadVlp(self, container_name_src: str, vlt: int = 0) -> T21_ResultString:
		""" Запрос записи D-Данных """
		container = controller_containers.Container(container_name_src)
		if container is None        : return T21_ResultString(RESULT_ERROR_ACCESS_CONNECTION)

		if self.struct_frame is None: return T21_ResultString(RESULT_ERROR_DATA_STRUCT)

		ido       = self.struct_frame.Ido()
		if not ido.code == RESULT_OK: return T21_ResultString(ido.code)

		idc       = self.struct_frame.Idc()
		if not idc.code == RESULT_OK: return T21_ResultString(idc.code)

		idp       = self.Idp()
		if not idp.code == RESULT_OK: return T21_ResultString(idp.code)

		if vlt == 0:
			vlts = self.VltRange(container_name_src)
			if not vlts.code == RESULT_OK: return T21_ResultString(vlts.code)
			if not vlts                  : return T21_ResultString(RESULT_WARNING_NO_DATA)

			vlt = vlts.vlt_r

		cell      = T20_StructCell(idc=idc.text, ido=ido.text, idp=idp.text, vlt=vlt)
		result    = container.ReadDCell(cell)

		return T21_ResultString(result.code, result.cell.vlp)

	def VltRange(self, container_name_src: str, vlt_l: int = 0, vlt_r: int = 0) -> T21_ResultRange:
		""" Запрос границ vlt D-Данных """
		container = controller_containers.Container(container_name_src)
		if container is None          : return T21_ResultRange(RESULT_ERROR_ACCESS_CONNECTION)

		if self.struct_frame is None  : return T21_ResultRange(RESULT_ERROR_DATA_STRUCT)

		ido       = self.struct_frame.Ido()
		if not ido.code == RESULT_OK  : return T21_ResultRange(ido.code)

		idc       = self.struct_frame.Idc()
		if not idc.code == RESULT_OK  : return T21_ResultRange(idc.code)

		idp       = self.Idp()
		if not idp.code == RESULT_OK  : return T21_ResultRange(idp.code)

		cell      = T21_StructRange(idc=idc.text, ido=ido.text, idp=idp.text, vlt_l=vlt_l, vlt_r=vlt_r)
		result    = container.ReadDVltRange(cell)

		return T21_ResultRange(result.code, vlt_l=result.range.vlt_l, vlt_r=result.range.vlt_r)

	def Vlts(self, container_name_src: str, vlt_l: int = 0, vlt_r: int = 0) -> T21_ResultList:
		""" Запрос списка vlt в диапазоне vlt D-Данных """
		container = controller_containers.Container(container_name_src)
		if container is None          : return T21_ResultList(RESULT_ERROR_ACCESS_CONNECTION)

		if self.struct_frame is None  : return T21_ResultList(RESULT_ERROR_DATA_STRUCT)

		ido       = self.struct_frame.Ido()
		if not ido.code == RESULT_OK  : return T21_ResultList(ido.code)

		idc       = self.struct_frame.Idc()
		if not idc.code == RESULT_OK  : return T21_ResultList(idc.code)

		idp       = self.Idp()
		if not idp.code == RESULT_OK  : return T21_ResultList(idp.code)

		cell      = T21_StructRange(idc=idc.text, ido=ido.text, idp=idp.text, vlt_l=vlt_l, vlt_r=vlt_r)

		return container.ReadDVlts(cell)

	def Vlps(self, container_name_src: str, vlt_l: int = 0, vlt_r: int = 0) -> T21_ResultDict:
		""" Запрос vlp/vlt в диапазоне vlt D-Данных """
		container = controller_containers.Container(container_name_src)
		if container is None          : return T21_ResultDict(RESULT_ERROR_ACCESS_CONNECTION)

		if self.struct_frame is None  : return T21_ResultDict(RESULT_ERROR_DATA_STRUCT)

		ido                     = self.struct_frame.Ido()
		if not ido.code == RESULT_OK  : return T21_ResultDict(ido.code)

		idc                     = self.struct_frame.Idc()
		if not idc.code == RESULT_OK  : return T21_ResultDict(idc.code)

		idp                     = self.Idp()
		if not idp.code == RESULT_OK  : return T21_ResultDict(idp.code)

		cell                    = T21_StructRange(idc=idc.text, ido=ido.text, idp=idp.text, vlt_l=vlt_l, vlt_r=vlt_r)
		dcells                  = container.ReadDCells(cell)
		result : dict[int, str] = dict()

		for cell in dcells.cells: result[cell.vlt] = cell.vlp

		return T21_ResultDict(dcells.code, result)
