# КАКТУС: СТРУКТУРЫ ДАННЫХ
# 08 июн 2024

from dataclasses import (dataclass,
                         field)


# ТИПЫ ДАННЫХ СТРУКТУРНОЙ ЯЧЕЙКИ
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


# ТИПЫ ДАННЫХ ФИЛЬТРОВ
@dataclass
class T20_FilterD1:
	""" Фильтр линейного типа """
	flag_invert  : bool      = False
	flag_include : bool      = False

	filter_type  : int       = 0

	filter_value : str       = ""
	filter_values: list[str] = field(default_factory=list)
