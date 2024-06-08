# КАКТУС: СТРУКТУРЫ ДАННЫХ
# 08 июн 2024

import datetime

from   dataclasses       import (dataclass,
                                 field)

from   G20_struct_result import T20_StructResult


# ТИПЫ ДАННЫХ ОБЩЕГО НАЗНАЧЕНИЯ
@dataclass
class T21_StructResult_Int(T20_StructResult):
	""" Результат-Число """
	data: int | None = None


@dataclass
class T21_StructResult_Float(T20_StructResult):
	""" Результат-Дробное число """
	data: float | None = None


@dataclass
class T21_StructResult_Range(T20_StructResult):
	""" Результат-Диапазон """
	cut_l: int | None = None
	cut_r: int | None = None


@dataclass
class T21_StructResult_String(T20_StructResult):
	""" Результат-Текст """
	data: str | None = None


@dataclass
class T21_StructResult_List(T20_StructResult):
	""" Результат-Текст """
	data: list = field(default_factory=list)


@dataclass
class T21_StructResult_Dict(T20_StructResult):
	""" Результат-Словарь """
	data: dict = field(default_factory=dict)


@dataclass
class T21_StructResult_Bool(T20_StructResult):
	""" Результат-Текст """
	data: bool = False


@dataclass
class T21_StructResult_Datetime(T20_StructResult):
	""" Результат-Текст """
	dtime: datetime.datetime | None = None
