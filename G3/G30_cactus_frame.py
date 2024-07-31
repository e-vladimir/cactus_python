# КАКТУС: СТРУКТУРНЫЙ КАРКАС
# 31 июл 2024

import datetime

from   G00_cactus_codes                 import  CACTUS_STRUCT_DATA
from   G00_status_codes                 import (CODES_COMPLETION,
				                                CODES_DATA,
				                                CODES_PROCESSING,
				                                CODES_CACTUS)

from   G10_cactus_convertors            import  UnificationIdc
from   G10_convertor_format             import (BooleanToString,
										 	    DatetimeToString,
											    StringsToFloats,
											    StringsToIntegers,
											    StringToBoolean,
											    StringToDateTime,
											    StringToFloat,
											    StringToInteger)
from   G10_cactus_generators            import  GenerateID
from   G10_cactus_check                 import (CheckIdc,
											    CheckIdo,
											    CheckIdp)
from   G10_datetime                     import  CurrentUTime

from   G20_cactus_struct                import  T20_StructCell
from   G20_meta_frame                   import  C20_MetaFrame
from   G20_struct_result                import  T20_StructResult
from   G21_cactus_struct                import (T21_StructResult_StructCell,
                                                T21_StructResult_StructCells,
                                                T21_VltRange,
                                                T21_StructResult_VltRange)
from   G21_struct_result                import (T21_StructResult_String,
                                                T21_StructResult_List,
                                                T21_StructResult_Bool,
                                                T21_StructResult_DTime,
                                                T21_StructResult_Int,
                                                T21_StructResult_Float)

from   G30_cactus_controller_containers import controller_containers


# Системные константы
SEPARATOR_LIST : str = '\n'


