# КАКТУС: РАСШИРЕНИЕ СТРУКТУРНОГО КАРКАСА
# 21 окт 2024

from G00_cactus_codes  import  POSTFIX
from G00_status_codes  import  CODES_COMPLETION

from G20_meta_frame    import  C20_MetaFrame
from G20_struct_result import  T20_StructResult
from G21_struct_result import  T21_StructResult_Bool

from G30_cactus_frame  import (C30_StructField,
                               C30_StructFrame)


class C31_StructFrameWithEvents(C30_StructFrame):
	""" КАКТУС: Структурный объект - Модель событий """

	# Модель событий: Объект - Инициализация
	def on_ObjectInitiated(self): pass

	# Модель событий: Объект - Регистрация
	def on_RequestRegisterObject(self): pass
	def on_ObjectRegistered(self): pass

	# Модель событий: Объект - Удаление
	def on_RequestDeleteObject(self): pass
	def on_ObjectDeleted(self): pass

	# Служебные методы: Инициализация объекта
	def __init__(self, ido: str = ""):
		super().__init__(ido)

		self.on_ObjectInitiated()

	# Механика управления: Объект
	def RegisterObject(self, container_name: str) -> T20_StructResult:
		""" Регистрация объекта в контейнере """
		self.on_RequestRegisterObject()

		result_register = super().RegisterObject(container_name)
		if result_register.code == CODES_COMPLETION: self.on_ObjectRegistered()

		return result_register

	def DeleteObject(self, container_name: str) -> T20_StructResult:
		""" Удаление объекта из контейнера """
		self.on_RequestDeleteObject()

		result_delete = super().DeleteObject(container_name)
		if result_delete.code == CODES_COMPLETION: self.on_ObjectDeleted()

		return result_delete


class C31_StructFieldCsRs(C30_StructField):
	""" КАКТУС: Структурный параметр CS-RS """

	def __init__(self, struct_frame: C30_StructFrame, idp: str, default_vlp: any = None):
		super().__init__(struct_frame, idp, default_vlp)

		self.cs = C30_StructField(self.struct_frame, f"{idp}_{POSTFIX.CS.postfix}", default_vlp)
		self.rs = C30_StructField(self.struct_frame, f"{idp}_{POSTFIX.RS.postfix}", default_vlp)

	def Init_10(self):
		super().Init_10()

		self.cs : C30_StructField | None = None
		self.rs : C30_StructField | None = None

	# УПРАВЛЕНИЕ CS ПАРАМЕТРОМ
	def MemoryVlpFromCs(self, container_name_cs: str, container_name: str) -> T20_StructResult:
		""" Запомнить CS-значение как S-Данные """
		result_value_cs = self.cs.ToString(container_name_cs)
		if not result_value_cs.code == CODES_COMPLETION.COMPLETED: return T20_StructResult(code     = CODES_COMPLETION.INTERRUPTED,
		                                                                                   subcodes = result_value_cs.subcodes)

		result_value    = self.FromString(container_name, result_value_cs.data)
		if not result_value.code    == CODES_COMPLETION.COMPLETED: return T20_StructResult(code     = CODES_COMPLETION.INTERRUPTED,
		                                                                                   subcodes = result_value_cs.subcodes)

		return T20_StructResult(code = CODES_COMPLETION.COMPLETED)

	def WriteCsVlp(self, container_name_dst: str, vlp: str, vlt: int = 0) -> T20_StructResult:
		""" Записать CS-значение как D-Данные """
		return self.cs.WriteVlp(container_name_dst, vlp, vlt)

	# УПРАВЛЕНИЕ RS ПАРАМЕТРОМ
	def MemoryVlpFromRs(self, container_name_rs: str, container_name: str) -> T20_StructResult:
		""" Запомнить CS-значение как S-Данные """
		result_value_rs = self.rs.ToString(container_name_rs)
		if not result_value_rs.code == CODES_COMPLETION.COMPLETED: return T20_StructResult(code     = CODES_COMPLETION.INTERRUPTED,
		                                                                                   subcodes = result_value_rs.subcodes)

		result_value    = self.FromString(container_name, result_value_rs.data)
		if not result_value.code    == CODES_COMPLETION.COMPLETED: return T20_StructResult(code     = CODES_COMPLETION.INTERRUPTED,
		                                                                                   subcodes = result_value.subcodes)

		return T20_StructResult(code = CODES_COMPLETION.COMPLETED)

	def WriteRsVlp(self, container_name_dst: str, vlp: str, vlt: int = 0) -> T20_StructResult:
		""" Записать CS-значение как D-Данные """
		return self.rs.WriteVlp(container_name_dst, vlp, vlt)

	# АНАЛИЗ CS\RS ЗНАЧЕНИЙ
	def CheckEqualCsRs(self, container_name: str) -> T21_StructResult_Bool:
		""" Проверка равенства CS и RS """
		result_value_cs = self.cs.ToString(container_name)
		if not result_value_cs.code == CODES_COMPLETION.COMPLETED: return T21_StructResult_Bool(code     = CODES_COMPLETION.INTERRUPTED,
		                                                                                        subcodes = result_value_cs.subcodes)

		result_value_rs = self.rs.ToString(container_name)
		if not result_value_rs.code == CODES_COMPLETION.COMPLETED: return T21_StructResult_Bool(code     = CODES_COMPLETION.INTERRUPTED,
		                                                                                        subcodes = result_value_rs.subcodes)

		return T21_StructResult_Bool(code = CODES_COMPLETION.COMPLETED,
		                             data = result_value_cs.data == result_value_rs.data)


class C31_StructFieldSrcDst(C20_MetaFrame):
	""" КАКТУС: Структурный параметр SRC-DST """

	def __init__(self, struct_frame: C30_StructFrame, idp: str, default_vlp: any = None):
		super().__init__()

		self.src = C30_StructField(struct_frame, f"{idp}_{POSTFIX.SRC.postfix}", default_vlp)
		self.dst = C30_StructField(struct_frame, f"{idp}_{POSTFIX.DST.postfix}", default_vlp)

	def Init_10(self):
		super().Init_10()

		self.src : C30_StructField | None = None
		self.dst : C30_StructField | None = None

	# УПРАВЛЕНИЕ ДАННЫМИ SRC-DST
	def SwapSrcDst(self, container_name: str) -> T20_StructResult:
		""" Перестановка значений между SRC-DST """
		result_value_src = self.src.ToString(container_name)
		if not result_value_src.code == CODES_COMPLETION.COMPLETED: return T20_StructResult(code     = CODES_COMPLETION.INTERRUPTED,
		                                                                                   subcodes = result_value_src.subcodes)

		result_value_dst = self.src.ToString(container_name)
		if not result_value_dst.code == CODES_COMPLETION.COMPLETED: return T20_StructResult(code     = CODES_COMPLETION.INTERRUPTED,
		                                                                                   subcodes = result_value_dst.subcodes)

		value_src = result_value_src.data
		value_dst = result_value_dst.data

		result_value_src = self.src.FromString(container_name, value_src)
		if not result_value_src.code == CODES_COMPLETION.COMPLETED: return T20_StructResult(code     = CODES_COMPLETION.INTERRUPTED,
		                                                                                   subcodes = result_value_src.subcodes)

		result_value_dst = self.src.FromString(container_name, value_dst)
		if not result_value_dst.code == CODES_COMPLETION.COMPLETED: return T20_StructResult(code     = CODES_COMPLETION.INTERRUPTED,
		                                                                                   subcodes = result_value_dst.subcodes)

		return T20_StructResult(code = CODES_COMPLETION.COMPLETED)
