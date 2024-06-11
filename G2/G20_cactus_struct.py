# КАКТУС: СТРУКТУРЫ ДАННЫХ
# 11 июн 2024

from dataclasses      import (dataclass,
                              field)

from G00_filter_codes import  FILTERS


# СТРУКТУРНАЯ ЯЧЕЙКА
@dataclass
class T20_StructCell:
	""" Структурная ячейка """
	oci: str = ""

	oid: str = ""
	pid: str = ""

	cvl: str = ""
	cut: int = 0

	sid: str = field(init = False)
	cid: str = field(init = False)

	def __regenerate_sid_cid__(self):
		self.__dict__["sid"] = f"{self.oid}.{self.pid}"
		self.__dict__["cid"] = f"{self.oci}.{self.__dict__.get('sid', '')}"

	def __setattr__(self, key, value):
		super().__setattr__(key, value)

		if   key == "cvl": return
		elif key == "cut": return

		self.__regenerate_sid_cid__()


# ФИЛЬТРЫ
@dataclass
class T20_FilterD1:
	""" Фильтр линейного типа """
	flag_invert  : bool             = False
	flag_include : bool             = False

	filter_type  : FILTERS | None   = None

	filter_value : str              = ""
	filter_values: list[str]        = field(default_factory=list)