class C30_StructFrame(C20_MetaFrame):
	""" КАКТУС: Структурный объект """

	def __init__(self, ido: str = ""):
		super().__init__()

		self.Ido(ido)

	# Модель данных
	_idc : str = ""

	def Init_00(self):
		super().Init_00()

		self._ido : str = ""

	# Модель событий
	pass

	# Механика данных: IDC
	@classmethod
	def Idc(cls) -> T21_StructResult_String:
		""" Запрос idc """
		result      = T21_StructResult_String()
		result.code = CODES_COMPLETION.COMPLETED
		result.data = UnificationIdc(cls._idc)

		if not CheckIdc(result.data): result.subcodes.add(CODES_DATA.ERROR_CHECK)

		return result

	# Механика данных: IDO
	def Ido(self, ido: str = None) -> T21_StructResult_String:
		""" Запрос/Установка ido """
		result      = T21_StructResult_String()
		result.code = CODES_COMPLETION.COMPLETED

		if ido is None:
			if not self._ido          : result.subcodes.add(CODES_DATA.NO_DATA)
			if not CheckIdo(self._ido): result.subcodes.add(CODES_DATA.ERROR_CHECK)

		else          :
			if not CheckIdo(ido): return T21_StructResult_String(code     = CODES_COMPLETION.INTERRUPTED,
			                                                     subcodes = {CODES_DATA.ERROR_CHECK},
			                                                     data     = ido)
			self._ido = ido

		result.data = self._ido
		return result

	@classmethod
	def Idos(self, container_name: str) -> T21_StructResult_List:
		""" Запрос списка IDO объектов класса из контейнера """
		container                                  = controller_containers.Container(container_name)
		if container is None                                 : return T21_StructResult_List(code     =  CODES_COMPLETION.INTERRUPTED,
		                                                                                    subcodes = {CODES_CACTUS.NO_CONTAINER})

		filter_cells                               = T20_StructCell(idc = UnificationIdc(self._idc))
		result_read : T21_StructResult_StructCells = container.ReadSCells(filter_cells)

		if not result_read.code == CODES_COMPLETION.COMPLETED: return T21_StructResult_List(code     = CODES_COMPLETION.INTERRUPTED,
		                                                                                    subcodes = result_read.subcodes)

		idos        : list[str]                    = [cell.ido for cell in result_read.data]
		idos                                       = list(set(idos))

		result                                     = T21_StructResult_List()
		result.code                                = CODES_COMPLETION.COMPLETED
		result.data                                = idos

		match len(result.data):
			case 0: result.subcodes.add(CODES_DATA.NO_DATA)
			case 1: result.subcodes.add(CODES_DATA.SINGLE)

		return result

	def GenerateIdo(self) -> T21_StructResult_String:
		""" Генерация IDO """
		return self.Ido(GenerateID())

	# Механика данных: IDP
	def Idps(self, container_name: str) -> T21_StructResult_List:
		""" Запрос списка IDP S-Ячеек из контейнера """
		if not CheckIdo(self._ido)                            : return T21_StructResult_List(code     =  CODES_COMPLETION.COMPLETED,
		                                                                                     subcodes = {CODES_DATA.ERROR_CHECK})

		container                                  = controller_containers.Container(container_name)
		if container is None                                  : return T21_StructResult_List(code     =  CODES_COMPLETION.COMPLETED,
		                                                                                     subcodes = {CODES_CACTUS.NO_CONTAINER})

		filter_cells                               = T20_StructCell(idc = UnificationIdc(self._idc),
		                                                            ido = self._ido)

		result_read : T21_StructResult_StructCells = container.ReadSCells(filter_cells)
		if not result_read.code == CODES_COMPLETION.COMPLETED : return T21_StructResult_List(code     = CODES_COMPLETION.INTERRUPTED,
		                                                                                     subcodes = result_read.subcodes)

		idps        : list[str]                    = [cell.idp for cell in result_read.data]
		idps                                       = list(set(idps))

		result                                     = T21_StructResult_List()
		result.code                                = CODES_COMPLETION.COMPLETED
		result.data                                = idps

		match len(result.data):
			case 0: result.subcodes.add(CODES_DATA.NO_DATA)
			case 1: result.subcodes.add(CODES_DATA.SINGLE)

		return result

	# Механика управления: Объект
	def RegisterObject(self, container_name: str) -> T20_StructResult:
		""" Регистрация объекта в контейнере """
		if not CheckIdo(self._ido) : return T20_StructResult(code     =  CODES_COMPLETION.INTERRUPTED,
		                                                     subcodes = {CODES_DATA.ERROR_CHECK})
		cell      = T20_StructCell()
		cell.idc  = UnificationIdc(self._idc)
		cell.ido  = self._ido
		cell.idp  = CACTUS_STRUCT_DATA.IDC.name_base
		cell.vlp  = UnificationIdc(self._idc)
		cell.vlt  = CurrentUTime()

		container = controller_containers.Container(container_name)
		if container is None       : return T20_StructResult(code     =  CODES_COMPLETION.INTERRUPTED,
		                                                     subcodes = {CODES_CACTUS.NO_CONTAINER})

		result    = container.WriteSCell(cell, True)
		return T20_StructResult(code     = result.code,
		                        subcodes = result.subcodes)

	def DeleteObject(self, container_name: str) -> T20_StructResult:
		""" Удаление объекта из контейнера """
		if not CheckIdo(self._ido) : return T20_StructResult(code     =  CODES_COMPLETION.INTERRUPTED,
		                                                     subcodes = {CODES_DATA.ERROR_CHECK})

		filter_cells = T20_StructCell(idc = UnificationIdc(self._idc),
		                              ido = self._ido)

		container    = controller_containers.Container(container_name)

		if container is None       : return T20_StructResult(code     =  CODES_COMPLETION.INTERRUPTED,
		                                                     subcodes = {CODES_CACTUS.NO_CONTAINER})

		result       = container.DeleteSCells(filter_cells)
		return T20_StructResult(code     = result.code,
		                        subcodes = result.subcodes)

	# Механика управления: Класс
	@classmethod
	def RegisterClass(cls, container_name: str) -> T20_StructResult:
		""" Регистрация класса в контейнере """
		result      = T20_StructResult()
		result.code = CODES_COMPLETION.COMPLETED

		container   = controller_containers.Container(container_name)

		if   container is None               :
			result.code = CODES_COMPLETION.INTERRUPTED
			result.subcodes.add(CODES_DATA.NO_DATA)

		elif container.Type_RAM().data       :
			result.subcodes.add(CODES_PROCESSING.SKIP)

		elif not CheckIdc(UnificationIdc(cls._idc)):
			result.code = CODES_COMPLETION.INTERRUPTED
			result.subcodes.add(CODES_DATA.ERROR_CHECK)

		elif container.Type_SQLite().data    :
			result_register = container.RegisterClass(UnificationIdc(cls._idc))

			result.code     = result_register.code
			result.subcodes = result_register.subcodes

		elif container.Type_PostgreSQL().data:
			result_register = container.RegisterClass(UnificationIdc(cls._idc))

			result.code     = result_register.code
			result.subcodes = result_register.subcodes

		return result

	# Механика управления: Данные в контейнере
	def CopyToContainer(self, container_name_src: str, container_name_dst: str) -> T20_StructResult:
		""" Копирование S-Ячеек из контейнера в контейнер """
		container_src   = controller_containers.Container(container_name_src)
		if container_src is None                             : return T20_StructResult(code     =  CODES_COMPLETION.INTERRUPTED,
		                                                                               subcodes = {CODES_CACTUS.NO_CONTAINER})

		container_dst   = controller_containers.Container(container_name_dst)
		if container_dst is None                             : return T20_StructResult(code     =  CODES_COMPLETION.INTERRUPTED,
		                                                                               subcodes = {CODES_CACTUS.NO_CONTAINER})

		filter_cells    = T20_StructCell(idc = self.Idc().data,
		                                 ido = self.Ido().data)

		result_read     = container_src.ReadSCells(filter_cells)
		if not result_read.code == CODES_COMPLETION.COMPLETED: return T20_StructResult(code     = result_read.code,
		                                                                               subcodes = result_read.subcodes)

		result_write    = container_dst.WriteSCells(result_read.data)

		result          = T20_StructResult()
		result.code     = result_write.code
		result.subcodes = result_write.subcodes

		return result

	def SyncBetweenContainers(self, container_name_1: str, container_name_2: str) -> T20_StructResult:
		""" Синхронизация S-Ячеек между контейнерами """
		container_1                                  = controller_containers.Container(container_name_1)
		if container_1 is None                                  : return T20_StructResult(code     =  CODES_COMPLETION.INTERRUPTED,
		                                                                                  subcodes = {CODES_CACTUS.NO_CONTAINER})
		container_2                                  = controller_containers.Container(container_name_2)
		if container_2 is None                                  : return T20_StructResult(code     =  CODES_COMPLETION.INTERRUPTED,
		                                                                                  subcodes = {CODES_CACTUS.NO_CONTAINER})
		filter_cells                                 = T20_StructCell(idc = self.Idc().data,
		                                                              ido = self.Ido().data)

		result_read_1 : T21_StructResult_StructCells = container_1.ReadSCells(filter_cells)
		if not result_read_1.code == CODES_COMPLETION.COMPLETED : return T20_StructResult(code     = CODES_COMPLETION.INTERRUPTED,
		                                                                                  subcodes = result_read_1.subcodes)

		result_read_2 : T21_StructResult_StructCells = container_2.ReadSCells(filter_cells)
		if not result_read_2.code == CODES_COMPLETION.COMPLETED : return T20_StructResult(code     = CODES_COMPLETION.INTERRUPTED,
		                                                                                  subcodes = result_read_1.subcodes)

		cells         : dict[str, T20_StructCell]    = dict()

		for cell in result_read_1.data + result_read_2.data:
			cell_exist = cells.get(cell.ids, T20_StructCell())

			result_set: bool = cell.ids not in cells
			result_set |= cell.vlt > cell_exist.vlt

			if not result_set: continue
			cells[cell.ids] = cell

		result_sync_1 : T21_StructResult_StructCells = container_1.SyncSCells(cells.values())
		if not result_sync_1.code == CODES_COMPLETION.COMPLETED : return T20_StructResult(code     = CODES_COMPLETION.INTERRUPTED,
		                                                                                  subcodes = result_read_1.subcodes)

		result_sync_2 : T21_StructResult_StructCells = container_2.SyncSCells(cells.values())
		if not result_sync_2.code == CODES_COMPLETION.COMPLETED : return T20_StructResult(code     = CODES_COMPLETION.INTERRUPTED,
		                                                                                  subcodes = result_read_1.subcodes)

		return T20_StructResult(code = CODES_COMPLETION.COMPLETED)

	# Логика данных
	pass

	# Логика управления
	pass


