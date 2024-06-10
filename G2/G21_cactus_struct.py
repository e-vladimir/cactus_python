# КАКТУС: СТРУКТУРЫ ДАННЫХ
# 10 июн 2024

import s3m

from   dataclasses       import (dataclass,
                                 field)

from   G20_cactus_struct import T20_StructCell
from   G20_struct_result import T20_StructResult


# ТИПЫ ДАННЫХ СТРУКТУРНОЙ ЯЧЕЙКИ
@dataclass
class T21_StructRange(T20_StructCell):
	""" Структурный диапазон cut """
	cut_l: int = 0  # Левая граница диапазона (меньшее)
	cut_r: int = 0  # Правая граница диапазона (большее)


@dataclass
class T21_StructResult_StructCell(T20_StructResult):
	""" Результат - Структурная ячейка """
	data: T20_StructCell = field(default_factory=T20_StructCell)


@dataclass
class T21_StructResult_StructCells(T20_StructResult):
	""" Результат - Список структурных ячеек """
	data: list[T20_StructCell] = field(default_factory=list)


@dataclass
class T21_StructResult_StructRange(T20_StructResult):
	""" Результат - Структурный диапазон cut """
	range: T21_StructRange = field(default_factory=T21_StructRange)


# ТИПЫ ДАННЫХ SQL КОНТЕЙНЕРА
@dataclass
class T31_StructResult_CursorS3m(T20_StructResult):
	""" Результат-Курсор """
	cursor : s3m.Cursor | None = None
