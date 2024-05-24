# КАКТУС: СТРУКТУРЫ ДАННЫХ
# 2022-11-21

import datetime

from   dataclasses       import dataclass, \
						        field
from   G30_cactus_struct import T30_StructCell, \
								T30_ResultCode


# ТИПЫ ДАННЫХ ОБЩЕГО НАЗНАЧЕНИЯ
@dataclass
class T31_ResultInt(T30_ResultCode):
	""" Результат-Число """
	value: int = 0


@dataclass
class T31_ResultFloat(T30_ResultCode):
	""" Результат-Дробное число """
	value: float = 0.0


@dataclass
class T31_ResultRange(T30_ResultCode):
	""" Результат-Диапазон """
	cut_l: int = 0
	cut_r: int = 0


@dataclass
class T31_ResultString(T30_ResultCode):
	""" Результат-Текст """
	text: str = ""


@dataclass
class T31_ResultList(T30_ResultCode):
	""" Результат-Текст """
	items: list = field(default_factory=list)


@dataclass
class T31_ResultDict(T30_ResultCode):
	""" Результат-Словарь """
	items: dict = field(default_factory=dict)


@dataclass
class T31_ResultBool(T30_ResultCode):
	""" Результат-Текст """
	flag: bool = False


@dataclass
class T31_ResultDatetime(T30_ResultCode):
	""" Результат-Текст """
	dtime: datetime.datetime = None


# ТИПЫ ДАННЫХ СТРУКТУРНОЙ ЯЧЕЙКИ
@dataclass
class T31_StructRange(T30_StructCell):
	""" Структурный диапазон cut """
	cut_l: int = 0  # Левая граница диапазона (меньшее)
	cut_r: int = 0  # Правая граница диапазона (большее)


@dataclass
class T31_ResultStructCell(T30_ResultCode):
	""" Результат - Структурная ячейка """
	cell: T30_StructCell = field(default_factory=T30_StructCell)


@dataclass
class T31_ResultStructCells(T30_ResultCode):
	""" Результат - Список структурных ячеек """
	cells: list[T30_StructCell] = field(default_factory=list)


@dataclass
class T31_ResultStructRange(T30_ResultCode):
	""" Результат - Структурный диапазон cut """
	range: T31_StructRange = field(default_factory=T31_StructRange)
