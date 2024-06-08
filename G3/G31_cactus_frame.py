# КАКТУС: РАСШИРЕНИЕ СТРУКТРУНОГО ПАРАМЕТРА
# 2022-12-01

from G00_result_codes  import RESULT_OK
from G20_meta_frame    import C20_MetaFrame
from G30_cactus_frame  import C30_StructField, C30_StructFrame
from G30_cactus_struct import T30_ResultCode
from G31_cactus_struct import T31_ResultBool

CS_POSTFIX  = "cs"
RS_POSTFIX  = "cs"
SRC_POSTFIX = "src"
DST_POSTFIX = "dst"


class C31_StructFieldCsRs(C30_StructField):
	""" Структурный параметр CS-RS """
	""" 2023-01-01 """

	def __init__(self, struct_frame: C30_StructFrame, pid: str, default_cvl: any = None):
		super().__init__(struct_frame, pid, default_cvl)

		self.cs = C30_StructField(self.struct_frame, f"{pid}_{CS_POSTFIX}", default_cvl)
		self.rs = C30_StructField(self.struct_frame, f"{pid}_{RS_POSTFIX}", default_cvl)

	def Init_10(self):
		super().Init_10()

		self.cs : C30_StructField | None = None
		self.rs : C30_StructField | None = None

	# УПРАВЛЕНИЕ CS ПАРАМЕТРОМ
	def MemoryCvlFromCs(self, container_name_cs: str, container_name: str) -> T30_ResultCode:
		""" Запомнить CS-значение как S-Данные """
		result_value_cs = self.cs.ToString(container_name_cs)
		if not result_value_cs.code == RESULT_OK: return T30_ResultCode(result_value_cs.code)

		result_value    = self.FromString(container_name, result_value_cs.text)
		if not result_value.code == RESULT_OK: return T30_ResultCode(result_value.code)

		return T30_ResultCode(RESULT_OK)

	def WriteCsCvl(self, container_name_dst: str, cvl: str, cut: int = 0) -> T30_ResultCode:
		""" Записать CS-значение как D-Данные """
		return self.cs.WriteCvl(container_name_dst, cvl, cut)

	# УПРАВЛЕНИЕ RS ПАРАМЕТРОМ
	def MemoryCvlFromRs(self, container_name_rs: str, container_name: str) -> T30_ResultCode:
		""" Запомнить CS-значение как S-Данные """
		result_value_rs = self.rs.ToString(container_name_rs)
		if not result_value_rs.code == RESULT_OK: return T30_ResultCode(result_value_rs.code)

		result_value    = self.FromString(container_name, result_value_rs.text)
		if not result_value.code == RESULT_OK: return T30_ResultCode(result_value.code)

		return T30_ResultCode(RESULT_OK)

	def WriteRsCvl(self, container_name_dst: str, cvl: str, cut: int = 0) -> T30_ResultCode:
		""" Записать CS-значение как D-Данные """
		return self.rs.WriteCvl(container_name_dst, cvl, cut)

	# АНАЛИЗ CS\RS ЗНАЧЕНИЙ
	def CheckEqualCsRs(self, container_name: str) -> T31_ResultBool:
		""" Проверка равенства CS и RS """
		result_value_cs = self.cs.ToString(container_name)
		if not result_value_cs.code == RESULT_OK: return T31_ResultBool(result_value_cs.code)

		result_value_rs = self.rs.ToString(container_name)
		if not result_value_rs.code == RESULT_OK: return T31_ResultBool(result_value_rs.code)

		return T31_ResultBool(RESULT_OK, result_value_cs.text == result_value_rs.text)


class C31_StructFieldSrcDst(C20_MetaFrame):
	""" Структурный параметр SRC-DST """
	""" 2023-01-01 """

	def __init__(self, struct_frame: C30_StructFrame, pid: str, default_cvl: any = None):
		super().__init__()

		self.src = C30_StructField(struct_frame, f"{pid}_{SRC_POSTFIX}", default_cvl)
		self.dst = C30_StructField(struct_frame, f"{pid}_{DST_POSTFIX}", default_cvl)

	def Init_10(self):
		super().Init_10()

		self.src : C30_StructField | None = None
		self.dst : C30_StructField | None = None

	# УПРАВЛЕНИЕ ДАННЫМИ SRC-DST
	def SwapSrcDst(self, container_name: str) -> T30_ResultCode:
		""" Перестановка значений между SRC-DST """
		result_value_src = self.src.ToString(container_name)
		if not result_value_src.code == RESULT_OK: return T31_ResultBool(result_value_src.code)

		result_value_dst = self.src.ToString(container_name)
		if not result_value_dst.code == RESULT_OK: return T31_ResultBool(result_value_dst.code)

		valus_src = result_value_src.text
		valus_dst = result_value_dst.text

		result_value_src = self.src.FromString(container_name, valus_src)
		if not result_value_src.code == RESULT_OK: return T31_ResultBool(result_value_src.code)

		result_value_dst = self.src.FromString(container_name, valus_dst)
		if not result_value_dst.code == RESULT_OK: return T31_ResultBool(result_value_dst.code)

		return T30_ResultCode(RESULT_OK)
