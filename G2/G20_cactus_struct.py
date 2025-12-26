# КАКТУС: СТРУКТУРЫ ДАННЫХ
# 19 апр 2025

from dataclasses      import (dataclass,
                              field)

from G00_filter_codes import  FILTERS


# СТРУКТУРНАЯ ЯЧЕЙКА
@dataclass
class T20_StructCell:
	""" Структурная ячейка """
	idc: str = ""

	ido: str = ""
	idp: str = ""

	vlp: str = ""
	vlt: int = 0

	ids: str = field(init = False)
	idf: str = field(init = False)

	def __regenerate_ids_idf__(self):
		self.__dict__["ids"] = f"{self.ido}.{self.idp}"
		self.__dict__["idf"] = f"{self.idc}.{self.__dict__.get('ids', '')}"

	def __setattr__(self, key, value):
		super().__setattr__(key, value)

		if   key == "vlp": return
		elif key == "vlt": return

		self.__regenerate_ids_idf__()

	def __hash__(self):
		return hash(self.idf)


# ФИЛЬТРЫ
@dataclass
class T20_FilterD1:
	""" Фильтр линейного типа """
	flag_invert  : bool             = False
	flag_include : bool             = False

	filter_type  : FILTERS | None   = None

	filter_value : str              = ""
	filter_values: list[str]        = field(default_factory=list)
