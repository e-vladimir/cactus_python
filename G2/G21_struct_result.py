# КАКТУС: СТРУКТУРЫ ДАННЫХ
# 31 окт 2024

import datetime
from   dataclasses       import (dataclass,
                                 field)

from   G20_struct_result import T20_StructResult


@dataclass
class T21_StructResult_Int(T20_StructResult):
	""" Структурный результат: Целое число """
	data: int = 0


@dataclass
class T21_StructResult_Float(T20_StructResult):
	""" Структурный результат: Дробное число """
	data: float = 0.000


@dataclass
class T21_StructResult_String(T20_StructResult):
	""" Структурный результат: Строка """
	data: str = ""


@dataclass
class T21_StructResult_List(T20_StructResult):
	""" Структурный результат: Список """
	data: list = field(default_factory=list)


@dataclass
class T21_StructResult_Set(T20_StructResult):
	""" Структурный результат: Множество """
	data: set = field(default_factory=set)


@dataclass
class T21_StructResult_Dict(T20_StructResult):
	""" Структурный результат: Словарь """
	data: dict = field(default_factory=dict)


@dataclass
class T21_StructResult_Bool(T20_StructResult):
	""" Структурный результат: Логическое значение """
	data: bool = False


@dataclass
class T21_StructResult_DTime(T20_StructResult):
	""" Структурный результат: Дата-Время """
	data: datetime.datetime = datetime.datetime.now()