class C30_StructField(C20_MetaFrame):
	""" КАКТУС: Структурный параметр """

	def __init__(self, struct_frame: C30_StructFrame, idp: str, default_vlp: any = None):
		super().__init__()

		self._idp         = idp
		self.struct_frame = struct_frame

		if default_vlp is not None: self.DefaultVlp(default_vlp)

	# Модель данных
	def Init_00(self):
		super().Init_00()

		self._default_vlp: str = ""
		self._idp        : str = ""

	def Init_10(self):
		super().Init_10()
		self.struct_frame : C30_StructFrame | None = None

	# Механика данных: Параметры
	def Ids(self) -> T21_StructResult_String:
		""" Запрос IDS """
		if self.struct_frame is None: return T21_StructResult_String(code     =  CODES_COMPLETION.INTERRUPTED,
		                                                             subcodes = {CODES_DATA.NOT_ENOUGH})

		ido          : str = self.struct_frame._ido
		idp          : str = self._idp
		ids          : str = f"{ido}.{idp}"

		result_check : bool = CheckIdo(ido)
		result_check       &= CheckIdp(idp)

		if not result_check         : return T21_StructResult_String(code     =  CODES_COMPLETION.INTERRUPTED,
		                                                             subcodes = {CODES_DATA.ERROR_CHECK})

		return T21_StructResult_String(code = CODES_COMPLETION.COMPLETED,
		                               data = ids)

	def Idf(self) -> T21_StructResult_String:
		""" Запрос IDF """
		if self.struct_frame is None: return T21_StructResult_String(code     =  CODES_COMPLETION.INTERRUPTED,
		                                                             subcodes = {CODES_DATA.NOT_ENOUGH})

		idc          : str = UnificationIdc(self.struct_frame._idc)
		ido          : str = self.struct_frame._ido
		idp          : str = self._idp
		ids          : str = f"{idc}.{ido}.{idp}"

		result_check : bool = CheckIdc(idc)
		result_check       &= CheckIdo(ido)
		result_check       &= CheckIdp(idp)

		if not result_check         : return T21_StructResult_String(code     =  CODES_COMPLETION.INTERRUPTED,
		                                                             subcodes = {CODES_DATA.ERROR_CHECK})

		return T21_StructResult_String(code = CODES_COMPLETION.COMPLETED,
		                               data = ids)

	def Idp(self) -> T21_StructResult_String:
		""" Запрос IDP """
		result      = T21_StructResult_String()
		result.data = self._idp

		if not CheckIdp(self._idp): result.subcodes.add(CODES_DATA.ERROR_CHECK)

		return result

	# Механика данных: Параметр по-умолчанию
	def DefaultVlp(self, vlp: any = None) -> T21_StructResult_String:
		""" Запрос/Установка значения параметра по умолчанию """
		if        vlp  is None : return T21_StructResult_String(code = CODES_COMPLETION.COMPLETED,
		                                                        data = self._default_vlp)

		elif type(vlp) is int  : self._default_vlp = f"{vlp}"
		elif type(vlp) is float: self._default_vlp = f"{vlp:0.5f}"
		elif type(vlp) is bool : self._default_vlp = BooleanToString(vlp)
		elif type(vlp) is list : self._default_vlp = SEPARATOR_LIST.join(list(map(str, vlp)))
		elif type(vlp) is str  : self._default_vlp = vlp

	# Логика данных: Конвертация из формата
	def _WriteVlpInSCell(self, container_name_dst: str, vlp: str, vlt: int = 0) -> T20_StructResult:
		""" Служебный метод записи данных для конверторов """
		container           = controller_containers.Container(container_name_dst)
		if container is None        : return T20_StructResult(code     =  CODES_COMPLETION.INTERRUPTED,
		                                                      subcodes = {CODES_CACTUS.NO_CONTAINER})

		if self.struct_frame is None: return T20_StructResult(code     =  CODES_COMPLETION.INTERRUPTED,
		                                                      subcodes = {CODES_DATA.NOT_ENOUGH})

		idc                 = UnificationIdc(self.struct_frame._idc)
		ido                 = self.struct_frame._ido
		idp                 = self._idp

		if vlt == 0: vlt = CurrentUTime()

		cell                = T20_StructCell(idc=idc, ido=ido, idp=idp, vlp=vlp, vlt=vlt)
		result_write        = container.WriteSCell(cell)

		result              = T20_StructResult()
		result.code         = result_write.code
		result.subcodes     = result_write.subcodes

		return result

	def FromBoolean(self, container_name_dst: str, flag: bool) -> T20_StructResult:
		""" Из логического значения """
		try   : data = BooleanToString(flag)
		except: return T20_StructResult(code     =  CODES_COMPLETION.INTERRUPTED,
		                                subcodes = {CODES_DATA.ERROR_CONVERT})

		return self._WriteVlpInSCell(container_name_dst, data)

	def FromDatetime(self, container_name_dst: str, dtime: datetime.datetime) -> T20_StructResult:
		""" Из логического значения """
		try   : data = DatetimeToString(dtime)
		except: return T20_StructResult(code     =  CODES_COMPLETION.INTERRUPTED,
		                                subcodes = {CODES_DATA.ERROR_CONVERT})

		return self._WriteVlpInSCell(container_name_dst, data)

	def FromInteger(self, container_name_dst: str, value: int) -> T20_StructResult:
		""" Из целого числа """
		try   : data = f"{value:d}"
		except: return T20_StructResult(code     =  CODES_COMPLETION.INTERRUPTED,
		                                subcodes = {CODES_DATA.ERROR_CONVERT})

		return self._WriteVlpInSCell(container_name_dst, data)

	def FromFloat(self, container_name_dst: str, value: float) -> T20_StructResult:
		""" Из дробного числа """
		try   : data = f"{value:0.5f}"
		except: return T20_StructResult(code     =  CODES_COMPLETION.INTERRUPTED,
		                                subcodes = {CODES_DATA.ERROR_CONVERT})

		return self._WriteVlpInSCell(container_name_dst, data)

	def FromString(self, container_name_dst: str, text: str) -> T20_StructResult:
		""" Из строки """
		return self._WriteVlpInSCell(container_name_dst, text)

	# Логика данных: Конвертация из списка формата
	def FromBooleans(self, container_name_dst: str, data: list[bool]) -> T20_StructResult:
		""" Из списка логических значений """
		try   : data = SEPARATOR_LIST.join(list(map(BooleanToString, data)))
		except: return T20_StructResult(code     =  CODES_COMPLETION.INTERRUPTED,
		                                subcodes = {CODES_DATA.ERROR_CONVERT})

		return self._WriteVlpInSCell(container_name_dst, data)

	def FromDatetimes(self, container_name_dst: str, data: list[datetime.datetime]) -> T20_StructResult:
		""" Из списка логических значений """
		try   : data = SEPARATOR_LIST.join(list(map(DatetimeToString, data)))
		except: return T20_StructResult(code     =  CODES_COMPLETION.INTERRUPTED,
		                                subcodes = {CODES_DATA.ERROR_CONVERT})

		return self._WriteVlpInSCell(container_name_dst, data)

	def FromIntegers(self, container_name_dst: str, data: list[int]) -> T20_StructResult:
		""" Из списка целых чисел """
		try   : data = SEPARATOR_LIST.join(list(map(format, data)))
		except: return T20_StructResult(code     =  CODES_COMPLETION.INTERRUPTED,
		                                subcodes = {CODES_DATA.ERROR_CONVERT})

		return self._WriteVlpInSCell(container_name_dst, data)

	def FromFloats(self, container_name_dst: str, data: list[float]) -> T20_StructResult:
		""" Из списка дробных чисел """
		try   : data = SEPARATOR_LIST.join(list(map("{:0.5f}".format, data)))
		except: return T20_StructResult(code     =  CODES_COMPLETION.INTERRUPTED,
		                                subcodes = {CODES_DATA.ERROR_CONVERT})

		return self._WriteVlpInSCell(container_name_dst, data)

	def FromStrings(self, container_name_dst: str, data: list[str]) -> T20_StructResult:
		""" Из списка строк """
		try   : data = SEPARATOR_LIST.join(data)
		except: return T20_StructResult(code     =  CODES_COMPLETION.INTERRUPTED,
		                                subcodes = {CODES_DATA.ERROR_CONVERT})

		return self._WriteVlpInSCell(container_name_dst, data)

	# Логика данных: Конвертация в формат
	def _ReadVlpSCell(self, container_name_src: str) -> T21_StructResult_String:
		""" Системный метод чтения данных для конверторов """
		container           = controller_containers.Container(container_name_src)
		if container is None                       : return T21_StructResult_String(code     =  CODES_COMPLETION.INTERRUPTED,
		                                                                            subcodes = {CODES_CACTUS.NO_CONTAINER})

		if self.struct_frame is None               : return T21_StructResult_String(code     =  CODES_COMPLETION.INTERRUPTED,
		                                                                            subcodes = {CODES_DATA.NOT_ENOUGH})

		idc                 = UnificationIdc(self.struct_frame._idc)
		ido                 = self.struct_frame._ido
		idp                 = self._idp

		cell                = T20_StructCell(idc=idc, ido=ido, idp=idp)
		result_read         = container.ReadSCell(cell)
		if not result_read.code == CODES_COMPLETION.COMPLETED: return T21_StructResult_String(code     = CODES_COMPLETION.INTERRUPTED,
		                                                                            subcodes = result_read.subcodes)

		result              = T21_StructResult_String()
		result.code         = result_read.code
		result.subcodes     = result_read.subcodes
		result.data         = result_read.data.vlp

		return result

	def ToBoolean(self, container_name_src: str) -> T21_StructResult_Bool:
		""" В логическое значение """
		result_read = self._ReadVlpSCell(container_name_src)
		vlp         = result_read.data if (result_read.code == CODES_COMPLETION.COMPLETED) else self._default_vlp

		try   :
			return T21_StructResult_Bool(code     = result_read.code,
			                             subcodes = result_read.subcodes,
		                                 data     = StringToBoolean(vlp))

		except:
			return T21_StructResult_Bool(code     = CODES_COMPLETION.INTERRUPTED,
			                             subcodes = {CODES_DATA.ERROR_CONVERT})

	def ToDatetime(self, container_name_src: str) -> T21_StructResult_DTime:
		""" В Datetime """
		result_read = self._ReadVlpSCell(container_name_src)
		vlp         = result_read.data if (result_read.code == CODES_COMPLETION.COMPLETED) else self._default_vlp
		result_vlp  = StringToDateTime(vlp)

		if result_vlp is None: return T21_StructResult_DTime(code     =  CODES_COMPLETION.INTERRUPTED,
		                                                     subcodes = {CODES_DATA.ERROR_CONVERT})

		return T21_StructResult_DTime(code     = result_read.code,
		                              subcodes = result_read.subcodes,
		                              data     = result_vlp)

	def ToInteger(self, container_name_src: str) -> T21_StructResult_Int:
		""" В целое число """
		result_read = self._ReadVlpSCell(container_name_src)
		vlp         = result_read.data if (result_read.code == CODES_COMPLETION.COMPLETED) else self._default_vlp

		try   :
			return T21_StructResult_Int(code     = CODES_COMPLETION.COMPLETED,
			                            subcodes = result_read.subcodes,
		                                data     = StringToInteger(vlp))

		except:
			return T21_StructResult_Int(code     = CODES_COMPLETION.INTERRUPTED,
			                            subcodes = {CODES_DATA.ERROR_CONVERT})

	def ToFloat(self, container_name_src: str) -> T21_StructResult_Float:
		""" В дробное число """
		result_read = self._ReadVlpSCell(container_name_src)
		vlp         = result_read.data if (result_read.code == CODES_COMPLETION.COMPLETED) else self._default_vlp

		try   :
			return T21_StructResult_Float(code     = result_read.code,
			                              subcodes = result_read.subcodes,
		                                  data     = StringToFloat(vlp))

		except:
			return T21_StructResult_Float(code     = CODES_COMPLETION.INTERRUPTED,
			                              subcodes = {CODES_DATA.ERROR_CONVERT})

	def ToString(self, container_name_src: str) -> T21_StructResult_String:
		""" В строку """
		result_read = self._ReadVlpSCell(container_name_src)
		vlp         = result_read.data if (result_read.code == CODES_COMPLETION.COMPLETED) else self._default_vlp

		return T21_StructResult_String(code     = result_read.code,
		                               subcodes = result_read.subcodes,
		                               data     = vlp)

	# Логика данных: Конвертация в список формата
	def ToBooleans(self, container_name_src : str) -> T21_StructResult_List:
		""" В список логических значений """
		result_read = self._ReadVlpSCell(container_name_src)
		vlp         = result_read.data if (result_read.code == CODES_COMPLETION.COMPLETED) else self._default_vlp
		vlp         = vlp.strip()

		try   :
			return T21_StructResult_List(code     = result_read.code,
			                             subcodes = result_read.subcodes,
			                             data     = list(map(StringToBoolean, vlp.split(SEPARATOR_LIST))))

		except:
			return T21_StructResult_List(code     = CODES_COMPLETION.INTERRUPTED,
			                             subcodes = {CODES_DATA.ERROR_CONVERT})

	def ToDatetimes(self, container_name_src : str) -> T21_StructResult_List:
		""" В список Datetime """
		result_read = self._ReadVlpSCell(container_name_src)
		vlp         = result_read.data if (result_read.code == CODES_COMPLETION.COMPLETED) else self._default_vlp
		vlp         = vlp.strip()

		try   :
			return T21_StructResult_List(code     = result_read.code,
			                             subcodes = result_read.subcodes,
			                             data     = list(map(StringToDateTime, vlp.split(SEPARATOR_LIST))))

		except:
			return T21_StructResult_List(code     = CODES_COMPLETION.INTERRUPTED,
			                             subcodes = {CODES_DATA.ERROR_CONVERT})

	def ToIntegers(self, container_name_src: str) -> T21_StructResult_List:
		""" В список целых чисел """
		result_read = self._ReadVlpSCell(container_name_src)
		vlp         = result_read.data if (result_read.code == CODES_COMPLETION.COMPLETED) else self._default_vlp
		vlp         = vlp.strip()

		try   :
			return T21_StructResult_List(code     = result_read.code,
			                             subcodes = result_read.subcodes,
			                             data     = StringsToIntegers(vlp.split(SEPARATOR_LIST)))

		except:
			return T21_StructResult_List(code     = CODES_COMPLETION.INTERRUPTED,
			                             subcodes = {CODES_DATA.ERROR_CONVERT})

	def ToFloats(self, container_name_src: str) -> T21_StructResult_List:
		""" В список дробных чисел """
		result_read = self._ReadVlpSCell(container_name_src)
		vlp         = result_read.data if (result_read.code == CODES_COMPLETION.COMPLETED) else self._default_vlp
		vlp         = vlp.strip()

		try   :
			return T21_StructResult_List(code     = result_read.code,
			                             subcodes = result_read.subcodes,
			                             data     = StringsToFloats(vlp.split(SEPARATOR_LIST)))

		except:
			return T21_StructResult_List(code     = CODES_COMPLETION.INTERRUPTED,
			                             subcodes = {CODES_DATA.ERROR_CONVERT})

	def ToStrings(self, container_name_src: str) -> T21_StructResult_List:
		""" В список строк """
		result_read = self._ReadVlpSCell(container_name_src)
		vlp         = result_read.data if (result_read.code == CODES_COMPLETION.COMPLETED) else self._default_vlp
		vlp         = vlp.strip()

		try   :
			return T21_StructResult_List(code     = result_read.code,
			                             subcodes = result_read.subcodes,
			                             data     = vlp.split(SEPARATOR_LIST))

		except:
			return T21_StructResult_List(code     = CODES_COMPLETION.INTERRUPTED,
			                             subcodes = {CODES_DATA.ERROR_CONVERT})

	# Механика управления: Данные в контейнере
	def CopyToContainer(self, container_name_src: str, container_name_dst: str) -> T20_StructResult:
		""" Копирование S-Ячейки из контейнера в контейнер """
		container_src                              = controller_containers.Container(container_name_src)
		if container_src is None                              : return T20_StructResult(code     =  CODES_COMPLETION.INTERRUPTED,
		                                                                                subcodes = {CODES_CACTUS.NO_CONTAINER})

		container_dst                              = controller_containers.Container(container_name_dst)
		if container_dst is None                              : return T20_StructResult(code     =  CODES_COMPLETION.INTERRUPTED,
		                                                                                subcodes = {CODES_CACTUS.NO_CONTAINER})

		idc                                        = UnificationIdc(self.struct_frame._idc)
		ido                                        = self.struct_frame._ido
		idp                                        = self._idp

		cell         : T20_StructCell              = T20_StructCell(idc=idc, ido=ido, idp=idp)
		result_read  : T21_StructResult_StructCell = container_src.ReadSCell(cell)
		if not result_read.code == CODES_COMPLETION.COMPLETED : return T20_StructResult(code     = CODES_COMPLETION.INTERRUPTED,
		                                                                                subcodes = result_read.subcodes)

		result_write : T21_StructResult_StructCell = container_src.WriteSCell(cell)

		result                                     = T20_StructResult()
		result.code                                = result_write.code
		result.subcodes                            = result_write.subcodes

		return result

	def SyncBetweenContainers(self, container_name_1: str, container_name_2: str) -> T20_StructResult:
		""" Синхронизация S-Ячейки между контейнерами """
		container_1                              = controller_containers.Container(container_name_1)
		if container_1 is None                                  : return T20_StructResult(code     =  CODES_COMPLETION.INTERRUPTED,
		                                                                                  subcodes = {CODES_CACTUS.NO_CONTAINER})

		container_2                              = controller_containers.Container(container_name_2)
		if container_2 is None                                  : return T20_StructResult(code     =  CODES_COMPLETION.INTERRUPTED,
		                                                                                  subcodes = {CODES_CACTUS.NO_CONTAINER})

		idc                                        = UnificationIdc(self.struct_frame._idc)
		ido                                        = self.struct_frame._ido
		idp                                        = self._idp

		cell   : T20_StructCell       = T20_StructCell(idc=idc, ido=ido, idp=idp)

		result_cell_1 : T21_StructResult_StructCell = container_1.ReadSCell(cell)
		if not result_cell_1.code == CODES_COMPLETION.COMPLETED : return T20_StructResult(code     = CODES_COMPLETION.INTERRUPTED,
		                                                                                  subcodes = result_cell_1.subcodes)

		result_cell_2 : T21_StructResult_StructCell = container_2.ReadSCell(cell)
		if not result_cell_2.code == CODES_COMPLETION.COMPLETED : return T20_StructResult(code     = CODES_COMPLETION.INTERRUPTED,
		                                                                                  subcodes = result_cell_2.subcodes)

		result = T20_StructResult()

		if   result_cell_1.data.vlt > result_cell_2.data.vlt:
			result_sync     = container_2.SyncSCell(result_cell_1.data)

			result.code     = result_sync.code
			result.subcodes = result_sync.subcodes

		elif result_cell_2.data.vlt > result_cell_1.data.vlt:
			result_sync     = container_1.SyncSCell(result_cell_2.data)

			result.code     = result_sync.code
			result.subcodes = result_sync.subcodes

		return result

	def DeleteFromContainer(self, container_name_src: str) -> T20_StructResult:
		""" Удаление S-Ячейки из контейнера """
		container_src                               = controller_containers.Container(container_name_src)
		if container_src is None : return T20_StructResult(code     =  CODES_COMPLETION.INTERRUPTED,
		                                                   subcodes = {CODES_CACTUS.NO_CONTAINER})

		idc                                         = UnificationIdc(self.struct_frame._idc)
		ido                                         = self.struct_frame._ido
		idp                                         = self._idp

		cell          : T20_StructCell              = T20_StructCell(idc=idc, ido=ido, idp=idp)
		result_delete : T21_StructResult_StructCell = container_src.DeleteSCell(cell)

		result                                      = T20_StructResult()
		result.code                                 = result_delete.code
		result.subcodes                             = result_delete.subcodes

		return result

	# Механика управления: D-VLP
	def WriteVlp(self, container_name_dst: str, vlp: str, vlt: int = 0) -> T20_StructResult:
		""" Добавление записи D-Данных """
		container_src                              = controller_containers.Container(container_name_dst)
		if container_src is None : return T20_StructResult(code     =  CODES_COMPLETION.INTERRUPTED,
		                                                   subcodes = {CODES_CACTUS.NO_CONTAINER})

		idc                                        = UnificationIdc(self.struct_frame._idc)
		ido                                        = self.struct_frame._ido
		idp                                        = self._idp
		if vlt == 0: vlt = CurrentUTime()

		cell         : T20_StructCell              = T20_StructCell(idc=idc, ido=ido, idp=idp, vlp=vlp, vlt=vlt)

		result_write : T21_StructResult_StructCell = container_src.WriteDCell(cell)

		result                                     = T20_StructResult()
		result.code                                = result_write.code
		result.subcodes                            = result_write.subcodes

		return result

	def ReadVlp(self, container_name_src: str, vlt: int = 0) -> T21_StructResult_String:
		""" Запрос записи D-Данных """
		container_src                             = controller_containers.Container(container_name_src)
		if container_src is None : return T21_StructResult_String(code     =  CODES_COMPLETION.INTERRUPTED,
		                                                          subcodes = {CODES_CACTUS.NO_CONTAINER})

		idc                                       = UnificationIdc(self.struct_frame._idc)
		ido                                       = self.struct_frame._ido
		idp                                       = self._idp

		if not vlt:
			cell_range  = T21_VltRange(idc=idc, ido=ido, idp=idp)
			result_vlts = container_src.ReadVltRange(cell_range)

			if   not result_vlts.code == CODES_COMPLETION.COMPLETED: return T21_StructResult_String(code     = CODES_COMPLETION.INTERRUPTED,
			                                                                                        subcodes = result_vlts.subcodes)

			elif not result_vlts.data                              : return T21_StructResult_String(code     = CODES_COMPLETION.INTERRUPTED,
			                                                                                        subcodes = {CODES_DATA.NO_DATA})

			vlt = result_vlts.data.vlt_r

		cell                                      = T20_StructCell(idc=idc, ido=ido, idp=idp, vlt=vlt)
		result_read : T21_StructResult_StructCell = container_src.ReadDCell(cell)

		result                                    = T21_StructResult_String()
		result.code                               = result_read.code
		result.subcodes                           = result_read.subcodes
		result.data                               = result_read.data.vlp

		return result

	# Логика данных: D-VLP
	def Vlps(self, container_name_src: str, vlt_l: int = 0, vlt_r: int = 0) -> T21_StructResult_List:
		""" Запрос vlp/vlt в диапазоне vlt D-Данных """
		container_src                              = controller_containers.Container(container_name_src)
		if container_src is None : return T21_StructResult_List(code     =  CODES_COMPLETION.INTERRUPTED,
		                                                        subcodes = {CODES_CACTUS.NO_CONTAINER})

		idc                                        = UnificationIdc(self.struct_frame._idc)
		ido                                        = self.struct_frame._ido
		idp                                        = self._idp

		cell                                       = T21_VltRange(idc=idc, ido=ido, idp=idp, vlt_l=vlt_l, vlt_r=vlt_r)
		result_read : T21_StructResult_StructCells = container_src.ReadDCells(cell)

		result                                     = T21_StructResult_List()

		if result_read.code == CODES_COMPLETION.COMPLETED:
			for dcell in result_read.data: result.data.append([dcell.vlt, dcell.vlp])

			match len(result.data):
				case 0: result.subcodes.add(CODES_DATA.NO_DATA)
				case 1: result.subcodes.add(CODES_DATA.SINGLE)

		else                                             :
			result.code     = CODES_COMPLETION.INTERRUPTED
			result.subcodes = result_read.subcodes

		return result

	# Логика данных: D-VLT
	def VltRange(self, container_name_src: str, vlt_l: int = 0, vlt_r: int = 0) -> T21_StructResult_VltRange:
		""" Запрос границ vlt D-Данных """
		container_src = controller_containers.Container(container_name_src)
		if container_src is None : return T21_StructResult_VltRange(code     =  CODES_COMPLETION.INTERRUPTED,
		                                                            subcodes = {CODES_CACTUS.NO_CONTAINER})

		idc           = UnificationIdc(self.struct_frame._idc)
		ido           = self.struct_frame._ido
		idp           = self._idp

		cell          = T21_VltRange(idc=idc, ido=ido, idp=idp, vlt_l=vlt_l, vlt_r=vlt_r)
		return container_src.ReadVltRange(cell)

	def Vlts(self, container_name_src: str, vlt_l: int = 0, vlt_r: int = 0) -> T21_StructResult_List:
		""" Запрос списка vlt в диапазоне vlt D-Данных """
		container_src = controller_containers.Container(container_name_src)
		if container_src is None : return T21_StructResult_List(code     =  CODES_COMPLETION.INTERRUPTED,
		                                                        subcodes = {CODES_CACTUS.NO_CONTAINER})

		idc           = UnificationIdc(self.struct_frame._idc)
		ido           = self.struct_frame._ido
		idp           = self._idp

		cell          = T21_VltRange(idc=idc, ido=ido, idp=idp, vlt_l=vlt_l, vlt_r=vlt_r)
		return container_src.ReadVlts(cell)

	# Логика данных: S-VLT
	def Vlt(self, container_name_src: str) -> T21_StructResult_Int:
		""" Запрос vlt """
		container           = controller_containers.Container(container_name_src)
		if container is None        : return T21_StructResult_Int(code     =  CODES_COMPLETION.INTERRUPTED,
		                                                          subcodes = {CODES_CACTUS.NO_CONTAINER})

		if self.struct_frame is None: return T21_StructResult_Int(code     =  CODES_COMPLETION.INTERRUPTED,
		                                                          subcodes = {CODES_DATA.NOT_ENOUGH})

		idc                 = UnificationIdc(self.struct_frame._idc)
		ido                 = self.struct_frame._ido
		idp                 = self._idp

		cell                = T20_StructCell(idc=idc, ido=ido, idp=idp)
		result_read         = container.ReadSCell(cell)
		if not result_read.code == CODES_COMPLETION: return T21_StructResult_Int(code     = CODES_COMPLETION.INTERRUPTED,
		                                                                         subcodes = result_read.subcodes)

		result              = T21_StructResult_Int()
		result.code         = result_read.code
		result.subcodes     = result_read.subcodes
		result.data         = result_read.data.vlt

		return result
